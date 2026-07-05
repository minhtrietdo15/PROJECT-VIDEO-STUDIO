'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

export interface ErrorDetailModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title?: string;
  error: Error | string | null;
  stackTrace?: string;
  onRetry?: () => void;
}

export function ErrorDetailModal({
  open,
  onOpenChange,
  title = 'An error occurred',
  error,
  stackTrace,
  onRetry,
}: ErrorDetailModalProps) {
  const errorMessage = typeof error === 'string' ? error : error?.message || '';
  const [showStackTrace, setShowStackTrace] = React.useState(false);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription className="mt-2">
            {errorMessage}
          </DialogDescription>
        </DialogHeader>

        {stackTrace && (
          <div className="mt-4">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowStackTrace(!showStackTrace)}
            >
              {showStackTrace ? 'Hide' : 'Show'} Stack Trace
            </Button>

            {showStackTrace && (
              <pre className="mt-2 max-h-60 overflow-y-auto rounded bg-muted p-4 text-xs">
                <code>{stackTrace}</code>
              </pre>
            )}
          </div>
        )}

        <DialogFooter className="mt-4">
          {onRetry && (
            <Button variant="default" onClick={onRetry}>
              Retry
            </Button>
          )}
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Close
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}