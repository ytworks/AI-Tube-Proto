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
        self.tts_provider = settings.tts_provider
        self.stt_provider = settings.stt_provider
        
        if self.api_key_exists:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        else:
            self.client = None
            
        # ローカルTTSを使用する場合
        if self.tts_provider == "local":
            from services.melotts_service import melotts_service
            self.melotts = melotts_service
            
        # ローカルSTTを使用する場合
        if self.stt_provider == "local":
            try:
                from services.whisper_service import whisper_service
                self.whisper = whisper_service
            except ImportError as e:
                logger.warning(f"Failed to import Whisper service: {str(e)}")
                self.whisper = None
    
    def _generate_mock_audio(self, text: str) -> Tuple[str, str]:
        """APIキーがない場合のモック音声データを生成"""
        # 簡単なWAVヘッダーを持つ無音の音声データを作成
        # これは実際には音が出ませんが、プレースホルダーとして機能します
        wav_header = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00'
        return base64.b64encode(wav_header).decode('utf-8'), "wav"
    
    async def speech_to_text(self, audio_base64: str, audio_format: str = "webm") -> str:
        # ローカルSTTを使用する場合
        if self.stt_provider == "local":
            if self.whisper is None:
                return "（ローカルWhisperが利用できません。必要なパッケージをインストールしてください）"
            try:
                return await self.whisper.speech_to_text(audio_base64, audio_format)
            except Exception as e:
                logger.error(f"Local Whisper error: {str(e)}")
                return f"（ローカル音声認識エラー: {str(e)}）"
        
        # OpenAI STTを使用する場合
        # APIキーがない場合の処理
        if not self.api_key_exists:
            return "（音声認識機能を使用するにはOpenAI APIキーが必要です）"
        
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
        # ローカルTTSを使用する場合
        if self.tts_provider == "local":
            try:
                return await self.melotts.text_to_speech(text, speed)
            except Exception as e:
                logger.error(f"MeloTTS error, falling back to mock audio: {str(e)}")
                return self._generate_mock_audio(text)
        
        # OpenAI TTSを使用する場合
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