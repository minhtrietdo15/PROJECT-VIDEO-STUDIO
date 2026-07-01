# REST API Contract — Video Localization AI Studio

> **Version:** 1.0
> **Base URL:** `http://localhost:8000/api/v1`
> **Protocol:** HTTP/1.1 + WebSocket (for real-time updates)
> **Auth:** Bearer Token (JWT) — future implementation

---

## 1. API Conventions

### 1.1 Standard Response Envelope

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "PROJECT_NOT_FOUND",
    "message": "Project with ID xyz not found",
    "details": { "project_id": "xyz" }
  },
  "meta": null
}
```

### 1.2 HTTP Status Codes

| Code | Meaning | Used When |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (resource created) |
| 202 | Accepted | Async task accepted (queued) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error, malformed input |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Duplicate resource, state conflict |
| 422 | Unprocessable Entity | Business rule violation |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Model loading, GPU not ready |

### 1.3 Pagination

All list endpoints support:
- `?page=1&per_page=20` (default: page=1, per_page=20, max: 100)
- Response includes `meta` with pagination info
- Sort: `?sort=created_at&order=desc`

### 1.4 WebSocket Events

Endpoint: `ws://localhost:8000/ws/projects/{project_id}`

| Event | Direction | Payload |
|-------|-----------|---------|
| `task.progress` | Server → Client | `{ task_id, step, progress_percent, eta }` |
| `task.completed` | Server → Client | `{ task_id, step, result }` |
| `task.failed` | Server → Client | `{ task_id, step, error }` |
| `transcription.word` | Server → Client | `{ segment_index, word, start_ms, end_ms }` |
| `render.frame` | Server → Client | `{ frame_number, total_frames, percent }` |

---

## 2. Endpoints

### 2.1 Projects

#### `GET /projects` — List all projects

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| status | string | — | Filter by status (`draft`, `completed`, etc.) |
| search | string | — | Search in title |
| sort | string | `created_at` | Sort field |
| order | string | `desc` | `asc` or `desc` |

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "title": "My Video Project",
      "source_language": "en",
      "target_language": "vi",
      "status": "transcript_ready",
      "thumbnail_url": "/api/v1/files/thumbnails/abc.jpg",
      "total_duration_ms": 600000,
      "pipeline_progress": {
        "stt": "completed",
        "translation": "pending",
        "tts": "pending",
        "subtitle": "pending",
        "render": "pending"
      },
      "created_at": "2026-01-01T12:00:00Z",
      "updated_at": "2026-01-01T12:05:00Z"
    }
  ],
  "meta": { "page": 1, "per_page": 20, "total": 5, "total_pages": 1 }
}
```

---

#### `POST /projects` — Create a new project

**Request Body:**
```json
{
  "title": "My Video Project",
  "source_language": "en",
  "target_language": "vi"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "My Video Project",
    "source_language": "en",
    "target_language": "vi",
    "status": "draft",
    "pipeline_progress": {
      "stt": "pending",
      "translation": "pending",
      "tts": "pending",
      "subtitle": "pending",
      "render": "pending"
    },
    "created_at": "2026-01-01T12:00:00Z",
    "updated_at": "2026-01-01T12:00:00Z"
  }
}
```

---

#### `GET /projects/{project_id}` — Get project details

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "My Video Project",
    "source_language": "en",
    "target_language": "vi",
    "status": "transcript_ready",
    "thumbnail_url": "/api/v1/files/thumbnails/abc.jpg",
    "total_duration_ms": 600000,
    "pipeline_progress": {
      "stt": "completed",
      "translation": "pending",
      "tts": "pending",
      "subtitle": "pending",
      "render": "pending"
    },
    "video": { /* see 2.2 */ },
    "created_at": "2026-01-01T12:00:00Z",
    "updated_at": "2026-01-01T12:05:00Z"
  }
}
```

---

#### `PATCH /projects/{project_id}` — Update project

