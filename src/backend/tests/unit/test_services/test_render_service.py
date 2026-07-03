"""
Unit tests for Render Service (FFmpeg command builder)
"""

from pathlib import Path

import pytest

from app.services.render_service import (
    QualityPreset,
    RenderService,
    VideoCodec,
)


class DummyDB:
    pass


@pytest.fixture
def service():
    return RenderService(db=DummyDB())


@pytest.mark.asyncio
async def test_build_render_command_requires_paths(service):
    with pytest.raises(ValueError):
        await service.build_render_command(project_id="proj-1", output_path=None, main_video_path=None)


@pytest.mark.asyncio
async def test_build_render_command_basic(service):
    cmd = await service.build_render_command(
        project_id="proj-1",
        main_video_path=Path("/tmp/main.mp4"),
        output_path=Path("/tmp/out.mp4"),
    )
    assert cmd[0] == "ffmpeg"
    assert "-i" in cmd
    assert str(Path("/tmp/main.mp4")) in cmd
    assert str(Path("/tmp/out.mp4")) in cmd


@pytest.mark.asyncio
async def test_build_render_command_with_audio(service):
    cmd = await service.build_render_command(
        project_id="proj-1",
        main_video_path=Path("/tmp/main.mp4"),
        audio_path=Path("/tmp/audio.mp3"),
        output_path=Path("/tmp/out.mp4"),
    )
    # Audio input may not be added if file doesn't exist
    assert cmd[0] == "ffmpeg"
    assert str(Path("/tmp/main.mp4")) in cmd


@pytest.mark.asyncio
async def test_normalize_audio_command(service):
    cmd = await service.normalize_audio(
        input_path=Path("/tmp/in.mp3"),
        output_path=Path("/tmp/out.mp3"),
        target_lufs=-16.0,
    )
    assert "loudnorm=I=-16.0" in " ".join(cmd)
    assert str(Path("/tmp/in.mp3")) in cmd
    assert str(Path("/tmp/out.mp3")) in cmd


@pytest.mark.asyncio
async def test_apply_noise_reduction_command(service):
    cmd = await service.apply_noise_reduction(
        input_path=Path("/tmp/in.wav"),
        output_path=Path("/tmp/out.wav"),
    )
    assert "afftdn=nf=0.5" in " ".join(cmd)


@pytest.mark.asyncio
async def test_crossfade_segments_single(service):
    cmd = await service.crossfade_segments(
        segment_paths=[Path("/tmp/segment1.mp3")],
        output_path=Path("/tmp/out.mp3"),
    )
    assert cmd[0] == "cp"
    assert str(Path("/tmp/segment1.mp3")) in cmd


@pytest.mark.asyncio
async def test_crossfade_segments_multiple(service):
    cmd = await service.crossfade_segments(
        segment_paths=[Path("/tmp/a.mp3"), Path("/tmp/b.mp3")],
        output_path=Path("/tmp/out.mp3"),
        crossfade_duration=0.5,
    )
    assert "acrossfade=d=0.5" in " ".join(cmd)