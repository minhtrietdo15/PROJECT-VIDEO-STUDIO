"""
Seed Data Script
Populates the database with sample data for development and testing.

Usage:
    python -m scripts.seed_data          # Uses default settings
    python -m scripts.seed_data --clear   # Clear all data first
"""

import asyncio
import uuid
import argparse
from datetime import datetime, timezone, timedelta
from typing import Optional

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.base import async_session_factory, engine, Base
from app.models.project import Project, ProjectStatus
from app.models.video import Video
from app.models.transcript import Transcript, TranscriptStatus
from app.models.translation import Translation, TranslationStatus
from app.models.dubbing import Dubbing, DubbingStatus
from app.models.subtitle import Subtitle, SubtitleFormat
from app.models.branding import Branding
from app.models.render_task import RenderTask, RenderStatus
from app.models.voice_profile import VoiceProfile
from app.models.chat import ChatMessage, MessageRole
from app.models.youtube_metadata import YouTubeMetadata, VisibilityType


# ─── Sample Data ────────────────────────────────────────────────────────────

SAMPLE_PROJECTS = [
    {
        "title": "Hướng dẫn làm video với AI",
        "source_lang": "en",
        "target_lang": "vi",
        "status": ProjectStatus.COMPLETED,
        "description": "Video hướng dẫn sử dụng AI để tạo video tự động",
    },
    {
        "title": "Review iPhone 16 Pro Max",
        "source_lang": "en",
        "target_lang": "vi",
        "status": ProjectStatus.TRANSCRIPT_READY,
        "description": "Review chi tiết về iPhone 16 Pro Max",
    },
    {
        "title": "Cách học lập trình Python",
        "source_lang": "en",
        "target_lang": "vi",
        "status": ProjectStatus.DRAFT,
        "description": "Hướng dẫn học Python từ cơ bản đến nâng cao",
    },
    {
        "title": "Top 10 món ăn Việt Nam",
        "source_lang": "vi",
        "target_lang": "en",
        "status": ProjectStatus.TRANSLATION_READY,
        "description": "Giới thiệu 10 món ăn đặc sắc của Việt Nam",
    },
    {
        "title": "Workshop: Kiếm tiền từ YouTube",
        "source_lang": "vi",
        "target_lang": "en",
        "status": ProjectStatus.DUBBING_READY,
        "description": "Chia sẻ kinh nghiệm kiếm tiền từ kênh YouTube",
    },
]

SAMPLE_VOICES = [
    {
        "name": "Giọng Nam trầm",
        "engine": "coqui",
        "voice_id": "male_deep_01",
        "language": "vi",
        "gender": "male",
        "description": "Giọng nam trầm ấm, phù hợp video giới thiệu",
        "is_cloned": False,
    },
    {
        "name": "Giọng Nữ dịu dàng",
        "engine": "coqui",
        "voice_id": "female_gentle_01",
        "language": "vi",
        "gender": "female",
        "description": "Giọng nữ nhẹ nhàng, phù hợp video hướng dẫn",
        "is_cloned": False,
    },
    {
        "name": "Giọng Nam trẻ trung",
        "engine": "piper",
        "voice_id": "male_young_01",
        "language": "vi",
        "gender": "male",
        "description": "Giọng nam trẻ trung, năng động",
        "is_cloned": False,
    },
    {
        "name": "Giọng Nữ năng động",
        "engine": "edge_tts",
        "voice_id": "vi-VN-HoaiMyNeural",
        "language": "vi",
        "gender": "female",
        "description": "Giọng nữ năng động từ Edge TTS",
        "is_cloned": False,
    },
    {
        "name": "Giọng Nam trung tính",
        "engine": "coqui",
        "voice_id": "male_neutral_01",
        "language": "vi",
        "gender": "male",
        "description": "Giọng nam trung tính, phù hợp video giáo dục",
        "is_cloned": False,
    },
]

