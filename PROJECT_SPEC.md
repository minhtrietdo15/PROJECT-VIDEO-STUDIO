# PRODUCT SPECIFICATION: Video Localization AI Studio

> **Version:** 1.0
> **Status:** Draft — Market Validation Completed
> **Author:** AI CEO / Planner

---

## 1. Executive Summary

**Video Localization AI Studio** là một nền tảng (desktop/web-based) giúp người sáng tạo nội dung tự động hóa quy trình bản địa hóa video sang tiếng Việt. Hệ thống sử dụng AI pipeline (Speech-to-Text → Translation → Text-to-Speech → Video Assembly) để giảm thời gian sản xuất từ nhiều ngày xuống còn vài chục phút, đồng thời đảm bảo chất lượng đầu ra chuyên nghiệp.

---

## 2. Market Validation (Phân tích thị trường)

### 2.1 Vấn đề (Problem)

| Vấn đề | Mô tả | Mức độ nghiêm trọng |
|--------|-------|---------------------|
| **Chi phí cao** | Thuê người dịch + lồng tiếng cho 1 video 10 phút tốn $50–$200+ | ⚠️ Rất cao |
| **Thời gian dài** | Quy trình thủ công mất 2–5 ngày cho 1 video | ⚠️ Rất cao |
| **Rào cản kỹ thuật** | Người sáng tạo nhỏ lẻ không có kỹ năng edit video chuyên sâu | ⚠️ Cao |
| **Thiếu công cụ tích hợp** | Phải dùng nhiều tool rời rạc (dịch thuật, TTS, edit video) | ⚠️ Cao |
| **Chất lượng không đồng đều** | Dịch máy thô, giọng đọc robot, mất ngữ cảnh | ⚠️ Trung bình |

### 2.2 Giải pháp (Solution)

Một **end-to-end pipeline** tích hợp tất cả công đoạn trong một giao diện duy nhất:

```
[Import Video] → [Speech-to-Text] → [AI Translation] → [Voice Dubbing] → [Subtitle] → [Branding] → [Export]
```

### 2.3 Phân khúc thị trường mục tiêu (Target Segments)

| Phân khúc | Mô tả | Quy mô (ước tính) | Mức độ phù hợp |
|-----------|-------|-------------------|----------------|
| **YouTube Creators Việt Nam** | Người làm nội dung muốn đăng video tiếng Việt từ nguồn nước ngoài | ~50,000–100,000 | ⭐⭐⭐⭐⭐ |
| **YouTube Creators quốc tế** | Người nước ngoài muốn tiếp cận thị trường Việt Nam | ~10,000–50,000 | ⭐⭐⭐⭐ |
| **EdTech / Online Learning** | Chuyển ngữ khóa học tiếng Anh sang tiếng Việt | ~5,000–20,000 | ⭐⭐⭐⭐⭐ |
| **Media Agencies** | Sản xuất nội dung đa ngôn ngữ cho khách hàng | ~1,000–5,000 | ⭐⭐⭐⭐ |
| **Doanh nghiệp SME** | Cần video quảng cáo, giới thiệu sản phẩm bằng tiếng Việt | ~10,000+ | ⭐⭐⭐ |

### 2.4 Phân tích đối thủ cạnh tranh (Competitor Analysis)

| Đối thủ | Điểm mạnh | Điểm yếu | Cơ hội cho chúng ta |
|---------|-----------|----------|---------------------|
| **Rask.ai** | Pipeline hoàn chỉnh, nhiều ngôn ngữ | Giá cao ($70–$200/tháng), ít tùy biến | Giá rẻ hơn, mã nguồn mở, tùy biến cao |
| **Dubverse.ai** | TTS chất lượng, UI đẹp | Chỉ hỗ trợ 30+ ngôn ngữ, không có video editor | Tập trung tiếng Việt, có subtitle editor |
| **Kapwing** | Dễ dùng, có sẵn trên web | Giới hạn dung lượng, watermark | Local processing, không giới hạn |
| **Descript** | All-in-one, mạnh về audio | Đắt ($24–$84/tháng), ít tính năng video | Batch processing, giá rẻ hơn |
| **Tự làm thủ công** | Kiểm soát hoàn toàn | Tốn thời gian, chi phí cao | Tự động hóa, tiết kiệm 90% thời gian |

