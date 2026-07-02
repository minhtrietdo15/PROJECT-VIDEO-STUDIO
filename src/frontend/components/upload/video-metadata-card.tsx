'use client';

import * as React from 'react';
import { useMemo } from 'react';
import {
  Clock,
  MonitorPlay,
  Gauge,
  HardDrive,
  FileType,
  Music,
  Volume2,
  Calendar,
  AlertCircle,
  ImageOff,
} from 'lucide-react';
import { cn, formatBytes } from '@/lib/utils';
import { Skeleton } from '@/components/ui/loading-skeleton';

/**
 * Enriched video metadata returned by the backend.
 *
 * Mirrors the `VideoMetadataResponse` Pydantic schema from
 * `src/backend/app/schemas/video.py`.
 */
export interface VideoMetadata {
  id: string;
  project_id: string;
  filename: string;
  duration_seconds?: number | null;
  duration_formatted?: string | null;
  resolution?: string | null;
  width?: number | null;
  height?: number | null;
  fps?: number | null;
  file_size_bytes?: number | null;
  file_size_formatted?: string | null;
  codec?: string | null;
  audio_codec?: string | null;
  audio_channels?: number | null;
  audio_sample_rate?: number | null;
  thumbnail_url?: string | null;
  created_at?: string | null;
}

export interface VideoMetadataCardProps {
  metadata: VideoMetadata | null | undefined;
  isLoading?: boolean;
  error?: string | null;
  className?: string;
}

/**
 * Format a duration in seconds as HH:MM:SS or MM:SS.
 *
 * Falls back to the backend-provided `duration_formatted` when available.
 */
function formatDuration(seconds: number | null | undefined): string | null {
  if (seconds === undefined || seconds === null || Number.isNaN(seconds)) {
    return null;
  }

  const totalSeconds = Math.floor(seconds);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const secs = totalSeconds % 60;

  const pad = (n: number) => n.toString().padStart(2, '0');

  if (hours > 0) {
    return `${hours}:${pad(minutes)}:${pad(secs)}`;
  }
  return `${minutes}:${pad(secs)}`;
}

/**
 * Resolve a thumbnail URL that may be a relative backend path.
 *
 * If the URL is already absolute, return it as-is. Otherwise prepend the
 * API base URL so it works in both client and server contexts.
 */
function resolveThumbnailUrl(url: string | null | undefined): string | null {
  if (!url) return null;
  if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
    return url;
  }
  const base =
    process.env.NEXT_PUBLIC_API_URL ||
    (typeof window === 'undefined' ? 'http://backend:8000' : '');
  // When no env is set in the browser, use the same origin (Next.js proxy).
  return `${base}${url}`;
}

/**
 * Presentational metadata row.
 *
 * Renders an icon, label, and value in a compact, accessible layout.
 */
function MetadataRow({
  icon: Icon,
  label,
  value,
  className,
}: {
  icon: React.ElementType;
  label: string;
  value: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn('flex items-start gap-3', className)}>
      <div className="mt-0.5 shrink-0 rounded-md bg-muted p-1.5">
        <Icon className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
      </div>
      <div className="min-w-0 flex-1">
        <p className="text-xs text-muted-foreground">{label}</p>
        <p className="truncate text-sm font-medium">{value}</p>
      </div>
    </div>
  );
}

/**
 * Loading skeleton for the metadata card.
 */
function VideoMetadataCardSkeleton() {
  return (
    <div className="rounded-xl border bg-card p-4 shadow-sm">
      <Skeleton className="aspect-video w-full rounded-lg" />
      <div className="mt-4 space-y-3">
        <Skeleton className="h-5 w-3/4" />
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <Skeleton className="h-12 w-full" />
          <Skeleton className="h-12 w-full" />
          <Skeleton className="h-12 w-full" />
          <Skeleton className="h-12 w-full" />
        </div>
      </div>
    </div>
  );
}

/**
 * Error state for the metadata card.
 */
function VideoMetadataCardError({ message }: { message: string }) {
  return (
    <div className="rounded-xl border border-destructive/50 bg-destructive/5 p-4">
      <div className="flex items-start gap-3">
        <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-destructive" />
        <div>
          <p className="text-sm font-medium text-destructive">
            Không thể tải thông tin video
          </p>
          <p className="text-xs text-destructive/80">{message}</p>
        </div>
      </div>
    </div>
  );
}

