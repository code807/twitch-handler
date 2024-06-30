from dotenv import load_dotenv

load_dotenv()

from pprint import pprint, pformat
from fastapi import FastAPI, Request, Response, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from enum import Enum
import time
import os
import requests
import hmac
import hashlib

clients = []
secretkey = bytes(os.environ['TWITCH_SECRET'], 'utf-8')

class BroadcasterUserID(BaseModel):
    broadcaster_user_id: str

class SubscriptionData(BaseModel):
    id: str
    status: str
    type: str
    version: str
    cost: int
    condition: BroadcasterUserID

class ResponseMessage(BaseModel):
    response: str

class TwitchMessage(BaseModel):
    challenge: str | None = None
    subscription: SubscriptionData

def generate_hmac(message):
    return "sha256="+hmac.new(secretkey, message, hashlib.sha256).hexdigest()

def verify_hmac(message, received_hmac):
    generated_hmac = generate_hmac(message)
    return hmac.compare_digest(generated_hmac, received_hmac)

async def get_header(request: Request):
    return request.headers

async def get_body(request: Request):
    return await request.body()

app = FastAPI()

@app.post("/twitch-handler")
@app.post("/twitch-handler/")
async def handle_message(data: TwitchMessage, headers: bytes = Depends(get_header), body = Depends(get_body), status_code=200): # -> ResponseMessage:
    if (set(headers.keys()) >= {"twitch-eventsub-message-id", "twitch-eventsub-message-timestamp", "twitch-eventsub-message-signature"}):
        id = headers.get('twitch-eventsub-message-id')
        timestamp = headers.get('twitch-eventsub-message-timestamp')
        text = bytes.decode(body, 'utf-8')
        message = bytes(id+timestamp+text, 'utf-8')
        if verify_hmac(
            message,
            headers["twitch-eventsub-message-signature"]
        ):
            rdata = pformat(data)
            if data.challenge:
                rdata = data.challenge
            headers = {
                "Content-Length":str(len(rdata))
            }
            await broadcast(
                {
                    "type":data.subscription.type,
                    "user":data.subscription.condition.broadcaster_user_id
                }
            )
            return Response(content=rdata, media_type="text/plain", status_code=200, headers=headers)
        else:
            return Response(content="Secret Key Invalid", media_type="text/plain", status_code=401)
    else:
        return Response(content="Missing Required EventSub Arguments", media_type="text/plain", status_code=412)

async def broadcast(message: dict):
    for client in clients:
        try:
            await client.send_json(message)
        except WebSocketDisconnect:
            clients.remove(client)

@app.websocket("/ws")
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        clients.remove(websocket)
