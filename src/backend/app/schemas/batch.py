"""
Batch Processing Schemas
"""

from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import TimestampedModel


class BatchItemBase(BaseModel):
    project_id: str
    priority: int = Field(default=1, ge=1, le=3)  # 1=high, 2=normal, 3=low
    status: str = Field(default="pending")  # pending, running, completed, failed, paused


class BatchItemCreate(BatchItemBase):
    pass


class BatchItemUpdate(BaseModel):
    priority: Optional[int] = None
    status: Optional[str] = None
    progress: Optional[int] = None
    error_log: Optional[str] = None


class BatchItemResponse(BatchItemBase, TimestampedModel):
    id: str
    progress: int = 0
    eta: Optional[str] = None
    error_log: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BatchQueueBase(BaseModel):
    name: str
    max_concurrent: int = Field(default=3, ge=1, le=10)


class BatchQueueCreate(BatchQueueBase):
    pass


class BatchQueueUpdate(BaseModel):
    name: Optional[str] = None
    max_concurrent: Optional[int] = None
    is_paused: Optional[bool] = None


class BatchQueueResponse(BatchQueueBase, TimestampedModel):
    id: str
    is_paused: bool = False
    total_items: int = 0
    completed_items: int = 0
    failed_items: int = 0

    model_config = ConfigDict(from_attributes=True)