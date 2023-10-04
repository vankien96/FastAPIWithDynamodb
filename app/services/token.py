from datetime import datetime, timedelta
from jose import jwt, JWTError
from ..schemas.token import GeneratedToken, Token, EncodeTokenData
from ..configs.env_config import get_settings
from ..utils.string_utils import random_string
from ..schemas.exception import UnAuthorizeException, BadRequestException
from ..configs.database import get_table, delete_item
from ..configs.constants import DBTable

class TokenService:

    @staticmethod
    def refresh_token(refresh_token: str, user_id: str) -> Token:
        token_table = get_table(DBTable.TOKENS)
        response = token_table.get_item(Key={"refresh_token": refresh_token})
        if "Item" in response:
            token_in_db = response["Item"]
            if token_in_db is not None:
                token = Token(**token_in_db)
                expire_at = datetime.fromtimestamp(token.refresh_token_expire_at)
                if expire_at > datetime.now():
                    new_token = TokenService.generate_token(user_id)
                    TokenService.save_token(new_token)
                    token_table.delete_item(Key={'refresh_token': refresh_token})
                    return new_token
        raise BadRequestException("Refresh token is incorrect")

    @staticmethod
    def verify_access_token(token: str, allow_expired: bool) -> str:
        settings = get_settings()
        try:
            data = jwt.decode(token, key=settings.access_token_secret, algorithms=settings.token_algo)
            encoded_data = EncodeTokenData(**data)
            expire_time = datetime.fromtimestamp(encoded_data.exp)
            if allow_expired or expire_time > datetime.now():
                return encoded_data.sub
            raise UnAuthorizeException()
        except:
            raise UnAuthorizeException()
        
    @staticmethod
    def save_token(token: Token):
        token_table = get_table(DBTable.TOKENS)
        token_table.put_item(Item=token.model_dump())

    @staticmethod
    def generate_token(subject: str) -> Token:
        settings = get_settings()
        access_token = TokenService.generate_access_token(subject)
        refresh_token = random_string(settings.refresh_token_length)
        refresh_token_expire_at = int((datetime.now() + timedelta(minutes=settings.refresh_token_life_time)).timestamp())
        return Token(access_token=access_token.token, 
                    access_token_expire_at=access_token.expire_at, 
                    refresh_token=refresh_token, 
                    refresh_token_expire_at=refresh_token_expire_at)

    @staticmethod
    def generate_access_token(subject: str) -> GeneratedToken:
        settings = get_settings()
        expire_time = int((datetime.now() + timedelta(minutes=settings.access_token_life_time)).timestamp())
        encode_data = {"exp": expire_time, "sub": subject}
        token = jwt.encode(encode_data, settings.access_token_secret, settings.token_algo)
        return GeneratedToken(token=token, expire_at=expire_time)