# 音声対話型AIアシスタント

ブラウザベースの音声対話型AIアシスタントシステムです。音声入力を受け取り、ChatGPT APIを使用して応答を生成し、音声で返答します。

## 機能

- 🎤 音声入力（Speech-to-Text）
- 🤖 ChatGPT APIによる応答生成
- 🔊 音声出力（Text-to-Speech）
- 🌐 ブラウザベースのインターフェース
- 🔒 セキュアなAPIキー管理
- 🔧 APIキーなしでも動作（制限付き）

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
- OpenAI APIキー

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

## ライセンス

MIT License