SAMPLE_CHAT_MESSAGES = [
    {
        "role": MessageRole.USER,
        "content": "Hãy giúp tôi cải thiện bản dịch này: 'Hello everyone, welcome to my channel'",
        "context": {"module": "translation", "segment_index": 0},
    },
    {
        "role": MessageRole.ASSISTANT,
        "content": "Tôi đề xuất: **'Xin chào mọi người, chào mừng các bạn đến với kênh của tôi'**\n\nBản dịch này tự nhiên hơn và phù hợp với văn nói tiếng Việt.",
        "context": {"module": "translation", "segment_index": 0},
    },
    {
        "role": MessageRole.USER,
        "content": "Hãy tạo tiêu đề YouTube cho video này",
        "context": {"module": "youtube", "action": "generate_title"},
    },
    {
        "role": MessageRole.ASSISTANT,
        "content": "Dưới đây là một số gợi ý tiêu đề:\n\n1. **Cách Làm Video AI Tự Động Trong 10 Phút** 🚀\n2. **Hướng Dẫn A-Z: Tạo Video Bằng AI Cho Người Mới**\n3. **Kiếm Tiền Từ Video AI: Bí Quyết Từ Chuyên Gia** 💰\n\nBạn thích tiêu đề nào nhất?",
        "context": {"module": "youtube", "action": "generate_title"},
    },
]


# ─── Helpers ────────────────────────────────────────────────────────────────

