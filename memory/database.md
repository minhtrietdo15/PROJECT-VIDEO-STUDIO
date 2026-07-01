# Database Design — Video Localization AI Studio

> **Version:** 1.0
> **Engine:** PostgreSQL (primary) + SQLite (local/fallback)
> **ORM:** SQLAlchemy 2.0 (async)
> **Migration:** Alembic

---

## 1. Entity-Relationship Diagram (Text)

```
User 1──N Project 1──1 Video
                        │
                        ├──1──N TranscriptSegment
                        │
                        ├──1──N TranslationSegment
                        │
                        ├──1──N AudioSegment → VoiceProfile
                        │
                        ├──1──1 SubtitleTrack
                        │
                        ├──1──1 BrandingConfig
                        │
                        └──1──N RenderTask
```

---

## 2. Table Definitions

### 2.1 users

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique user ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| display_name | VARCHAR(100) | NOT NULL | Display name |
| avatar_url | TEXT | nullable | Profile picture URL |
| settings | JSONB | default '{}' | User preferences (theme, language, default engine) |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |
| updated_at | TIMESTAMPTZ | NOT NULL, default now(), onupdate now() | |

**Indexes:**
- `idx_users_email` ON email (UNIQUE)

**Settings JSONB Schema:**
```json
{
  "theme": "dark" | "light",
  "language": "vi" | "en",
  "default_stt_model": "medium",
  "default_translation_engine": "local",
  "default_tts_voice": "female_1",
  "gpu_enabled": true
}
```

---

### 2.2 projects

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique project ID |
| user_id | UUID | FK → users.id, NOT NULL | Owner |
| title | VARCHAR(255) | NOT NULL | Project name |
| source_language | VARCHAR(10) | NOT NULL, default 'en' | Source language code (ISO 639-1) |
| target_language | VARCHAR(10) | NOT NULL, default 'vi' | Target language code |
| status | ENUM | NOT NULL, default 'draft' | See status enum below |
| thumbnail_path | TEXT | nullable | Path to project thumbnail |
| total_duration_ms | BIGINT | default 0 | Video duration in milliseconds |
| pipeline_progress | JSONB | default '{}' | Per-step completion status |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |
| updated_at | TIMESTAMPTZ | NOT NULL, default now(), onupdate now() | |

**Status Enum:** `draft` → `video_imported` → `transcript_ready` → `translated` → `dubbing_ready` → `subtitle_ready` → `branding_ready` → `rendering` → `completed` → `failed`

**Indexes:**
- `idx_projects_user_id` ON user_id
- `idx_projects_status` ON status
- `idx_projects_created_at` ON created_at DESC
- `idx_projects_user_status` ON (user_id, status) — composite

**pipeline_progress JSONB Schema:**
```json
{
  "stt": "pending" | "processing" | "completed" | "failed",
  "translation": "pending" | "processing" | "completed" | "failed",
  "tts": "pending" | "processing" | "completed" | "failed",
  "subtitle": "pending" | "completed",
  "render": "pending" | "processing" | "completed" | "failed"
}
```

---

### 2.3 videos

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| project_id | UUID | FK → projects.id, UNIQUE, NOT NULL | 1 project = 1 video |
| filename | VARCHAR(255) | NOT NULL | Original filename |
| file_path | TEXT | NOT NULL | Path to stored video file |
| file_size_bytes | BIGINT | NOT NULL | File size |
| duration_ms | BIGINT | NOT NULL | Duration in milliseconds |
| width | INT | NOT NULL | Resolution width (px) |
| height | INT | NOT NULL | Resolution height (px) |
| fps | FLOAT | NOT NULL | Frames per second |
| codec | VARCHAR(50) | NOT NULL | Video codec (e.g., h264, hevc) |
| audio_codec | VARCHAR(50) | nullable | Audio codec |
| audio_sample_rate | INT | nullable | Audio sample rate (Hz) |
| thumbnail_path | TEXT | nullable | Path to generated thumbnail |
| source_type | ENUM | NOT NULL, default 'upload' | `upload` | `url` |
| source_url | TEXT | nullable | Original URL if imported |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |

**Indexes:**
- `idx_videos_project_id` ON project_id (UNIQUE)

---

