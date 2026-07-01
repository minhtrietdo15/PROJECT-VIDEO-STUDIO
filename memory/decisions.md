# Technology Decisions — Video Localization AI Studio

> **Version:** 1.0
> **Author:** AI Architect
> **Last Updated:** 2026-07-01

---

## Decision Log

| # | Decision | Status | Date | Context |
|---|----------|--------|------|---------|
| 001 | FastAPI làm backend framework | ✅ Accepted | 2026-07-01 | Performance & async support |
| 002 | Next.js làm frontend framework | ✅ Accepted | 2026-07-01 | SSR, routing, ecosystem |
| 003 | PostgreSQL làm database chính | ✅ Accepted | 2026-07-01 | Production-ready, ACID |
| 004 | Celery + Redis làm task queue | ✅ Accepted | 2026-07-01 | Xử lý tác vụ nặng async |
| 005 | Whisper cho Speech-to-Text | ✅ Accepted | 2026-07-01 | Local processing, accuracy cao |
| 006 | Local LLM (Ollama) cho Translation | ✅ Accepted | 2026-07-01 | Privacy, flexible, free |
| 007 | Coqui TTS cho Voice Dubbing | ✅ Accepted | 2026-07-01 | Hỗ trợ tiếng Việt, open-source |
| 008 | FFmpeg cho Video Processing | ✅ Accepted | 2026-07-01 | Standard công nghiệp |
| 009 | SQLAlchemy 2.0 async làm ORM | ✅ Accepted | 2026-07-01 | Async-native, type-safe |
| 010 | pysubs2 cho Subtitle Generation | ✅ Accepted | 2026-07-01 | Full format support |
| 011 | TailwindCSS + shadcn/ui cho UI | ✅ Accepted | 2026-07-01 | Responsive, accessible |
| 012 | Docker Compose cho deployment | ✅ Accepted | 2026-07-01 | Portable, reproducible |
| 013 | TanStack Query cho client state | ✅ Accepted | 2026-07-01 | Caching, async state |
| 014 | Zustand cho UI state | ✅ Accepted | 2026-07-01 | Lightweight, simple |
| 015 | JWT cho authentication | ✅ Accepted | 2026-07-01 | Stateless, scalable |

---

## D001: Chọn FastAPI cho Backend

### Context
Cần một Python backend framework hỗ trợ async/await, type hints, và performance cao để xử lý nhiều request đồng thời từ frontend + WebSocket real-time cho progress tracking.

### Options Considered

| Option | Ưu điểm | Nhược điểm |
|--------|---------|------------|
| **FastAPI** ✅ | Async native, Pydantic validation, auto docs, WebSocket support, OpenAPI spec, performance top-tier | Hệ sinh thái nhỏ hơn Django |
| **Django + DRF** | Mature, many plugins, ORM mạnh, admin panel | Sync by default (hacky async), heavy, chậm hơn FastAPI |
| **Flask** | Lightweight, flexible | Không async, thiếu built-in validation, không auto docs |
| **Starlette** | Low-level, siêu nhanh | Thiếu tính năng high-level, phải tự xây dựng nhiều |

### Decision
**FastAPI** — vì:
1. **Async-native**: Quan trọng cho I/O-bound tasks như file upload/download, WebSocket, database queries
2. **Pydantic validation**: Giảm boilerplate, type-safe request/response
3. **Tự động OpenAPI/Swagger docs**: Frontend team có thể xem và test API ngay
4. **WebSocket support built-in**: Cần thiết cho real-time progress updates
5. **Performance**: Tốt nhất trong các Python web frameworks (ngang với Node.js/Go)
6. **Dependency Injection**: Clean, testable code

### Consequences
- Phải tự xây dựng authentication, admin panel (không có sẵn như Django)
- Hệ sinh thái package nhỏ hơn, cần tự integrate nhiều thứ
- **Positive**: Performance cao, code sạch, developer experience tốt

---

## D002: Chọn Next.js cho Frontend

