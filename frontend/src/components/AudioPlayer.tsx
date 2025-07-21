import React, { useState, useRef, useEffect } from 'react';

interface AudioPlayerProps {
  audioBase64: string | null;
  format: string;
  autoPlay?: boolean;
}

export const AudioPlayer: React.FC<AudioPlayerProps> = ({ audioBase64, format, autoPlay = true }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (audioBase64 && autoPlay) {
      playAudio();
    }
  }, [audioBase64, autoPlay]);

  const playAudio = () => {
    if (!audioBase64) return;

    try {
      setError(null);
      const audioBlob = base64ToBlob(audioBase64, `audio/${format}`);
      const audioUrl = URL.createObjectURL(audioBlob);
      
      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.play()
          .then(() => setIsPlaying(true))
          .catch(err => {
            setError('音声の再生に失敗しました');
            console.error('Audio playback error:', err);
          });
      }
    } catch (err) {
      setError('音声データの処理に失敗しました');
      console.error('Audio processing error:', err);
    }
  };

  const base64ToBlob = (base64: string, mimeType: string): Blob => {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
  };

  const handleAudioEnd = () => {
    setIsPlaying(false);
  };

  return (
    <div className="audio-player">
      {error && (
        <div className="error-message" style={{ color: 'red', marginBottom: '10px' }}>
          {error}
        </div>
      )}
      <audio
        ref={audioRef}
        onEnded={handleAudioEnd}
        style={{ display: 'none' }}
      />
      {isPlaying && (
        <div className="playing-indicator" style={{ color: '#4CAF50' }}>
          🔊 音声再生中...
        </div>
      )}
    </div>
  );
};