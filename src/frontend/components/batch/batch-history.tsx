'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FileDown, Calendar, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

export interface BatchHistoryItem {
  id: string;
  batch_name: string;
  completed_at: string;
  duration: string;
  items_total: number;
  items_completed: number;
  items_failed: number;
  status: 'success' | 'partial' | 'failed';
}

export interface BatchHistoryProps {
  history: BatchHistoryItem[];
  onExport?: (batchId: string) => void;
  className?: string;
}

const statusIcons: Record<BatchHistoryItem['status'], React.ReactNode> = {
  success: <CheckCircle className="h-5 w-5 text-green-500" />,
  partial: <AlertCircle className="h-5 w-5 text-yellow-500" />,
  failed: <XCircle className="h-5 w-5 text-red-500" />,
};

export function BatchHistory({
  history,
  onExport,
  className,
}: BatchHistoryProps) {
  if (history.length === 0) {
    return (
      <div className={cn('text-center py-8 text-muted-foreground', className)}>
        No batch history yet. Completed batches will appear here.
      </div>
    );
  }

  return (
    <div className={cn('space-y-4', className)}>
      <h2 className="text-lg font-semibold">Batch History</h2>

      <div className="space-y-2">
        {history.map((item) => (
          <Card key={item.id}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {statusIcons[item.status]}
                  <div>
                    <div className="font-medium">{item.batch_name}</div>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        {item.completed_at}
                      </span>
                      <span>Duration: {item.duration}</span>
                      <span>
                        {item.items_completed}/{item.items_total} completed
                      </span>
                      {item.items_failed > 0 && (
                        <span className="text-red-500">
                          {item.items_failed} failed
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onExport?.(item.id)}
                >
                  <FileDown className="mr-2 h-4 w-4" />
                  Export Report
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}