**Request Body:** (partial update)
```json
{
  "title": "Updated Title",
  "source_language": "fr",
  "target_language": "vi"
}
```

**Response (200):** Same as GET

---

#### `DELETE /projects/{project_id}` — Delete project

**Response (204):** No content

---

### 2.2 Video Management

#### `POST /projects/{project_id}/video/upload` — Upload video

**Content-Type:** `multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| file | File | Video file (MP4, MOV, MKV, AVI, WebM) |

**Supported chunked upload (for files > 100MB):**
1. `POST /projects/{project_id}/video/upload/init` — Initiate upload, get `upload_id`
2. `PATCH /projects/{project_id}/video/upload/{upload_id}` — Upload chunk (with `Content-Range` header)
3. `POST /projects/{project_id}/video/upload/{upload_id}/complete` — Finalize

**Simple Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "filename": "intro.mp4",
    "file_path": "/data/projects/uuid/video.mp4",
    "file_size_bytes": 524288000,
    "duration_ms": 600000,
    "width": 1920,
    "height": 1080,
    "fps": 30.0,
    "codec": "h264",
    "audio_codec": "aac",
    "audio_sample_rate": 44100,
    "thumbnail_url": "/api/v1/files/thumbnails/abc.jpg",
    "source_type": "upload",
    "source_url": null
  }
}
```

---

#### `POST /projects/{project_id}/video/import-url` — Import from URL

**Request Body:**
```json
{
  "url": "https://example.com/video.mp4"
}
```

**Response (202) — Async:**
```json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "status": "downloading",
    "message": "Download started"
  }
}
```

---

#### `GET /projects/{project_id}/video` — Get video metadata

**Response (200):** Same video object as upload response

---

### 2.3 Speech-to-Text (Transcript)

#### `GET /projects/{project_id}/transcript` — Get transcript (all segments)

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | int | 1 | Page number |
| per_page | int | 50 | Segments per page |

**Response (200):**
```json
{
  "success": true,
  "data": {
    "project_id": "uuid",
    "language": "en",
    "segments": [
      {
        "id": "uuid",
        "segment_index": 0,
        "start_ms": 0,
        "end_ms": 3200,
        "text": "Hello and welcome to today's video",
        "confidence": 0.97,
        "speaker_label": null,
        "words": [
          { "word": "Hello", "start_ms": 0, "end_ms": 500, "confidence": 0.99 },
          { "word": "and", "start_ms": 500, "end_ms": 700, "confidence": 0.98 }
        ]
      }
    ],
    "total_segments": 45
  }
}
```

---

#### `POST /projects/{project_id}/transcribe` — Start transcription

**Request Body:**
```json
{
  "model_size": "medium",
  "language": null,
  "word_timestamps": true
}
```

| Field | Type | Default | Options |
|-------|------|---------|---------|
| model_size | string | `medium` | `tiny`, `base`, `small`, `medium`, `large` |
| language | string | `null` (auto) | ISO 639-1 code or null for auto-detect |
| word_timestamps | boolean | `true` | Enable word-level timestamps |

**Response (202):**
```json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "status": "queued",
    "estimated_duration_seconds": 120
  }
}
```

---

#### `PATCH /projects/{project_id}/transcript/segments/{segment_index}` — Edit a transcript segment

**Request Body:**
```json
{
  "text": "Hello and welcome to my channel",
  "start_ms": 0,
  "end_ms": 3500
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "segment_index": 0,
    "text": "Hello and welcome to my channel",
    "start_ms": 0,
    "end_ms": 3500
  }
}
```

---

#### `POST /projects/{project_id}/transcript/segments/{segment_index}/split` — Split a segment

**Request Body:**
```json
{
  "split_at_ms": 1500
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "segments": [
      { "segment_index": 0, "text": "Hello and", "start_ms": 0, "end_ms": 1500 },
      { "segment_index": 1, "text": "welcome to today's video", "start_ms": 1500, "end_ms": 3200 }
    ]
  }
}
```