/**
 * Video metadata display card.
 *
 * Displays a thumbnail alongside structured metadata returned from the
 * backend: duration, resolution, fps, codec, file size, audio info, etc.
 *
 * The component is purely presentational; data fetching is handled by the
 * parent or by a separate container hook.
 */
export function VideoMetadataCard({
  metadata,
  isLoading = false,
  error = null,
  className,
}: VideoMetadataCardProps) {
  const thumbnailUrl = useMemo(
    () => resolveThumbnailUrl(metadata?.thumbnail_url),
    [metadata?.thumbnail_url]
  );

  const duration = useMemo(
    () => metadata?.duration_formatted ?? formatDuration(metadata?.duration_seconds),
    [metadata?.duration_formatted, metadata?.duration_seconds]
  );

  const fileSize = useMemo(
    () =>
      metadata?.file_size_formatted ??
      (metadata?.file_size_bytes != null
        ? formatBytes(metadata.file_size_bytes)
        : null),
    [metadata?.file_size_formatted, metadata?.file_size_bytes]
  );

  const resolution = useMemo(
    () =>
      metadata?.resolution ??
      (metadata?.width && metadata?.height
        ? `${metadata.width}x${metadata.height}`
        : null),
    [metadata?.resolution, metadata?.width, metadata?.height]
  );

  if (isLoading) {
    return <VideoMetadataCardSkeleton />;
  }

  if (error) {
    return <VideoMetadataCardError message={error} />;
  }

  if (!metadata) {
    return null;
  }

  return (
    <div
      className={cn(
        'overflow-hidden rounded-xl border bg-card text-card-foreground shadow-sm',
        className
      )}
    >
      {/* Thumbnail */}
      <div className="relative aspect-video w-full bg-muted">
        {thumbnailUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={thumbnailUrl}
            alt={`Thumbnail của ${metadata.filename}`}
            className="h-full w-full object-cover"
            loading="lazy"
            onError={(event) => {
              // Replace broken thumbnails with the placeholder state
              const target = event.currentTarget;
              target.style.display = 'none';
              const placeholder = target.nextElementSibling as HTMLElement | null;
              if (placeholder) placeholder.style.display = 'flex';
            }}
          />
        ) : null}
        <div
          className={cn(
            'absolute inset-0 flex flex-col items-center justify-center gap-2 text-muted-foreground',
            thumbnailUrl ? 'hidden' : 'flex'
          )}
        >
          <ImageOff className="h-10 w-10" aria-hidden="true" />
          <span className="text-xs">Chưa có thumbnail</span>
        </div>
      </div>

      {/* Metadata body */}
      <div className="p-4 sm:p-5">
        <h3 className="truncate text-base font-semibold sm:text-lg" title={metadata.filename}>
          {metadata.filename}
        </h3>

        <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
          {duration && (
            <MetadataRow icon={Clock} label="Thời lượng" value={duration} />
          )}
          {resolution && (
            <MetadataRow
              icon={MonitorPlay}
              label="Độ phân giải"
              value={resolution}
            />
          )}
          {metadata.fps != null && (
            <MetadataRow icon={Gauge} label="FPS" value={`${metadata.fps}`} />
          )}
          {fileSize && (
            <MetadataRow icon={HardDrive} label="Dung lượng" value={fileSize} />
          )}
          {metadata.codec && (
            <MetadataRow icon={FileType} label="Codec video" value={metadata.codec} />
          )}
          {metadata.audio_codec && (
            <MetadataRow
              icon={Music}
              label="Codec âm thanh"
              value={metadata.audio_codec}
            />
          )}
          {metadata.audio_channels != null && (
            <MetadataRow
              icon={Volume2}
              label="Kênh âm thanh"
              value={`${metadata.audio_channels} kênh`}
            />
          )}
          {metadata.audio_sample_rate != null && (
            <MetadataRow
              icon={Volume2}
              label="Sample rate"
              value={`${metadata.audio_sample_rate} Hz`}
            />
          )}
          {metadata.created_at && (
            <MetadataRow
              icon={Calendar}
              label="Tạo lúc"
              value={new Date(metadata.created_at).toLocaleString('vi-VN')}
            />
          )}
        </div>

        {metadata.id && (
          <p className="mt-4 text-xs text-muted-foreground">
            ID: <span className="font-mono">{metadata.id}</span>
          </p>
        )}
      </div>
    </div>
  );
}
