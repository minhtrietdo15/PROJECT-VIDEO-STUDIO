# Architecture Design — Video Localization AI Studio

> **Version:** 1.0
> **Author:** AI Architect
> **Last Updated:** 2026-07-01

---

## 1. System Architecture Overview

### 1.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              Next.js 14 (App Router)                         │    │
│  │  ┌─────────┐ ┌──────────┐ ┌──────────────┐ ┌───────────┐   │    │
│  │  │Dashboard│ │Project   │ │Subtitle      │ │AI Chatbot │   │    │
│  │  │         │ │Workspace │ │Editor        │ │Assistant  │   │    │
│  │  └─────────┘ └──────────┘ └──────────────┘ └───────────┘   │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  TanStack Query (Client State) + Zustand (UI State) │    │    │
│  │  │  Axios (HTTP) + WebSocket (Real-time)               │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │  HTTP REST / WebSocket   │
              │  (JSON / SSE / Binary)   │
              └────────────┬────────────┘
                           │
┌─────────────────────────────────────────────────────────────────────┐
│                       API GATEWAY LAYER                              │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              FastAPI (Python 3.11+)                          │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │    │
│  │  │Auth      │ │Project   │ │Task      │ │File Streaming│   │    │
│  │  │Middleware│ │CRUD API  │ │Manager   │ │Service       │   │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  Pydantic (Validation) + SQLAlchemy Async (ORM)     │    │    │
│  │  │  Celery Client (Task Dispatch) + Redis Client       │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │  Redis (Message Broker)  │
              └────────────┬────────────┘
                           │
┌─────────────────────────────────────────────────────────────────────┐
│                       WORKER LAYER (Celery)                          │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  ┌────────────┐ ┌──────────────┐ ┌──────────┐ ┌─────────┐  │    │
│  │  │STT Worker  │ │Translation   │ │TTS Worker│ │Video    │  │    │
│  │  │(Whisper)   │ │Worker (LLM)  │ │(Coqui)   │ │Renderer │  │    │
│  │  └────────────┘ └──────────────┘ └──────────┘ └─────────┘  │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  GPU Scheduler (CUDA/CPU Fallback)                   │    │    │
│  │  │  Worker Pool: 1 GPU worker + N CPU workers           │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │  PostgreSQL + File System│
              └────────────┬────────────┘
                           │
┌─────────────────────────────────────────────────────────────────────┐
│                       STORAGE LAYER                                  │
│  ┌────────────────────┐ ┌────────────────┐ ┌──────────────────┐    │
│  │  PostgreSQL (Meta) │ │ File System    │ │ Redis (Cache +   │    │
│  │  • Projects        │ │ (Video/Audio)  │ │ Queue + Session) │    │
│  │  • Users           │ │ • Uploads      │ │ • Celery Broker  │    │
│  │  • Segments        │ │ • Outputs      │ │ • Result Backend │    │
│  │  • Tasks           │ │ • Thumbnails   │ │ • Project Cache  │    │
│  │  • Settings        │ │ • Templates    │ │ • Rate Limiting  │    │
│  └────────────────────┘ └────────────────┘ └──────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Module Architecture

### 2.1 Frontend Module Tree

```
frontend/
├── app/                              # Next.js App Router
│   ├── (auth)/                       # Authentication routes
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/                  # Protected routes
│   │   ├── dashboard/                # Project list
│   │   └── projects/
│   │       └── [projectId]/          # Project workspace
│   │           ├── page.tsx          # Workspace shell
│   │           ├── transcript/
│   │           ├── translation/
│   │           ├── dubbing/
│   │           ├── subtitle/
│   │           ├── branding/
│   │           ├── render/
│   │           └── publish/
│   └── layout.tsx                    # Root layout
│
├── components/                       # Shared components
│   ├── ui/                           # shadcn/ui primitives
│   ├── layout/                       # Sidebar, Header, Shell
│   ├── upload/                       # Drag-drop uploader
│   ├── timeline/                     # Segment timeline
│   ├── media/                        # Video/Audio players
│   └── chat/                         # AI Assistant UI
│
├── hooks/                            # Custom hooks
│   ├── use-websocket.ts
│   ├── use-project.ts
│   └── use-transcript.ts
│
├── lib/                              # Utilities
│   ├── api-client.ts                 # Axios instance
│   ├── ws-client.ts                  # WebSocket client
│   └── utils.ts
│
├── stores/                           # Zustand stores
│   ├── project-store.ts
│   └── ui-store.ts
│
└── types/                            # TypeScript types
    ├── api.ts
    └── models.ts
```