### Context
Cần một React framework hỗ trợ SSR (SEO cho landing page), routing mạnh mẽ, và hệ sinh thái phong phú để xây dựng UI phức tạp với nhiều workspace state.

### Options Considered

| Option | Ưu điểm | Nhược điểm |
|--------|---------|------------|
| **Next.js 14** ✅ | App Router, SSR/SSG, React Server Components, file-based routing, large ecosystem | Heavier than Vite, more boilerplate |
| **Vite + React** | Fast dev server, lightweight, flexible | Không SSR, phải tự setup routing |
| **Remix** | Nested routes, forms, excellent data loading | Nhỏ hơn, ít resources |

### Decision
**Next.js 14** — vì:
1. **App Router**: Server Components, nested layouts, loading states — phù hợp với project workspace có tabs/steps
2. **SSR cho landing pages**: SEO cho product website
3. **File-based routing**: Dễ maintain với cấu trúc projects/[id]/transcript...
4. **Large ecosystem**: shadcn/ui, TanStack Query, etc. đều có sẵn
5. **Image Optimization**: next/image cho thumbnails và media

### Consequences
- Phải deploy như Node.js server (không static file đơn thuần)
- Server Components giới hạn client-side interactivity
- **Positive**: SEO tốt, routing gọn gàng, cộng đồng lớn

---

## D003: Chọn PostgreSQL cho Database

### Context
Cần một relational database cho metadata, users, projects, segments, tasks. Yêu cầu ACID, JSON support, và production-ready.

### Options Considered

| Option | Ưu điểm | Nhược điểm |
|--------|---------|------------|
| **PostgreSQL 16** ✅ | ACID, JSONB, full-text search, mature, replication, partitioning | Heavy hơn SQLite, cần server riêng |
| **SQLite** | Zero-config, file-based, đủ cho single-user local use | Không concurrent writes, limited JSON, no partitioning |
| **MongoDB** | Schema-less, flexible, horizontal scaling | No ACID transactions (multi-doc), không phù hợp relational data |
| **MySQL** | Popular, mature | JSON support kém hơn PostgreSQL, less advanced features |

### Decision
**PostgreSQL** làm database chính, với SQLite làm fallback cho local development:
1. **JSONB**: Lưu segments, style configs, settings — query được bên trong JSON
2. **ACID transactions**: Quan trọng cho pipeline state consistency
3. **Full-text search**: Cho search projects/titles
4. **Partitioning**: Cho scaling lên 100K+ projects
5. **Mature ORM support**: SQLAlchemy 2.0 async hoạt động tốt

### Consequences
- Phải chạy PostgreSQL server (Docker container)
- Setup phức tạp hơn SQLite
- **Positive**: Reliable, scalable, feature-rich

---

## D004: Chọn Celery + Redis cho Task Queue

### Context
Cần xử lý các tác vụ nặng không đồng bộ: STT (Whisper), Translation (LLM), TTS, Video Rendering (FFmpeg). Các tác vụ này có thể chạy từ vài phút đến hàng giờ.

### Options Considered

| Option | Ưu điểm | Nhược điểm |
|--------|---------|------------|
| **Celery + Redis** ✅ | Mature, distributed, task scheduling, retry, rate limiting, monitoring (Flower) | Complex config, Redis dependency, heavy |
| **RQ (Redis Queue)** | Simple, lightweight, Pythonic | Ít features hơn (no scheduling, no complex routing) |
| **Arq** | Modern async, Redis-based | Newer, smaller community |
| **Background tasks (FastAPI BackgroundTasks)** | Simple, built-in | Không persistent, không retry, không distributed, mất task khi crash |

### Decision
**Celery + Redis** — vì:
1. **Distributed workers**: Có thể scale workers riêng cho STT, TTS, Render
2. **Task retry với backoff**: Xử lý transient failures (GPU OOM, network timeout)
3. **Task scheduling**: Batch processing scheduling
4. **Progress reporting**: Cập nhật progress lên Redis → WebSocket
5. **Task result backend**: Lưu kết quả để frontend poll
6. **Mature ecosystem**: Flower cho monitoring, Celery beat cho scheduled tasks

