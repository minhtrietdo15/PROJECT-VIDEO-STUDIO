'use client';

import { VideoUpload } from '@/components/upload/video-upload';
import { UrlImport } from '@/components/upload/url-import';

/**
 * New project page.
 *
 * Renders the VideoUpload and UrlImport components so users can upload a
 * video file or import from a URL as the first step of creating a project.
 * The full project creation flow (title, language selection, etc.) will
 * be added in Phase 2.1.
 */
export default function NewProjectPage() {
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
          onUploadComplete={(file, response) => {
            // eslint-disable-next-line no-console
            console.log('Upload complete', file, response);
          }}
          onUploadError={(file, error) => {
            // eslint-disable-next-line no-console
            console.error('Upload error', file, error);
          }}
        />
      </section>

      <section className="space-y-4">
        <h2 className="text-lg font-semibold">Hoặc import từ URL</h2>
        <UrlImport
          onImportComplete={(result, response) => {
            // eslint-disable-next-line no-console
            console.log('URL import complete', result, response);
          }}
          onImportError={(error) => {
            // eslint-disable-next-line no-console
            console.error('URL import error', error);
          }}
        />
      </section>
    </div>
  );
}
