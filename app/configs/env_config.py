from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class AppSetting(BaseSettings):
    access_token_life_time: int
    access_token_secret: str
    refresh_token_life_time: int
    refresh_token_length: int
    token_algo: str
    app_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    dynamo_endpoint: Optional[str]

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return AppSetting()