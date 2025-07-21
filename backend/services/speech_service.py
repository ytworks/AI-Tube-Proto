from openai import AsyncOpenAI
import base64
import io
from typing import Tuple, Optional
import logging
import tempfile
import os
import json
from config.settings import settings

logger = logging.getLogger(__name__)

class SpeechService:
    def __init__(self):
        self.api_key_exists = bool(settings.openai_api_key)
        if self.api_key_exists:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        else:
            self.client = None
    
    def _generate_mock_audio(self, text: str) -> Tuple[str, str]:
        """APIキーがない場合のモック音声データを生成"""
        # 簡単なWAVヘッダーを持つ無音の音声データを作成
        # これは実際には音が出ませんが、プレースホルダーとして機能します
        wav_header = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00'
        return base64.b64encode(wav_header).decode('utf-8'), "wav"
    
    async def speech_to_text(self, audio_base64: str, audio_format: str = "webm") -> str:
        # APIキーがない場合は定型文を返す
        if not self.api_key_exists:
            return "（音声認識機能を使用するにはAPIキーが必要です）"
        
        try:
            audio_data = base64.b64decode(audio_base64)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_format}") as tmp_file:
                tmp_file.write(audio_data)
                tmp_file_path = tmp_file.name
            
            try:
                with open(tmp_file_path, "rb") as audio_file:
                    transcript = await self.client.audio.transcriptions.create(
                        model=settings.openai_whisper_model,
                        file=audio_file,
                        language="ja"
                    )
                
                return transcript.text
            finally:
                os.unlink(tmp_file_path)
                
        except Exception as e:
            logger.error(f"Error in speech to text: {str(e)}")
            raise Exception(f"Failed to convert speech to text: {str(e)}")
    
    async def text_to_speech(
        self, 
        text: str, 
        voice: Optional[str] = None,
        speed: float = 1.0
    ) -> Tuple[str, str]:
        # APIキーがない場合はモック音声を返す
        if not self.api_key_exists:
            return self._generate_mock_audio(text)
        
        # 環境変数から音声を取得、指定がなければデフォルト
        voice = voice or settings.openai_tts_voice
        
        try:
            response = await self.client.audio.speech.create(
                model=settings.openai_tts_model,
                voice=voice,
                input=text,
                speed=speed
            )
            
            audio_content = response.content
            
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            
            return audio_base64, "mp3"
            
        except Exception as e:
            logger.error(f"Error in text to speech: {str(e)}")
            raise Exception(f"Failed to convert text to speech: {str(e)}")

speech_service = SpeechService()