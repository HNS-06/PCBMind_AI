'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Plus, FolderOpen, Clock, CheckCircle, AlertCircle, Trash2 } from 'lucide-react';
import { projectsAPI } from '@/lib/api';
import { formatDate } from '@/lib/utils';
import type { Project } from '@/types';

export default function DashboardPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    loadProjects();
  }, []);

  async function loadProjects() {
    try {
      const res = await projectsAPI.list();
      setProjects(res.data.projects);
      setTotal(res.data.total);
    } catch {
      setProjects([]);
    } finally {
      setLoading(false);
    }
  }

  async function deleteProject(id: string) {
    if (!confirm('Delete this project?')) return;
    try {
      await projectsAPI.delete(id);
      setProjects((prev) => prev.filter((p) => p.id !== id));
      setTotal((prev) => prev - 1);
    } catch {}
  }

  const statusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'generating': return <Clock className="w-4 h-4 text-yellow-400 animate-spin" />;
      case 'error': return <AlertCircle className="w-4 h-4 text-red-400" />;
      default: return <FolderOpen className="w-4 h-4 text-muted-foreground" />;
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-sm text-muted-foreground">{total} projects</p>
        </div>
        <Link
          href="/project/new"
          className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary/90"
        >
          <Plus className="w-4 h-4" />
          New Project
        </Link>
      </div>

      {loading ? (
        <div className="text-center py-20 text-muted-foreground">Loading projects...</div>
      ) : projects.length === 0 ? (
        <div className="text-center py-20 space-y-4">
          <FolderOpen className="w-16 h-16 mx-auto text-muted-foreground" />
          <h2 className="text-xl font-medium">No projects yet</h2>
          <p className="text-muted-foreground">Create your first AI-powered hardware project</p>
          <Link
            href="/project/new"
            className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-6 py-3 rounded-lg"
          >
            <Plus className="w-5 h-5" />
            Create Project
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((project) => (
            <Link
              key={project.id}
              href={`/project/${project.id}`}
              className="group p-4 bg-card border border-border rounded-xl hover:border-primary/50 transition-colors"
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-medium group-hover:text-primary transition-colors truncate flex-1">
                  {project.name}
                </h3>
                <div className="flex items-center gap-2 ml-2">
                  {statusIcon(project.status)}
                  <button
                    onClick={(e) => { e.preventDefault(); deleteProject(project.id); }}
                    className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-400 transition-all"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
              <p className="text-sm text-muted-foreground line-clamp-2 mb-3">{project.description}</p>
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>{project.components?.length || 0} components</span>
                <span>{formatDate(project.created_at)}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
