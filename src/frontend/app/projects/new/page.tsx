'use client';

import { VideoUpload } from '@/components/upload/video-upload';

/**
 * New project page.
 *
 * Renders the VideoUpload component so users can upload a video file
 * as the first step of creating a project. The full project creation
 * flow (title, language selection, etc.) will be added in Phase 2.1.
 */
export default function NewProjectPage() {
  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Tạo project mới</h1>
        <p className="text-muted-foreground">
          Bắt đầu bằng cách upload video bạn muốn bản địa hóa.
        </p>
      </div>

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
    </div>
  );
}
