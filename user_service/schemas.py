from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional
import re

class UserCreate(BaseModel):
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: EmailStr
    password: str = Field(
        ..., 
        min_length=6, 
        max_length=50
    )

    @staticmethod
    def validate_password(password: str):
        if not re.search(r"[A-Z]", password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[a-z]", password):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r"\d", password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол (!@#$ и т.д.)")
        return password

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_password

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    birth_date: Optional[date] = None
    phone: Optional[str] = Field(
        None, 
        min_length=10, 
        max_length=15, 
        pattern=r"^\+?[1-9]\d{1,14}$"
    )

class UserAuth(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[datetime]
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime

