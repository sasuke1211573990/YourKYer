from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    target_university: Optional[str] = None
    target_major: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UniversityBase(BaseModel):
    name: str
    location: str
    level: str
    website: Optional[str] = None

class UniversityCreate(UniversityBase):
    admission_guide: Optional[str] = None
    recruit_policy: Optional[str] = None

class University(UniversityBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChatQuestion(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = []
