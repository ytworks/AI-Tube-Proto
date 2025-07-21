import { useState } from 'react'
import './App.css'
import { AudioRecorder } from './components/AudioRecorder'
import { AudioPlayer } from './components/AudioPlayer'
import { ChatDisplay, type ChatMessage } from './components/ChatDisplay'
import { AvatarDisplay } from './components/AvatarDisplay'
import { apiService } from './services/api'

type AppStatus = 'idle' | 'listening' | 'thinking' | 'speaking';

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [status, setStatus] = useState<AppStatus>('idle');
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [responseAudio, setResponseAudio] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const speakText = (text: string) => {
    // Web Speech API を使用してテキストを音声で読み上げる
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'ja-JP';
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;
      
      utterance.onend = () => {
        setStatus('idle');
      };
      
      window.speechSynthesis.speak(utterance);
    }
  };

  const handleRecordingComplete = async (audioBase64: string, format: string) => {
    try {
      setError(null);
      setStatus('thinking');
      
      const response = await apiService.processVoice(audioBase64, format, sessionId);
      
      setSessionId(response.sessionId);
      
      const userMessage: ChatMessage = {
        id: Date.now().toString() + '-user',
        role: 'user',
        content: response.inputText,
        timestamp: new Date()
      };
      
      const assistantMessage: ChatMessage = {
        id: Date.now().toString() + '-assistant',
        role: 'assistant',
        content: response.responseText,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, userMessage, assistantMessage]);
      setStatus('speaking');
      
      // ローカルTTSテストメッセージの場合は、ビープ音を再生してからWeb Speech APIで読み上げる
      if (response.inputText === 'ローカルTTSのテストメッセージ' && 
          response.responseText.startsWith('こんにちは、ローカルTTSです。')) {
        // まずビープ音を再生
        setResponseAudio(response.responseAudio);
        
        // ビープ音の後にWeb Speech APIでテキストを読み上げる
        setTimeout(() => {
          speakText(response.responseText);
        }, 600); // ビープ音が0.5秒なので少し待つ
      }
      // APIキーエラーメッセージの場合は、Web Speech APIで読み上げる
      else if (response.responseText.includes('APIキーがセットされていません') || 
          response.responseText.includes('APIキーが必要です') ||
          response.inputText.includes('音声認識機能を使用するには')) {
        // 音声認識エラーと応答生成エラーを組み合わせたメッセージを作成
        let messageToSpeak = response.responseText;
        if (response.inputText.includes('音声認識機能を使用するには') && 
            response.responseText.includes('APIキーがセットされていません')) {
          messageToSpeak = "音声認識と応答生成の両方にAPIキーが必要です。OpenAI APIキーとClaude APIキーを設定してください。";
        }
        speakText(messageToSpeak);
      } else {
        // 通常の音声再生
        setResponseAudio(response.responseAudio);
        setTimeout(() => {
          setStatus('idle');
        }, 3000);
      }
      
    } catch (err) {
      setError(err instanceof Error ? err.message : '予期しないエラーが発生しました');
      setStatus('idle');
    }
  };


  return (
    <div className="app" style={{
      maxWidth: '800px',
      margin: '0 auto',
      padding: '20px',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      <h1 style={{ textAlign: 'center', marginBottom: '40px' }}>
        🎙️ 音声対話型AIアシスタント
      </h1>
      
      {error && (
        <div style={{
          backgroundColor: '#ffebee',
          color: '#c62828',
          padding: '15px',
          borderRadius: '5px',
          marginBottom: '20px'
        }}>
          ⚠️ {error}
        </div>
      )}
      
      <AvatarDisplay status={status} />
      
      <ChatDisplay messages={messages} />
      
      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <AudioRecorder onRecordingComplete={handleRecordingComplete} />
      </div>
      
      <AudioPlayer 
        audioBase64={responseAudio} 
        format="wav"  // MeloTTSはwav形式を返す
        autoPlay={true}
      />
      
      <div style={{
        marginTop: '40px',
        padding: '20px',
        backgroundColor: '#f5f5f5',
        borderRadius: '10px',
        fontSize: '14px',
        color: '#666'
      }}>
        <h3>使い方</h3>
        <ol style={{ marginLeft: '20px' }}>
          <li>「録音開始」ボタンをクリック</li>
          <li>マイクに向かって話しかける</li>
          <li>「録音停止」ボタンをクリック</li>
          <li>AIの応答を聞く</li>
        </ol>
      </div>
    </div>
  )
}

export default App
