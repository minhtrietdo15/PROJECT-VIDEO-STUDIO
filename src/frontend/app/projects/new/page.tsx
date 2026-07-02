'use client';

import { useState } from 'react';
import { VideoUpload, type VideoUploadFile } from '@/components/upload/video-upload';
import { UrlImport, type UrlImportResult } from '@/components/upload/url-import';
import { VideoMetadataCardContainer } from '@/components/upload/video-metadata-card-container';

/**
 * New project page.
 *
 * Renders the VideoUpload and UrlImport components so users can upload a
 * video file or import from a URL as the first step of creating a project.
 * After a successful upload or import, the video metadata card is displayed
 * using the projectId returned from the backend.
 * The full project creation flow (title, language selection, etc.) will
 * be added in Phase 2.1.
 */
export default function NewProjectPage() {
  const [activeProjectId, setActiveProjectId] = useState<string | null>(null);

  const handleUploadComplete = (file: VideoUploadFile, response?: unknown) => {
    // eslint-disable-next-line no-console
    console.log('Upload complete', file, response);
    const projectId =
      (response as { project_id?: string } | undefined)?.project_id ??
      file.videoId ??
      null;
    if (projectId) {
      setActiveProjectId(projectId);
    }
  };

  const handleUploadError = (file: VideoUploadFile, error: unknown) => {
    // eslint-disable-next-line no-console
    console.error('Upload error', file, error);
  };

  const handleImportComplete = (result: UrlImportResult, response?: unknown) => {
    // eslint-disable-next-line no-console
    console.log('URL import complete', result, response);
    if (result.projectId) {
      setActiveProjectId(result.projectId);
    }
  };

  const handleImportError = (error: unknown) => {
    // eslint-disable-next-line no-console
    console.error('URL import error', error);
  };

  return (
    <div className="mx-auto max-w-3xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Tạo project mới</h1>
        <p className="text-muted-foreground">
          Bắt đầu bằng cách upload video hoặc import từ URL bạn muốn bản địa
          hóa.
        </p>
      </div>

      <section className="space-y-4">
        <h2 className="text-lg font-semibold">Upload file video</h2>
        <VideoUpload
          onUploadComplete={handleUploadComplete}
          onUploadError={handleUploadError}
        />
      </section>

      <section className="space-y-4">
        <h2 className="text-lg font-semibold">Hoặc import từ URL</h2>
        <UrlImport
          onImportComplete={handleImportComplete}
          onImportError={handleImportError}
        />
      </section>

      {activeProjectId && (
        <section className="space-y-4">
          <h2 className="text-lg font-semibold">Thông tin video</h2>
          <VideoMetadataCardContainer projectId={activeProjectId} />
        </section>
      )}
    </div>
  );
}
