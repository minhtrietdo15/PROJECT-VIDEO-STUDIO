"""
Project Service
Business logic for project management
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project, ProjectStatus
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """Service layer for project operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, user_id: str, data: ProjectCreate) -> Project:
        """Create a new project."""
        project = Project(
            user_id=user_id,
            title=data.title,
            source_lang=data.source_lang,
            target_lang=data.target_lang,
            description=data.description,
            settings=data.settings or {},
        )
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def get_project(self, project_id: str, user_id: str) -> Project | None:
        """Get a project by ID."""
        from sqlalchemy import select
        stmt = select(Project).where(Project.id == project_id, Project.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_projects(self, user_id: str, page: int = 1, page_size: int = 20):
        """List projects for a user."""
        from sqlalchemy import select, func
        offset = (page - 1) * page_size

        count_stmt = select(func.count()).select_from(Project).where(Project.user_id == user_id)
        total = (await self.db.execute(count_stmt)).scalar_one()

        stmt = (
            select(Project)
            .where(Project.user_id == user_id)
            .order_by(Project.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def update_project(self, project: Project, data: ProjectUpdate) -> Project:
        """Update a project."""
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete_project(self, project: Project) -> None:
        """Delete a project."""
        await self.db.delete(project)