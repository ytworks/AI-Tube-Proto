#!/usr/bin/env python
"""
MeloTTSのインストールとセットアップスクリプト
"""
import subprocess
import sys

def install_melotts():
    """MeloTTSをインストール"""
    print("MeloTTSをインストールしています...")
    
    try:
        # MeloTTSをGitHubからインストール
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "git+https://github.com/myshell-ai/MeloTTS.git"
        ])
        
        # 日本語辞書をダウンロード
        print("\n日本語辞書をダウンロードしています...")
        subprocess.check_call([sys.executable, "-m", "unidic", "download"])
        
        print("\n✅ MeloTTSのインストールが完了しました！")
        print("\n使用方法:")
        print("1. .envファイルで TTS_PROVIDER=local を設定")
        print("2. MELOTTS_LANGUAGE を EN, JP, ZH から選択")
        print("3. サーバーを再起動")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ インストール中にエラーが発生しました: {e}")
        print("\n手動でインストールする場合:")
        print("pip install git+https://github.com/myshell-ai/MeloTTS.git")
        print("python -m unidic download")
        sys.exit(1)

if __name__ == "__main__":
    install_melotts()