### Consequences
- Phải chạy Redis riêng (thêm service trong Docker)
- Cấu hình phức tạp hơn RQ
- **Positive**: Production-ready, scalable, reliable

---

## D005: Chọn Whisper cho Speech-to-Text

### Context
Core feature của sản phẩm là tự động nhận diện giọng nói từ video. Cần model chạy local (privacy), accuracy cao, hỗ trợ nhiều ngôn ngữ, và có word-level timestamps.

### Options Considered

| Option | Ưu điểm | Nhược điểm |
|--------|---------|------------|
| **OpenAI Whisper** ✅ | Accuracy tốt nhất, word-level timestamps, multi-language, local, open-source | Nặng (large model ~3GB), chậm trên CPU |
| **faster-whisper** | Nhanh hơn Whisper gốc 4x, ít RAM hơn | Accuracy slightly lower |
| **Google Speech-to-Text API** | Cloud, latency thấp, accuracy cao | Trả phí, cần Internet, gửi data ra ngoài |
| **Vosk** | Nhẹ, real-time | Accuracy thấp hơn, ít ngôn ngữ |

### Decision
**Whisper (faster-whisper)** — vì:
1. **Local processing**: Không gửi data ra ngoài — privacy-first
2. **Word-level timestamps**: Cần cho subtitle editor đồng bộ
3. **Multi-language support**: 99+ languages, auto-detection
4. **Model size flexibility**: tiny (39MB) → large (3GB) tùy hardware
5. **faster-whisper optimization**: 4x nhanh hơn, phù hợp production
6. **Miễn phí**: Không API costs

### Consequences
- Yêu cầu GPU để xử lý nhanh (CPU: 1 phút video = 2-5 phút xử lý)
- Disk space cho models (large = 3GB)
- **Positive**: Free, private, accurate, flexible

---

## D006: Chọn Local LLM (Ollama) cho Translation

### Context
Cần dịch transcript từ ngôn ngữ gốc sang tiếng Việt. Yêu cầu: dịch tự nhiên, giữ ngữ cảnh, không dịch tên riêng/thuật ngữ, hỗ trợ nhiều style.

### Options Considered

| Option | Ưu điểm | Nhược điểm |
|--------|---------|------------|
| **Local LLM (Ollama)** ✅ | Free, private, flexible prompting, có thể fine-tune | Chậm trên CPU, cần GPU cho tốc độ tốt |
| **OpenAI GPT-4 API** | Chất lượng tốt nhất, nhanh | Trả phí ($0.01-0.03/request), cần API key |
| **Google Gemini API** | Miễn phí quota, chất lượng tốt | Cần Internet, API rate limits |
| **Claude API** | Xuất sắc cho translation | Trả phí, ít flexibility |
| **Argos Translate** | Local, nhẹ | Chất lượng thấp, không context-aware |

### Decision
**Local LLM (Ollama)** làm mặc định, với API wrapper cho các engine khác (Strategy pattern):
1. **Privacy**: Dữ liệu không rời khỏi máy
2. **Free**: Không API costs khi dùng local
3. **Flexible prompting**: Có thể tùy chỉnh style, context rules
4. **Model options**: Llama 3, Mistral, Qwen — models hỗ trợ tiếng Việt tốt
5. **Strategy pattern**: Cho phép user chọn engine (local/API) tùy nhu cầu quality vs speed

### Consequences
- Cần Ollama server chạy local (cài đặt thêm)
- Quality thấp hơn GPT-4 trên các đoạn phức tạp
- **Positive**: Free, private, flexible

---

## D007: Chọn Coqui TTS cho Voice Dubbing

### Context
Cần sinh giọng đọc tiếng Việt tự nhiên. Yêu cầu: hỗ trợ tiếng Việt tốt, nhiều giọng (nam/nữ/trẻ/trầm), có thể clone giọng.

