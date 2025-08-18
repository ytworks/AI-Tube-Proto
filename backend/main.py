from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from pydantic import BaseModel
from typing import Optional
import uuid
from config.settings import settings
from services.llm_service import llm_service
from services.speech_service import speech_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    logger.info(f"Server running on {settings.host}:{settings.port}")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="Voice Assistant API",
    description="API for voice-based AI assistant",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Voice Assistant API is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

class SpeechToTextRequest(BaseModel):
    audio: str
    format: str = "webm"

class SpeechToTextResponse(BaseModel):
    text: str
    confidence: Optional[float] = None

class ChatRequest(BaseModel):
    message: str
    sessionId: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sessionId: str

class TextToSpeechRequest(BaseModel):
    text: str
    voice: Optional[str] = "alloy"
    speed: Optional[float] = 1.0

class TextToSpeechResponse(BaseModel):
    audio: str
    format: str

class ProcessVoiceRequest(BaseModel):
    audio: str
    format: str = "webm"
    sessionId: Optional[str] = None

class ProcessVoiceResponse(BaseModel):
    responseAudio: str
    responseText: str
    inputText: str
    sessionId: str
    isLocalTts: bool

@app.post("/api/speech-to-text", response_model=SpeechToTextResponse)
async def speech_to_text(request: SpeechToTextRequest):
    try:
        text = await speech_service.speech_to_text(request.audio, request.format)
        return SpeechToTextResponse(text=text)
    except Exception as e:
        logger.error(f"Speech to text error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id = request.sessionId or str(uuid.uuid4())
        response = await llm_service.get_chat_response(
            request.message,
            session_id
        )
        return ChatResponse(response=response, sessionId=session_id)
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/text-to-speech", response_model=TextToSpeechResponse)
async def text_to_speech(request: TextToSpeechRequest):
    try:
        audio_base64, format = await speech_service.text_to_speech(
            request.text,
            request.voice,
            request.speed
        )
        return TextToSpeechResponse(audio=audio_base64, format=format)
    except Exception as e:
        logger.error(f"Text to speech error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-voice", response_model=ProcessVoiceResponse)
async def process_voice(request: ProcessVoiceRequest):
    try:
        session_id = request.sessionId or str(uuid.uuid4())

        input_text = await speech_service.speech_to_text(request.audio, request.format)

        response_text = await llm_service.get_chat_response(input_text, session_id)

        response_audio, _ = await speech_service.text_to_speech(response_text)

        return ProcessVoiceResponse(
            responseAudio=response_audio,
            responseText=response_text,
            inputText=input_text,
            sessionId=session_id,
            isLocalTts=settings.tts_provider == "local",
        )
    except Exception as e:
        logger.error(f"Process voice error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