### 2.2 Backend Module Tree

```
backend/
├── app/
│   ├── __init__.py
│   │
│   ├── main.py                       # FastAPI app entry
│   ├── config.py                     # Settings (pydantic-settings)
│   ├── dependencies.py               # FastAPI DI
│   │
│   ├── api/                          # API Layer
│   │   ├── __init__.py
│   │   ├── router.py                 # Root router aggregation
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── projects.py           # Project CRUD
│   │   │   ├── videos.py             # Video upload/import
│   │   │   ├── transcripts.py        # STT endpoints
│   │   │   ├── translations.py       # Translation endpoints
│   │   │   ├── dubbing.py            # TTS endpoints
│   │   │   ├── subtitles.py          # Subtitle endpoints
│   │   │   ├── branding.py           # Branding endpoints
│   │   │   ├── renders.py            # Render/export endpoints
│   │   │   ├── chat.py               # AI Assistant endpoints
│   │   │   ├── youtube.py            # YouTube metadata
│   │   │   ├── voice_profiles.py     # Voice management
│   │   │   ├── branding_templates.py # Template CRUD
│   │   │   ├── batch.py              # Batch processing
│   │   │   └── files.py              # File serving
│   │   └── ws/
│   │       └── project_ws.py         # WebSocket handler
│   │
│   ├── core/                         # Core Framework
│   │   ├── __init__.py
│   │   ├── config.py                 # App configuration
│   │   ├── security.py               # Auth, JWT, API keys
│   │   ├── logging.py                # Logging setup
│   │   ├── exceptions.py             # Custom exception classes
│   │   ├── middleware.py             # CORS, rate limiting, error handler
│   │   └── events.py                 # Startup/shutdown events
│   │
│   ├── models/                       # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── base.py                   # Declarative base
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── video.py
│   │   ├── transcript.py
│   │   ├── translation.py
│   │   ├── dubbing.py
│   │   ├── subtitle.py
│   │   ├── branding.py
│   │   ├── render_task.py
│   │   ├── voice_profile.py
│   │   ├── chat.py
│   │   └── youtube_metadata.py
│   │
│   ├── schemas/                      # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── project.py                # Project create/update/response
│   │   ├── video.py
│   │   ├── transcript.py
│   │   ├── translation.py
│   │   ├── dubbing.py
│   │   ├── subtitle.py
│   │   ├── branding.py
│   │   ├── render.py
│   │   ├── chat.py
│   │   ├── youtube.py
│   │   ├── voice.py
│   │   └── common.py                 # Pagination, Error, Response
│   │
│   ├── services/                     # Business Logic
│   │   ├── __init__.py
│   │   ├── project_service.py
│   │   ├── video_service.py          # FFprobe, validation
│   │   ├── stt_service.py            # Whisper abstraction
│   │   ├── translation_service.py    # LLM abstraction
│   │   ├── tts_service.py            # TTS abstraction
│   │   ├── subtitle_service.py       # pysubs2
│   │   ├── branding_service.py
│   │   ├── render_service.py         # FFmpeg pipeline
│   │   ├── chat_service.py           # AI Assistant logic
│   │   ├── youtube_service.py
│   │   ├── file_service.py           # File I/O manager
│   │   └── batch_service.py
│   │
│   ├── tasks/                        # Celery Tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py             # Celery configuration
│   │   ├── base.py                   # Base task class
│   │   ├── stt_task.py               # Transcription
│   │   ├── translation_task.py       # Translation
│   │   ├── tts_task.py               # Voice generation
│   │   ├── render_task.py            # Video rendering
│   │   ├── download_task.py          # URL import
│   │   └── batch_task.py             # Batch orchestration
│   │
│   └── utils/                        # Helpers
│       ├── __init__.py
│       ├── ffmpeg.py                 # FFmpeg command builder
│       ├── file_utils.py             # Path, format helpers
│       ├── audio_utils.py            # Audio processing
│       └── srt_utils.py              # Subtitle parsing
│
├── alembic/                          # Database migrations
│   ├── env.py
│   └── versions/
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_services/
│   │   └── test_api/
│   ├── integration/
│   │   └── test_pipeline.py
│   └── fixtures/
│       └── sample_video.mp4
│
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── Dockerfile
└── pyproject.toml
```

