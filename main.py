from dotenv import load_dotenv

load_dotenv()

from pprint import pprint
from fastapi import FastAPI, Request
from pydantic import BaseModel
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
async def handle_message(data: TwitchMessage)  -> ResponseMessage:
    q = data.q
    target = data.target.value.upper()
    source = data.source.value.upper()
    user = data.user
    api = data.method
    return "what a mess"
