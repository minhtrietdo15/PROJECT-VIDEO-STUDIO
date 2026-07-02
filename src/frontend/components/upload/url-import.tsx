'use client';

import * as React from 'react';
import { useState, useCallback } from 'react';
import { Link2, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { apiClient, ApiClientError } from '@/lib/api-client';

export interface UrlImportResult {
  id: string;
  projectId: string;
  filename: string;
  taskId: string;
  status: string;
}

export interface UrlImportProps {
  projectId?: string;
  onImportComplete?: (result: UrlImportResult, response?: unknown) => void;
  onImportError?: (error: ApiClientError) => void;
  className?: string;
}

interface UrlImportState {
  url: string;
  filename: string;
  status: 'idle' | 'loading' | 'success' | 'error';
  error: string | null;
  result: UrlImportResult | null;
}

const INITIAL_STATE: UrlImportState = {
  url: '',
  filename: '',
  status: 'idle',
  error: null,
  result: null,
};

/**
 * Validate a URL string.
 *
 * Accepts http:// and https:// schemes with a non-empty host.
 * Returns a human-readable error message or null when valid.
 */
export function validateUrl(value: string): string | null {
  const trimmed = value.trim();
  if (!trimmed) {
    return 'Vui lòng nhập URL video.';
  }

  try {
    const parsed = new URL(trimmed);
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      return 'URL phải bắt đầu bằng http:// hoặc https://.';
    }
    if (!parsed.hostname || parsed.hostname.includes(' ')) {
      return 'URL không hợp lệ.';
    }
    return null;
  } catch {
    return 'URL không đúng định dạng.';
  }
}

/**
 * Extract a default filename from a URL path.
 */
function deriveFilenameFromUrl(url: string): string {
  try {
    const pathname = new URL(url.trim()).pathname;
    const basename = pathname.split('/').pop();
    if (basename && basename.includes('.')) {
      return basename;
    }
  } catch {
    // ignore
  }
  return '';
}

/**
 * URL import form for downloading videos from a remote URL.
 *
 * Presentation is separated from submission logic via the internal
 * `UrlImportForm` component. The container handles validation, API
 * integration preparation, and state management.
 */
export function UrlImport({
  projectId,
  onImportComplete,
  onImportError,
  className,
}: UrlImportProps) {
  const [state, setState] = useState<UrlImportState>(INITIAL_STATE);

  const setUrl = useCallback((url: string) => {
    setState((prev) => ({
      ...prev,
      url,
      error: null,
      status: prev.status === 'error' ? 'idle' : prev.status,
    }));
  }, []);

  const setFilename = useCallback((filename: string) => {
    setState((prev) => ({ ...prev, filename }));
  }, []);

  const reset = useCallback(() => {
    setState(INITIAL_STATE);
  }, []);

  const handleSubmit = useCallback(
    async (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();

      const urlError = validateUrl(state.url);
      if (urlError) {
        setState((prev) => ({ ...prev, status: 'error', error: urlError }));
        return;
      }

      setState((prev) => ({
        ...prev,
        status: 'loading',
        error: null,
        result: null,
      }));

      const formData = new URLSearchParams();
      formData.append('url', state.url.trim());
      if (state.filename.trim()) {
        formData.append('filename', state.filename.trim());
      }

      try {
        const targetProjectId = projectId || 'new';
        const response = (await apiClient.post(
          `/api/v1/videos/${targetProjectId}/import-url`,
          formData.toString(),
          {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          }
        )) as {
          id: string;
          project_id: string;
          filename: string;
          task_id: string;
          status: string;
        };

        const result: UrlImportResult = {
          id: response.id,
          projectId: response.project_id,
          filename: response.filename,
          taskId: response.task_id,
          status: response.status,
        };

        setState((prev) => ({
          ...prev,
          status: 'success',
          result,
        }));
        onImportComplete?.(result, response);
      } catch (error) {
        const err =
          error instanceof ApiClientError
            ? error
            : new ApiClientError(
                error instanceof Error ? error.message : 'Import failed',
                'IMPORT_ERROR',
                0
              );
        setState((prev) => ({
          ...prev,
          status: 'error',
          error: err.message,
        }));
        onImportError?.(err);
      }
    },
    [state.url, state.filename, projectId, onImportComplete, onImportError]
  );

  const autoFillFilename = useCallback(() => {
    const derived = deriveFilenameFromUrl(state.url);
    if (derived) {
      setState((prev) => ({ ...prev, filename: derived }));
    }
  }, [state.url]);

  return (
    <UrlImportForm
      url={state.url}
      filename={state.filename}
      status={state.status}
      error={state.error}
      result={state.result}
      onUrlChange={setUrl}
      onFilenameChange={setFilename}
      onAutoFillFilename={autoFillFilename}
      onSubmit={handleSubmit}
      onReset={reset}
      className={className}
    />
  );
}

