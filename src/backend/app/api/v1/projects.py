"""
Projects API Router
CRUD endpoints for project management
"""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.models.project import Project, ProjectStatus
from app.schemas.project import ProjectCreate, ProjectListResponse, ProjectResponse, ProjectUpdate

router = APIRouter()


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Create a new project."""
    project = Project(
        user_id=user_id,
        title=data.title,
        source_lang=data.source_lang,
        target_lang=data.target_lang,
        description=data.description,
        settings=data.settings or {},
    )
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return ProjectResponse.model_validate(project)


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    page: int = 1,
    page_size: int = 20,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProjectListResponse:
    """List all projects for the current user."""
    offset = (page - 1) * page_size

    # Count total
    count_stmt = select(func.count()).select_from(Project).where(Project.user_id == user_id)
    total = (await db.execute(count_stmt)).scalar_one()

    # Fetch page
    stmt = (
        select(Project)
        .where(Project.user_id == user_id)
        .order_by(Project.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    items = result.scalars().all()

    return ProjectListResponse(
        items=[ProjectResponse.model_validate(p) for p in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Get a single project by ID."""
    stmt = select(Project).where(Project.id == uuid.UUID(project_id), Project.user_id == user_id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return ProjectResponse.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    data: ProjectUpdate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Update a project."""
    stmt = select(Project).where(Project.id == uuid.UUID(project_id), Project.user_id == user_id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await db.flush()
    await db.refresh(project)
    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a project."""
    stmt = select(Project).where(Project.id == uuid.UUID(project_id), Project.user_id == user_id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    await db.delete(project)
    await db.flush()


@router.post("/{project_id}/duplicate", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def duplicate_project(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Duplicate an existing project."""
    stmt = select(Project).where(Project.id == uuid.UUID(project_id), Project.user_id == user_id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    new_project = Project(
        user_id=user_id,
        title=f"{project.title} (Copy)",
        source_lang=project.source_lang,
        target_lang=project.target_lang,
        description=project.description,
        settings=project.settings or {},
    )
    db.add(new_project)
    await db.flush()
    await db.refresh(new_project)
    return ProjectResponse.model_validate(new_project)


@router.get("/stats/dashboard", response_model=dict)
async def dashboard_stats(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Return dashboard statistics for the current user."""
    total_stmt = select(func.count()).select_from(Project).where(Project.user_id == user_id)
    total = (await db.execute(total_stmt)).scalar_one()

    status_counts = {}
    for status in ProjectStatus:
        stmt = (
            select(func.count())
            .select_from(Project)
            .where(Project.user_id == user_id, Project.status == status)
        )
        status_counts[status.value] = (await db.execute(stmt)).scalar_one()

    return {
        "total_projects": total,
        "status_counts": status_counts,
        "storage_used_mb": 0,
    }
