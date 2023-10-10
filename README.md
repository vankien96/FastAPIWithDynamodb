## BASE FastAPI app with dynamodb

### How to run
#### Create a virtual env and install requirement
##### Create new virtual env
```
python3 -m venv env
```
##### Activate the environment
```
source ./venv/bin/activate
```
To check it worked, use:
```
which pip
```
If it shows the pip binary at venv/bin/pip then it worked. 🎉
##### Install requirements
```
pip install -r requirements.txt
```

##### Prepare IAM user in AWS Account (If you want to connect directly to Dynamodb on AWS)
You can follow this [link](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) to create a new IAM user
and don't forget to attach Dynamodb permission
We will use this IAM user access_key/secret_key in next step

##### Prepare env file
Create new file and name it `.env`
Copy content from `.env.example` and fill in the value

##### Install mypy_boto3_builder
In this project i'm using [Boto3 type annotations generator](https://github.com/youtype/mypy_boto3_builder) to support autocomplete, find and fix potential bugs.

##### Start the server
```
uvicorn app.main:app --reload
```

### Create database table
Create table code will be in `helpers/create_database.py`
You can call `http://127.0.0.1/createDatabase` to execute it

### Run with Docker
In this setup, these ports will be use:
FastAPI app: 8080
Dynamodb-local: 8000
Dynamodb-admin: 8001

##### Prepare env file
Create new file and name it `.env`
Copy content from `.env.example` and fill in the value
Note: Since we will run dynamodb locally so you can put random string in AWS_ACCESS_KEY, AWS_SECRET_KEY,AWS_REGION
with DYNAMO_ENDPOINT="http://localhost:8000" (if localhost doesn't work for you, let's try your actual IP address)

#### Start the server
```
docker compose --env-file .env up
```

#### Check if it works
Call http://localhost:8080/createDatabase
Go to http://localhost:8001 and check if 2 tables Users and Tokens is created or not