# TASKS: Video Localization AI Studio

> **Version:** 1.0
> **Author:** AI CEO / Planner
> **Estimated Duration:** ~17 weeks (4 months)

---

## Phase 0: Foundation (2 tuần)

### 0.1 Repository & Project Structure
- [x] Khởi tạo monorepo structure (frontend + backend + shared)
- [x] Thiết lập Git flow (main / develop / feature branches)
- [x] Viết .gitignore, .editorconfig, .env.example
- [x] Cấu hình ESLint, Prettier cho frontend
- [x] Cấu hình Ruff / Black cho Python backend
- [x] Thiết lập CI/CD pipeline (GitHub Actions)
  - [x] Lint & type-check trên PR
  - [x] Auto-build Docker images
  - [x] Unit test runner

### 0.2 Docker Environment
- [x] Tạo Dockerfile cho frontend (Node.js multi-stage)
- [x] Tạo Dockerfile cho backend (Python slim)
- [x] Tạo docker-compose.yml với services:
  - [x] frontend (Next.js dev server)
  - [x] backend (FastAPI + Uvicorn)
  - [x] postgres (database)
  - [x] redis (queue broker)
  - [x] celery-worker (task processing)
- [x] Thiết lập volume mounts cho project data
- [x] Thiết lập network isolation

### 0.3 Backend Foundation (FastAPI)
- [x] Khởi tạo project structure:
  ```
  backend/
  ├── app/
  │   ├── api/          # Routes & endpoints
  │   ├── core/         # Config, security, dependencies
  │   ├── models/       # SQLAlchemy models
  │   ├── schemas/      # Pydantic schemas
  │   ├── services/     # Business logic
  │   ├── tasks/        # Celery tasks
  │   └── utils/        # Helpers
  ├── tests/
  ├── alembic/          # Migrations
  ├── requirements/
  └── Dockerfile
  ```
- [x] Cấu hình FastAPI app (middleware, CORS, logging)
- [x] Thiết lập SQLAlchemy + Alembic migrations
- [x] Thiết lập Redis connection
- [x] Thiết lập Celery app + task base class
- [x] Viết health check endpoint (`/health`)
- [x] Cấu hình settings management (pydantic-settings)

### 0.4 Frontend Foundation (Next.js)
- [x] Khởi tạo Next.js 14 project với App Router
- [x] Cấu hình TailwindCSS + theme
- [x] Cài đặt shadcn/ui component library
- [x] Thiết lập React Query (TanStack Query) cho API calls
- [x] Thiết lập Zustand / Context cho state management
- [x] Cấu hình Axios instance với interceptors
- [x] Tạo layout cơ bản (Sidebar + Header + Main Content)
- [x] Tạo Error Boundary, Loading skeleton components

### 0.5 Database Schema
- [x] Thiết kế và tạo models:
  - [x] **User**: id, email, name, avatar, settings (model exists at src/backend/app/models/)
  - [x] **Project**: id, user_id, title, source_lang, target_lang, status, created_at, updated_at
  - [x] **Video**: id, project_id, filename, path, duration, resolution, fps, size, codec, thumbnail_path
  - [x] **Transcript**: id, project_id, segments (JSON), raw_text, language
  - [x] **Translation**: id, transcript_id, translated_text, segments (JSON), style, engine_used
  - [x] **Dubbing**: id, project_id, voice_id, audio_path, speed, pitch, volume
  - [x] **Subtitle**: id, project_id, format, content (JSON), style_config (JSON)
  - [x] **Branding**: id, project_id, intro_template, outro_template, watermark_config, bg_music_path
  - [x] **RenderTask**: id, project_id, status, progress, error_log, output_path, settings (JSON)
- [x] Viết Alembic migration scripts (001_initial_schema.py)
- [x] Tạo seed data scripts (scripts/seed_data.py)

---

## Phase 1: Core Pipeline (6 tuần)

### 1.1 Video Import Module
- [x] **Backend**: File upload endpoint (multipart, chunked upload cho file lớn)
- [x] **Backend**: URL download + validation service
- [x] **Backend**: Video metadata extraction (FFprobe wrapper)
- [x] **Backend**: Thumbnail generation service (FFmpeg)
- [x] **Backend**: File validation (format, size, codec check)
- [x] **Frontend**: Upload component (drag & drop, progress bar, file picker)
- [x] **Frontend**: URL import form
- [x] **Frontend**: Video metadata display card (thumbnail, duration, resolution, etc.)

### 1.2 Speech-to-Text Module (Whisper)
- [x] **Backend**: Whisper integration service
  - [x] Support all model sizes (tiny → large)
  - [x] GPU acceleration (CUDA) / CPU fallback
  - [x] Language auto-detection
