from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json

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

@app.post("/chat")
async def chat(
    question: schemas.ChatQuestion,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    # Use StreamingResponse
    async def generate():
        full_answer = ""
        async for chunk_str in ai_service.ai_service.get_answer_stream(question.question, db):
            yield chunk_str
            # Parse chunk to accumulate full answer for history
            try:
                chunk_data = json.loads(chunk_str)
                if chunk_data["type"] == "answer":
                    full_answer += chunk_data["content"]
            except:
                pass
        
        # Save history after streaming is complete
        # Note: In a real app, this should be done in a background task or handled carefully
        # since the response is already sent. However, with generator, code after yield runs.
        try:
            # We need a new DB session or ensure the current one is still valid.
            # Since 'db' dependency is closed after request, we should use it carefully.
            # Actually, FastAPI dependencies with yield close after response.
            # But here we are inside the response generator.
            history = models.ChatHistory(
                user_id=current_user.id,
                question=question.question,
                answer=full_answer
            )
            db.add(history)
            db.commit()
        except Exception as e:
            print(f"Failed to save history: {e}")

    return StreamingResponse(generate(), media_type="application/x-ndjson")

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket, db: Session = Depends(database.get_db)):
    await websocket.accept()
    current_user = None
    try:
        # Authenticate user from query parameter token
        token = websocket.query_params.get("token")
        if not token:
            await websocket.send_json({"type": "error", "content": "Authentication token missing"})
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = auth.decode_access_token(token)
            user_email: str = payload.get("sub")
            if user_email is None:
                raise credentials_exception
            current_user = db.query(models.User).filter(models.User.email == user_email).first()
            if current_user is None:
                raise credentials_exception
        except Exception:
            await websocket.send_json({"type": "error", "content": "Invalid authentication token"})
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get("type") == "question":
                    question_text = message.get("content")
                    if not question_text:
                        await websocket.send_json({"type": "error", "content": "Question content missing"})
                        continue

                    full_answer = ""
                    async for chunk_str in ai_service.ai_service.get_answer_stream(question_text, db):
                        await websocket.send_text(chunk_str)
                        try:
                            chunk_data = json.loads(chunk_str)
                            if chunk_data["type"] == "answer":
                                full_answer += chunk_data["content"]
                        except:
                            pass
                    
                    try:
                        history = models.ChatHistory(
                            user_id=current_user.id,
                            question=question_text,
                            answer=full_answer
                        )
                        db.add(history)
                        db.commit()
                    except Exception as e:
                        print(f"Failed to save history: {e}")
                else:
                    await websocket.send_json({"type": "error", "content": "Unknown message type"})
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "content": "Invalid JSON format"})
            except Exception as e:
                await websocket.send_json({"type": "error", "content": f"Server error: {str(e)}"})

    except WebSocketDisconnect:
        print(f"Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")

@app.get("/universities/", response_model=List[schemas.University])
def read_universities(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    universities = db.query(models.University).offset(skip).limit(limit).all()
    return universities

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Post-Graduate Entrance Exam Platform API"}
