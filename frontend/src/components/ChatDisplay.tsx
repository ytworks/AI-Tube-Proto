import React from "react";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface ChatDisplayProps {
  messages: ChatMessage[];
}

export const ChatDisplay: React.FC<ChatDisplayProps> = ({ messages }) => {
  return (
    <div
      className="chat-display"
      style={{
        maxHeight: "400px",
        overflowY: "auto",
        padding: "20px",
        backgroundColor: "#f5f5f5",
        borderRadius: "10px",
        marginBottom: "20px",
      }}
    >
      {messages.length === 0 ? (
        <div style={{ textAlign: "center", color: "#888" }}>
          会話履歴がありません。録音ボタンを押して話しかけてください。
        </div>
      ) : (
        messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role}`}
            style={{
              marginBottom: "15px",
              padding: "10px 15px",
              borderRadius: "10px",
              backgroundColor: message.role === "user" ? "#e3f2fd" : "#f3e5f5",
              marginLeft: message.role === "user" ? "0" : "50px",
              marginRight: message.role === "user" ? "50px" : "0",
            }}
          >
            <div
              style={{
                fontSize: "12px",
                color: "#666",
                marginBottom: "5px",
              }}
            >
              {message.role === "user" ? "👤 あなた" : "🤖 AI"}
            </div>
            <div style={{ fontSize: "14px", color: "black" }}>
              {message.content}
            </div>
          </div>
        ))
      )}
    </div>
  );
};