---

#### `POST /projects/{project_id}/transcript/segments/{segment_index}/merge` — Merge with next segment

**Response (200):**
```json
{
  "success": true,
  "data": {
    "segment_index": 0,
    "text": "Hello and welcome to today's video",
    "start_ms": 0,
    "end_ms": 5500
  }
}
```

---

### 2.4 Translation

#### `GET /projects/{project_id}/translations` — Get translations

**Response (200):**
```json
{
  "success": true,
  "data": {
    "project_id": "uuid",
    "style": "natural",
    "engine_used": "local_llm",
    "segments": [
      {
        "id": "uuid",
        "segment_index": 0,
        "source_text": "Hello and welcome to today's video",
        "translated_text": "Xin chào và chào mừng đến với video hôm nay",
        "confidence": null,
        "is_edited": false,
        "style": "natural"
      }
    ],
    "total_segments": 45
  }
}
```

---

#### `POST /projects/{project_id}/translate` — Start translation

**Request Body:**
```json
{
  "engine": "local_llm",
  "style": "natural",
  "api_key": null
}
```

| Field | Type | Default | Options |
|-------|------|---------|---------|
| engine | string | `local_llm` | `local_llm`, `openai`, `gemini`, `claude` |
| style | string | `neutral` | `neutral`, `natural`, `short_video`, `educational` |
| api_key | string | `null` | Required if engine is API-based |

**Response (202):**
```json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "status": "queued",
    "total_segments": 45
  }
}
```

---

#### `PATCH /projects/{project_id}/translations/segments/{segment_index}` — Edit a translation

**Request Body:**
```json
{
  "translated_text": "Xin chào mọi người, chào mừng đến với video hôm nay",
  "style": "natural"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "segment_index": 0,
    "source_text": "Hello and welcome to today's video",
    "translated_text": "Xin chào mọi người, chào mừng đến với video hôm nay",
    "is_edited": true
  }
}
```

---

#### `POST /projects/{project_id}/translations/segments/{segment_index}/retranslate` — Re-translate single segment

**Request Body:**
```json
{
  "engine": "openai",
  "style": "educational"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "segment_index": 0,
    "translated_text": "Xin chào và chào mừng các bạn đến với video ngày hôm nay",
    "engine_used": "openai",
    "style": "educational"
  }
}
```

---

### 2.5 Voice Dubbing (TTS)