---

## 3. AI Pipeline Processing Flow

### 3.1 Sequential Pipeline Workflow

```
                    ┌──────────────┐
                    │  START       │
                    │  New Project │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
               ┌────│ Video Import │────┐
               │    └──────┬───────┘    │
               │           │            │
               │    ┌──────▼───────┐    │
               │    │  STT (Whisper)│    │
               │    │  Async Task  │    │
               │    └──────┬───────┘    │
               │           │            │
               │    ┌──────▼───────┐    │
               │    │ Translation  │    │
               │    │ (LLM) Async  │    │
               │    └──────┬───────┘    │
               │           │            │
               │    ┌──────▼───────┐    │
               │    │ TTS (Dubbing)│    │
               │    │ Async Task   │    │
               │    └──────┬───────┘    │
               │           │            │
               │    ┌──────▼───────┐    │
               │    │   Subtitle   │    │
               │    │  Generation  │    │
               │    └──────┬───────┘    │
               │           │            │
               │    ┌──────▼───────┐    │
               │    │   Branding   │    │
               │    │  (Optional)  │    │
               │    └──────┬───────┘    │
               │           │            │
               │    ┌──────▼───────┐    │
               │    │   Render     │    │
               └────│  (FFmpeg)    │    │
                    │  Async Task  │    │
                    └──────┬───────┘    │
                           │            │
                    ┌──────▼───────┐    │
                    │   COMPLETED  │    │
                    └──────────────┘    │
```

### 3.2 Parallel Processing Strategy

```
                    ┌─────────────────┐
                    │  Video Import   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼──────┐ ┌────▼─────┐  ┌─────▼────────┐
     │  STT Worker 1 │ │STT Worker│  │STT Worker N  │
     │  (GPU Core 0) │ │2 (GPU 1) │  │  (CPU)       │
     └────────┬──────┘ └────┬─────┘  └──────┬────────┘
              │              │               │
              └──────────────┼───────────────┘
                             │
                    ┌────────▼────────┐
                    │  Translation    │
                    │  Batch (LLM)    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼──────┐ ┌────▼─────┐  ┌─────▼────────┐
     │ TTS Segment 1 │ │TTS Seg 2 │  │TTS Segment N │
     └────────┬──────┘ └────┬─────┘  └──────┬────────┘
              │              │               │
              └──────────────┼───────────────┘
                             │
                    ┌────────▼────────┐
                    │  Audio Stitch   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  FFmpeg Render  │
                    │  (GPU/CPU)      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    Output       │
                    └─────────────────┘
```

### 3.3 STT Pipeline Detail (Whisper)

```
Input Video (.mp4)
       │
       ▼
┌──────────────────┐
│  Audio Extraction│  ← FFmpeg: ffmpeg -i input.mp4 -vn audio.wav
│  (16kHz mono)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Whisper Model   │  ← Options: tiny/base/small/medium/large
│  • Load Model    │     GPU: CUDA if available, else CPU
│  • Transcribe    │     Language: auto-detect or force
│  • Word-level    │
│    timestamps    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Post-process    │
│  • Segment merge │  ← Merge short segments, split long ones
│    (min 1s, max  │     Target segment length: 2-10 seconds
│     10s)         │
│  • Punctuation   │  ← Restore punctuation via regex rules
│    restoration   │
│  • Word alignment│  ← Align words to segments
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Write to DB     │  ← INSERT into transcript_segments
│  • Segment list  │     Publish WebSocket event
│  • WebSocket     │     Update project.pipeline_progress
│    notification  │
└──────────────────┘
```

### 3.4 Translation Pipeline Detail

```
Transcript Segments (from DB)
       │
       ▼
┌─────────────────────────────────┐
│  Build Prompt                   │
│  "Translate the following       │
│   transcript segments to        │
│   Vietnamese. Style: {style}    │
│   Keep technical terms and      │
│   proper names unchanged."      │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Batch Translation              │  ← Can split into batches
│  • Group 10-20 segments/request │     of 10-20 segments
│  • Send to LLM engine           │
│  • Parse structured response    │
│    (JSON format)                │
└────────┬────────────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│Local   │ │API     │
│LLM     │ │OpenAI  │
│(Ollama)│ │Gemini  │
│llama.cpp│ │Claude  │
└───┬────┘ └───┬────┘
    │         │
    └────┬────┘
         │
         ▼
┌──────────────────┐
│  Post-process    │
│  • Validate JSON │  ← Parse LLM output
│  • Sanity check  │     Ensure segment count matches
│  • Apply edits   │     Apply any user-preserved edits
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Write to DB     │  ← INSERT into translation_segments
│  • Translations  │     Publish WebSocket event
│  • WebSocket     │
└──────────────────┘
```

