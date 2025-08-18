import whisper
import base64
import tempfile
import os
import logging
from typing import Optional
import torch
import numpy as np

logger = logging.getLogger(__name__)

class WhisperService:
    def __init__(self):
        self.model = None
        self.model_name = "base"  # base model as default for good balance of speed and accuracy
        self.device = None
        self._initialize_model()

    def _initialize_model(self):
        """Whisperモデルの初期化"""
        try:
            # デバイスの選択（CUDA利用可能ならCUDA、そうでなければCPU）
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {self.device}")

            # モデルのロード
            logger.info(f"Loading Whisper model: {self.model_name}")
            self.model = whisper.load_model(self.model_name, device=self.device)
            logger.info("Whisper model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Whisper model: {str(e)}")
            self.model = None

    async def speech_to_text(
        self,
        audio_base64: str,
        audio_format: str = "webm",
        language: str = "ja"
    ) -> str:
        """
        音声データをテキストに変換

        Args:
            audio_base64: Base64エンコードされた音声データ
            audio_format: 音声フォーマット（webm, mp3, wav等）
            language: 言語コード（デフォルトは日本語）

        Returns:
            認識されたテキスト
        """
        if self.model is None:
            raise Exception("Whisper model is not initialized")

        try:
            # Base64デコード
            audio_data = base64.b64decode(audio_base64)

            # 一時ファイルに保存
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f".{audio_format}"
            ) as tmp_file:
                tmp_file.write(audio_data)
                tmp_file_path = tmp_file.name

            try:
                # Whisperで音声認識
                result = self.model.transcribe(
                    tmp_file_path,
                    language=language,
                    task="transcribe",  # translate ではなく transcribe を使用
                    fp16=self.device == "cuda"  # CUDAの場合はFP16を使用
                )

                # 認識結果のテキストを返す
                text = result["text"].strip()
                logger.info(f"Transcription successful: {text[:50]}...")
                return text

            finally:
                # 一時ファイルを削除
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)

        except Exception as e:
            logger.error(f"Error in Whisper speech-to-text: {str(e)}")
            raise Exception(f"Failed to convert speech to text: {str(e)}")

    def change_model(self, model_name: str):
        """
        Whisperモデルを変更

        Available models:
        - tiny: 最速、精度低
        - base: バランス型（デフォルト）
        - small: やや高精度
        - medium: 高精度
        - large: 最高精度、最も遅い
        """
        available_models = ["tiny", "base", "small", "medium", "large"]
        if model_name not in available_models:
            raise ValueError(f"Model must be one of {available_models}")

        self.model_name = model_name
        self._initialize_model()

# シングルトンインスタンス
whisper_service = WhisperService()