#### `GET /voice-profiles` — List available voices

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "Giọng Nam trầm",
      "gender": "male",
      "style": "deep",
      "engine": "coqui",
      "preview_audio_url": "/api/v1/files/audio/previews/voice1.mp3",
      "is_clone": false,
      "is_system": true
    }
  ]
}
```

---

#### `GET /projects/{project_id}/dubbing` — Get dubbing configuration

**Response (200):**
```json
{
  "success": true,
  "data": {
    "project_id": "uuid",
    "voice_profile_id": "uuid",
    "speed": 1.0,
    "pitch_shift": 0,
    "volume_gain_db": 0,
    "segments": [
      {
        "segment_index": 0,
        "audio_url": "/api/v1/files/audio/project_uuid/segment_0.mp3",
        "start_ms": 0,
        "end_ms": 3200,
        "duration_ms": 3100,
        "voice_profile_id": "uuid"
      }
    ]
  }
}
```

---

#### `POST /projects/{project_id}/generate-dubbing` — Generate voice dubbing

**Request Body:**
```json
{
  "voice_profile_id": "uuid",
  "speed": 1.0,
  "pitch_shift": 0,
  "volume_gain_db": 0
}
```

**Response (202):**
```json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "status": "queued",
    "total_segments": 45,
    "estimated_duration_seconds": 180
  }
}
```

---

#### `PATCH /projects/{project_id}/dubbing` — Update dubbing settings

**Request Body:**
```json
{
  "voice_profile_id": "uuid",
  "speed": 1.2,
  "pitch_shift": 2,
  "volume_gain_db": 3
}
```

**Response (200):** Same as GET

---

### 2.6 Subtitle

#### `GET /projects/{project_id}/subtitles` — Get subtitles

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| format | string | `srt` | `srt`, `ass`, `vtt` |

**Response (200):**
```json
{
  "success": true,
  "data": {
    "project_id": "uuid",
    "format": "srt",
    "content": "1\n00:00:00,000 --> 00:00:03,200\nXin chào và chào mừng đến với video hôm nay\n\n2\n00:00:03,200 --> ...",
    "style_config": {
      "font_family": "Arial",
      "font_size": 24,
      "font_color": "#FFFFFF",
      "border_color": "#000000",
      "border_width": 2,
      "position": "bottom",
      "animation": "none"
    },
    "is_burned": false
  }
}
```

---

#### `POST /projects/{project_id}/subtitles` — Generate subtitles

**Request Body:**
```json
{
  "format": "ass",
  "style_config": {
    "font_family": "Arial",
    "font_size": 24,
    "font_color": "#FFFFFF",
    "position": "bottom",
    "animation": "fade"
  }
}
```

**Response (200):** Same as GET

---

#### `PATCH /projects/{project_id}/subtitles/style` — Update subtitle style

**Request Body:**
```json
{
  "font_family": "Roboto",
  "font_size": 28,
  "font_color": "#00FF00",
  "border_color": "#000000",
  "border_width": 3,
  "position": "top",
  "animation": "slide"
}
```

**Response (200):** Updated subtitle content

---

### 2.7 Branding

#### `GET /projects/{project_id}/branding` — Get branding config

**Response (200):**
```json
{
  "success": true,
  "data": {
    "project_id": "uuid",
    "intro_enabled": true,
    "intro_template": {
      "id": "uuid",
      "name": "My Intro",
      "preview_url": "/api/v1/files/previews/intro.mp4"
    },
    "outro_enabled": true,
    "outro_template": {
      "id": "uuid",
      "name": "My Outro"
    },
    "watermark_enabled": true,
    "watermark_config": {
      "image_url": "/api/v1/files/watermarks/logo.png",
      "position": "bottom_right",
      "opacity": 0.7,
      "scale_percent": 15
    },
    "bg_music_enabled": true,
    "bg_music_url": "/api/v1/files/music/bg.mp3",
    "bg_music_volume": 0.3,
    "bg_music_loop": true
  }
}
```

---

#### `PATCH /projects/{project_id}/branding` — Update branding config

**Request Body:**
```json
{
  "intro_enabled": true,
  "intro_template_id": "uuid",
  "watermark_enabled": true,
  "watermark_config": {
    "position": "top_left",
    "opacity": 0.5
  }
}
```

**Response (200):** Same as GET

---

#### `GET /branding-templates` — List branding templates

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| type | string | — | `intro`, `outro` |

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "Professional Intro",
      "type": "intro",
      "preview_url": "/api/v1/files/previews/intro_template.mp4",
      "is_system": true
    }
  ]
}
```

---

#### `POST /branding-templates` — Create a branding template

**Request Body:**
```json
{
  "name": "My Custom Intro",
  "type": "intro",
  "config": {
    "duration_ms": 5000,
    "animation": "fade_in_scale",
    "background_color": "#1a1a2e"
  }
}
```

**Response (201):** Created template object

---

### 2.8 Render & Export

