'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Loader2, CheckCircle, AlertCircle, Clock } from 'lucide-react';
import { projectsAPI } from '@/lib/api';
import type { Project } from '@/types';

export default function ProjectOverviewPage() {
  const params = useParams();
  const projectId = params.id as string;
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProject();
    const interval = setInterval(loadProject, 5000);
    return () => clearInterval(interval);
  }, [projectId]);

  async function loadProject() {
    try {
      const res = await projectsAPI.get(projectId);
      setProject(res.data);
    } catch {} finally {
      setLoading(false);
    }
  }

  if (loading) return <div className="flex items-center justify-center h-64"><Loader2 className="w-8 h-8 animate-spin" /></div>;
  if (!project) return <div className="p-6 text-center text-muted-foreground">Project not found</div>;

  const statusConfig: Record<string, { icon: any; color: string; bg: string; animate?: boolean }> = {
    draft: { icon: Clock, color: 'text-muted-foreground', bg: 'bg-secondary' },
    generating: { icon: Loader2, color: 'text-yellow-400', bg: 'bg-yellow-500/10', animate: true },
    completed: { icon: CheckCircle, color: 'text-green-400', bg: 'bg-green-500/10' },
    error: { icon: AlertCircle, color: 'text-red-400', bg: 'bg-red-500/10' },
    archived: { icon: Clock, color: 'text-muted-foreground', bg: 'bg-secondary' },
  };

  const status = statusConfig[project.status] || statusConfig.draft;
  const StatusIcon = status.icon;

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">{project.name}</h1>
          <p className="text-sm text-muted-foreground mt-1">{project.description}</p>
        </div>
        <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full ${status.bg}`}>
          <StatusIcon className={`w-4 h-4 ${status.color} ${status.animate ? 'animate-spin' : ''}`} />
          <span className={`text-sm font-medium ${status.color}`}>{project.status}</span>
        </div>
      </div>

      {project.status === 'generating' && (
        <div className="p-6 bg-card border border-border rounded-xl text-center space-y-3">
          <Loader2 className="w-12 h-12 animate-spin text-primary mx-auto" />
          <h3 className="font-medium">Generating your project...</h3>
          <p className="text-sm text-muted-foreground">This may take 1-3 minutes. The AI is analyzing requirements, selecting components, and designing the circuit.</p>
        </div>
      )}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Components', value: project.components?.length || 0 },
          { label: 'Connections', value: project.connections?.length || 0 },
          { label: 'BOM Items', value: project.bom?.length || 0 },
          { label: 'Version', value: project.version },
        ].map((stat) => (
          <div key={stat.label} className="p-4 bg-card border border-border rounded-xl">
            <p className="text-2xl font-bold">{stat.value}</p>
            <p className="text-sm text-muted-foreground">{stat.label}</p>
          </div>
        ))}
      </div>

      {project.components?.length > 0 && (
        <div className="p-4 bg-card border border-border rounded-xl">
          <h3 className="font-medium mb-3">Selected Components</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {project.components.map((comp, i) => (
              <div key={i} className="flex items-center gap-3 p-3 bg-secondary rounded-lg">
                <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center text-xs font-mono text-primary">
                  {comp.ref}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm truncate">{comp.name}</p>
                  <p className="text-xs text-muted-foreground truncate">{comp.value} - {comp.package}</p>
                </div>
                <p className="text-sm font-mono">${comp.price?.toFixed(2)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {project.documentation && (
        <div className="p-4 bg-card border border-border rounded-xl">
          <h3 className="font-medium mb-3">Documentation</h3>
          <div className="prose prose-invert prose-sm max-w-none whitespace-pre-wrap text-sm">
            {project.documentation}
          </div>
        </div>
      )}
    </div>
  );
}
