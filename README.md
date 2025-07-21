# 音声対話型AIアシスタント

ブラウザベースの音声対話型AIアシスタントシステムです。音声入力を受け取り、ChatGPT APIを使用して応答を生成し、音声で返答します。

## 機能

- 🎤 音声入力（Speech-to-Text）
- 🤖 ChatGPT/Claude APIによる応答生成
- 🔊 音声出力（Text-to-Speech）
- 🌐 ブラウザベースのインターフェース
- 🔒 セキュアなAPIキー管理
- 🔧 APIキーなしでも動作（制限付き）
- ⚙️ 環境変数によるモデル選択
- 🔄 LLMプロバイダー切り替え（OpenAI/Claude）
- 🏠 ローカルTTSサポート（MeloTTS）

## 技術スタック

### バックエンド
- Python 3.8+
- FastAPI
- OpenAI API (Whisper, ChatGPT, TTS)
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
- OpenAI APIキー または Anthropic APIキー

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

# MeloTTSを使用する場合は追加でインストール（オプション）
# 方法1: インストールスクリプトを使用
python install_melotts.py

# 方法2: 手動インストール
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
```

4. 環境変数を設定
```bash
cp .env.example .env
```
`.env`ファイルを編集し、OpenAI APIキーを設定してください。

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
- OpenAI APIキーが正しく設定されているか確認
- APIの利用制限に達していないか確認

### APIキーがない場合
- システムは正常に動作しますが、音声認識と応答生成の代わりに「APIキーがセットされていません」というメッセージが返されます
- このメッセージはWeb Speech APIを使用してブラウザ側で音声合成されます

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

### TTSプロバイダーの選択

```env
# TTSプロバイダー選択 (openai または local)
TTS_PROVIDER=local

# MeloTTS使用時の設定
MELOTTS_LANGUAGE=JP  # EN, JP, ZH から選択
MELOTTS_DEVICE=auto  # cpu, cuda, auto から選択
```

**重要な注意事項**: 
- Claudeを使用する場合でも、音声認識にはOpenAI APIが必要です
- ローカルTTS（MeloTTS）を使用する場合：
  - 音声合成はAPIキーなしで動作します
  - 初回実行時にモデルのダウンロードが必要です（自動）
  - GPUがある場合は自動的にCUDAを使用します
  - OpenAI APIキーがない場合、「ローカルTTSで話しています」というテストメッセージを音声で返します

## ライセンス

MIT License