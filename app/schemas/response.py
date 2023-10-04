from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

class ResponseMeta(BaseModel):
    error: str

class BaseResponse(BaseModel):
    meta: Optional[ResponseMeta] = None

    def error(self, message: str):
        self.meta = ResponseMeta(error=message)
        return self

T = TypeVar("T", bound=BaseModel)

class DataResponse(BaseResponse, Generic[T]):
    data: Optional[T] = None

    def success_response(self, data: T):
        self.data = data
        return self