interface UrlImportFormProps {
  url: string;
  filename: string;
  status: UrlImportState['status'];
  error: string | null;
  result: UrlImportResult | null;
  onUrlChange: (url: string) => void;
  onFilenameChange: (filename: string) => void;
  onAutoFillFilename: () => void;
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
  onReset: () => void;
  className?: string;
}

/**
 * Presentational URL import form.
 *
 * Renders an accessible form with validation feedback, loading state,
 * disabled state while submitting, and success/error messages.
 */
function UrlImportForm({
  url,
  filename,
  status,
  error,
  result,
  onUrlChange,
  onFilenameChange,
  onAutoFillFilename,
  onSubmit,
  onReset,
  className,
}: UrlImportFormProps) {
  const isLoading = status === 'loading';
  const isSuccess = status === 'success';
  const isError = status === 'error';
  const isDisabled = isLoading || isSuccess;

  return (
    <div className={cn('space-y-4', className)}>
      <form onSubmit={onSubmit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <label
            htmlFor="video-url"
            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            URL video
          </label>
          <div className="relative">
            <input
              id="video-url"
              name="video-url"
              type="url"
              inputMode="url"
              autoComplete="url"
              placeholder="https://example.com/video.mp4"
              value={url}
              onChange={(event) => onUrlChange(event.target.value)}
              onBlur={onAutoFillFilename}
              disabled={isDisabled}
              aria-invalid={isError}
              aria-describedby={
                isError ? 'url-error' : 'url-help'
              }
              className={cn(
                'flex h-10 w-full rounded-md border bg-background px-3 py-2 pl-10 text-sm ring-offset-background transition-colors',
                'placeholder:text-muted-foreground',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
                'disabled:cursor-not-allowed disabled:opacity-50',
                isError
                  ? 'border-destructive focus-visible:ring-destructive'
                  : 'border-input'
              )}
            />
            <Link2 className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          </div>
          <p id="url-help" className="text-xs text-muted-foreground">
            Hỗ trợ link trực tiếp đến file video (MP4, MOV, MKV...)
          </p>
          {isError && error && (
            <p
              id="url-error"
              className="flex items-center gap-1.5 text-xs text-destructive"
              role="alert"
            >
              <AlertCircle className="h-3.5 w-3.5" />
              {error}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <label
            htmlFor="video-filename"
            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            Tên file (tùy chọn)
          </label>
          <input
            id="video-filename"
            name="video-filename"
            type="text"
            placeholder="video.mp4"
            value={filename}
            onChange={(event) => onFilenameChange(event.target.value)}
            disabled={isDisabled}
            className={cn(
              'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background transition-colors',
              'placeholder:text-muted-foreground',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
              'disabled:cursor-not-allowed disabled:opacity-50'
            )}
          />
        </div>

        <Button
          type="submit"
          disabled={isDisabled}
          className="w-full sm:w-auto"
        >
          {isLoading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Đang xử lý...
            </>
          ) : (
            <>
              <Link2 className="h-4 w-4" />
              Import từ URL
            </>
          )}
        </Button>
      </form>

      {isSuccess && result && (
        <div className="rounded-lg border border-green-500/50 bg-green-500/5 p-4">
          <div className="flex items-start gap-3">
            <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-green-600" />
            <div className="flex-1 space-y-1">
              <p className="text-sm font-medium text-green-700">
                Đã bắt đầu tải video
              </p>
              <p className="text-xs text-green-600">
                File <span className="font-medium">{result.filename}</span>{' '}
                đang được tải xuống. Task ID:{' '}
                <span className="font-mono">{result.taskId}</span>
              </p>
            </div>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={onReset}
            >
              Import khác
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