#### `GET /projects/{project_id}/render-tasks` — List render tasks

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "project_id": "uuid",
      "status": "completed",
      "progress_percent": 100,
      "current_step": "Finalizing",
      "eta_seconds": 0,
      "output_format": "mp4",
      "output_resolution": "1080p",
      "output_url": "/api/v1/files/output/project_uuid/final.mp4",
      "output_size_bytes": 157286400,
      "error_log": [],
      "created_at": "2026-01-01T12:00:00Z",
      "completed_at": "2026-01-01T12:10:00Z"
    }
  ]
}
```

---

#### `POST /projects/{project_id}/render` — Start rendering

**Request Body:**
```json
{
  "output_format": "mp4",
  "output_resolution": "1080p",
  "output_codec": "h264",
  "settings": {
    "quality_preset": "balanced",
    "crf": 23,
    "gpu_acceleration": true,
    "include_intro": true,
    "include_outro": true,
    "burn_subtitles": true,
    "replace_audio": true
  }
}
```

**Response (202):**
```json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "status": "queued",
    "estimated_duration_seconds": 600,
    "settings": { /* ... */ }
  }
}
```

---

#### `GET /render-tasks/{task_id}` — Get task status

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "project_id": "uuid",
    "status": "processing",
    "progress_percent": 45.5,
    "current_step": "Assembling video: frame 4523/10000",
    "eta_seconds": 327,
    "settings": { /* ... */ }
  }
}
```

---

#### `POST /render-tasks/{task_id}/cancel` — Cancel render

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "status": "cancelled"
  }
}
```

---

### 2.9 AI Assistant (Chatbot)

#### `POST /projects/{project_id}/chat/sessions` — Create chat session

**Response (201):**
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "project_id": "uuid",
    "created_at": "2026-01-01T12:00:00Z"
  }
}
```

---

#### `GET /projects/{project_id}/chat/sessions/{session_id}` — Get chat history

**Response (200):**
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "messages": [
      {
        "id": "uuid",
        "role": "user",
        "content": "Can you improve this translation?",
        "created_at": "2026-01-01T12:00:00Z"
      },
      {
        "id": "uuid",
        "role": "assistant",
        "content": "Sure! Here's an improved version...",
        "tool_calls": null,
        "created_at": "2026-01-01T12:00:05Z"
      }
    ]
  }
}
```

---

#### `POST /projects/{project_id}/chat/sessions/{session_id}/messages` — Send message (streaming)

**Request Body:**
```json
{
  "content": "Generate a YouTube title for this video"
}
```

**Response (200) — SSE Stream:**
```
event: token
data: {"token": "How", "finish_reason": null}

event: token
data: {"token": " to", "finish_reason": null}