- [x] **Backend**: Segment processing
  - [x] Word-level timestamp alignment
  - [x] Segment merging/splitting logic
  - [x] Output normalization (JSON format)
- [x] **Backend**: Celery task for STT processing
  - [x] Progress reporting (current segment, ETA)
  - [x] Error handling & retry logic
 - [x] **Frontend**: Transcript editor
   - [x] Display segments with timestamps
   - [x] Inline edit text
   - [x] Adjust segment boundaries (drag handles on timeline)
   - [x] Playback sync (highlight current segment)
 - [x] **Frontend**: STT configuration panel (model selection, language)

### 1.3 Translation Module
- [x] **Backend**: Translation engine abstraction (Strategy pattern)
  - [x] Local LLM adapter (Ollama / Llama.cpp)
  - [x] OpenAI API adapter
  - [x] Gemini API adapter
  - [x] Claude API adapter
- [x] **Backend**: Translation prompt engineering
  - [x] Style templates (Trung tính, Tự nhiên, Video ngắn, Giáo dục)
  - [x] Context preservation rules (names, technical terms)
  - [x] Batch translation (theo segments)
- [x] **Backend**: Celery task for translation
  - [x] Progress tracking per segment
  - [x] Fallback engine if one fails
- [x] **Frontend**: Translation interface
  - [x] Side-by-side view (original vs translated)
  - [x] Style selector dropdown
  - [x] Engine selector
  - [x] Segment-level re-translate button
  - [x] Translation quality indicators

### 1.4 Voice Dubbing Module (TTS)
- [x] **Backend**: TTS engine abstraction
  - [x] Coqui TTS adapter (tiếng Việt models)
  - [x] Piper TTS adapter
  - [x] Edge-TTS adapter (free online)
  - [x] Voice profile management (5+ voices)
- [x] **Backend**: Voice customization
  - [x] Speed adjustment (SSML/audio manipulation)
  - [x] Pitch shifting (FFmpeg)
  - [x] Volume normalization (LUFS target)
- [x] **Backend**: Audio sync service
  - [x] Time compression/expansion (match video duration)
  - [x] Crossfade between segments
- [x] **Backend**: Celery task for TTS
  - [x] Batch generate audio segments
  - [x] Stitch segments into full audio
- [x] **Frontend**: Voice configuration
  - [x] Voice preview (play sample)
  - [x] Speed/pitch/volume sliders
  - [x] Voice selector grid
  - [x] Audio waveform preview

### 1.5 Video Processing Engine (FFmpeg)
- [x] **Backend**: FFmpeg command builder
  - [x] Video assembly pipeline (intro → main → outro)
  - [x] Audio replacement service
  - [x] Subtitle burning service (hardcode)
  - [x] Subtitle embedding service (softcode/mux)
  - [x] Resolution scaling
  - [x] Codec selection (H.264 / H.265)
  - [x] GPU acceleration (CUDA, VAAPI, VideoToolbox)
- [x] **Backend**: Audio processing
  - [x] Volume normalization (EBU R128 / LUFS)
  - [x] Noise reduction (afftdn filter)
  - [x] Crossfade transitions
- [x] **Backend**: Celery task for video rendering
  - [x] Progress reporting (frame-level percentage)
  - [x] ETA calculation
  - [x] Cancel/resume support
- [x] **Backend**: Export service
  - [x] Multiple output formats (MP4, MOV, MKV)
  - [x] Quality presets (fast/balanced/best)
- [x] **Frontend**: Export configuration
  - [x] Format/resolution selector
  - [x] Quality preset selector
  - [x] Progress display with cancel button
  - [x] Download button after completion

---

## Phase 2: UI/UX (4 tuần)

### 2.1 Dashboard
- [x] **Frontend**: Project list view
  - [x] Grid/list toggle
  - [x] Search & filter (by status, date)
  - [x] Sort (by name, created date, updated date)
  - [x] Project thumbnails
- [x] **Frontend**: Create new project dialog
  - [x] Name input
  - [x] Source language selector
  - [x] Target language selector
- [x] **Frontend**: Quick actions (continue, duplicate, delete)
- [x] **Frontend**: Welcome/onboarding screen for new users
- [x] **Backend**: Project CRUD API endpoints
- [x] **Backend**: Dashboard stats API (total projects, storage used, etc.)

### 2.2 Project Workspace
- [x] **Frontend**: Pipeline step navigation (stepper / tabs)
- [x] **Frontend**: Project sidebar (file info, settings, timeline)
- [x] **Frontend**: Auto-save indicator
- [x] **Frontend**: Unsaved changes warning
- [x] **Frontend**: Project settings panel (rename, delete, export project)
- [x] **Backend**: Project settings API (export endpoint)

