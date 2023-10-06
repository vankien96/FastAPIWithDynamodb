from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T", bound=BaseModel)

class ErrorResponse(BaseModel):
    errorCode: Optional[str] = None
    message: str

class DataResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    error: Optional[ErrorResponse] = None

    def success_response(self, data: T):
        self.data = data
        return self
    
    def error_response(self, message: str, errorCode: Optional[str] = None):
        self.error = ErrorResponse(errorCode=errorCode, message=message)
        return self
    