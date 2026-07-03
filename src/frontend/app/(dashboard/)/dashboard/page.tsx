'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ProjectList, type Project } from '@/components/dashboard/project-list';
import { CreateProjectDialog } from '@/components/dashboard/create-project-dialog';
import { WelcomeScreen } from '@/components/dashboard/welcome-screen';
import { Plus } from 'lucide-react';

const SAMPLE_PROJECTS: Project[] = [
  {
    id: '1',
    title: 'Product Demo EN → VI',
    status: 'completed',
    createdAt: '2026-07-01T08:00:00Z',
    updatedAt: '2026-07-02T10:30:00Z',
    sourceLang: 'en',
    targetLang: 'vi',
  },
  {
    id: '2',
    title: 'Tutorial Video JA → EN',
    status: 'processing',
    createdAt: '2026-07-02T09:00:00Z',
    updatedAt: '2026-07-02T11:00:00Z',
    sourceLang: 'ja',
    targetLang: 'en',
  },
  {
    id: '3',
    title: 'Marketing Clip KO → VI',
    status: 'draft',
    createdAt: '2026-07-03T07:00:00Z',
    updatedAt: '2026-07-03T07:15:00Z',
    sourceLang: 'ko',
    targetLang: 'vi',
  },
];

export default function DashboardPage() {
  const [projects, setProjects] = useState<Project[]>(SAMPLE_PROJECTS);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const handleCreate = (data: { name: string; sourceLang: string; targetLang: string }) => {
    const newProject: Project = {
      id: String(Date.now()),
      title: data.name,
      status: 'draft',
      sourceLang: data.sourceLang,
      targetLang: data.targetLang,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    setProjects((prev) => [newProject, ...prev]);
  };

  const handleDuplicate = (id: string) => {
    const project = projects.find((p) => p.id === id);
    if (!project) return;
    const copy: Project = {
      ...project,
      id: String(Date.now()),
      title: `${project.title} (Copy)`,
      status: 'draft',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    setProjects((prev) => [copy, ...prev]);
  };

  const handleDelete = (id: string) => {
    setProjects((prev) => prev.filter((p) => p.id !== id));
  };

  return (
    <div className="space-y-8">
      <header className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">Manage your video localization projects</p>
        </div>
        <CreateProjectDialog
          onCreate={handleCreate}
          trigger={
            <Button>
              <Plus className="h-4 w-4" />
              New Project
            </Button>
          }
        />
      </header>

      {projects.length === 0 ? (
        <WelcomeScreen onCreateProject={() => {}} />
      ) : (
        <ProjectList
          projects={projects}
          viewMode={viewMode}
          onViewModeChange={setViewMode}
          onContinue={(id) => console.log('Continue', id)}
          onDuplicate={handleDuplicate}
          onDelete={handleDelete}
        />
      )}
    </div>
  );
}
