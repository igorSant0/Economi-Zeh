from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserParams(BaseModel):
    id_user: str


class UserQuerys(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    page: Optional[int] = Field(1, ge=1, description="Page number")
    limit: Optional[int] = Field(10, ge=1, le=100, description="Items per page")


class UserCreateData(BaseModel):
    name: str = Field(..., min_length=3, description="Full name")
    email: EmailStr = Field(..., description="Unique system e-mail")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF")
    password: str = Field(..., min_length=6, description="Strong password")
    model_config = ConfigDict(extra="forbid")


class UserUpdateData(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    model_config = ConfigDict(extra="forbid")


class UserResponse(BaseModel):
    id_user: str
    name: str
    email: str
    cpf: str
    model_config = ConfigDict(from_attributes=True)
