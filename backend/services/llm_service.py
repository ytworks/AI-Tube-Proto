from openai import AsyncOpenAI
from typing import Dict, List, Optional
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.api_key_exists = bool(settings.openai_api_key)
        if self.api_key_exists:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        else:
            self.client = None
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
    
    async def get_chat_response(
        self, 
        message: str, 
        session_id: Optional[str] = None,
        system_prompt: str = "You are a helpful voice assistant. Keep your responses concise and conversational."
    ) -> str:
        # APIキーがない場合は定型文を返す
        if not self.api_key_exists:
            return "APIキーがセットされていません。環境変数にOpenAI APIキーを設定してください。"
        
        try:
            messages = [{"role": "system", "content": system_prompt}]
            
            if session_id and session_id in self.sessions:
                messages.extend(self.sessions[session_id])
            
            messages.append({"role": "user", "content": message})
            
            response = await self.client.chat.completions.create(
                model=settings.openai_chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            if session_id:
                if session_id not in self.sessions:
                    self.sessions[session_id] = []
                self.sessions[session_id].append({"role": "user", "content": message})
                self.sessions[session_id].append({"role": "assistant", "content": assistant_message})
                
                if len(self.sessions[session_id]) > 20:
                    self.sessions[session_id] = self.sessions[session_id][-20:]
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error getting chat response: {str(e)}")
            raise Exception(f"Failed to get LLM response: {str(e)}")
    
    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

llm_service = LLMService()