### 3.5 TTS Pipeline Detail

```
Translation Segments (from DB)
       │
       ▼
┌─────────────────────┐
│  Segment Preparation│
│  • SSML wrapping    │  ← Add prosody tags for speed/pitch
│  • Text sanitization│     Remove special characters
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────┐ ┌──────────┐
│Coqui   │ │Piper TTS │
│TTS     │ │Edge-TTS  │
│(Local) │ │(Online)  │
└───┬────┘ └─────┬────┘
    │            │
    └──────┬─────┘
           │
           ▼
┌─────────────────────┐
│  Parallel Segment   │  ← Process N segments in parallel
│  Generation         │     (N = CPU core count)
│  • Each segment →   │     Each produces .wav file
│    audio file       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Audio Stitching    │  ← Concatenate audio files
│  • Concat segments  │     Apply crossfade (50ms)
│  • Normalize volume │     Target: -16 LUFS
│  • Time stretch     │     Match original video duration
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Write to DB + Disk │  ← Save audio files
│  • Save audio files │     INSERT into audio_segments
│  • Insert segments  │     Publish WebSocket event
│  • WebSocket notify │
└─────────────────────┘
```

### 3.6 Video Render Pipeline (FFmpeg)

```
┌────────────────────────────────────────────────────────────────┐
│                     FFMPEG COMMAND PIPELINE                     │
│                                                                │
│  Step 1: Prepare inputs                                        │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ Input 1: Original Video (with original audio)       │       │
│  │ Input 2: New Dubbed Audio (TTS output)              │       │
│  │ Input 3: Intro Video (if enabled)                   │       │
│  │ Input 4: Outro Video (if enabled)                   │       │
│  │ Input 5: Watermark Image (if enabled)               │       │
│  │ Input 6: Background Music (if enabled)              │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                │
│  Step 2: Filter Graph                                          │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ [0:v] → scale, set PTS → [main_v]                  │       │
│  │ [0:a] → volume=0dB → [main_a_orig]                 │       │
│  │ [1:a] → volume normalization → [dub_a]             │       │
│  │ [dub_a][main_a_orig] → amix → [mixed_a]            │       │
│  │ [mixed_a][6:a] → amix → [final_a] (bg music)       │       │
│  │ [main_v][5:v] → overlay (watermark) → [final_v]    │       │
│  │ [final_v] → drawtext/drawsub (subtitles) → [out_v] │       │
│  │ Concat intro + [out_v] + outro → [output]          │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                │
│  Step 3: Encode                                                │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ Video: H.264/H.265 (libx264/libx265 or NVENC)      │       │
│  │ Audio: AAC (aac) at 192kbps                         │       │
│  │ Subtitle: Burn (subtitles filter) or Embed (mov_text)│      │
│  │ Resolution: 1080p/2K/4K (scale if needed)          │       │
│  │ CRF: 18-28 (quality vs size trade-off)              │       │
│  └─────────────────────────────────────────────────────┘       │
└────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow Diagrams

### 4.1 Project Creation Flow

```
User (Frontend)
  │
  ├── POST /api/v1/projects { title, source_lang, target_lang }
  │
  ▼
FastAPI
  │
  ├── Validate input (Pydantic)
  ├── Create project in DB (SQLAlchemy)
  ├── Create empty video record
  ├── Create empty branding_config record
  │
  ▼
Response 201 → { project_id, status: "draft" }
  │
  ▼
Frontend → Navigate to /projects/{id}/workspace
```

### 4.2 Upload + Transcribe Flow

```
User uploads video
  │
  ├── POST /projects/{id}/video/upload (multipart)
  │
  ▼
FastAPI
  │
  ├── Validate file type & size
  ├── Save to filesystem
  ├── Extract metadata (FFprobe)
  ├── Generate thumbnail (FFmpeg seek)
  ├── Update project status → "video_imported"
  │
  ▼
