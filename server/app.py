import time
import string
from hashlib import sha512
from random import choice
import motor.motor_asyncio
from bson import ObjectId
from fastapi import Body, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from os import getenv

url = getenv("mongour")

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(url)
db = client.publickeys


class PublicKeyModel(BaseModel):
    title: str = Field(...)
    publickey: str = Field(...)
    twitter: str = ""
    github: str = ""

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        jsonable_encoder = {ObjectId: str}

        schema_extra = {
            "example": {
                "title": "Example Ed25519 Public Key - Aayush",
                "publickey": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDbiwd0Ssu+NHqav4i6TlABli7p/YxDa08t79FMeCX9H aayushpokharel36@gmail.com"
            }
        }


class PublicKeyResponse(BaseModel):
    title: str = Field(...)
    publickey: str = Field(...)
    twitter: str = ""
    github: str = ""
    key: str = Field(...)
    hash: str = Field(...)
    timestamp: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        jsonable_encoder = {ObjectId: str}

        schema_extra = {
            "example": {
                "title": "Example Ed25519 Public Key - Aayush",
                "publickey": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDbiwd0Ssu+NHqav4i6TlABli7p/YxDa08t79FMeCX9H aayushpokharel36@gmail.com",
                "key": "aayush",
                "hash": "531f75cb2340a97f06962405207606601991213c9f74416a7e6473b1886b38698f9dc390663621a78592a34a87e0bbf138b909bf45c59ee303452f7dacc273ca",
                "twitter": "",
                "github": "Aayush9029",
                "timestamp": "1653547807789"}}

# Helper Functions


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