### 2.5 Lợi thế cạnh tranh (Competitive Advantage)

1. **Ưu tiên tiếng Việt**: Dịch thuật và TTS được tối ưu cho tiếng Việt — chất lượng vượt trội so với các công cụ đa ngôn ngữ chung chung.
2. **Local-first / Offline-capable**: Chạy local với GPU, không phụ thuộc Internet — bảo mật dữ liệu, không giới hạn dung lượng.
3. **Mã nguồn mở (core)**: Cộng đồng có thể đóng góp, fork, tùy biến — tạo hệ sinh thái plugin.
4. **Chi phí thấp**: Sử dụng model open-source (Whisper, LLM local, Coqui TTS) — gần như miễn phí vận hành.
5. **All-in-one workflow**: Từ import đến xuất YouTube — không cần chuyển đổi giữa các tool.

### 2.6 Kênh tiếp cận khách hàng (Go-to-Market)

| Kênh | Chiến lược | Chi phí | Hiệu quả dự kiến |
|------|-----------|---------|------------------|
| **YouTube Creator Community** | Đăng video demo, tutorial, case study | Thấp (tự làm) | Cao |
| **Facebook Groups (Creator, EdTech)** | Chia sẻ miễn phí, thu thập feedback | Miễn phí | Cao |
| **GitHub / Open Source** | Public repo, thu hút contributor | Miễn phí | Trung bình |
| **Product Hunt** | Launch sản phẩm | Miễn phí | Cao (nếu được vote) |
| **Google Ads / Facebook Ads** | Targeted ads đến creator | Trung bình–Cao | Trung bình |

### 2.7 Rủi ro & Giảm thiểu (Risk Mitigation)

| Rủi ro | Mức độ | Giải pháp |
|--------|--------|-----------|
| **Chất lượng AI chưa đủ tốt** | Trung bình | Cho phép chỉnh sửa thủ công, fine-tune model |
| **Cạnh tranh từ big tech (Google, Meta)** | Cao | Tập trung vào niche tiếng Việt + local processing |
| **Chi phí GPU cao** | Trung bình | Hỗ trợ CPU fallback, cloud GPU option |
| **Khó tiếp cận người dùng** | Trung bình | Freemium model, cộng đồng open-source |
| **Vấn đề bản quyền nội dung** | Thấp | Yêu cầu người dùng xác nhận quyền sở hữu |

### 2.8 Kết luận Market Validation

> **✅ Thị trường có nhu cầu thực sự.** Các đối thủ hiện tại hoặc quá đắt, hoặc không tập trung vào tiếng Việt, hoặc thiếu tính năng all-in-one. Sản phẩm có lợi thế cạnh tranh rõ ràng ở phân khúc tiếng Việt + local-first + open-source. **Khuyến nghị: TIẾN HÀNH PHÁT TRIỂN.**

---

## 3. Product Vision & Goals

### 3.1 Vision
Trở thành công cụ bản địa hóa video số 1 cho thị trường Việt Nam, sau đó mở rộng ra các ngôn ngữ khác.

### 3.2 Mission
Giúp mọi người sáng tạo nội dung dễ dàng tiếp cận khán giả Việt Nam thông qua video chất lượng cao, bất kể ngôn ngữ gốc.

### 3.3 Goals (OKRs)

| Mục tiêu | Key Result | Timeline |
|----------|-----------|----------|
| **Product-Market Fit** | 100 người dùng active/tháng | 3 tháng sau launch |
| **Chất lượng** | Độ chính xác dịch > 90% | Release v1.0 |
| **Tốc độ** | Xử lý video 10 phút < 15 phút | Release v1.0 |
| **Cộng đồng** | 50 GitHub stars, 10 contributors | 1 tháng sau public |

---

