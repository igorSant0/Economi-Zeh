from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LoginData(BaseModel):
    user_email: Optional[EmailStr] = None
    user_password: str = Field(..., min_length=6, description="Strong password")
    user_phone: Optional[str] = None
    uer_cpf: Optional[str] = None

class LoginToken(BaseModel):
    token: str