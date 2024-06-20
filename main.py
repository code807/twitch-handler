from dotenv import load_dotenv

load_dotenv()

from pprint import pprint
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from enum import Enum
import time
import os
import requests

twitch_key = os.environ['TWITCH_API_KEY']

class BroadcasterUserID(BaseModel):
    broadcaster_user_id: str

class SubscriptionData(BaseModel):
    id: str | None = None
    status: str
    type: str
    version: str
    cost: int
    condition: BroadcasterUserID

class ResponseMessage(BaseModel):
    response: str

class TwitchMessage(BaseModel):
    subscription: SubscriptionData

async def checkquota() -> bool:
    return True

app = FastAPI()

async def checkquota(method):
    return True

@app.post("/twitch-handler")
@app.post("/twitch-handler/")
async def handle_message(data: TwitchMessage, status_code=200)  -> ResponseMessage:
    if "challenge" in data:
        rdata = data["challenge"]
    return Response(content=rdata, media_type="text/plain", status_code=200, headers=[len(rdata)])

    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)
