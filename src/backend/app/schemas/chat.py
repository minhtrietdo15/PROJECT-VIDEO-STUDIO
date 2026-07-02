"""
Chat Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.common import TimestampedModel


class ChatMessageResponse(TimestampedModel):
    id: str
    project_id: Optional[str] = None
    role: str
    content: str
    context: Optional[dict[str, Any]] = None
    tokens_used: Optional[int] = None
    model: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    message: str
    project_id: Optional[str] = None
    context: Optional[dict[str, Any]] = None


class ChatResponse(BaseModel):
    message: ChatMessageResponse
    conversation_id: str