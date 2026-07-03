## Backend Whisper Integration — lần thử #1
- Thời gian: 2025-07-03 10:50
- Nhánh: `feature/backend-whisper-integration`
- Lỗi: Whisper import fails on Windows with `TypeError: LoadLibrary() argument 1 must be str, not None` due to libc detection in `whisper.py`.
- Ghi chú: Upgrading `openai-whisper` resolved import. Re-running tests revealed 2 async tests failing due to missing `pytest-asyncio` plugin, not business logic.

## Backend Whisper Integration — lần thử #2
- Thời gian: 2025-07-03 10:52
- Nhánh: `feature/backend-whisper-integration`
- Lỗi: After fixing Whisper runtime, `pytest` fails 2 async tests (`test_transcribe_unsupported_language`, `test_transcribe_no_video_found`) because `pytest-asyncio` is not installed in test environment.
- Ghi chú: 21/23 tests pass. Failures are test-runner config/environment issue, not implementation error. Quality Gate cannot pass without fixing test environment dependency.