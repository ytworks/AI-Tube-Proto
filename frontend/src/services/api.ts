const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface SpeechToTextResponse {
  text: string;
  confidence?: number;
}

interface ChatResponse {
  response: string;
  sessionId: string;
}

interface TextToSpeechResponse {
  audio: string;
  format: string;
}

interface ProcessVoiceResponse {
  responseAudio: string;
  responseText: string;
  inputText: string;
  sessionId: string;
  isLocalTts: boolean;
}

class ApiService {
  private async fetchApi(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response
        .json()
        .catch(() => ({ detail: "Unknown error" }));
      throw new Error(error.detail || "API request failed");
    }

    return response.json();
  }

  async speechToText(
    audioBase64: string,
    format: string = "webm"
  ): Promise<SpeechToTextResponse> {
    return this.fetchApi("/api/speech-to-text", {
      method: "POST",
      body: JSON.stringify({ audio: audioBase64, format }),
    });
  }

  async chat(message: string, sessionId?: string): Promise<ChatResponse> {
    return this.fetchApi("/api/chat", {
      method: "POST",
      body: JSON.stringify({ message, sessionId }),
    });
  }

  async textToSpeech(
    text: string,
    voice?: string,
    speed?: number
  ): Promise<TextToSpeechResponse> {
    return this.fetchApi("/api/text-to-speech", {
      method: "POST",
      body: JSON.stringify({ text, voice, speed }),
    });
  }

  async processVoice(
    audioBase64: string,
    format: string = "webm",
    sessionId?: string
  ): Promise<ProcessVoiceResponse> {
    return this.fetchApi("/api/process-voice", {
      method: "POST",
      body: JSON.stringify({ audio: audioBase64, format, sessionId }),
    });
  }
}

export const apiService = new ApiService();
