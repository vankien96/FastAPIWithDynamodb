from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from ..schemas.exception import UnAuthorizeException, BadRequestException
from ..schemas.response import BaseResponse

def add_exception_handler(app: FastAPI):
    @app.exception_handler(UnAuthorizeException)
    async def unauthorize_exception_handler(request: Request, exc: UnAuthorizeException):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=BaseResponse().error(message="Unauthorized").model_dump())
    
    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request: Request, exc: BadRequestException):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=BaseResponse().error(message=exc.name).model_dump())
    

