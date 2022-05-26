from bson import ObjectId
from pydantic import BaseModel, Field


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
