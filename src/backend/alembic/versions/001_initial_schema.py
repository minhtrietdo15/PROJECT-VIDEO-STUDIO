"""
Initial database schema migration
Creates all core tables for Video Localization AI Studio
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

# revision identifiers
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all tables."""
    # Projects table
    op.create_table(
        "projects",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("source_lang", sa.String(10), nullable=False, server_default="auto"),
        sa.Column("target_lang", sa.String(10), nullable=False, server_default="vi"),
        sa.Column("status", sa.String(50), nullable=False, server_default="draft", index=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("settings", JSONB, nullable=True, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Videos table
    op.create_table(
        "videos",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("filename", sa.String(500), nullable=False),
        sa.Column("filepath", sa.String(1000), nullable=False),
        sa.Column("duration", sa.Float(), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("fps", sa.Float(), nullable=True),
        sa.Column("file_size", sa.Integer(), nullable=True),
        sa.Column("codec", sa.String(50), nullable=True),
        sa.Column("thumbnail_path", sa.String(1000), nullable=True),
        sa.Column("audio_codec", sa.String(50), nullable=True),
        sa.Column("audio_channels", sa.Integer(), nullable=True),
        sa.Column("audio_sample_rate", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Transcripts table
    op.create_table(
        "transcripts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending", index=True),
        sa.Column("language", sa.String(10), nullable=True),
        sa.Column("model_used", sa.String(50), nullable=True),
        sa.Column("segments", JSONB, nullable=True, server_default="[]"),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("duration_seconds", sa.Float(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Translations table
    op.create_table(
        "translations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("transcript_id", UUID(as_uuid=True), sa.ForeignKey("transcripts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending", index=True),
        sa.Column("translated_text", sa.Text(), nullable=True),
        sa.Column("segments", JSONB, nullable=True, server_default="[]"),
        sa.Column("style", sa.String(50), nullable=True),
        sa.Column("engine_used", sa.String(50), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Dubbing table
    op.create_table(
        "dubbing",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending", index=True),
        sa.Column("voice_id", sa.String(100), nullable=True),
        sa.Column("voice_name", sa.String(100), nullable=True),
        sa.Column("engine_used", sa.String(50), nullable=True),
        sa.Column("audio_path", sa.String(1000), nullable=True),
        sa.Column("speed", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("pitch", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("volume", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("segments", JSONB, nullable=True, server_default="[]"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Subtitles table
    op.create_table(
        "subtitles",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("format", sa.String(20), nullable=False, server_default="srt"),
        sa.Column("content", JSONB, nullable=True, server_default="[]"),
        sa.Column("style_config", JSONB, nullable=True, server_default="{}"),
        sa.Column("file_path", sa.String(1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Branding table
    op.create_table(
        "branding",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("intro_enabled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("intro_template_id", sa.String(100), nullable=True),
        sa.Column("intro_duration", sa.Float(), nullable=False, server_default="5.0"),
        sa.Column("outro_enabled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("outro_template_id", sa.String(100), nullable=True),
        sa.Column("watermark_enabled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("watermark_config", JSONB, nullable=True, server_default="{}"),
        sa.Column("bg_music_enabled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("bg_music_path", sa.String(1000), nullable=True),
        sa.Column("bg_music_volume", sa.Float(), nullable=False, server_default="0.3"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Render tasks table
    op.create_table(
        "render_tasks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending", index=True),
        sa.Column("progress", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("output_path", sa.String(1000), nullable=True),
        sa.Column("settings", JSONB, nullable=True, server_default="{}"),
        sa.Column("error_log", sa.Text(), nullable=True),
        sa.Column("started_at", sa.String(50), nullable=True),
        sa.Column("completed_at", sa.String(50), nullable=True),
        sa.Column("duration_seconds", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Voice profiles table
    op.create_table(
        "voice_profiles",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("engine", sa.String(50), nullable=False),
        sa.Column("voice_id", sa.String(100), nullable=False),
        sa.Column("language", sa.String(10), nullable=False, server_default="vi"),
        sa.Column("gender", sa.String(20), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("preview_path", sa.String(1000), nullable=True),
        sa.Column("is_cloned", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("config", JSONB, nullable=True, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Chat messages table
    op.create_table(
        "chat_messages",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("context", JSONB, nullable=True, server_default="{}"),
        sa.Column("tokens_used", sa.Integer(), nullable=True),
        sa.Column("model", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # YouTube metadata table
    op.create_table(
        "youtube_metadata",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("title", sa.String(500), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("tags", JSONB, nullable=True, server_default="[]"),
        sa.Column("category_id", sa.String(20), nullable=True),
        sa.Column("visibility", sa.String(20), nullable=False, server_default="private"),
        sa.Column("playlist_id", sa.String(100), nullable=True),
        sa.Column("chapters", JSONB, nullable=True, server_default="[]"),
        sa.Column("thumbnail_path", sa.String(1000), nullable=True),
        sa.Column("exported_metadata_path", sa.String(1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Create indexes
    op.create_index("ix_projects_user_id", "projects", ["user_id"])
    op.create_index("ix_projects_status", "projects", ["status"])
    op.create_index("ix_render_tasks_project_id", "render_tasks", ["project_id"])
    op.create_index("ix_render_tasks_status", "render_tasks", ["status"])
    op.create_index("ix_voice_profiles_user_id", "voice_profiles", ["user_id"])
    op.create_index("ix_chat_messages_project_id", "chat_messages", ["project_id"])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_index("ix_chat_messages_project_id")
    op.drop_index("ix_voice_profiles_user_id")
    op.drop_index("ix_render_tasks_status")
    op.drop_index("ix_render_tasks_project_id")
    op.drop_index("ix_projects_status")
    op.drop_index("ix_projects_user_id")

    op.drop_table("youtube_metadata")
    op.drop_table("chat_messages")
    op.drop_table("voice_profiles")
    op.drop_table("render_tasks")
    op.drop_table("branding")
    op.drop_table("subtitles")
    op.drop_table("dubbing")
    op.drop_table("translations")
    op.drop_table("transcripts")
    op.drop_table("videos")
    op.drop_table("projects")