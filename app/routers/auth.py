from fastapi import APIRouter, Depends, Body
from typing import Annotated
import uuid
from boto3.dynamodb.conditions import Attr
from datetime import datetime

from ..schemas.user import UserCreate, User, DBUser, LoginResponse
from ..schemas.token import Token
from ..schemas.exception import BadRequestException
from ..configs.database import get_table
from fastapi.security import OAuth2PasswordRequestForm
from ..services.token import TokenService
from ..services.user import UserService
from ..utils import password_utils
from ..configs.constants import DBTable
from ..schemas.response import DataResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/refreshToken", response_model=DataResponse[Token])
def refresh_token(refresh_token: Annotated[str, Body(embed=True)], user_id: Annotated[str, Depends(UserService.get_current_user_id)]):
    token = TokenService.refresh_token(refresh_token, user_id)
    return DataResponse().success_response(token)

@router.post("/login", response_model=DataResponse[LoginResponse])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_table = get_table(DBTable.USERS)
    users = user_table.scan(
        FilterExpression=Attr("email").eq(form_data.username)
    )["Items"]
    if len(users) > 0:
        user = users[0]
        user_in_db = DBUser(**user)
        if password_utils.verify_password(form_data.password, user_in_db.password):
            token = TokenService.generate_token(user_in_db.id)
            TokenService.save_token(token)
            user_response = User(**user_in_db.model_dump())
            return DataResponse().success_response(LoginResponse(user=user_response, token=token))
    raise BadRequestException(name="Your email or password is incorrect")


@router.post("/signup", response_model=DataResponse[LoginResponse])
def signup(user: UserCreate):
    user_table = get_table(DBTable.USERS)
    exist_user = user_table.scan(
        FilterExpression=Attr("email").eq(user.email)
    )
    if len(exist_user["Items"]) > 0:
        raise BadRequestException(name="Users already exist")
    
    hashed_password = password_utils.hash_password(user.password)
    user.password = hashed_password
    new_user = DBUser(**user.model_dump(), id=uuid.uuid4().hex, created_at=datetime.now().astimezone().isoformat())

    user_table.put_item(Item=new_user.model_dump())

    user_response = User(**new_user.model_dump())

    token = TokenService.generate_token(new_user.id)
    TokenService.save_token(token)

    return DataResponse().success_response(LoginResponse(user=user_response, token=token))