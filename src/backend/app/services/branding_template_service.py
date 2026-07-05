"""
Branding Template Storage Service
Handles intro/outro template storage and retrieval
"""

from typing import Any
from pathlib import Path

from app.core.config import settings


class BrandingTemplateService:
    """Service for managing branding templates."""

    def __init__(self, storage_path: Path | None = None):
        self.storage_path = storage_path or Path(settings.PROJECT_DATA_DIR) / "templates"
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save_template(self, project_id: str, template_type: str, config: dict[str, Any]) -> str:
        """
        Save a branding template.

        Args:
            project_id: Project identifier
            template_type: Type of template (intro/outro/watermark)
            config: Template configuration

        Returns:
            Template ID
        """
        import json
        import uuid

        template_id = f"{project_id}_{template_type}_{uuid.uuid4().hex[:8]}"
        template_path = self.storage_path / f"{template_id}.json"

        with open(template_path, "w") as f:
            json.dump({"type": template_type, "config": config}, f)

        return template_id

    def load_template(self, template_id: str) -> dict[str, Any] | None:
        """
        Load a branding template by ID.

        Args:
            template_id: Template identifier

        Returns:
            Template configuration or None if not found
        """
        import json

        template_path = self.storage_path / f"{template_id}.json"
        if not template_path.exists():
            return None

        with open(template_path) as f:
            return json.load(f)

    def delete_template(self, template_id: str) -> bool:
        """
        Delete a branding template.

        Args:
            template_id: Template identifier

        Returns:
            True if deleted, False if not found
        """
        template_path = self.storage_path / f"{template_id}.json"
        if not template_path.exists():
            return False
        template_path.unlink()
        return True

    def list_templates(self, project_id: str, template_type: str | None = None) -> list[dict[str, Any]]:
        """
        List all templates for a project.

        Args:
            project_id: Project identifier
            template_type: Optional filter by type

        Returns:
            List of templates with metadata
        """
        import json

        templates = []
        prefix = f"{project_id}_{template_type or ''}"

        for template_file in self.storage_path.glob(f"{prefix}*.json"):
            with open(template_file) as f:
                data = json.load(f)
                templates.append({
                    "id": template_file.stem,
                    "type": data.get("type"),
                    "config": data.get("config"),
                })

        return templates