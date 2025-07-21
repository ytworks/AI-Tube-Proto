from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    google_cloud_api_key: Optional[str] = None
    host: str = "0.0.0.0"
    port: int = 8000
    
    # OpenAI Model Settings
    openai_chat_model: str = "gpt-3.5-turbo"
    openai_whisper_model: str = "whisper-1"
    openai_tts_model: str = "tts-1"
    openai_tts_voice: str = "alloy"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 環境変数から取得を試みる
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")

settings = Settings()