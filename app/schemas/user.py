from pydantic import BaseModel, EmailStr
from .token import Token

class UserBase(BaseModel):
    display_name: str
    first_name: str
    last_name: str
    email: EmailStr

class User(UserBase):
    id: str
    created_at: str
    
class UserCreate(UserBase):
    password: str

class DBUser(UserBase):
    id: str
    password: str
    created_at: str

class LoginResponse(BaseModel):
    user: User
    token: Token