### 2.3 Subtitle Editor (Trực quan)
- [x] **Frontend**: Timeline component
  - [x] Zoom in/out (second-level to minute-level)
  - [x] Drag segments to adjust timing
  - [x] Split/merge segments
  - [x] Snap to grid (keyframes)
- [x] **Frontend**: Subtitle styling panel
  - [x] Font picker (system fonts)
  - [x] Color picker + presets
  - [x] Border/shadow controls
  - [x] Position presets (top, bottom, custom)
  - [x] Animation selector (fade, slide, typewriter, none)
  - [x] Preview panel (real-time)
- [x] **Frontend**: Subtitle text editor
  - [x] Multi-line support
  - [x] Character limit per line
  - [x] Auto-line-break
  - [ ] Spell check (future)
- [x] **Frontend**: Format selector (SRT/ASS/VTT preview)
- [x] **Backend**: Subtitle styling renderer (ASS format with styling)

### 2.4 Branding Module
- [x] **Frontend**: Intro template editor
  - [x] Logo upload + positioning
  - [x] Channel name text input
  - [x] Animation style selector
  - [x] Duration slider (3-15 seconds)
  - [x] Audio upload (brand music)
  - [x] Fade in/out toggles
  - [x] Save as template
- [x] **Frontend**: Outro template editor
  - [x] Subscribe button animation
  - [x] Like animation
  - [x] QR code generator (URL input)
  - [x] Website URL display
  - [x] Social links (YouTube, Facebook, TikTok, Instagram)
- [x] **Frontend**: Watermark overlay
  - [x] Image upload (logo)
  - [x] Position presets (4 corners, center)
  - [x] Opacity slider
  - [x] Size slider
  - [x] Show entire video / specific range
- [x] **Frontend**: Background music
  - [x] File upload
  - [x] Volume mix slider (music vs voice)
  - [x] Loop toggle
  - [x] Fade in/out
- [ ] **Backend**: Branding config API (CRUD templates)
- [ ] **Backend**: Template storage service

---

## Phase 3: Advanced Features (3 tuần)

### 3.1 Batch Processing
- [ ] **Frontend**: Batch queue manager
  - [ ] Add multiple projects to queue
  - [ ] Reorder queue (drag & drop)
  - [ ] Priority settings (high/normal/low)
  - [ ] Batch progress overview (aggregated)
  - [ ] Individual progress per project
- [ ] **Frontend**: Queue controls
  - [ ] Pause/resume all
  - [ ] Cancel individual items
  - [ ] Clear completed
  - [ ] Retry failed
- [ ] **Frontend**: Batch history
  - [ ] Completed batch logs
  - [ ] Export batch report
- [ ] **Backend**: Batch service
  - [ ] Queue management API
  - [ ] Parallel processing controller
  - [ ] Resource-aware scheduling (CPU/GPU/memory limits)
  - [ ] Error aggregation and reporting

### 3.2 AI Assistant (Chatbot)
- [ ] **Frontend**: Chat interface
  - [ ] Sidebar chat panel
  - [ ] Context-aware (attached to current project/segment)
  - [ ] Message history per project
  - [ ] Markdown rendering
  - [ ] Copy-to-clipboard buttons
- [ ] **Frontend**: AI action buttons (contextual)
  - [ ] "Improve translation" button in translation tab
  - [ ] "Generate title" button in publish tab
  - [ ] "Suggest hashtags" button
  - [ ] "Generate chapters" button
- [ ] **Backend**: AI Assistant service
  - [ ] System prompt engineering
  - [ ] Context window management (project data as context)
  - [ ] Tool calling (translate, generate, analyze)
  - [ ] Streaming response (SSE)
- [ ] **Backend**: Prompt templates
  - [ ] Title generation
  - [ ] Description writing
  - [ ] Hashtag suggestion
  - [ ] Chapter generation from transcript
  - [ ] Thumbnail text suggestion
  - [ ] SEO keyword recommendation
  - [ ] Translation refinement

### 3.3 YouTube Publishing
- [ ] **Frontend**: YouTube metadata form
  - [ ] Title input (with character counter)
  - [ ] Description textarea (with formatting toolbar)
  - [ ] Tags input (comma separated, autocomplete)
  - [ ] Playlist selector
  - [ ] Chapter editor (auto-generated from transcript)
  - [ ] Visibility selector (public/unlisted/private)
- [ ] **Frontend**: Thumbnail generator
  - [ ] Frame selector from video timeline
  - [ ] Text overlay editor
  - [ ] Template presets
- [ ] **Frontend**: Metadata export
  - [ ] JSON export
  - [ ] YAML export
  - [ ] Copy to clipboard
  - [ ] YouTube API integration (future)
- [ ] **Backend**: YouTube metadata service
  - [ ] Metadata schema validation
  - [ ] Chapter auto-generation from transcript
  - [ ] Thumbnail generation service (FFmpeg + PIL)

