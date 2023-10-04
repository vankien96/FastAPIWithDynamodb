import boto3
from typing import Union
from .env_config import get_settings

def connect_database():
    settings = get_settings()
    db = boto3.resource('dynamodb',
                        region_name=settings.aws_region,
                        aws_access_key_id=settings.aws_access_key,
                        aws_secret_access_key=settings.aws_secret_key)
    return db

def get_table(name: str):
    dynamodb = connect_database()
    table = dynamodb.Table(name)
    return table

TableAttributeValueTypeDef = Union[
    bytes,
    bytearray,
    str,
    int,
    bool,
    None,
]


def delete_item(primaryKey: str, value: TableAttributeValueTypeDef, table_name: str):
    dynamodb = connect_database()
    table = dynamodb.Table(table_name)
    table.delete_item(Key={primaryKey: value})