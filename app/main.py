from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .configs.env_config import get_settings
from .configs.error_handler import add_exception_handler
from .routers import auth, user
from .helpers.create_database import create_tables

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(user.router)
add_exception_handler(app)

@app.get("/")
async def root():
    return {"message": get_settings().app_name}

@app.get("/createDatabase")
async def create_database_table():
    create_tables()
    return {"message": "Create tables success"}