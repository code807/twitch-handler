from dotenv import load_dotenv

load_dotenv()

from pprint import pprint, pformat
from fastapi import FastAPI, Request, Response, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from enum import Enum
import time
import os
import requests
import hmac

twitch_key = os.environ['TWITCH_API_KEY']

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

async def get_header(request: Request):
    return request.headers

async def get_body(request: Request):
    return await request.body()

async def checkquota() -> bool:
    return True

app = FastAPI()

async def checkquota(method):
    return True

@app.post("/twitch-handler")
@app.post("/twitch-handler/")
async def handle_message(data: TwitchMessage, headers: bytes = Depends(get_header), body = Depends(get_body), status_code=200): #  -> ResponseMessage:
    return headers
    pprint(data)
    rdata = pformat(data)
    if data.challenge:
        rdata = data.challenge
    headers = {
        "Content-Length":str(len(rdata))
    }
    return Response(content=rdata, media_type="text/plain", status_code=200, headers=headers)

    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)
