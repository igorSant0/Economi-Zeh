from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserParams(BaseModel):
    user_id: str


class UserQuerys(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_cpf: Optional[str] = None
    page: Optional[int] = Field(1, ge=1, description="Page number")
    limit: Optional[int] = Field(10, ge=1, le=100, description="Items per page")


class UserCreateData(BaseModel):
    user_name: str = Field(..., min_length=3, description="Full name")
    user_email: EmailStr = Field(..., description="Unique system e-mail")
    user_cpf: str = Field(..., min_length=11, max_length=14, description="CPF")
    user_password: str = Field(..., min_length=6, description="Strong password")
    model_config = ConfigDict(extra="forbid")


class UserUpdateData(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_cpf: Optional[str] = None
    model_config = ConfigDict(extra="forbid")


class UserResponse(BaseModel):
    id_user: str
    user_name: str
    user_email: str
    user_cpf: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PaginationInfo(BaseModel):
    count: int
    lastPage: int
    page: int
    perPage: int


class UserListResponse(BaseModel):
    data: List[UserResponse]
    pagination: PaginationInfo
