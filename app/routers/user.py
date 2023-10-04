from fastapi import APIRouter, Depends
from typing import Annotated
from ..schemas.user import User
from ..schemas.response import DataResponse
from ..services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.get("/me", response_model=DataResponse[User])
async def get_user_me(current_user: Annotated[User, Depends(UserService.get_current_user)]):
    print(current_user.first_name)
    return DataResponse().success_response(current_user)