## 4. Core Features (Chi tiết)

### 4.1 Video Import Module
- **Upload**: Drag & drop, file picker — hỗ trợ MP4, MOV, MKV, AVI, WebM
- **URL Import**: Download từ URL (yêu cầu người dùng có quyền)
- **Metadata Display**: Thumbnail, duration, resolution, FPS, size, codec
- **Validation**: Kiểm tra format, dung lượng, cảnh báo nếu không hỗ trợ

### 4.2 Speech Recognition Module
- **Engine**: Whisper (local) — models: tiny/base/small/medium/large
- **Output**: Transcript + timestamps (word-level & segment-level)
- **Language Detection**: Tự động phát hiện ngôn ngữ gốc
- **Speaker Diarization** (v2.0): Phân biệt người nói

### 4.3 Translation Module
- **Engine**: Local LLM (Llama, Mistral, Qwen) hoặc API (OpenAI, Gemini, Claude) — do người dùng chọn
- **Style Options**: Trung tính, Tự nhiên, Video ngắn, Giáo dục
- **Context Preservation**: Giữ tên riêng, thuật ngữ kỹ thuật, số liệu
- **Review Mode**: So sánh song ngữ, chỉnh sửa thủ công

### 4.4 Voice Dubbing Module
- **Engine**: Coqui TTS / Piper TTS / Edge TTS (tiếng Việt)
- **Voice Options**: Nam/Nữ/Trẻ/Trầm/Năng động — tối thiểu 5 giọng
- **Voice Clone** (v2.0): Clone giọng từ mẫu audio (yêu cầu quyền sử dụng)
- **Adjustments**: Tốc độ (±50%), Cao độ (±6 semitones), Âm lượng
- **Sync**: Đồng bộ hóa với video gốc, giữ khớp môi (lip-sync cơ bản)

### 4.5 Subtitle Module
- **Formats**: SRT, ASS, VTT, SSA
- **Visual Editor**: Timeline-based, click-to-edit, real-time preview
- **Styling**: Font, Color, Border, Shadow, Position, Animation (fade, slide, typewriter)
- **Auto-generation**: Tạo sub từ transcript đã dịch

### 4.6 Branding Module
- **Intro Generator**: Logo + tên kênh + animation + âm thanh — lưu template
- **Outro Generator**: Subscribe/Like animation, QR code, website, social links
- **Watermark**: Vị trí, opacity, kích thước
- **Background Music**: Upload hoặc chọn từ thư viện (royalty-free)

### 4.7 Video Processing Engine
- **Assembly Pipeline**: Ghép intro → video chính → thay audio → gắn sub → outro
- **Audio Processing**: Chuẩn hóa âm lượng (LUFS), noise reduction, crossfade
- **Output Formats**: MP4 (H.264/H.265), MOV, MKV
- **Resolutions**: 1080p, 2K, 4K — giữ nguyên tỷ lệ khung hình
- **GPU Acceleration**: CUDA (NVIDIA), VAAPI (Intel), VideoToolbox (Apple)

### 4.8 Batch Processing
- **Queue Management**: Thêm nhiều video, sắp xếp, ưu tiên
- **Progress Tracking**: Progress bar, ETA, current step
- **Error Handling**: Retry, skip, error log chi tiết
- **Parallel Processing**: Xử lý nhiều video đồng thời (tùy hardware)

### 4.9 Project Management
- **Project Structure**: Mỗi video = 1 project — lưu tất cả assets + settings
- **Save/Load**: Auto-save, manual save, resume bất kỳ lúc nào
- **Version History** (v2.0): Lưu lịch sử chỉnh sửa
- **Export/Import Project**: Chia sẻ project file

### 4.10 AI Assistant (Chatbot)
- **Capabilities**:
  - Chỉnh sửa bản dịch (theo ngữ cảnh)
  - Viết tiêu đề YouTube (SEO-optimized)
  - Viết mô tả video
  - Sinh hashtag, chapter, timestamps
  - Gợi ý thumbnail concept
  - Đề xuất SEO keywords