### 2.4 transcript_segments

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| project_id | UUID | FK → projects.id, NOT NULL | |
| segment_index | INT | NOT NULL | Order index (0-based) |
| start_ms | BIGINT | NOT NULL | Start time (ms) |
| end_ms | BIGINT | NOT NULL | End time (ms) |
| text | TEXT | NOT NULL | Transcribed text |
| language | VARCHAR(10) | nullable | Detected language per segment |
| confidence | FLOAT | nullable | Whisper confidence score (0-1) |
| words | JSONB | default '[]' | Word-level timestamps |
| speaker_label | VARCHAR(50) | nullable | Speaker diarization label (v2.0) |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |

**Indexes:**
- `idx_ts_project_id` ON project_id
- `idx_ts_project_segment` ON (project_id, segment_index) — UNIQUE composite

**words JSONB Schema:**
```json
[
  {"word": "Hello", "start_ms": 1000, "end_ms": 1200, "confidence": 0.98},
  {"word": "world", "start_ms": 1200, "end_ms": 1400, "confidence": 0.95}
]
```

---

### 2.5 translation_segments

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| project_id | UUID | FK → projects.id, NOT NULL | |
| segment_index | INT | NOT NULL | Corresponds to transcript_segments.segment_index |
| source_text | TEXT | NOT NULL | Original text (denormalized for convenience) |
| translated_text | TEXT | NOT NULL | Translated text |
| style | VARCHAR(50) | NOT NULL, default 'neutral' | `neutral` | `natural` | `short_video` | `educational` |
| engine_used | VARCHAR(50) | NOT NULL | `local_llm` | `openai` | `gemini` | `claude` |
| confidence | FLOAT | nullable | Translation quality score (if available) |
| is_edited | BOOLEAN | default false | Whether user manually edited |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |
| updated_at | TIMESTAMPTZ | NOT NULL, default now(), onupdate now() | |

**Indexes:**
- `idx_transl_project_id` ON project_id
- `idx_transl_project_segment` ON (project_id, segment_index) — UNIQUE composite
- `idx_transl_edited` ON (project_id, is_edited) — for filtering edited segments

---

### 2.6 voice_profiles

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| name | VARCHAR(100) | NOT NULL | Display name (e.g., "Giọng Nam trầm") |
| gender | ENUM | NOT NULL | `male` | `female` | `neutral` |
| style | VARCHAR(50) | NOT NULL | `young` | `deep` | `energetic` | `gentle` |
| engine | VARCHAR(50) | NOT NULL | `coqui` | `piper` | `edge_tts` |
| engine_voice_id | VARCHAR(100) | NOT NULL | Engine-specific voice identifier |
| preview_audio_path | TEXT | nullable | Path to preview audio sample |
| is_clone | BOOLEAN | default false | Whether this is a cloned voice |
| clone_sample_path | TEXT | nullable | Path to clone source audio |
| is_system | BOOLEAN | default true | System-provided vs user-created |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |

**Indexes:**
- `idx_voice_profiles_engine` ON engine
- `idx_voice_profiles_gender_style` ON (gender, style)

---

### 2.7 audio_segments (Dubbing)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| project_id | UUID | FK → projects.id, NOT NULL | |
| segment_index | INT | NOT NULL | Corresponds to translation_segments.segment_index |
| voice_profile_id | UUID | FK → voice_profiles.id, NOT NULL | |
| audio_path | TEXT | NOT NULL | Path to generated audio file |
| start_ms | BIGINT | NOT NULL | Start time in video |
| end_ms | BIGINT | NOT NULL | End time in video |
| duration_ms | BIGINT | NOT NULL | Actual audio duration |
| speed | FLOAT | NOT NULL, default 1.0 | Speed multiplier (0.5-1.5) |
| pitch_shift | FLOAT | NOT NULL, default 0 | Pitch shift in semitones (-6 to +6) |
| volume_gain_db | FLOAT | NOT NULL, default 0 | Volume adjustment in dB |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |

**Indexes:**
- `idx_audio_project_id` ON project_id
- `idx_audio_project_segment` ON (project_id, segment_index)

---

### 2.8 subtitle_tracks

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| project_id | UUID | FK → projects.id, UNIQUE, NOT NULL | |
| format | ENUM | NOT NULL, default 'srt' | `srt` | `ass` | `vtt` |
| content | TEXT | NOT NULL | Full subtitle file content |
| style_config | JSONB | default '{}' | Styling configuration |
| is_burned | BOOLEAN | default false | Whether burned into video |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |
| updated_at | TIMESTAMPTZ | NOT NULL, default now(), onupdate now() | |

