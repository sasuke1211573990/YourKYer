from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Post-Graduate Entrance Exam Platform"
    
    # Database
    # POSTGRES_USER: str = "postgres"
    # POSTGRES_PASSWORD: str = "postgres"
    # POSTGRES_SERVER: str = "db"
    # POSTGRES_PORT: str = "5432"
    # POSTGRES_DB: str = "edu_platform"
    # DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Security
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Service
    # Use a compatible OpenAI API (e.g. DeepSeek, Moonshot, or OpenAI itself)
    # Defaulting to a free compatible endpoint or placeholder
    LLM_API_KEY: str = "sk-..." 
    LLM_BASE_URL: str = "https://api.openai.com/v1" 
    LLM_MODEL: str = "gpt-3.5-turbo"
    
    BAIDU_API_KEY: str = ""
    BAIDU_SECRET_KEY: str = ""
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
