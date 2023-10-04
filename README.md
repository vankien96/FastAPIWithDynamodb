## BASE FastAPI app with dynamodb

### How to run this
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

##### Prepare IAM user in AWS Account
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
Create table code will be in `bin/create_database.py`
You can call `http://127.0.0.1/createDatabase` to execute it