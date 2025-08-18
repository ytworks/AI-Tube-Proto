import React, { useState, useRef } from "react";

interface AudioRecorderProps {
  onRecordingComplete: (audioBase64: string, format: string) => void;
}

export const AudioRecorder: React.FC<AudioRecorderProps> = ({
  onRecordingComplete,
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: "audio/webm;codecs=opus",
      });

      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/webm",
        });
        const reader = new FileReader();

        reader.onloadend = () => {
          const base64String = reader.result as string;
          const base64Audio = base64String.split(",")[1];
          onRecordingComplete(base64Audio, "webm");
        };

        reader.readAsDataURL(audioBlob);

        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      setError(
        "マイクへのアクセスが拒否されました。ブラウザの設定を確認してください。"
      );
      console.error("Error accessing microphone:", err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className="audio-recorder">
      {error && (
        <div
          className="error-message"
          style={{ color: "red", marginBottom: "10px" }}
        >
          {error}
        </div>
      )}
      <button
        onClick={isRecording ? stopRecording : startRecording}
        className={`record-button ${isRecording ? "recording" : ""}`}
        style={{
          padding: "15px 30px",
          fontSize: "16px",
          borderRadius: "50px",
          border: "none",
          cursor: "pointer",
          backgroundColor: isRecording ? "#ff4444" : "#4CAF50",
          color: "white",
          transition: "all 0.3s ease",
        }}
      >
        {isRecording ? "🔴 録音停止" : "🎤 録音開始"}
      </button>
      {isRecording && (
        <div
          className="recording-indicator"
          style={{ marginTop: "10px", color: "#ff4444" }}
        >
          録音中...
        </div>
      )}
    </div>
  );
};
