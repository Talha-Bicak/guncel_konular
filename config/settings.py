from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Gemini API
    GOOGLE_API_KEY: Optional[str] = None
    
    # Model Settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    
    # Cache Settings
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600  # 1 hour
    
    # RAG Settings
    CHROMA_DB_PATH: str = "./chroma_db"
    TOP_K_DOCUMENTS: int = 5
    
    # RARE Settings
    REASONING_DEPTH: int = 3
    PREDICTION_CONFIDENCE_THRESHOLD: float = 0.7
    
    class Config:
        env_file = ".env"

settings = Settings()