### Options Considered

| Option | Ưu điểm | Nhược điểm |
|--------|---------|------------|
| **Coqui TTS** ✅ | Open-source, hỗ trợ tiếng Việt, voice cloning, fine-tuning | Cần GPU cho inference nhanh, setup phức tạp |
| **Piper TTS** | Nhẹ, nhanh trên CPU, nhiều voices | Chất lượng thấp hơn Coqui, ít tiếng Việt |
| **Edge-TTS** | Free, quality tốt, nhiều voices | Cần Internet, Microsoft service |
| **Google Cloud TTS** | Chất lượng cao nhất | Trả phí, cần Internet |
| **Zalo AI TTS** | Tiếng Việt tốt nhất | API của Zalo, cần Internet |

### Decision
**Coqui TTS** làm chính, với Piper TTS và Edge-TTS làm fallback:
1. **Open-source**: Có thể chạy local, tùy biến
2. **Vietnamese models**: Cộng đồng đã train models cho tiếng Việt
3. **Voice cloning**: Tính năng quan trọng cho v2.0
4. **Fine-tuning**: Có thể cải thiện chất lượng cho use case cụ thể
5. **Multi-engine fallback**: Nếu Coqui không hoạt động, fallback sang Piper (local) hoặc Edge-TTS (online)

### Consequences
- Coqui TTS setup phức tạp, cần Python environment riêng
- Quality tiếng Việt chưa bằng các API thương mại
- **Positive**: Free, local, có voice cloning

---

## D008: Chọn FFmpeg cho Video Processing

### Context
Core engine cho xử lý video: cắt, ghép, thay audio, gắn subtitle, encode/decode, scale resolution. Cần công cụ mạnh mẽ, đã được kiểm chứng.

### Options Considered

| Option | Ưu điểm | Nhược điểm |
|--------|---------|------------|
| **FFmpeg** ✅ | Standard công nghiệp, mọi format, GPU acceleration, filter graph phức tạp | CLI-based, cần wrapper |
| **MoviePy** | Pythonic, dễ dùng | Chậm, không GPU, limited formats, không production-ready |
| **OpenCV** | Computer vision features, real-time | Không phải video editor, không codec support đầy đủ |
| **GStreamer** | Pipeline-based, mạnh mẽ | Complex, ít tài liệu Python |

### Decision
**FFmpeg** (qua `ffmpeg-python` wrapper):
1. **Standard công nghiệp**: Được dùng bởi YouTube, Netflix, Twitch
2. **GPU acceleration**: CUDA (NVIDIA), VAAPI (Intel), VideoToolbox (Apple)
3. **Filter graph**: Có thể xây dựng pipeline phức tạp (concat, overlay, amix, drawtext)
4. **Mọi format**: Input/output format không giới hạn
5. **Python wrapper**: `ffmpeg-python` cung cấp API Pythonic, dễ maintain

### Consequences
- Phải cài FFmpeg binary trên hệ thống (Docker image có sẵn)
- Build command phức tạp cho filter graphs
- **Positive**: Mạnh mẽ, linh hoạt, production-proven

---

## D009: Chọn SQLAlchemy 2.0 Async làm ORM

### Context
Cần ORM hỗ trợ async PostgreSQL driver (asyncpg) để không block event loop khi query database. Yêu cầu type-safe, migration support.

### Decision
**SQLAlchemy 2.0** với async mode — vì:
1. **Async-native**: `selectinload`, `await session.execute()` — không block
2. **Type-safe**: Với Pydantic schemas ở service layer
3. **Alembic integration**: Migration workflow trưởng thành
4. **Phổ biến**: Tài liệu phong phú, cộng đồng lớn
5. **Declarative models**: Clean, Pythonic

### Alternatives Rejected
- **Tortoise ORM**: Pythonic, async-native nhưng ít mature
- **SQLModel**: Mới, ít tính năng, mixing Pydantic + SQLAlchemy gây confusion

