from pydantic_settings import BaseSettings
from typing import Optional, Literal
import os

class Settings(BaseSettings):
    # LLM Provider Selection
    llm_provider: Literal["openai", "claude"] = "openai"
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_cloud_api_key: Optional[str] = None
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # OpenAI Model Settings
    openai_chat_model: str = "gpt-3.5-turbo"
    openai_whisper_model: str = "whisper-1"
    openai_tts_model: str = "tts-1"
    openai_tts_voice: str = "alloy"
    
    # Claude Model Settings
    claude_model: str = "claude-3-opus-20240229"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 環境変数から取得を試みる
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.anthropic_api_key:
            self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # 空文字列やダミー値をNoneに変換
        if self.openai_api_key in ["", "your-openai-api-key-here", None]:
            self.openai_api_key = None
        if self.anthropic_api_key in ["", "your-anthropic-api-key-here", None]:
            self.anthropic_api_key = None

settings = Settings()