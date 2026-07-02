'use client';

import * as React from 'react';
import { useCallback, useRef, useState } from 'react';
import { UploadCloud, FileVideo, X, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { apiClient, ApiClientError } from '@/lib/api-client';

export interface VideoUploadFile {
  id: string;
  file: File;
  name: string;
  size: number;
  progress: number;
  status: 'pending' | 'uploading' | 'success' | 'error';
  error?: string;
  videoId?: string;
}

export interface VideoUploadProps {
  projectId?: string;
  accept?: string;
  maxSize?: number; // bytes
  multiple?: boolean;
  onUploadComplete?: (file: VideoUploadFile, response?: unknown) => void;
  onUploadError?: (file: VideoUploadFile, error: ApiClientError) => void;
  className?: string;
}

const DEFAULT_ACCEPT = 'video/*';
const DEFAULT_MAX_SIZE = 2 * 1024 * 1024 * 1024; // 2GB

function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / k ** i).toFixed(2))} ${sizes[i]}`;
}

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

/**
 * Video upload component with drag & drop, file picker, and progress UI.
 *
 * Supports single or multiple video files, validates format/size, and uploads
 * to the backend `/api/v1/videos/upload` endpoint using multipart/form-data
 * with Axios onUploadProgress.
 */
export function VideoUpload({
  projectId,
  accept = DEFAULT_ACCEPT,
  maxSize = DEFAULT_MAX_SIZE,
  multiple = false,
  onUploadComplete,
  onUploadError,
  className,
}: VideoUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState<VideoUploadFile[]>([]);

  const updateFile = useCallback((id: string, patch: Partial<VideoUploadFile>) => {
    setFiles((prev) =>
      prev.map((item) => (item.id === id ? { ...item, ...patch } : item))
    );
  }, []);

  const removeFile = useCallback((id: string) => {
    setFiles((prev) => prev.filter((item) => item.id !== id));
  }, []);

  const validateFile = useCallback(
    (file: File): string | null => {
      if (!file.type.startsWith('video/')) {
        return 'File không phải định dạng video.';
      }
      if (file.size > maxSize) {
        return `File vượt quá dung lượng tối đa ${formatBytes(maxSize)}.`;
      }
      return null;
    },
    [maxSize]
  );

  const uploadFile = useCallback(
    async (uploadFile: VideoUploadFile) => {
      updateFile(uploadFile.id, { status: 'uploading', progress: 0, error: undefined });

      const formData = new FormData();
      formData.append('file', uploadFile.file);
      if (projectId) {
        formData.append('project_id', projectId);
      }

      try {
        const response = await apiClient.post('/api/v1/videos/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: (event) => {
            const progress = event.total
              ? Math.round((event.loaded * 100) / event.total)
              : 0;
            updateFile(uploadFile.id, { progress });
          },
        });

        const updated: VideoUploadFile = {
          ...uploadFile,
          status: 'success',
          progress: 100,
          videoId: (response as { id?: string })?.id,
        };
        updateFile(uploadFile.id, updated);
        onUploadComplete?.(updated, response);
      } catch (error) {
        const err =
          error instanceof ApiClientError
            ? error
            : new ApiClientError(
                error instanceof Error ? error.message : 'Upload failed',
                'UPLOAD_ERROR',
                0
              );
        const updated: VideoUploadFile = {
          ...uploadFile,
          status: 'error',
          error: err.message,
        };
        updateFile(uploadFile.id, updated);
        onUploadError?.(updated, err);
      }
    },
    [projectId, updateFile, onUploadComplete, onUploadError]
  );

  const handleFiles = useCallback(
    (incoming: FileList | null) => {
      if (!incoming) return;

      const newFiles: VideoUploadFile[] = Array.from(incoming)
        .slice(0, multiple ? undefined : 1)
        .map((file) => {
          const error = validateFile(file);
          return {
            id: generateId(),
            file,
            name: file.name,
            size: file.size,
            progress: 0,
            status: error ? 'error' : 'pending',
            error: error || undefined,
          };
        });

      setFiles((prev) => (multiple ? [...prev, ...newFiles] : newFiles));

      newFiles
        .filter((item) => item.status === 'pending')
        .forEach((item) => void uploadFile(item));
    },
    [multiple, validateFile, uploadFile]
  );

  const onDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(true);
  }, []);

  const onDragLeave = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      event.stopPropagation();
      setIsDragging(false);
      handleFiles(event.dataTransfer.files);
    },
    [handleFiles]
  );

  const onInputChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      handleFiles(event.target.files);
      if (inputRef.current) {
        inputRef.current.value = '';
      }
    },
    [handleFiles]
  );

  const openFilePicker = useCallback(() => {
    inputRef.current?.click();
  }, []);

  return (
    <div className={cn('space-y-4', className)}>
      <div
        role="button"
        tabIndex={0}
        aria-label="Kéo thả video vào đây hoặc nhấn để chọn file"
        onClick={openFilePicker}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onKeyDown={(event) => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            openFilePicker();
          }
        }}
        className={cn(
          'flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed p-8 text-center transition-colors',
          isDragging
            ? 'border-primary bg-primary/5'
            : 'border-border bg-background hover:bg-accent/50'
        )}
      >
        <input
          ref={inputRef}
          type="file"
          accept={accept}
          multiple={multiple}
          className="hidden"
          onChange={onInputChange}
        />
        <div className="mb-4 rounded-full bg-primary/10 p-4">
          <UploadCloud className="h-8 w-8 text-primary" />
        </div>
        <p className="text-sm font-medium">
          Kéo thả video vào đây hoặc{' '}
          <span className="text-primary">chọn file</span>
        </p>
        <p className="mt-1 text-xs text-muted-foreground">
          Hỗ trợ MP4, MOV, MKV... tối đa {formatBytes(maxSize)}
          {multiple ? ' (có thể chọn nhiều file)' : ''}
        </p>
      </div>

      {files.length > 0 && (
        <ul className="space-y-3">
          {files.map((item) => (
            <li
              key={item.id}
              className={cn(
                'flex items-center gap-3 rounded-lg border p-3',
                item.status === 'error' && 'border-destructive/50 bg-destructive/5',
                item.status === 'success' && 'border-green-500/50 bg-green-500/5'
              )}
            >
              <FileVideo className="h-5 w-5 shrink-0 text-muted-foreground" />
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium">{item.name}</p>
                <p className="text-xs text-muted-foreground">
                  {formatBytes(item.size)}
                </p>
                {item.status === 'uploading' && (
                  <div className="mt-2">
                    <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
                      <div
                        className="h-full bg-primary transition-all"
                        style={{ width: `${item.progress}%` }}
                      />
                    </div>
                    <p className="mt-1 text-xs text-muted-foreground">
                      {item.progress}%
                    </p>
                  </div>
                )}
                {item.status === 'error' && item.error && (
                  <p className="mt-1 text-xs text-destructive">{item.error}</p>
                )}
                {item.status === 'success' && (
                  <p className="mt-1 text-xs text-green-600">Tải lên thành công</p>
                )}
              </div>
              {item.status === 'uploading' && (
                <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
              )}
              <Button
                type="button"
                variant="ghost"
                size="icon"
                aria-label="Xoá file"
                onClick={() => removeFile(item.id)}
              >
                <X className="h-4 w-4" />
              </Button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
