import string
import time
from hashlib import sha512
from os import getenv
from random import choice
from html import escape
import motor.motor_asyncio
from fastapi import Body, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.pubkey import PublicKeyModel, PublicKeyResponse

url = getenv("mongourl")

app = FastAPI(
    title="Public Key Share",
    description="API for storing and retrieving public keys.",
    version="0.0.125",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

client = motor.motor_asyncio.AsyncIOMotorClient(url)
db = client.publickeys


# Helper Functions
def custom_escape(text, strict=True):
    allowed_punctuation = list("-@ +/._'=^*|~")
    disallowed_punctuation = string.punctuation - set(allowed_punctuation)

    escaped = escape(text, quote=True)

    if strict:
        for char in escaped:
            if char in disallowed_punctuation:
                escaped = escaped.replace(char, "")

    return escaped


async def key_exists(key):
    if await db["public_key_collection"].find_one({"key": key}):
        return True
    return False


async def sha_exists(hash):
    if await db["public_key_collection"].find_one({"hash": hash}):
        return True
    return False


async def generate_key():
    generated = ''.join(
        choice(
            string.ascii_letters +
            string.digits) for _ in range(10))
    if await key_exists(generated):
        return generate_key()
    return generated


async def populate_key(json_key):
    key = json_key
    key["key"] = await generate_key()
    key["hash"] = sha512(json_key["publickey"].encode("utf-8")).hexdigest()
    key["timestamp"] = str(int(round(time.time() * 1000)))
    return key


# create public key route
@app.post("/", response_description="Add new public key",
          response_model=PublicKeyModel)
async def add_public_key(public_key: PublicKeyModel):
    json_key = jsonable_encoder(public_key)
    json_key = await populate_key(json_key)

    if await sha_exists(json_key["hash"]):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Public key already exists")

    # escape all html tags in json_key values
    for key in json_key:
        json_key[key] = custom_escape(json_key[key], strict=True)

    new_key = await db["public_key_collection"].insert_one(json_key)
    created_key = await db["public_key_collection"].find_one({"_id": new_key.inserted_id})

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={
            "key": created_key["key"]})


@app.get("/{key}", response_description="Get public key",
         response_model=PublicKeyResponse)
async def get_public_key(key: str):
    if (public_key := await db["public_key_collection"].find_one({"key": key})):
        return public_key

    raise HTTPException(
        status_code=404,
        detail=f"Public key with key: {key} not found")
