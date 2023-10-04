from pydantic import BaseModel

class EncodeTokenData(BaseModel):
    sub: str
    exp: int

class Token(BaseModel):
    access_token: str
    access_token_expire_at: int
    refresh_token: str
    refresh_token_expire_at: int

class GeneratedToken(BaseModel):
    token: str
    expire_at: int