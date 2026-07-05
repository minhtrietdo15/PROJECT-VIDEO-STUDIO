'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { PipelineStepper } from './pipeline-stepper';
import { ProjectSidebar, type VideoInfo, type ProjectSettings } from './project-sidebar';
import { AutoSaveIndicator } from './auto-save-indicator';

export interface WorkspaceShellProps {
  steps: Array<{ id: string; label: string; icon?: React.ReactNode; disabled?: boolean }>;
  currentStep: string;
  onStepChange?: (stepId: string) => void;
  videoInfo?: VideoInfo;
  projectSettings?: ProjectSettings;
  autoSaveStatus?: 'idle' | 'saving' | 'saved' | 'error';
  lastSaved?: Date | null;
  hasUnsavedChanges?: boolean;
  onOpenSettings?: () => void;
  children?: React.ReactNode;
  className?: string;
}

/**
 * Workspace shell layout combining stepper, sidebar, and content area.
 */
export function WorkspaceShell({
  steps,
  currentStep,
  onStepChange,
  videoInfo,
  projectSettings,
  autoSaveStatus = 'idle',
  lastSaved,
  hasUnsavedChanges = false,
  onOpenSettings,
  children,
  className,
}: WorkspaceShellProps) {
  return (
    <div className={cn('flex flex-col', className)}>
      {/* Pipeline Stepper */}
      <header className="border-b bg-background">
        <PipelineStepper
          steps={steps}
          currentStep={currentStep}
          onStepChange={onStepChange}
        />
      </header>

      {/* Main content area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Project Sidebar */}
        <ProjectSidebar
          videoInfo={videoInfo}
          settings={projectSettings}
          onOpenSettings={onOpenSettings}
        />

        {/* Content */}
        <main className="flex-1 overflow-y-auto">
          {/* Auto-save indicator */}
          {hasUnsavedChanges && (
            <div className="border-b bg-yellow-50 px-4 py-2">
              <AutoSaveIndicator status={autoSaveStatus} lastSaved={lastSaved} />
            </div>
          )}

          {/* Page content */}
          <div className="p-6">{children}</div>
        </main>
      </div>
    </div>
  );
}