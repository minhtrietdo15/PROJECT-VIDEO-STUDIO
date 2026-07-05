'use client';

import * as React from 'react';
import { WorkspaceShell } from '@/components/workspace/workspace-shell';
import { type PipelineStep } from '@/components/workspace/pipeline-stepper';

const PIPELINE_STEPS: PipelineStep[] = [
  { id: 'upload', label: 'Upload' },
  { id: 'transcript', label: 'Transcript' },
  { id: 'translation', label: 'Translation' },
  { id: 'dubbing', label: 'Dubbing' },
  { id: 'subtitle', label: 'Subtitles' },
  { id: 'branding', label: 'Branding' },
  { id: 'render', label: 'Render' },
  { id: 'publish', label: 'Publish' },
];

/**
 * Layout for project workspace pages.
 * Provides the workspace shell with stepper and sidebar.
 */
export default function WorkspaceLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { projectId: string };
}) {
  const [currentStep, setCurrentStep] = React.useState('upload');
  const [showSettings, setShowSettings] = React.useState(false);

  return (
    <WorkspaceShell
      steps={PIPELINE_STEPS}
      currentStep={currentStep}
      onStepChange={setCurrentStep}
      videoInfo={undefined}
      projectSettings={{
        title: 'Project Title',
        sourceLang: 'en',
        targetLang: 'vi',
      }}
      hasUnsavedChanges={false}
      onOpenSettings={() => setShowSettings(true)}
    >
      {children}
    </WorkspaceShell>
  );
}