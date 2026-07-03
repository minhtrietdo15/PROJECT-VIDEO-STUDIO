'use client';

import * as React from 'react';
import { useState, useMemo } from 'react';
import { LayoutGrid, List, Search, Play, Copy, Trash2, Clock, Calendar } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export interface Project {
  id: string;
  title: string;
  status: 'draft' | 'processing' | 'completed' | 'error';
  thumbnailUrl?: string;
  createdAt: string;
  updatedAt: string;
  sourceLang: string;
  targetLang: string;
}

export interface ProjectListProps {
  projects?: Project[];
  viewMode?: 'grid' | 'list';
  onViewModeChange?: (mode: 'grid' | 'list') => void;
  onContinue?: (projectId: string) => void;
  onDuplicate?: (projectId: string) => void;
  onDelete?: (projectId: string) => void;
  className?: string;
}

const STATUS_LABELS: Record<string, string> = {
  draft: 'Draft',
  processing: 'Processing',
  completed: 'Completed',
  error: 'Error',
};

const STATUS_COLORS: Record<string, string> = {
  draft: 'bg-muted text-muted-foreground',
  processing: 'bg-blue-100 text-blue-700',
  completed: 'bg-green-100 text-green-700',
  error: 'bg-red-100 text-red-700',
};

export function ProjectList({
  projects = [],
  viewMode = 'grid',
  onViewModeChange,
  onContinue,
  onDuplicate,
  onDelete,
  className,
}: ProjectListProps) {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'name' | 'created' | 'updated'>('updated');

  const filteredProjects = useMemo(() => {
    let result = [...projects];

    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(
        (p) =>
          p.title.toLowerCase().includes(q) ||
          p.sourceLang.toLowerCase().includes(q) ||
          p.targetLang.toLowerCase().includes(q)
      );
    }

    if (statusFilter !== 'all') {
      result = result.filter((p) => p.status === statusFilter);
    }

    result.sort((a, b) => {
      if (sortBy === 'name') return a.title.localeCompare(b.title);
      if (sortBy === 'created') return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
      return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
    });

    return result;
  }, [projects, search, statusFilter, sortBy]);

  return (
    <div className={cn('space-y-4', className)}>
      {/* Toolbar */}
      <div className="flex flex-wrap items-center gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search projects..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>

        <select
          value={statusFilter}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setStatusFilter(e.target.value)}
          className="rounded border px-2 py-1.5 text-sm"
        >
          <option value="all">All statuses</option>
          <option value="draft">Draft</option>
          <option value="processing">Processing</option>
          <option value="completed">Completed</option>
          <option value="error">Error</option>
        </select>

        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
          className="rounded border px-2 py-1.5 text-sm"
        >
          <option value="updated">Sort by updated</option>
          <option value="created">Sort by created</option>
          <option value="name">Sort by name</option>
        </select>

        <div className="flex rounded border">
          <button
            type="button"
            onClick={() => onViewModeChange?.('grid')}
            className={cn('px-3 py-1.5', viewMode === 'grid' && 'bg-primary text-primary-foreground')}
            aria-label="Grid view"
          >
            <LayoutGrid className="h-4 w-4" />
          </button>
          <button
            type="button"
            onClick={() => onViewModeChange?.('list')}
            className={cn('px-3 py-1.5', viewMode === 'list' && 'bg-primary text-primary-foreground')}
            aria-label="List view"
          >
            <List className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Empty state */}
      {filteredProjects.length === 0 && (
        <div className="rounded-lg border border-dashed p-8 text-center text-sm text-muted-foreground">
          No projects found.
        </div>
      )}

      {/* Grid view */}
      {viewMode === 'grid' && filteredProjects.length > 0 && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filteredProjects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onContinue={onContinue}
              onDuplicate={onDuplicate}
              onDelete={onDelete}
            />
          ))}
        </div>
      )}

      {/* List view */}
      {viewMode === 'list' && filteredProjects.length > 0 && (
        <div className="space-y-2">
          {filteredProjects.map((project) => (
            <ProjectRow
              key={project.id}
              project={project}
              onContinue={onContinue}
              onDuplicate={onDuplicate}
              onDelete={onDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function ProjectCard({
  project,
  onContinue,
  onDuplicate,
  onDelete,
}: {
  project: Project;
  onContinue?: (id: string) => void;
  onDuplicate?: (id: string) => void;
  onDelete?: (id: string) => void;
}) {
  return (
    <div className="group rounded-lg border bg-background p-3 shadow-sm transition-shadow hover:shadow-md">
      <div className="mb-3 aspect-video overflow-hidden rounded-md bg-muted">
        {project.thumbnailUrl ? (
          <img
            src={project.thumbnailUrl}
            alt={project.title}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-xs text-muted-foreground">
            No thumbnail
          </div>
        )}
      </div>

      <div className="mb-2 flex items-start justify-between gap-2">
        <h3 className="line-clamp-1 font-medium">{project.title}</h3>
        <span className={cn('rounded px-2 py-0.5 text-xs', STATUS_COLORS[project.status])}>
          {STATUS_LABELS[project.status]}
        </span>
      </div>

      <div className="mb-3 flex items-center gap-3 text-xs text-muted-foreground">
        <span className="flex items-center gap-1">
          <Calendar className="h-3 w-3" />
          {new Date(project.updatedAt).toLocaleDateString()}
        </span>
        <span>
          {project.sourceLang} → {project.targetLang}
        </span>
      </div>

      <div className="flex gap-2">
        <Button size="sm" variant="outline" className="flex-1" onClick={() => onContinue?.(project.id)}>
          <Play className="mr-1 h-3 w-3" />
          Continue
        </Button>
        <Button size="sm" variant="ghost" onClick={() => onDuplicate?.(project.id)} aria-label="Duplicate">
          <Copy className="h-4 w-4" />
        </Button>
        <Button size="sm" variant="ghost" onClick={() => onDelete?.(project.id)} aria-label="Delete">
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}

function ProjectRow({
  project,
  onContinue,
  onDuplicate,
  onDelete,
}: {
  project: Project;
  onContinue?: (id: string) => void;
  onDuplicate?: (id: string) => void;
  onDelete?: (id: string) => void;
}) {
  return (
    <div className="flex items-center gap-4 rounded-lg border bg-background p-3 shadow-sm">
      <div className="h-16 w-24 flex-shrink-0 overflow-hidden rounded-md bg-muted">
        {project.thumbnailUrl ? (
          <img
            src={project.thumbnailUrl}
            alt={project.title}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-xs text-muted-foreground">
            No thumbnail
          </div>
        )}
      </div>

      <div className="min-w-0 flex-1">
        <h3 className="truncate font-medium">{project.title}</h3>
        <div className="flex items-center gap-3 text-xs text-muted-foreground">
          <span className={cn('rounded px-2 py-0.5', STATUS_COLORS[project.status])}>
            {STATUS_LABELS[project.status]}
          </span>
          <span className="flex items-center gap-1">
            <Clock className="h-3 w-3" />
            {new Date(project.updatedAt).toLocaleDateString()}
          </span>
          <span>
            {project.sourceLang} → {project.targetLang}
          </span>
        </div>
      </div>

      <div className="flex gap-2">
        <Button size="sm" variant="outline" onClick={() => onContinue?.(project.id)}>
          <Play className="mr-1 h-3 w-3" />
          Continue
        </Button>
        <Button size="sm" variant="ghost" onClick={() => onDuplicate?.(project.id)} aria-label="Duplicate">
          <Copy className="h-4 w-4" />
        </Button>
        <Button size="sm" variant="ghost" onClick={() => onDelete?.(project.id)} aria-label="Delete">
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
