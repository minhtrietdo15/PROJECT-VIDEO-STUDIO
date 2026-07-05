'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Save, Trash2, Download } from 'lucide-react';

export interface ProjectSettingsPanelProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  project: {
    id: string;
    title: string;
    description?: string;
  };
  onSave?: (data: { title: string; description?: string }) => void;
  onDelete?: () => void;
  onExport?: () => void;
}

/**
 * Project settings panel for rename, delete, and export functionality.
 */
export function ProjectSettingsPanel({
  open,
  onOpenChange,
  project,
  onSave,
  onDelete,
  onExport,
}: ProjectSettingsPanelProps) {
  const [title, setTitle] = React.useState(project.title);
  const [description, setDescription] = React.useState(project.description || '');

  React.useEffect(() => {
    setTitle(project.title);
    setDescription(project.description || '');
  }, [project.title, project.description]);

  const handleSave = () => {
    onSave?.({ title, description });
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Project Settings</DialogTitle>
          <DialogDescription>
            Manage your project details and export options.
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="title">Project Name</Label>
            <Input
              id="title"
              value={title}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)}
              placeholder="Enter project name"
            />
          </div>

          <div className="grid gap-2">
            <Label htmlFor="description">Description (optional)</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setDescription(e.target.value)}
              placeholder="Project description"
              rows={3}
            />
          </div>
        </div>

        <DialogFooter className="flex-col gap-2 sm:flex-col">
          <div className="flex w-full gap-2">
            <Button variant="outline" size="sm" className="flex-1" onClick={onExport}>
              <Download className="mr-2 h-4 w-4" />
              Export Project
            </Button>
            <Button size="sm" className="flex-1" onClick={handleSave}>
              <Save className="mr-2 h-4 w-4" />
              Save Changes
            </Button>
          </div>

          <div className="w-full border-t pt-2">
            <Button
              variant="destructive"
              size="sm"
              className="w-full"
              onClick={onDelete}
            >
              <Trash2 className="mr-2 h-4 w-4" />
              Delete Project
            </Button>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}