---

## D010: Chọn pysubs2 cho Subtitle Generation

### Context
Cần thư viện để tạo, parse, và chuyển đổi giữa các format subtitle (SRT, ASS, VTT).

### Decision
**pysubs2** — vì:
1. **Full format support**: SRT, ASS, VTT, SSA
2. **Pythonic API**: Dễ dùng, clean
3. **Style support**: Đặc biệt quan trọng cho ASS format (styling, position, animation)
4. **Time operations**: Shift, scale, sort segments

---

## D011: Chọn TailwindCSS + shadcn/ui cho UI

### Context
Cần UI framework responsive, accessible, dễ tùy biến cho các component phức tạp (timeline editor, video player, chat interface).

### Decision
**TailwindCSS** + **shadcn/ui** — vì:
1. **TailwindCSS**: Utility-first, responsive design nhanh, bundle nhỏ (purge unused)
2. **shadcn/ui**: Copy-paste components, fully customizable, Radix UI primitives (accessible)
3. **Dark mode**: Built-in support
4. **No CSS-in-JS**: Runtime cost = 0

---

## D012: Chọn Docker Compose cho Deployment

### Context
Cần môi trường reproducible cho development và production. 5 services (frontend, backend, postgres, redis, celery-worker).

### Decision
**Docker Compose** — vì:
1. **Multi-service**: 5 services trong 1 file
2. **Volume mounts**: Persist project data
3. **GPU passthrough**: NVIDIA container toolkit
4. **Network isolation**: Services communicate via internal network
5. **Environment variables**: Config management dễ dàng

---

## D013: Chọn TanStack Query cho Client State

### Context
Cần quản lý server state (API calls, caching, refetching, pagination) cho dashboard và project workspace.

### Decision
**TanStack Query (React Query)** — vì:
1. **Auto caching**: Cache API responses, invalidate on mutations
2. **Background refetching**: Luôn có data mới
3. **Pagination + infinite query**: Cho transcript segments
4. **Optimistic updates**: Cho translation edits, segment splits
5. **Loading/error states**: Built-in

---

## D014: Chọn Zustand cho UI State

### Context
Cần lightweight state management cho UI state (sidebar open/close, active tab, selected segment).

### Decision
**Zustand** — vì:
1. **Lightweight**: 1KB, không boilerplate
2. **Simple API**: `create((set) => ({...}))`
3. **No providers**: Không cần wrap app
4. **Persist middleware**: Cho user preferences
5. **Devtools**: Redux DevTools integration

---

## D015: Chọn JWT cho Authentication

### Context
Cần authentication stateless, scalable cho API. Frontend cần lưu token và gửi trong mỗi request.

### Decision
**JWT (JSON Web Tokens)** — vì:
1. **Stateless**: Server không cần lưu session, dễ scale
2. **Self-contained**: User info, roles, expiration trong token
3. **Access + Refresh tokens**: Access token ngắn hạn (15 phút), refresh token dài hạn (7 ngày)
4. **Thư viện**: `python-jose` cho backend

### Security Considerations
- Token lưu trong localStorage (cần HTTPS)
- CSRF protection cho browser
- Token rotation strategy

---

## Summary of Architectural Principles

| Principle | Description |
|-----------|-------------|
| **Local-first** | Ưu tiên chạy local, không phụ thuộc Internet |
| **Modular** | Mỗi module (STT, Translation, TTS, Render) độc lập, dễ thay thế |
| **Graceful Degradation** | Fallback khi component fail (GPU→CPU, local→API) |
| **Async by default** | Tận dụng async/await cho I/O, Celery cho CPU-bound |
| **Type-safe** | Pydantic cho API, TypeScript cho frontend |
| **Open-source** | Sử dụng open-source tools khi có thể |
| **Privacy-first** | Dữ liệu người dùng không rời khỏi máy (trừ khi họ chọn API) |