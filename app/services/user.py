from fastapi import Depends
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordBearer

from ..configs.env_config import get_settings, AppSetting
from ..schemas.user import User
from .token import TokenService
from ..configs.constants import DBTable
from ..configs.database import get_table
from ..schemas.exception import UnAuthorizeException

class UserService:

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

    @staticmethod
    def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> Optional[str]:
        current_user_id = TokenService.verify_access_token(token, allow_expired=True)
        return current_user_id

    @staticmethod
    def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Optional[User]:
        current_user_id = TokenService.verify_access_token(token, allow_expired=False)
        user_table = get_table(DBTable.USERS)
        user = user_table.get_item(Key={"id":current_user_id})["Item"]
        if user is not None:
            return User(**user)
        raise UnAuthorizeException()
