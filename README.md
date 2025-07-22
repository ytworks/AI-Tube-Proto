# 音声対話型AIアシスタント

ブラウザベースの音声対話型AIアシスタントシステムです。音声入力を受け取り、ChatGPT/Claude APIを使用して応答を生成し、音声で返答します。

## 機能

- 🎤 音声入力（Speech-to-Text）
  - OpenAI Whisper API
  - ローカルWhisper（APIキー不要）
- 🤖 LLMによる応答生成
  - OpenAI ChatGPT
  - Anthropic Claude
- 🔊 音声出力（Text-to-Speech）
  - OpenAI TTS API
  - ローカルTTS（簡易実装）
- 🌐 ブラウザベースのインターフェース
- 🔒 セキュアなAPIキー管理
- 🔧 APIキーなしでも動作（テストモード）
- ⚙️ 環境変数による柔軟な設定
- 🔄 プロバイダー切り替え機能

## 技術スタック

### バックエンド
- Python 3.8+
- FastAPI
- OpenAI API (Whisper, ChatGPT, TTS)
- Anthropic Claude API
- OpenAI Whisper（ローカル音声認識）
- python-dotenv

### フロントエンド
- React 18
- TypeScript
- Vite
- Web Audio API

## セットアップ

### 前提条件
- Python 3.8以上
- Node.js 16以上
- （オプション）OpenAI APIキー
- （オプション）Anthropic APIキー

### バックエンドのセットアップ

1. バックエンドディレクトリに移動
```bash
cd backend
```

2. Python仮想環境を作成・有効化
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. 依存関係をインストール
```bash
pip install -r requirements.txt

# ローカルWhisperを使用する場合（自動的にインストールされます）
# 初回実行時にモデルが自動ダウンロードされます

# MeloTTSを使用する場合は追加でインストール（オプション、現在は簡易実装のため不要）
# MeCabが必要: brew install mecab (macOS) または apt-get install mecab (Ubuntu)
# pip install git+https://github.com/myshell-ai/MeloTTS.git
```

4. 環境変数を設定
```bash
cp .env.example .env
```
`.env`ファイルを編集し、必要に応じてAPIキーを設定してください。
APIキーなしでもローカル機能で動作可能です。

5. サーバーを起動
```bash
uvicorn main:app --reload
```

### フロントエンドのセットアップ

1. フロントエンドディレクトリに移動
```bash
cd frontend
```

2. 依存関係をインストール
```bash
npm install
```

3. 環境変数を設定
```bash
cp .env.example .env
```

4. 開発サーバーを起動
```bash
npm run dev
```

## 使い方

1. ブラウザで http://localhost:5173 にアクセス
2. マイクへのアクセスを許可
3. 録音ボタンをクリックして話しかける
4. 録音停止ボタンをクリック
5. AIの応答を音声で聞く

### APIキーなしでの動作
- **STT_PROVIDER=local**: ローカルWhisperで音声認識
- **TTS_PROVIDER=local**: ビープ音 + Web Speech APIで音声合成
- **LLMなし**: 「こんにちは、ローカルTTSです。現在の時刻は...」というテストメッセージを返答

## API仕様

### エンドポイント

- `POST /api/speech-to-text` - 音声をテキストに変換
- `POST /api/chat` - テキストメッセージをLLMに送信
- `POST /api/text-to-speech` - テキストを音声に変換
- `POST /api/process-voice` - 音声入力から音声応答まで一括処理

## トラブルシューティング

### マイクが使えない場合
- HTTPSでアクセスしているか確認（開発環境ではlocalhostは例外）
- ブラウザの設定でマイクアクセスが許可されているか確認

### APIエラーが発生する場合
- APIキーが正しく設定されているか確認
- APIの利用制限に達していないか確認

### APIキーがない場合
- ローカル機能を使用して動作します
- STT: ローカルWhisperで音声認識（初回はモデルダウンロードに時間がかかります）
- LLM: テストメッセージを返答
- TTS: ビープ音 + Web Speech APIで音声合成

## カスタマイズ

### LLMプロバイダーの選択

`.env`ファイルで以下を設定：

```env
# LLMプロバイダー選択 (openai または claude)
LLM_PROVIDER=claude

# Claude使用時はAnthropicのAPIキーが必要
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### OpenAIモデルの変更

`.env`ファイルで以下の環境変数を設定できます：

```env
# チャットモデル (デフォルト: gpt-3.5-turbo)
OPENAI_CHAT_MODEL=gpt-4

# 音声認識モデル (デフォルト: whisper-1)
OPENAI_WHISPER_MODEL=whisper-1

# 音声合成モデル (デフォルト: tts-1)
OPENAI_TTS_MODEL=tts-1-hd

# 音声の種類 (デフォルト: alloy)
# 選択肢: alloy, echo, fable, onyx, nova, shimmer
OPENAI_TTS_VOICE=nova
```

### Claudeモデルの変更

```env
# Claudeモデル (デフォルト: claude-3-opus-20240229)
# 選択肢: claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307
CLAUDE_MODEL=claude-3-sonnet-20240229
```

利用可能なモデル：
- **OpenAI チャット**: gpt-3.5-turbo, gpt-4, gpt-4-turbo-preview
- **Claude**: claude-3-opus (最高性能), claude-3-sonnet (バランス), claude-3-haiku (高速)
- **音声合成**: tts-1 (標準品質), tts-1-hd (高品質)
- **音声**: alloy, echo, fable, onyx, nova, shimmer

### Speech-to-Textプロバイダーの選択

```env
# STTプロバイダー選択 (openai または local)
STT_PROVIDER=local

# ローカルWhisper使用時の設定
WHISPER_MODEL=base  # tiny, base, small, medium, large から選択
WHISPER_DEVICE=auto  # cpu, cuda, auto から選択
```

### Text-to-Speechプロバイダーの選択

```env
# TTSプロバイダー選択 (openai または local)
TTS_PROVIDER=local

# MeloTTS使用時の設定（現在は簡易実装のため未使用）
MELOTTS_LANGUAGE=JP  # EN, JP, ZH から選択
MELOTTS_DEVICE=auto  # cpu, cuda, auto から選択
```

## 動作モードの組み合わせ

| STT | LLM | TTS | 説明 |
|-----|-----|-----|------|
| local | なし | local | 完全ローカル動作（テストモード） |
| openai | openai | openai | フルAPI利用（最高品質） |
| local | openai | openai | 音声認識のみローカル |
| openai | claude | local | ClaudeとローカルTTS |

**注意事項**: 
- ローカルWhisperは初回実行時にモデルをダウンロードします（約140MB〜1.5GB）
- GPUがある場合は自動的にCUDAアクセラレーションを使用します
- ローカルTTSは現在簡易実装（ビープ音 + Web Speech API）です

## ライセンス

MIT License