---

## Phase 4: Polish & Release (2 tuần)

### 4.1 Error Handling & Recovery
- [ ] **Backend**: Comprehensive error handling
  - [ ] Graceful degradation (CPU fallback if GPU fails)
  - [ ] Task retry with exponential backoff
  - [ ] Partial failure recovery (skip bad segment, continue)
  - [ ] Dead letter queue for unprocessable tasks
- [ ] **Backend**: Checkpoint system
  - [ ] Save intermediate results (transcript, translation, audio)
  - [ ] Resume from last checkpoint on restart
  - [ ] Auto-recovery on system crash
- [x] **Frontend**: Error display
  - [x] Toast notifications for errors
  - [x] Error detail modal (with stack trace option)
  - [x] Retry buttons
  - [ ] Offline detection

### 4.2 Testing
- [ ] **Backend**: Unit tests
  - [ ] API endpoint tests (pytest + httpx)
  - [ ] Service layer tests (mocked dependencies)
  - [ ] FFmpeg command builder tests
  - [ ] Translation engine tests
- [ ] **Backend**: Integration tests
  - [ ] Full pipeline test (STT → Translation → TTS → Render)
  - [ ] Database CRUD tests
  - [ ] File upload/download tests
- [x] **Frontend**: Component tests (Vitest + Testing Library)
  - [x] Upload component tests
  - [x] Transcript editor tests
  - [x] Subtitle editor tests
  - [x] Dashboard tests
- [ ] **Frontend**: E2E tests (Playwright)
  - [ ] User flow: Create project → Upload → STT → Translate → Export
  - [ ] Batch processing flow
- [ ] **Performance benchmarks**
  - [ ] STT speed benchmarks (all Whisper models)
  - [ ] Translation speed benchmarks (all engines)
  - [ ] Render speed benchmarks (all resolutions)
  - [ ] Memory usage profiling

### 4.3 Performance Optimization
- [ ] **Backend**: Caching
  - [ ] Redis caching for repeated operations
  - [ ] Model warm-up on startup
  - [ ] File system cache for intermediate results
- [ ] **Backend**: Database optimization
  - [ ] Index optimization
  - [ ] Query optimization (N+1 fixes)
  - [ ] Connection pooling
- [ ] **Frontend**: Bundle optimization
  - [ ] Code splitting (lazy load modules)
  - [ ] Image optimization (next/image)
  - [ ] Memoization (React.memo, useMemo)
- [ ] **Frontend**: Virtual scrolling for long lists/projects

### 4.4 Documentation
- [ ] **README.md**: Project overview, setup, usage
- [ ] **API Documentation**: FastAPI auto-docs + manual examples
- [ ] **User Guide**: Step-by-step with screenshots
- [ ] **Developer Guide**: Architecture, contribution, local dev
- [ ] **Docker Setup Guide**: How to run with Docker
- [ ] **Video Demo**: Screen recording of full workflow

### 4.5 Release Preparation
- [ ] Security audit (dependency scanning, API security)
- [ ] License selection (MIT / GPL / AGPL)
- [ ] CHANGELOG.md generation
- [ ] Version tagging (v1.0.0)
- [ ] Docker image build & push
- [ ] Release checklist finalization

---

## Legend

| Priority | Symbol | Ý nghĩa |
|----------|--------|---------|
| **P0** | 🔴 | Must-have cho v1.0 |
| **P1** | 🟡 | Important nhưng có thể trì hoãn |
| **P2** | 🟢 | Nice-to-have, v2.0 |
| **Dep** | 🔗 | Phụ thuộc vào task khác |

---

## Task Dependencies Map

```
P0.1 (Repo) ──→ P0.2 (Docker) ──→ P0.4 (Frontend Init)
                                       │
P0.3 (Backend Init) ←──────────────────┘
    │
    ├──→ P1.1 (Video Import) ──→ P1.2 (STT) ──→ P1.3 (Translation)
    │                                                          │
    └──→ P0.5 (Database)                                       │
                                                               │
                                        P1.4 (TTS) ←───────────┘
                                            │
                                            └──→ P1.5 (Video Processing)
                                                      │
                                ┌─────────────────────┘
                                │
                     P2.1 (Dashboard) ──→ P2.2 (Workspace)
                                                │
                                       P2.3 (Subtitle Editor)
                                                │
                                       P2.4 (Branding)
                                                │
                     P3.1 (Batch) ──→ P3.2 (AI Assistant) ──→ P3.3 (YouTube)
                                                │
                     P4.1 (Error) ←── P4.2 (Test) ←── P4.3 (Performance)
                                                │
                                       P4.4 (Docs) ──→ P4.5 (Release)