- **Integration**: Gắn trực tiếp vào từng module (dịch, metadata)

### 4.11 YouTube Publishing
- **Metadata Preparation**: Title, description, tags, playlist, chapters
- **Thumbnail**: Tự động tạo từ video frame + text overlay
- **Export**: JSON/YAML metadata file — sẵn sàng để upload thủ công hoặc qua API

---

## 5. User Personas

### Persona 1: Minh — YouTube Creator (Việt kiều)
- **Tuổi**: 28
- **Nghề nghiệp**: Freelancer, làm video về công nghệ
- **Nỗi đau**: Có kênh YouTube tiếng Anh 50K subs, muốn mở rộng sang thị trường Việt Nam nhưng không có thời gian dịch và lồng tiếng thủ công
- **Nhu cầu**: Tool tự động dịch + lồng tiếng chất lượng cao, giá rẻ
- **Hành vi**: Sẵn sàng trả $10–$20/tháng nếu tool tốt

### Persona 2: Lan — Giáo viên Online (EdTech)
- **Tuổi**: 35
- **Nghề nghiệp**: Giáo viên tiếng Anh, bán khóa học online
- **Nỗi đau**: Muốn chuyển ngữ khóa học sang tiếng Việt nhưng chi phí thuê người dịch quá cao
- **Nhu cầu**: Dịch thuật chính xác thuật ngữ giáo dục, giọng đọc tự nhiên
- **Hành vi**: Ưu tiên chất lượng hơn giá cả

### Persona 3: Tuấn — Agency Owner
- **Tuổi**: 42
- **Nghề nghiệp**: Chủ studio sản xuất video
- **Nỗi đau**: Khách hàng yêu cầu video đa ngôn ngữ, quy trình thủ công không scale được
- **Nhu cầu**: Batch processing, pipeline tự động, chất lượng ổn định
- **Hành vi**: Cần tool mạnh, sẵn sàng đầu tư hardware

---

## 6. Technical Architecture (Tổng quan)

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│  Dashboard │ Project Manager │ Subtitle Editor │ Chatbot │
└──────────────────────┬──────────────────────────────────┘
                       │ REST API / WebSocket
┌──────────────────────┴──────────────────────────────────┐
│                  Backend (FastAPI)                       │
│  Auth │ Project CRUD │ Task Management │ File Streaming │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────┐
│              Queue System (Celery + Redis)               │
│  Speech-to-Text │ Translation │ TTS │ Video Processing  │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────┐
│              AI Models & Processing Engines              │
│  Whisper │ LLM │ Coqui TTS │ FFmpeg │ pysubs2          │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────┐
│              Storage Layer                               │
│  PostgreSQL (metadata) │ File System (assets) │ Redis   │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack (Chi tiết)

| Layer | Technology | Lý do chọn |
|-------|-----------|------------|
| **Frontend** | React 18 + Next.js 14 + TailwindCSS | SSR, SEO, responsive, ecosystem lớn |
| **Backend** | Python 3.11+ / FastAPI | Async, type-safe, performance cao |
| **Queue** | Celery + Redis | Mature, scalable, hỗ trợ task scheduling |
| **Database** | PostgreSQL (chính) + SQLite (local fallback) | Production-ready, ACID |
| **Video** | FFmpeg (Python wrapper: ffmpeg-python) | Standard công nghiệp |
| **STT** | Whisper (openai-whisper / faster-whisper) | Local, accuracy cao, free |
| **Translation** | Local LLM (Llama.cpp / Ollama) + API wrapper | Flexible, privacy |
| **TTS** | Coqui TTS / Piper TTS / Edge-TTS | Hỗ trợ tiếng Việt tốt |
| **Subtitle** | pysubs2 + FFmpeg | Full format support |
| **Container** | Docker + Docker Compose | Portable, reproducible |
| **GPU** | CUDA (NVIDIA) / DirectML (Windows) | Acceleration |

---

## 7. User Flow (Luồng người dùng)