def _make_segments(count: int, base_text: str, lang: str = "en") -> list[dict]:
    """Generate sample transcript/translation segments."""
    segments = []
    for i in range(count):
        start_ms = i * 5000
        end_ms = start_ms + 4500
        segments.append({
            "segment_index": i,
            "start_ms": start_ms,
            "end_ms": end_ms,
            "text": f"{base_text} — segment {i + 1}",
            "language": lang,
            "confidence": 0.95 + (i % 5) * 0.01,
            "words": [
                {"word": f"Word{j}", "start_ms": start_ms + j * 500, "end_ms": start_ms + (j + 1) * 500, "confidence": 0.98}
                for j in range(min(8, (end_ms - start_ms) // 500))
            ],
        })
    return segments


# ─── Main Seeder ────────────────────────────────────────────────────────────

async def clear_data(session: AsyncSession) -> None:
    """Clear all data from tables in correct order (respecting FK constraints)."""
    tables = [
        "youtube_metadata", "chat_messages", "voice_profiles",
        "render_tasks", "branding", "subtitles", "dubbing",
        "translations", "transcripts", "videos", "projects",
    ]
    for table in tables:
        await session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
    await session.commit()
    print("✅ All data cleared.")


async def seed_database(clear: bool = False) -> None:
    """Main seed function."""
    async with async_session_factory() as session:
        try:
            if clear:
                await clear_data(session)
            else:
                print("  📦 Using existing data (use --clear to reset)")

            user_id = "seed-user-001"

            # ── Projects ──────────────────────────────────────────────
            project_ids = []
            for proj_data in SAMPLE_PROJECTS:
                project = Project(
                    user_id=user_id,
                    title=proj_data["title"],
                    source_lang=proj_data["source_lang"],
                    target_lang=proj_data["target_lang"],
                    status=proj_data["status"],
                    description=proj_data["description"],
                    settings={
                        "default_stt_model": "medium",
                        "default_translation_engine": "local_llm",
                        "gpu_enabled": False,
                    },
                )
                session.add(project)
                await session.flush()
                project_ids.append(project.id)
                print(f"  📁 Project: {project.title} ({project.status.value})")

            # ── Videos (for first 3 projects) ─────────────────────────
            video_data = [
                ("tutorial_intro.mp4", 120.5, 1920, 1080, 30.0, 52428800, "h264", "aac"),
                ("iphone_review.mp4", 845.0, 3840, 2160, 60.0, 209715200, "hevc", "aac"),
                ("python_course.mp4", 3600.0, 1920, 1080, 30.0, 157286400, "h264", "aac"),
            ]
            for i, (proj_id, (fname, dur, w, h, fps, size, codec, acodec)) in enumerate(
                zip(project_ids[:3], video_data)
            ):
                video = Video(
                    project_id=proj_id,
                    filename=fname,
                    filepath=f"/data/projects/{proj_id}/video/{fname}",
                    duration=dur,
                    width=w,
                    height=h,
                    fps=fps,
                    file_size=size,
                    codec=codec,
                    audio_codec=acodec,
                    audio_channels=2,
                    audio_sample_rate=44100,
                    thumbnail_path=f"/data/projects/{proj_id}/video/thumbnail.jpg",
                )
                session.add(video)
            print("  🎬 Videos created for first 3 projects")

            # ── Transcripts (for projects with status >= TRANSCRIPT_READY) ──
            transcript_statuses = {
                ProjectStatus.COMPLETED: TranscriptStatus.COMPLETED,
                ProjectStatus.TRANSCRIPT_READY: TranscriptStatus.COMPLETED,
                ProjectStatus.TRANSLATION_READY: TranscriptStatus.COMPLETED,
                ProjectStatus.DUBBING_READY: TranscriptStatus.COMPLETED,
            }
            for proj_data, proj_id in zip(SAMPLE_PROJECTS, project_ids):
                if proj_data["status"] in transcript_statuses:
                    transcript = Transcript(
                        project_id=proj_id,
                        status=transcript_statuses[proj_data["status"]],
                        language=proj_data["source_lang"],
                        model_used="whisper-medium",
                        segments=_make_segments(10, f"Sample transcript for {proj_data['title']}", proj_data["source_lang"]),
                        raw_text=f"Full transcript text for {proj_data['title']}. " * 20,
                        duration_seconds=45.0,
                    )
                    session.add(transcript)
            print("  📝 Transcripts created")

            # ── Translations (for projects with status >= TRANSLATION_READY) ──
            translation_statuses = {
                ProjectStatus.COMPLETED: TranslationStatus.COMPLETED,
                ProjectStatus.TRANSLATION_READY: TranslationStatus.COMPLETED,
                ProjectStatus.DUBBING_READY: TranslationStatus.COMPLETED,
            }
            for proj_data, proj_id in zip(SAMPLE_PROJECTS, project_ids):
                if proj_data["status"] in translation_statuses:
                    # Get the transcript for this project
                    result = await session.execute(
                        select(Transcript).where(Transcript.project_id == proj_id)
                    )
                    transcript = result.scalar_one_or_none()
                    if transcript:
                        translation = Translation(
                            project_id=proj_id,
                            transcript_id=transcript.id,
                            status=translation_statuses[proj_data["status"]],
                            translated_text=f"Bản dịch tiếng Việt cho {proj_data['title']}. " * 20,
                            segments=_make_segments(10, f"Bản dịch cho {proj_data['title']}", "vi"),
                            style="natural",
                            engine_used="local_llm",
                        )
                        session.add(translation)
            print("  🌐 Translations created")

            # ── Dubbing (for projects with status >= DUBBING_READY) ──
            dubbing_statuses = {
                ProjectStatus.COMPLETED: DubbingStatus.COMPLETED,
                ProjectStatus.DUBBING_READY: DubbingStatus.COMPLETED,
            }
            for proj_data, proj_id in zip(SAMPLE_PROJECTS, project_ids):
                if proj_data["status"] in dubbing_statuses:
                    dubbing = Dubbing(
                        project_id=proj_id,
                        status=dubbing_statuses[proj_data["status"]],
                        voice_id="male_deep_01",
                        voice_name="Giọng Nam trầm",
                        engine_used="coqui",
                        audio_path=f"/data/projects/{proj_id}/audio/full_dub.wav",
                        speed=1.0,
                        pitch=0.0,
                        volume=1.0,
                        segments=_make_segments(10, f"Dubbing for {proj_data['title']}", "vi"),
                    )
                    session.add(dubbing)
            print("  🎤 Dubbing created")

            # ── Subtitles (for completed project) ─────────────────────
            for proj_data, proj_id in zip(SAMPLE_PROJECTS, project_ids):
                if proj_data["status"] == ProjectStatus.COMPLETED:
                    subtitle = Subtitle(
                        project_id=proj_id,
                        format=SubtitleFormat.SRT,
                        content=_make_segments(10, f"Subtitle for {proj_data['title']}", "vi"),
                        style_config={
                            "font_family": "Arial",
                            "font_size": 24,
                            "font_color": "#FFFFFF",
                            "border_color": "#000000",
                            "border_width": 2,
                            "position": "bottom",
                            "animation": "fade",
                        },
                        file_path=f"/data/projects/{proj_id}/subtitles/output.srt",
                    )
                    session.add(subtitle)
            print("  📄 Subtitles created")

            # ── Branding (for completed project) ──────────────────────
            for proj_data, proj_id in zip(SAMPLE_PROJECTS, project_ids):
                if proj_data["status"] == ProjectStatus.COMPLETED:
                    branding = Branding(
                        project_id=proj_id,
                        intro_enabled=True,
                        intro_template_id="intro_professional_01",
                        intro_duration=5.0,
                        outro_enabled=True,
                        outro_template_id="outro_subscribe_01",
                        watermark_enabled=True,
                        watermark_config={
                            "position": "bottom_right",
                            "opacity": 0.7,
                            "scale_percent": 15,
                            "margin_x": 20,
                            "margin_y": 20,
                        },
                        bg_music_enabled=True,
                        bg_music_path=f"/data/projects/{proj_id}/branding/bg_music.mp3",
                        bg_music_volume=0.3,
                    )
                    session.add(branding)
            print("  🎨 Branding created")

            # ── Render Tasks (for completed project) ──────────────────
            for proj_data, proj_id in zip(SAMPLE_PROJECTS, project_ids):
                if proj_data["status"] == ProjectStatus.COMPLETED:
                    render_task = RenderTask(
                        project_id=proj_id,
                        status=RenderStatus.COMPLETED,
                        progress=100.0,
                        output_path=f"/data/projects/{proj_id}/output/final.mp4",
                        settings={
                            "quality_preset": "balanced",
                            "crf": 23,
                            "gpu_acceleration": False,
                            "include_intro": True,
                            "include_outro": True,
                            "burn_subtitles": True,
                            "replace_audio": True,
                        },
                        started_at=datetime.now(timezone.utc).isoformat(),
                        completed_at=datetime.now(timezone.utc).isoformat(),
                        duration_seconds=300.0,
                    )
                    session.add(render_task)
            print("  ⚙️  Render tasks created")

            # ── YouTube Metadata (for completed project) ──────────────
            for proj_data, proj_id in zip(SAMPLE_PROJECTS, project_ids):
                if proj_data["status"] == ProjectStatus.COMPLETED:
                    youtube_meta = YouTubeMetadata(
                        project_id=proj_id,
                        title=f"{proj_data['title']} — Bản địa hóa bởi AI",
                        description=f"Video này được tạo tự động bằng AI.\n\n{proj_data['description']}\n\n#AI #Video #Localization",
                        tags=["AI", "video", "localization", "tutorial", "Vietnamese"],
                        category_id="22",  # Education
                        visibility=VisibilityType.UNLISTED,
                        chapters=[
                            {"title": "Giới thiệu", "start_ms": 0},
                            {"title": "Nội dung chính", "start_ms": 30000},
                            {"title": "Kết luận", "start_ms": 90000},
                        ],
                        thumbnail_path=f"/data/projects/{proj_id}/output/thumbnail.jpg",
                    )
                    session.add(youtube_meta)
            print("  ▶️  YouTube metadata created")

            # ── Voice Profiles ────────────────────────────────────────
            for voice_data in SAMPLE_VOICES:
                voice = VoiceProfile(
                    user_id=user_id,
                    name=voice_data["name"],
                    engine=voice_data["engine"],
                    voice_id=voice_data["voice_id"],
                    language=voice_data["language"],
                    gender=voice_data["gender"],
                    description=voice_data["description"],
                    preview_path=f"/data/voice-profiles/previews/{voice_data['voice_id']}.mp3",
                    is_cloned=voice_data["is_cloned"],
                    config={
                        "sample_rate": 22050,
                        "model_path": f"models/{voice_data['engine']}/{voice_data['voice_id']}",
                    },
                )
                session.add(voice)
            print("  🗣️  Voice profiles created")

            # ── Chat Messages (for first project) ─────────────────────
            first_project_id = project_ids[0]
            for msg_data in SAMPLE_CHAT_MESSAGES:
                chat_msg = ChatMessage(
                    project_id=first_project_id,
                    role=msg_data["role"],
                    content=msg_data["content"],
                    context=msg_data["context"],
                    tokens_used=150 if msg_data["role"] == MessageRole.ASSISTANT else None,
                    model="gpt-4" if msg_data["role"] == MessageRole.ASSISTANT else None,
                )
                session.add(chat_msg)
            print("  💬 Chat messages created")

            await session.commit()
            print(f"\n✅ Seed completed successfully!")
            print(f"   - {len(project_ids)} projects")
            print(f"   - {len(SAMPLE_VOICES)} voice profiles")
            print(f"   - {len(SAMPLE_CHAT_MESSAGES)} chat messages")

        except Exception as e:
            await session.rollback()
            print(f"\n❌ Seed failed: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(description="Seed database with sample data")
    parser.add_argument("--clear", action="store_true", help="Clear all data before seeding")
    args = parser.parse_args()

    print("🌱 Seeding database...")
    asyncio.run(seed_database(clear=args.clear))


if __name__ == "__main__":
    main()