**style_config JSONB Schema:**
```json
{
  "font_family": "Arial",
  "font_size": 24,
  "font_color": "#FFFFFF",
  "border_color": "#000000",
  "border_width": 2,
  "shadow_color": "#000000",
  "shadow_offset": 1,
  "position": "bottom" | "top" | "custom",
  "custom_y_percent": 90,
  "animation": "none" | "fade" | "slide" | "typewriter",
  "background_color": "transparent",
  "background_opacity": 0.5
}
```

---

### 2.9 branding_configs

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| project_id | UUID | FK → projects.id, UNIQUE, NOT NULL | |
| intro_enabled | BOOLEAN | default false | |
| intro_template_id | UUID | FK → branding_templates.id, nullable | |
| outro_enabled | BOOLEAN | default false | |
| outro_template_id | UUID | FK → branding_templates.id, nullable | |
| watermark_enabled | BOOLEAN | default false | |
| watermark_config | JSONB | default '{}' | Watermark settings |
| bg_music_enabled | BOOLEAN | default false | |
| bg_music_path | TEXT | nullable | Path to background music file |
| bg_music_volume | FLOAT | default 0.3 | Background music volume (0-1) |
| bg_music_loop | BOOLEAN | default true | |
| bg_music_fade_in_ms | INT | default 2000 | Fade in duration (ms) |
| bg_music_fade_out_ms | INT | default 2000 | Fade out duration (ms) |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |
| updated_at | TIMESTAMPTZ | NOT NULL, default now(), onupdate now() | |

**watermark_config JSONB Schema:**
```json
{
  "image_path": "/data/projects/xxx/logo.png",
  "position": "bottom_right" | "top_left" | "top_right" | "bottom_left" | "center",
  "opacity": 0.7,
  "scale_percent": 15,
  "margin_x": 20,
  "margin_y": 20,
  "show_start_ms": 0,
  "show_end_ms": null
}
```

---

### 2.10 branding_templates

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| user_id | UUID | FK → users.id, NOT NULL | |
| name | VARCHAR(100) | NOT NULL | Template name |
| type | ENUM | NOT NULL | `intro` | `outro` |
| config | JSONB | NOT NULL | Full template configuration |
| preview_path | TEXT | nullable | Path to preview video/image |
| is_system | BOOLEAN | default false | System-provided defaults |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |
| updated_at | TIMESTAMPTZ | NOT NULL, default now(), onupdate now() | |

**Indexes:**
- `idx_templates_user_type` ON (user_id, type)
- `idx_templates_system` ON is_system

**Intro Template config JSONB Schema:**
```json
{
  "duration_ms": 5000,
  "logo_path": "/data/templates/xxx/logo.png",
  "logo_position": "center",
  "logo_scale": 50,
  "channel_name": "My Channel",
  "channel_name_font": "Arial",
  "channel_name_size": 48,
  "channel_name_color": "#FFFFFF",
  "animation": "fade_in_scale",
  "background_color": "#1a1a2e",
  "audio_path": "/data/templates/xxx/intro.mp3",
  "fade_in_ms": 500,
  "fade_out_ms": 500
}
```

---

### 2.11 render_tasks

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| project_id | UUID | FK → projects.id, NOT NULL | |
| status | ENUM | NOT NULL, default 'queued' | `queued` | `processing` | `completed` | `failed` | `cancelled` |
| progress_percent | FLOAT | default 0 | Progress 0-100 |
| current_step | VARCHAR(100) | nullable | Human-readable step description |
| eta_seconds | INT | nullable | Estimated remaining time |
| output_format | VARCHAR(10) | NOT NULL, default 'mp4' | `mp4` | `mov` | `mkv` |
| output_resolution | VARCHAR(20) | NOT NULL, default '1080p' | `1080p` | `2k` | `4k` |
| output_codec | VARCHAR(20) | NOT NULL, default 'h264' | `h264` | `h265` |
| output_path | TEXT | nullable | Path to final rendered video |
| output_size_bytes | BIGINT | nullable | Output file size |
| settings | JSONB | default '{}' | Render settings |
| error_log | JSONB | default '[]' | Array of error objects |
| celery_task_id | VARCHAR(255) | nullable | Celery task ID for monitoring |
| started_at | TIMESTAMPTZ | nullable | |
| completed_at | TIMESTAMPTZ | nullable | |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |

**Indexes:**
- `idx_render_project_id` ON project_id
- `idx_render_status` ON status
- `idx_render_celery` ON celery_task_id

