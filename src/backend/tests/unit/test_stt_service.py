import pytest
from unittest.mock import MagicMock, patch

from app.services.stt_service import (
    STTService,
    _detect_gpu,
    _get_device,
    _get_whisper_model_size,
    VALID_MODEL_SIZES,
    SUPPORTED_LANGUAGES,
    _merge_short_segments,
)


class TestGPUDetection:
    def test_detect_gpu_disabled_in_config(self):
        with patch("app.services.stt_service.settings") as mock_settings:
            mock_settings.GPU_ENABLED = False
            assert _detect_gpu() is False

    def test_detect_gpu_enabled_no_cuda(self):
        with patch("app.services.stt_service.settings") as mock_settings:
            mock_settings.GPU_ENABLED = True
            with patch("app.services.stt_service.torch.cuda.is_available", return_value=False):
                assert _detect_gpu() is False

    def test_detect_gpu_enabled_with_cuda(self):
        with patch("app.services.stt_service.settings") as mock_settings:
            mock_settings.GPU_ENABLED = True
            with patch("app.services.stt_service.torch.cuda.is_available", return_value=True):
                assert _detect_gpu() is True


class TestDeviceSelection:
    def test_get_device_returns_cpu_when_gpu_unavailable(self):
        with patch("app.services.stt_service._detect_gpu", return_value=False):
            assert _get_device() == "cpu"

    def test_get_device_returns_cuda_when_gpu_available(self):
        with patch("app.services.stt_service._detect_gpu", return_value=True):
            assert _get_device() == "cuda"


class TestModelSizeValidation:
    def test_valid_model_sizes(self):
        for size in VALID_MODEL_SIZES:
            with patch("app.services.stt_service.settings") as mock_settings:
                mock_settings.WHISPER_MODEL = "medium"
                assert _get_whisper_model_size(size) == size

    def test_invalid_model_size_falls_back_to_default(self):
        with patch("app.services.stt_service.settings") as mock_settings:
            mock_settings.WHISPER_MODEL = "medium"
            result = _get_whisper_model_size("invalid-size")
            assert result == "medium"

    def test_case_insensitivity(self):
        with patch("app.services.stt_service.settings") as mock_settings:
            mock_settings.WHISPER_MODEL = "medium"
            assert _get_whisper_model_size("Base") == "base"
            assert _get_whisper_model_size("LARGE") == "large"


class TestSupportedLanguages:
    def test_vi_is_supported(self):
        assert "vi" in SUPPORTED_LANGUAGES

    def test_en_is_supported(self):
        assert "en" in SUPPORTED_LANGUAGES

    def test_unsupported_language(self):
        assert "xx" not in SUPPORTED_LANGUAGES


class TestModelLoading:
    def test_load_model_sets_model_size(self):
        mock_model = MagicMock()
        with patch("app.services.stt_service.whisper.load_model", return_value=mock_model):
            service = STTService()
            service._load_model("base")
            assert service._model_size == "base"
            assert service._model is not None

    def test_load_model_skips_if_same_size(self):
        mock_model = MagicMock()
        service = STTService()
        service._model = mock_model
        service._model_size = "base"
        with patch("app.services.stt_service.whisper.load_model") as mock_load:
            service._load_model("base")
            mock_load.assert_not_called()

    def test_load_model_reloads_if_different_size(self):
        mock_model = MagicMock()
        new_mock = MagicMock()
        service = STTService()
        service._model = mock_model
        service._model_size = "base"
        with patch("app.services.stt_service.whisper.load_model", return_value=new_mock):
            service._load_model("large")
            assert service._model is new_mock
            assert service._model_size == "large"


class TestSegmentProcessing:
    @staticmethod
    def _make_segment(start, end, text):
        return {"start": start, "end": end, "text": text}

    def test_empty_segments(self):
        assert _merge_short_segments([]) == []

    def test_single_segment_within_range(self):
        segs = [self._make_segment(0.0, 5.0, "hello world")]
        result = _merge_short_segments(segs)
        assert len(result) == 1
        assert result[0]["text"] == "hello world"

    def test_merges_short_segments(self):
        segs = [
            self._make_segment(0.0, 0.5, "hello"),
            self._make_segment(0.5, 0.9, "world"),
        ]
        result = _merge_short_segments(segs, min_duration=1.0, max_duration=10.0)
        assert len(result) == 1
        assert "hello" in result[0]["text"]

    def test_respects_max_duration(self):
        segs = [self._make_segment(0.0, 12.0, "word " * 50)]
        result = _merge_short_segments(segs, min_duration=1.0, max_duration=10.0)
        assert len(result) >= 1


class TestNormaliseSegments:
    def test_normalise_basic_segments(self):
        service = STTService()
        raw = [
            {"start": 0.0, "end": 2.5, "text": " Hello world "},
            {"start": 2.5, "end": 5.0, "text": "Foo bar"},
        ]
        result = service._normalise_segments(raw, word_timestamps=False)
        assert len(result) == 2
        assert result[0]["start"] == 0.0
        assert result[0]["end"] == 2.5
        assert result[0]["text"] == "Hello world"
        assert "words" not in result[0]

    def test_normalise_with_word_timestamps(self):
        service = STTService()
        raw = [
            {
                "start": 0.0,
                "end": 2.0,
                "text": "hello world",
                "words": [
                    {"word": "hello", "start": 0.0, "end": 1.0, "probability": 0.95},
                    {"word": "world", "start": 1.0, "end": 2.0, "probability": 0.98},
                ],
            }
        ]
        result = service._normalise_segments(raw, word_timestamps=True)
        assert len(result) == 1
        assert "words" in result[0]
        assert len(result[0]["words"]) == 2
        assert result[0]["words"][0]["word"] == "hello"


class TestTranscribeValidation:
    @pytest.mark.asyncio
    async def test_transcribe_unsupported_language(self):
        service = STTService()
        with pytest.raises(ValueError, match="Unsupported language code: xx"):
            await service.transcribe(
                project_id="test-id",
                model_size="base",
                language="xx",
            )

    @pytest.mark.asyncio
    async def test_transcribe_no_video_found(self):
        service = STTService()
        with patch.object(service, "_resolve_video_path", side_effect=FileNotFoundError("no video")):
            with pytest.raises(FileNotFoundError):
                await service.transcribe(project_id="nonexistent", model_size="tiny")


class TestSTTServiceInit:
    def test_initial_device_detection(self):
        with patch("app.services.stt_service._get_device", return_value="cpu"):
            service = STTService()
            assert service._device == "cpu"
            assert service._model is None
            assert service._model_size == ""
