'use client';

import * as React from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient, ApiClientError } from '@/lib/api-client';
import {
  VideoMetadataCard,
  type VideoMetadata,
} from './video-metadata-card';

export interface VideoMetadataCardContainerProps {
  projectId: string;
  className?: string;
}

/**
 * Fetch enriched video metadata for a project.
 *
 * Calls the backend endpoint introduced in Phase 1.1:
 * GET /api/v1/videos/{project_id}/metadata
 */
async function fetchVideoMetadata(projectId: string): Promise<VideoMetadata> {
  const response = (await apiClient.get(
    `/api/v1/videos/${projectId}/metadata`
  )) as VideoMetadata;
  return response;
}

/**
 * Container component for the video metadata card.
 *
 * Handles data fetching via TanStack Query and delegates all rendering to
 * the presentational `VideoMetadataCard`. This keeps UI and business logic
 * separate and makes both pieces easy to test in isolation.
 */
export function VideoMetadataCardContainer({
  projectId,
  className,
}: VideoMetadataCardContainerProps) {
  const { data, isLoading, error } = useQuery<VideoMetadata, ApiClientError>({
    queryKey: ['video-metadata', projectId],
    queryFn: () => fetchVideoMetadata(projectId),
    enabled: Boolean(projectId),
  });

  const errorMessage = error
    ? error instanceof ApiClientError
      ? error.message
      : 'Đã xảy ra lỗi không xác định.'
    : null;

  return (
    <VideoMetadataCard
      metadata={data}
      isLoading={isLoading}
      error={errorMessage}
      className={className}
    />
  );
}
