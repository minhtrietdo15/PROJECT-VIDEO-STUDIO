'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Pause, Play, Trash2, RefreshCw, Plus, GripVertical } from 'lucide-react';

export type BatchPriority = 'high' | 'normal' | 'low';

export interface BatchItem {
  id: string;
  project_id: string;
  project_name: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'paused';
  progress: number;
  priority: BatchPriority;
  eta?: string;
}

export interface BatchQueueManagerProps {
  items: BatchItem[];
  onAddProject?: () => void;
  onReorder?: (items: BatchItem[]) => void;
  onPauseResume?: (projectId: string) => void;
  onCancel?: (projectId: string) => void;
  onRetry?: (projectId: string) => void;
  onClearCompleted?: () => void;
  className?: string;
}

const priorityColors: Record<BatchPriority, string> = {
  high: 'border-red-500 bg-red-50',
  normal: 'border-blue-500 bg-blue-50',
  low: 'border-gray-300 bg-gray-50',
};

const statusColors: Record<BatchItem['status'], string> = {
  pending: 'bg-gray-400',
  running: 'bg-blue-500',
  completed: 'bg-green-500',
  failed: 'bg-red-500',
  paused: 'bg-yellow-500',
};

export function BatchQueueManager({
  items,
  onAddProject,
  onReorder,
  onPauseResume,
  onCancel,
  onRetry,
  onClearCompleted,
  className,
}: BatchQueueManagerProps) {
  return (
    <div className={cn('space-y-4', className)}>
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Batch Queue</h2>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={onClearCompleted}>
            <Trash2 className="mr-2 h-4 w-4" />
            Clear Completed
          </Button>
          <Button size="sm" onClick={onAddProject}>
            <Plus className="mr-2 h-4 w-4" />
            Add Projects
          </Button>
        </div>
      </div>

      <div className="space-y-2">
        {items.map((item) => (
          <Card key={item.id} className={priorityColors[item.priority]}>
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <div className="cursor-move">
                  <GripVertical className="h-4 w-4 text-muted-foreground" />
                </div>
                <div className={cn('h-2 w-2 rounded-full', statusColors[item.status])} />
                <div className="flex-1">
                  <div className="font-medium">{item.project_name}</div>
                  <div className="text-sm text-muted-foreground">
                    Status: {item.status} {item.eta && `| ETA: ${item.eta}`}
                  </div>
                </div>
                <div className="w-24">
                  <Progress value={item.progress} className="h-2" />
                </div>
                <div className="text-sm">{item.progress}%</div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onPauseResume?.(item.project_id)}
                >
                  {item.status === 'running' ? (
                    <Pause className="h-4 w-4" />
                  ) : (
                    <Play className="h-4 w-4" />
                  )}
                </Button>
                {item.status === 'failed' && (
                  <Button variant="ghost" size="sm" onClick={() => onRetry?.(item.project_id)}>
                    <RefreshCw className="h-4 w-4" />
                  </Button>
                )}
                <Button variant="ghost" size="sm" onClick={() => onCancel?.(item.project_id)}>
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

// Batch controls component
export interface BatchControlsProps {
  isPaused: boolean;
  onPauseAll?: () => void;
  onResumeAll?: () => void;
  isProcessing: boolean;
}

export function BatchControls({ isPaused, onPauseAll, onResumeAll, isProcessing }: BatchControlsProps) {
  return (
    <div className="flex items-center gap-2">
      {isPaused ? (
        <Button onClick={onResumeAll} disabled={!isProcessing}>
          <Play className="mr-2 h-4 w-4" />
          Resume All
        </Button>
      ) : (
        <Button onClick={onPauseAll} disabled={!isProcessing}>
          <Pause className="mr-2 h-4 w-4" />
          Pause All
        </Button>
      )}
    </div>
  );
}