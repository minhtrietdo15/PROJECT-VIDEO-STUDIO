"""
Batch Processing Service
Handles queue management and parallel processing
"""

import asyncio
from typing import Any

from app.models.batch import BatchQueue, BatchItem


class BatchProcessingService:
    """Service for managing batch processing with resource-aware scheduling."""

    def __init__(self, max_concurrent: int = 3):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.running_tasks: dict[str, Any] = {}

    async def process_queue(self, queue: BatchQueue) -> None:
        """Process all items in a queue with resource-aware scheduling."""
        if queue.is_paused:
            return

        # Get pending items ordered by priority
        items = sorted(
            [i for i in queue.items if i.status == "pending"],
            key=lambda x: x.priority,
        )

        # Process items concurrently with limit
        tasks = []
        for item in items[: queue.max_concurrent]:
            task = asyncio.create_task(self.process_item(item))
            tasks.append(task)
            self.running_tasks[str(item.id)] = task

        await asyncio.gather(*tasks, return_exceptions=True)

    async def process_item(self, item: BatchItem) -> bool:
        """Process a single batch item."""
        async with self.semaphore:
            item.status = "running"
            item.progress = 0

            try:
                # Simulate processing steps
                for step in range(100):
                    if item.status == "paused":
                        await asyncio.sleep(1)
                        continue

                    item.progress = step + 1
                    await asyncio.sleep(0.1)  # Simulate work

                item.status = "completed"
                return True
            except Exception as e:
                item.status = "failed"
                item.error_log = str(e)
                return False
            finally:
                self.running_tasks.pop(str(item.id), None)

    def can_process(self, item: BatchItem) -> bool:
        """Check if system resources allow processing this item."""
        # Placeholder for resource checking logic
        # Could check CPU, GPU, memory availability
        return len(self.running_tasks) < self.semaphore._value

    def get_resource_usage(self) -> dict[str, Any]:
        """Get current system resource usage."""
        return {
            "running_tasks": len(self.running_tasks),
            "max_concurrent": self.semaphore._value,
            "available_slots": self.semaphore._value - len(self.running_tasks),
        }