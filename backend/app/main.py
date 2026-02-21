from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, auth, database, ai_service
from .database import engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Post-Graduate Entrance Exam Platform")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/chat", response_model=schemas.ChatResponse)
async def chat(
    question: schemas.ChatQuestion,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    # Get answer from AI Service
    response = await ai_service.ai_service.get_answer(question.question)
    
    # Save history
    history = models.ChatHistory(
        user_id=current_user.id,
        question=question.question,
        answer=response.answer
    )
    db.add(history)
    db.commit()
    
    return response

@app.get("/universities/", response_model=List[schemas.University])
def read_universities(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    universities = db.query(models.University).offset(skip).limit(limit).all()
    return universities

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Post-Graduate Entrance Exam Platform API"}
