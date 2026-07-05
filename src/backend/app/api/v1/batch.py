"""
Batch Processing API Router
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.models.batch import BatchQueue, BatchItem
from app.schemas.batch import (
    BatchQueueCreate,
    BatchQueueResponse,
    BatchQueueUpdate,
    BatchItemCreate,
    BatchItemResponse,
    BatchItemUpdate,
)

router = APIRouter()


@router.get("/queues", response_model=list[BatchQueueResponse])
async def list_queues(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[BatchQueueResponse]:
    """List all batch queues for the user."""
    stmt = select(BatchQueue).where(BatchQueue.user_id == uuid.UUID(user_id))
    result = await db.execute(stmt)
    queues = result.scalars().all()
    return [BatchQueueResponse.model_validate(q) for q in queues]


@router.post("/queues", response_model=BatchQueueResponse, status_code=status.HTTP_201_CREATED)
async def create_queue(
    data: BatchQueueCreate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BatchQueueResponse:
    """Create a new batch queue."""
    queue = BatchQueue(
        user_id=user_id,
        name=data.name,
        max_concurrent=data.max_concurrent,
    )
    db.add(queue)
    await db.flush()
    await db.refresh(queue)
    return BatchQueueResponse.model_validate(queue)


@router.put("/queues/{queue_id}", response_model=BatchQueueResponse)
async def update_queue(
    queue_id: str,
    data: BatchQueueUpdate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BatchQueueResponse:
    """Update a batch queue."""
    stmt = select(BatchQueue).where(BatchQueue.id == uuid.UUID(queue_id))
    result = await db.execute(stmt)
    queue = result.scalar_one_or_none()
    if not queue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(queue, field, value)

    await db.flush()
    await db.refresh(queue)
    return BatchQueueResponse.model_validate(queue)


@router.post("/queues/{queue_id}/items", response_model=BatchItemResponse, status_code=status.HTTP_201_CREATED)
async def add_item(
    queue_id: str,
    data: BatchItemCreate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BatchItemResponse:
    """Add an item to a batch queue."""
    item = BatchItem(
        queue_id=queue_id,
        project_id=data.project_id,
        priority=data.priority,
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return BatchItemResponse.model_validate(item)


@router.put("/queues/{queue_id}/items/{item_id}", response_model=BatchItemResponse)
async def update_item(
    queue_id: str,
    item_id: str,
    data: BatchItemUpdate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BatchItemResponse:
    """Update a batch item."""
    stmt = select(BatchItem).where(
        BatchItem.id == uuid.UUID(item_id),
        BatchItem.queue_id == uuid.UUID(queue_id),
    )
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    await db.flush()
    await db.refresh(item)
    return BatchItemResponse.model_validate(item)


@router.delete("/queues/{queue_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(
    queue_id: str,
    item_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove an item from a batch queue."""
    stmt = select(BatchItem).where(
        BatchItem.id == uuid.UUID(item_id),
        BatchItem.queue_id == uuid.UUID(queue_id),
    )
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await db.delete(item)
    await db.flush()


@router.post("/queues/{queue_id}/pause", response_model=BatchQueueResponse)
async def pause_queue(
    queue_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BatchQueueResponse:
    """Pause a batch queue."""
    stmt = select(BatchQueue).where(BatchQueue.id == uuid.UUID(queue_id))
    result = await db.execute(stmt)
    queue = result.scalar_one_or_none()
    if not queue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue not found")
    queue.is_paused = True
    await db.flush()
    await db.refresh(queue)
    return BatchQueueResponse.model_validate(queue)


@router.post("/queues/{queue_id}/resume", response_model=BatchQueueResponse)
async def resume_queue(
    queue_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BatchQueueResponse:
    """Resume a batch queue."""
    stmt = select(BatchQueue).where(BatchQueue.id == uuid.UUID(queue_id))
    result = await db.execute(stmt)
    queue = result.scalar_one_or_none()
    if not queue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue not found")
    queue.is_paused = False
    await db.flush()
    await db.refresh(queue)
    return BatchQueueResponse.model_validate(queue)