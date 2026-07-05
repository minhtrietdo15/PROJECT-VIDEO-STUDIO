'use client';

/**
 * Project workspace page shell.
 * This is the main workspace page that uses the layout with stepper.
 */
export default function ProjectWorkspacePage({
  params,
}: {
  params: { projectId: string };
}) {
  return (
    <div className="flex h-full flex-col items-center justify-center gap-4">
      <h2 className="text-xl font-semibold">Project {params.projectId}</h2>
      <p className="text-muted-foreground">
        Select a step from the pipeline above to begin editing
      </p>
    </div>
  );
}
