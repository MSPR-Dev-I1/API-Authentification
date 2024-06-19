from pydantic import BaseModel

class ValidationRequest(BaseModel):
    token: str
    service_key: str

class ValidationResponse(BaseModel):
    validation: bool

class TokenRequest(BaseModel):
    role: int

class TokenResponse(BaseModel):
    token: str