**settings JSONB Schema:**
```json
{
  "quality_preset": "fast" | "balanced" | "best",
  "crf": 23,
  "preset": "medium",
  "gpu_acceleration": true,
  "include_intro": true,
  "include_outro": true,
  "burn_subtitles": true,
  "replace_audio": true,
  "audio_bitrate": "192k",
  "video_bitrate": "8M"
}
```

**error_log JSONB Schema:**
```json
[
  {
    "timestamp": "2026-01-01T12:00:00Z",
    "step": "video_assembly",
    "message": "FFmpeg error: Invalid data found when processing input",
    "code": "FFMPEG_INVALID_INPUT",
    "retry_count": 2
  }
]
```

---

### 2.12 ai_assistant_chats

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| project_id | UUID | FK → projects.id, NOT NULL | |
| session_id | UUID | NOT NULL | Group messages into sessions |
| role | ENUM | NOT NULL | `user` | `assistant` | `system` |
| content | TEXT | NOT NULL | Message content (markdown) |
| tool_calls | JSONB | nullable | Tool invocation data |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |

**Indexes:**
- `idx_chat_project_session` ON (project_id, session_id)
- `idx_chat_created` ON created_at

---

### 2.13 youtube_metadata

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | |
| project_id | UUID | FK → projects.id, UNIQUE, NOT NULL | |
| title | TEXT | nullable | YouTube video title |
| description | TEXT | nullable | Video description |
| tags | JSONB | default '[]' | Array of tag strings |
| category | VARCHAR(100) | nullable | YouTube category |
| playlist | VARCHAR(255) | nullable | Playlist name |
| visibility | ENUM | default 'unlisted' | `public` | `unlisted` | `private` |
| chapters | JSONB | default '[]' | Auto-generated chapters |
| thumbnail_path | TEXT | nullable | Path to custom thumbnail |
| language | VARCHAR(10) | default 'vi' | Video language |
| created_at | TIMESTAMPTZ | NOT NULL, default now() | |
| updated_at | TIMESTAMPTZ | NOT NULL, default now(), onupdate now() | |

**chapters JSONB Schema:**
```json
[
  {"title": "Introduction", "start_ms": 0},
  {"title": "Main Content", "start_ms": 60000},
  {"title": "Conclusion", "start_ms": 300000}
]
```

---

## 3. Relationships Summary

```
users
  └─── projects (1:N) — user_id
         ├─── videos (1:1) — project_id
         ├─── transcript_segments (1:N) — project_id
         ├─── translation_segments (1:N) — project_id
         ├─── audio_segments (1:N) — project_id
         │     └─── voice_profiles (N:1) — voice_profile_id
         ├─── subtitle_tracks (1:1) — project_id
         ├─── branding_configs (1:1) — project_id
         │     └─── branding_templates (N:1) — intro_template_id / outro_template_id
         ├─── render_tasks (1:N) — project_id
         ├─── ai_assistant_chats (1:N) — project_id
         └─── youtube_metadata (1:1) — project_id
```

---

## 4. Index Strategy

| Table | Index | Type | Purpose |
|-------|-------|------|---------|
| projects | user_id + status | B-tree composite | Dashboard filtering |
| projects | created_at DESC | B-tree | Sort by newest |
| transcript_segments | project_id + segment_index | UNIQUE B-tree | Ordered retrieval |
| translation_segments | project_id + is_edited | B-tree partial | Find edited translations |
| render_tasks | status | B-tree | Queue processing |
| ai_assistant_chats | project_id + session_id | B-tree composite | Session retrieval |
| voice_profiles | gender + style | B-tree composite | Voice selection UI |

---

## 5. Partitioning Strategy (Future)

For production scaling, consider partitioning:
- **projects**: By `created_at` (monthly ranges) — for 100K+ projects
- **transcript_segments**: By `project_id` (list partitioning) — segments are always queried by project
- **ai_assistant_chats**: By `created_at` (monthly) — high volume append-only table

---

## 6. SQLite Compatibility Notes

For local/fallback mode using SQLite:
- Replace `JSONB` with `JSON` (SQLite supports JSON natively)
- Replace `TIMESTAMPTZ` with `TIMESTAMP` or `TEXT` (ISO 8601)
- Remove `ENUM` types, use `VARCHAR` with CHECK constraints instead
- UUIDs stored as TEXT
- Disable concurrent write-heavy operations