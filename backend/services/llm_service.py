from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from typing import Dict, List, Optional
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.provider = settings.llm_provider
        self.sessions: Dict[str, List[Dict[str, str]]] = {}

        # OpenAI クライアントの初期化
        if self.provider == "openai":
            self.api_key_exists = bool(settings.openai_api_key)
            if self.api_key_exists:
                self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)
            else:
                self.openai_client = None

        # Claude クライアントの初期化
        elif self.provider == "claude":
            self.api_key_exists = bool(settings.anthropic_api_key)
            if self.api_key_exists:
                self.claude_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
            else:
                self.claude_client = None

    async def get_chat_response(
        self,
        message: str,
        session_id: Optional[str] = None,
        system_prompt: str = "You are a helpful voice assistant. Keep your responses concise and conversational."
    ) -> str:
        # APIキーがない場合は定型文を返す
        if not self.api_key_exists:
            # ローカルTTSのテストメッセージの場合
            if message == "ローカルTTSのテストメッセージ":
                from datetime import datetime
                import pytz

                # 日本時間を取得
                japan_tz = pytz.timezone('Asia/Tokyo')
                now = datetime.now(japan_tz)

                # 時刻を日本語形式でフォーマット
                hour = now.hour
                minute = now.minute

                # 午前/午後の判定
                period = "午前" if hour < 12 else "午後"
                display_hour = hour if hour <= 12 else hour - 12
                if display_hour == 0:
                    display_hour = 12

                time_str = f"{period}{display_hour}時{minute}分"

                return f"こんにちは、ローカルTTSです。現在の時刻は{time_str}です。"

            provider_name = "OpenAI" if self.provider == "openai" else "Anthropic"
            return f"APIキーがセットされていません。環境変数に{provider_name} APIキーを設定してください。"

        try:
            if self.provider == "openai":
                messages = [{"role": "system", "content": system_prompt}]

                if session_id and session_id in self.sessions:
                    messages.extend(self.sessions[session_id])

                messages.append({"role": "user", "content": message})

                response = await self.openai_client.chat.completions.create(
                    model=settings.openai_chat_model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )

                assistant_message = response.choices[0].message.content

            elif self.provider == "claude":
                # Claudeのメッセージ形式に変換
                claude_messages = []

                if session_id and session_id in self.sessions:
                    for msg in self.sessions[session_id]:
                        claude_messages.append({
                            "role": msg["role"] if msg["role"] != "system" else "user",
                            "content": msg["content"]
                        })

                claude_messages.append({"role": "user", "content": message})

                response = await self.claude_client.messages.create(
                    model=settings.claude_model,
                    system=system_prompt,
                    messages=claude_messages,
                    temperature=0.7,
                    max_tokens=500
                )

                assistant_message = response.content[0].text

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
