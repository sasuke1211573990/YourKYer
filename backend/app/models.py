from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    target_university = Column(String, nullable=True)
    target_major = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    chat_history = relationship("ChatHistory", back_populates="user")

class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    level = Column(String) # 985/211/Ordinary
    website = Column(String)
    admission_guide = Column(Text) # 招生简章
    recruit_policy = Column(Text) # 招生政策
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Major(Base):
    __tablename__ = "majors"
    
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    name = Column(String)
    code = Column(String)
    exam_subjects = Column(String) # 考试科目
    score_line = Column(String) # 录取分数线 JSON or Text
    
    university = relationship("University", backref="majors")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="chat_history")

class CrawledData(Base):
    __tablename__ = "crawled_data"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    link = Column(Text, unique=True)
    publish_date = Column(DateTime)
    content = Column(Text)
    source = Column(Text)
    category = Column(Text)
    university = Column(Text)