```
1. Tạo Project mới
   ├── Upload video (hoặc import URL)
   └── Xem metadata → Xác nhận

2. Speech-to-Text
   ├── Chọn model Whisper (tiny → large)
   ├── Chạy nhận diện
   └── Review & chỉnh sửa transcript

3. Translation
   ├── Chọn style dịch
   ├── Chọn engine (local LLM / API)
   ├── Chạy dịch
   └── Review & chỉnh sửa bản dịch (song ngữ)

4. Voice Dubbing
   ├── Chọn giọng đọc
   ├── Tùy chỉnh tốc độ/cao độ
   ├── Chạy TTS
   └── Preview audio

5. Subtitle
   ├── Chọn format (SRT/ASS/VTT)
   ├── Tùy chỉnh style
   └── Preview

6. Branding (tùy chọn)
   ├── Chọn Intro template
   ├── Chọn Outro template
   ├── Thêm Watermark
   └── Thêm Background Music

7. Export
   ├── Chọn resolution (1080p/2K/4K)
   ├── Chọn format (MP4/MOV/MKV)
   ├── Chạy render
   └── Download / Xuất metadata YouTube
```

---

## 8. Non-functional Requirements

| Yêu cầu | Mô tả | Target |
|---------|-------|--------|
| **Performance** | Thời gian xử lý | Video 10 phút < 15 phút (với GPU) |
| **Scalability** | Xử lý đồng thời | Tối thiểu 3 video batch |
| **Reliability** | Uptime / Error rate | > 99% tasks hoàn thành không lỗi |
| **Security** | Dữ liệu người dùng | Local processing, không gửi data ra ngoài (trừ API dịch nếu dùng) |
| **Usability** | UX cho người không chuyên | Hoàn thành video đầu tiên trong < 30 phút |
| **Portability** | Cross-platform | Windows, macOS, Linux (Docker) |
| **Memory** | RAM tối thiểu | 8GB (CPU), 16GB (GPU) |
| **Storage** | Disk cho project | Tùy thuộc video, khuyến nghị 50GB+ |

---

## 9. Milestones & Timeline

| Phase | Nội dung | Thời gian | Deliverables |
|-------|----------|-----------|--------------|
| **P0 — Foundation** | Setup project, Docker, database, queue | 2 tuần | Repo structure, CI/CD, dev environment |
| **P1 — Core Pipeline** | Video import, STT, Translation, TTS, Export | 6 tuần | Pipeline cơ bản hoàn chỉnh |
| **P2 — UI/UX** | Dashboard, Subtitle Editor, Branding | 4 tuần | Giao diện đầy đủ |
| **P3 — Advanced** | Batch processing, AI Assistant, YouTube export | 3 tuần | Tính năng nâng cao |
| **P4 — Polish** | Testing, optimization, documentation | 2 tuần | Release v1.0 |

**Tổng thời gian: ~17 tuần (4 tháng)**

---

## 10. Success Metrics (KPIs)

| KPI | Target | Cách đo |
|-----|--------|---------|
| **Translation Accuracy** | > 90% | BLEU score + human evaluation |
| **Processing Speed** | < 15 phút / 10 phút video | Benchmark với video test |
| **User Satisfaction** | NPS > 40 | Survey sau khi dùng |
| **Task Completion Rate** | > 80% | % người dùng hoàn thành video đầu tiên |
| **Error Rate** | < 5% | % tasks failed / total tasks |
| **Active Users** | 100 MAU | Tháng thứ 3 sau launch |

---

## 11. Future Roadmap (v2.0+)

- [ ] **Multi-language support**: Mở rộng ra các ngôn ngữ khác (Trung, Nhật, Hàn, Thái)
- [ ] **Cloud version**: SaaS platform với web UI
- [ ] **API for developers**: Public API cho tích hợp bên thứ ba
- [ ] **Mobile app**: iOS/Android cho quản lý project
- [ ] **Real-time collaboration**: Team editing
- [ ] **Advanced lip-sync**: Wav2Lip integration
- [ ] **AI video generation**: Text-to-video cho intro/outro
- [ ] **Marketplace**: Template sharing community