Response 200 → { video_metadata }
  │
  ▼
User clicks "Transcribe"
  │
  ├── POST /projects/{id}/transcribe { model_size: "medium" }
  │
  ▼
FastAPI
  │
  ├── Validate pipeline state (video must exist)
  ├── Dispatch Celery task: stt_task.delay(project_id, model_size)
  ├── Update pipeline_progress.stt → "processing"
  │
  ▼
Response 202 → { task_id }
  │
  ▼
WebSocket → "task.progress" { step: "stt", progress: 45% }
  │
  ▼
User sees progress bar in frontend (real-time)
  │
  ▼
Celery Worker (STT Task)
  │
  ├── Extract audio from video (FFmpeg)
  ├── Load Whisper model
  ├── Run transcription
  ├── Post-process segments
  ├── Write segments to DB (BATCH INSERT)
  ├── Update project status → "transcript_ready"
  ├── Publish WebSocket "task.completed"
  │
  ▼
Frontend → Loads transcript segments via GET /projects/{id}/transcript
```

### 4.3 Full Pipeline Automation (Batch Mode)

```
User adds 3 projects to batch queue
  │
  ├── POST /batch/render { project_ids: [...] }
  │
  ▼
Batch Service
  │
  ├── Create batch record
  ├── For each project:
  │   ├── Check pipeline state
  │   ├── If missing steps → queue them sequentially
  │   └── Queue final render task
  │
  ▼
Celery Workers (Pool)
  │
  ├── Worker 1: STT for Project A
  ├── Worker 2: STT for Project B
  ├── Worker 3: STT for Project C
  │   (Parallel STT processing)
  │
  ├── After STT completed:
  │   ├── Worker 1: Translation for Project A
  │   ├── Worker 2: Translation for Project B
  │   └── Worker 3: Translation for Project C
  │
  ├── After Translation completed:
  │   ├── TTS Workers (parallel segments)
  │   └── Render Workers (GPU-scheduled)
  │
  ▼
All projects completed
  │
  ├── WebSocket "batch.completed" { batch_id, stats }
  └── Frontend shows batch summary
