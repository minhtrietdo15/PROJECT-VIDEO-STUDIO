import whisper
from fastapi import HTTPException

class STTService:
    def __init__(self):
        self.model = whisper.load_model("base")

    def transcribe(self, audio_path: str) -> dict:
        try:
            result = self.model.transcribe(audio_path)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))