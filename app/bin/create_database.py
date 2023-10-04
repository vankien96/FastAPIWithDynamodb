from ..configs.database import connect_database

def create_user_table():
    dynamodb = connect_database()
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.wait_until_exists()

def create_token_table():
    dynamodb = connect_database()
    table = dynamodb.create_table(
        TableName='Tokens',
        KeySchema=[
            {
                'AttributeName': 'refresh_token',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'refresh_token',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.wait_until_exists()
    

def create_tables():
    create_token_table()
    create_user_table()