```

---

## 5. Tech Stack Deep Dive

### 5.1 Layer-by-Layer Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER          │ TECHNOLOGY             │ ROLE                      │
├─────────────────────────────────────────────────────────────────────┤
│ Presentation   │ Next.js 14 (App Router)│ SSR, routing, SEO         │
│                │ TailwindCSS            │ Styling, responsive       │
│                │ shadcn/ui              │ Accessible components     │
│                │ TanStack Query         │ Server state, caching     │
│                │ Zustand                │ Client UI state           │
│                │ Axios                  │ HTTP client               │
│                │ WebSocket (native)     │ Real-time updates         │
├─────────────────────────────────────────────────────────────────────┤
│ API Gateway    │ FastAPI (Python 3.11+) │ REST + WebSocket          │
│                │ Pydantic v2            │ Request/response schema   │
│                │ SQLAlchemy 2.0 (async) │ ORM                       │
│                │ Alembic                │ Migration management      │
│                │ Uvicorn + Gunicorn     │ ASGI server               │
├─────────────────────────────────────────────────────────────────────┤
│ Task Queue     │ Celery                 │ Distributed task queue    │
│                │ Redis                  │ Broker + result backend   │
│                │ Flower                 │ Task monitoring (dev)     │
├─────────────────────────────────────────────────────────────────────┤
│ AI/ML          │ Whisper (faster-whisper)│ Speech-to-text           │
│                │ Ollama / llama.cpp     │ Local LLM inference       │
│                │ Coqui TTS / Piper TTS  │ Text-to-speech            │
│                │ Edge-TTS               │ Free online TTS fallback  │
│                │ CUDA / DirectML        │ GPU acceleration          │
├─────────────────────────────────────────────────────────────────────┤
│ Video          │ FFmpeg (ffmpeg-python) │ Video/audio processing    │
│                │ pysubs2                │ Subtitle generation       │
│                │ Pillow (PIL)           │ Thumbnail, image overlay  │
├─────────────────────────────────────────────────────────────────────┤
│ Storage        │ PostgreSQL 15+         │ Metadata database         │
│                │ File System (local)     │ Video/audio/assets       │
│                │ Redis 7+               │ Cache + Queue + Session   │
├─────────────────────────────────────────────────────────────────────┤
│ Infrastructure │ Docker + Compose       │ Container orchestration   │
│                │ GitHub Actions         │ CI/CD                     │
│                │ Nginx (optional)       │ Reverse proxy             │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Key Library Dependencies

**Python (Backend):**
```
fastapi>=0.109.0
uvicorn[standard]>=0.25.0
sqlalchemy[asyncio]>=2.0.25
asyncpg>=0.29.0
alembic>=1.13.0
celery>=5.3.4
redis[hiredis]>=5.0.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-multipart>=0.0.6
httpx>=0.26.0
ffmpeg-python>=0.2.0
Pillow>=10.1.0
pysubs2>=1.7.1
openai-whisper>=20231117  # or faster-whisper>=1.0.0
ollama>=0.1.0
websockets>=12.0
python-jose[cryptography]>=3.3.0  # JWT auth
```

**TypeScript/JavaScript (Frontend):**
```json
{
  "next": "^14.1.0",
  "react": "^18.2.0",
  "tailwindcss": "^3.4.0",
  "@radix-ui/react-*": "^1.0.0",
  "@tanstack/react-query": "^5.17.0",
  "zustand": "^4.4.0",
  "axios": "^1.6.0",
  "lucide-react": "^0.300.0",
  "react-hook-form": "^7.49.0",
  "zod": "^3.22.0",
  "react-dropzone": "^14.2.0"
}
```

---

## 6. File System Structure

### 6.1 Data Directory Layout

```
/data/
├── projects/                          # All project data
│   ├── {project_uuid}/
│   │   ├── video/
│   │   │   ├── original.mp4           # Uploaded video
│   │   │   ├── audio.wav             # Extracted audio for STT
│   │   │   └── thumbnail.jpg         # Auto-generated thumbnail
│   │   ├── audio/
│   │   │   ├── segments/             # Per-segment TTS output
│   │   │   │   ├── seg_000.wav
│   │   │   │   ├── seg_001.wav
│   │   │   │   └── ...
│   │   │   └── full_dub.wav          # Stitched final audio
│   │   ├── branding/
│   │   │   ├── logo.png              # User-uploaded logo
│   │   │   ├── bg_music.mp3          # Background music
│   │   │   └── watermark.png         # Watermark image
│   │   ├── output/
│   │   │   ├── final.mp4             # Rendered output
│   │   │   └── metadata.json         # YouTube metadata
│   │   └── subtitles/
│   │       ├── output.srt
│   │       ├── output.ass
│   │       └── output.vtt
│   └── ... (more projects)
│
├── templates/                         # Branding templates
│   ├── intro/                         # Intro video templates
│   └── outro/                         # Outro video templates
│
├── voice-profiles/                    # Voice profile samples
│   └── previews/                      # Preview audio clips
│
├── exports/                           # Exported metadata files
│   └── {project_uuid}/
│       └── metadata.json
│
└── cache/                             # Temporary files
    ├── stt/                           # Whisper model cache
    └── thumbnails/                    # Generated thumbnails cache
```

---

## 7. Error Handling Strategy

### 7.1 Error Hierarchy

```
AppException (base)
├── NotFoundException
│   ├── ProjectNotFoundException
│   ├── VideoNotFoundException
│   ├── TranscriptNotFoundException
│   └── VoiceProfileNotFoundException
├── ValidationException
│   ├── InvalidFileFormatException
│   ├── FileTooLargeException
│   └── PipelineStepMissingException
├── TaskException
│   ├── TaskInProgressException
│   ├── EngineUnavailableException
│   └── GPUNotAvailableException
└── InternalException
    └── DatabaseException
```

### 7.2 Graceful Degradation Matrix

| Component | Failure Mode | Fallback Strategy |
|-----------|-------------|-------------------|
| GPU (STT) | CUDA out of memory | Fallback to CPU with model size downgrade (large → medium → small) |
| Local LLM | Ollama not running | Prompt user to start Ollama OR switch to API engine |
| TTS (Coqui) | Model load failed | Fallback to Edge-TTS (online) or Piper TTS |
| FFmpeg | Codec not found | Fallback to software encoding (libx264 instead of NVENC) |
| Redis | Connection lost | Celery broker fallback to filesystem transport |
| PostgreSQL | Connection lost | Queue tasks, retry with exponential backoff |
| Disk space | No space left | Stop processing, alert user, suggest cleanup |

### 7.3 Checkpoint & Resume

```
Project Processing State
       │
       ▼
