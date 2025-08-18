import base64
import struct
import logging
from typing import Tuple
from config.settings import settings

logger = logging.getLogger(__name__)

class MeloTTSService:
    def __init__(self):
        self.language = settings.melotts_language

    def _create_simple_wav(self, text: str) -> bytes:
        """簡単なWAVファイルを生成（テスト用）"""
        # 簡単なテスト音声として、ビープ音を生成
        sample_rate = 22050
        duration = 0.5  # 0.5秒
        frequency = 440  # A4音（ラ）

        num_samples = int(sample_rate * duration)

        # サイン波を生成
        import math
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * t))
            samples.append(sample)

        # WAVファイルのヘッダー
        wav_data = b'RIFF'
        wav_data += struct.pack('<I', 36 + num_samples * 2)  # ファイルサイズ
        wav_data += b'WAVE'
        wav_data += b'fmt '
        wav_data += struct.pack('<I', 16)  # fmt チャンクサイズ
        wav_data += struct.pack('<H', 1)   # PCM
        wav_data += struct.pack('<H', 1)   # モノラル
        wav_data += struct.pack('<I', sample_rate)  # サンプルレート
        wav_data += struct.pack('<I', sample_rate * 2)  # バイトレート
        wav_data += struct.pack('<H', 2)   # ブロックアライン
        wav_data += struct.pack('<H', 16)  # ビット深度
        wav_data += b'data'
        wav_data += struct.pack('<I', num_samples * 2)  # データサイズ

        # 音声データを追加
        for sample in samples:
            wav_data += struct.pack('<h', sample)

        return wav_data

    async def text_to_speech(
        self,
        text: str,
        speed: float = 1.0
    ) -> Tuple[str, str]:
        """テキストを音声に変換"""
        logger.info(f"MeloTTS text_to_speech called with text: {text}")

        # MeloTTSが利用できない場合は、簡単なビープ音を返す
        # （実際の音声合成はWeb Speech APIで行う）
        wav_data = self._create_simple_wav(text)
        audio_base64 = base64.b64encode(wav_data).decode('utf-8')

        logger.info(f"Generated simple WAV audio: {len(wav_data)} bytes")
        return audio_base64, "wav"

# シングルトンインスタンス
melotts_service = MeloTTSService()