event: done
data: {"full_response": "How to Master Video Localization in 2026", "tokens_used": 45}
```

---

### 2.10 YouTube Publishing

#### `GET /projects/{project_id}/youtube-metadata` — Get YouTube metadata

**Response (200):**
```json
{
  "success": true,
  "data": {
    "project_id": "uuid",
    "title": "How to Master Video Localization in 2026",
    "description": "In this video, we explore...",
    "tags": ["localization", "video editing", "AI"],
    "category": "Education",
    "playlist": "Tutorials",
    "visibility": "unlisted",
    "chapters": [
      { "title": "Introduction", "start_ms": 0 },
      { "title": "What is Localization", "start_ms": 60000 }
    ],
    "thumbnail_url": "/api/v1/files/thumbnails/youtube_thumb.jpg",
    "language": "vi"
  }
}
```

---

#### `PATCH /projects/{project_id}/youtube-metadata` — Update YouTube metadata

**Request Body:**
```json
{
  "title": "New Title",
  "description": "Updated description",
  "tags": ["new", "tags"],
  "visibility": "public"
}
```

**Response (200):** Same as GET

---

#### `POST /projects/{project_id}/youtube-metadata/export` — Export metadata as file

**Request Body:**
```json
{
  "format": "json"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "download_url": "/api/v1/files/exports/project_uuid/metadata.json",
    "format": "json"
  }
}
```

---

### 2.11 File Serving

#### `GET /api/v1/files/{type}/{project_id}/{filename}` — Serve a file

**Path Parameters:**
| Param | Description |
|-------|-------------|
| type | File category: `video`, `audio`, `thumbnails`, `previews`, `watermarks`, `music`, `exports`, `output` |

**Response (200):** Binary file stream with appropriate Content-Type header

---

### 2.12 Batch Processing

#### `POST /batch/render` — Add multiple projects to render queue

**Request Body:**
```json
{
  "project_ids": ["uuid1", "uuid2", "uuid3"],
  "render_settings": {
    "output_format": "mp4",
    "output_resolution": "1080p",
    "quality_preset": "balanced"
  },
  "priority": "normal"
}
```

**Response (202):**
```json
{
  "success": true,
  "data": {
    "batch_id": "uuid",
    "tasks": [
      { "project_id": "uuid1", "task_id": "task_uuid1", "status": "queued" },
      { "project_id": "uuid2", "task_id": "task_uuid2", "status": "queued" }
    ],
    "total_tasks": 3
  }
}
```

---

#### `GET /batch/{batch_id}` — Get batch status

**Response (200):**
```json
{
  "success": true,
  "data": {
    "batch_id": "uuid",
    "status": "processing",
    "progress_percent": 45.0,
    "tasks": [
      { "project_id": "uuid1", "status": "completed", "progress": 100 },
      { "project_id": "uuid2", "status": "processing", "progress": 35 },
      { "project_id": "uuid3", "status": "queued", "progress": 0 }
    ],
    "completed_count": 1,
    "failed_count": 0,
    "total_tasks": 3,
    "created_at": "2026-01-01T12:00:00Z"
  }
}
```

---

## 3. WebSocket Events (Chi tiết)

### 3.1 Connection

```
ws://localhost:8000/ws/projects/{project_id}?token=jwt_token
```

### 3.2 Client → Server Events

```json
{
  "type": "subscribe",
  "channels": ["transcript", "translation", "tts", "render"]
}
```

### 3.3 Server → Client Events

**Task Progress:**
```json
{
  "type": "task.progress",
  "data": {
    "task_id": "uuid",
    "step": "speech_to_text",
    "progress_percent": 65.0,
    "current_segment": 29,
    "total_segments": 45,
    "eta_seconds": 45
  }
}
```

**Task Completed:**
```json
{
  "type": "task.completed",
  "data": {
    "task_id": "uuid",
    "step": "speech_to_text",
    "result": {
      "total_segments": 45,
      "duration_seconds": 120,
      "language": "en"
    }
  }
}
```

**Task Failed:**
```json
{
  "type": "task.failed",
  "data": {
    "task_id": "uuid",
    "step": "translation",
    "error": {
      "code": "TRANSLATION_ENGINE_UNAVAILABLE",
      "message": "Local LLM is not running. Please start Ollama."
    },
    "retry_allowed": true
  }
}
```

---

## 4. Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `PROJECT_NOT_FOUND` | 404 | Project ID does not exist |
| `VIDEO_NOT_FOUND` | 404 | No video uploaded for project |
| `TRANSCRIPT_NOT_FOUND` | 404 | Run STT first |
| `TRANSLATION_NOT_FOUND` | 404 | Run translation first |
| `VOICE_PROFILE_NOT_FOUND` | 404 | Voice profile ID invalid |
| `INVALID_FILE_FORMAT` | 400 | Unsupported video format |
| `FILE_TOO_LARGE` | 400 | Exceeds max file size |
| `TASK_IN_PROGRESS` | 409 | Cannot start task while another is running |
| `PIPELINE_STEP_MISSING` | 422 | Previous step not completed |
| `ENGINE_UNAVAILABLE` | 503 | AI engine not ready/failed to load |
| `GPU_NOT_AVAILABLE` | 503 | GPU required but not found |
| `VALIDATION_ERROR` | 400 | Input validation failed |
| `INTERNAL_ERROR` | 500 | Unexpected server error |