┌─────────────────────┐
│  Checkpoint Manager │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────┐ ┌────────────┐
│STT     │ │Translation  │
│Done ✔  │ │In Progress  │
│Segments│ │(seg 15/45) │
│saved   │ │saved to DB  │
└────────┘ └────────────┘
    │             │
    └──────┬──────┘
           │
           ▼
    System Crash!
           │
           ▼
    On Restart:
    ├── Detect incomplete pipeline
    ├── Resume from last checkpoint
    │   └── Translation: continue from segment 15
    └── Skip already completed steps
```

---

## 8. Security Architecture

### 8.1 Authentication & Authorization

```
┌──────────────┐
│   Frontend    │
│  (Next.js)    │
└──────┬───────┘
       │
       │ 1. Login → POST /auth/login { email, password }
       ▼
┌──────────────┐
│   FastAPI     │
│  ┌──────────┐│
│  │ JWT Issue││ ← Access Token (15min) + Refresh Token (7d)
│  └──────────┘│
└──────┬───────┘
       │
       │ 2. Response → { access_token, refresh_token }
       ▼
┌──────────────┐
│   Frontend    │
│  ┌──────────┐│
│  │ LocalStorage│ ← Store tokens
│  └──────────┘│
└──────┬───────┘
       │
       │ 3. Subsequent requests
       │    Header: Authorization: Bearer <access_token>
       ▼
┌──────────────┐
│   FastAPI     │
│  ┌──────────┐│
│  │ JWT Verify│ ← Verify signature + expiration
│  └──────────┘│
└──────────────┘
```

### 8.2 Data Isolation

- **Project-level isolation**: All queries include `user_id = current_user.id`
- **File-level isolation**: File paths include `project_uuid` to prevent directory traversal
- **API-level isolation**: All endpoints check project ownership before returning data

---

## 9. Monitoring & Observability

### 9.1 Logging Strategy

```python
# Structured JSON logging format
{
  "timestamp": "2026-01-01T12:00:00Z",
  "level": "INFO" | "WARN" | "ERROR",
  "service": "stt-worker",
  "project_id": "uuid",
  "task_id": "uuid",
  "message": "Transcription completed",
  "metrics": {
    "duration_seconds": 120.5,
    "segments": 45,
    "model": "medium",
    "gpu_used": true
  },
  "trace_id": "abc123"
}
```

### 9.2 Key Metrics to Track

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| Task duration | Celery | > 2x expected duration |
| Task failure rate | Celery | > 5% in 1 hour |
| GPU memory usage | nvidia-smi | > 90% |
| Queue depth | Redis | > 100 pending tasks |
| API response time | FastAPI | > 5 seconds (p99) |
| Disk usage | System | > 85% |

---

## 10. Deployment Architecture

### 10.1 Docker Compose Services

```yaml
version: "3.8"

services:
  # ─── Frontend ──────────────────────────────
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on: [backend]

  # ─── Backend ───────────────────────────────
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@postgres:5432/videostudio
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - /data/projects:/data/projects
      - /data/templates:/data/templates
      - /data/voice-profiles:/data/voice-profiles
    depends_on: [postgres, redis]
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              capabilities: [gpu]  # If GPU available

  # ─── Queue ─────────────────────────────────
  celery-worker:
    build: ./backend
    command: celery -A app.tasks.celery_app worker --loglevel=info --concurrency=4
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@postgres:5432/videostudio
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - /data/projects:/data/projects
    depends_on: [postgres, redis]
    deploy:
      replicas: 2
      resources:
        reservations:
          devices:
            - driver: nvidia
              capabilities: [gpu]

  # ─── Storage ───────────────────────────────
  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=videostudio
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports: ["5432:5432"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

### 10.2 Scaling Considerations

| Scenario | Scale Strategy |
|----------|---------------|
| More users | Increase Celery worker replicas |
| More GPUs | Add GPU worker instances, each pinned to specific GPU |
| More storage | Mount NAS/object storage, symlink to /data |
| More concurrent renders | Increase worker count + add GPU scheduling |
| High DB load | Add PostgreSQL read replicas, connection pooling (PgBouncer) |