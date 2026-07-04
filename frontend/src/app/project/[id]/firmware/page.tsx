'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Loader2, Copy, Download, Check } from 'lucide-react';
import { projectsAPI, exportAPI } from '@/lib/api';
import type { Project } from '@/types';

export default function FirmwarePage() {
  const params = useParams();
  const projectId = params.id as string;
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    loadProject();
  }, [projectId]);

  async function loadProject() {
    try {
      const res = await projectsAPI.get(projectId);
      setProject(res.data);
    } catch {} finally {
      setLoading(false);
    }
  }

  function copyCode() {
    if (project?.firmware_code) {
      navigator.clipboard.writeText(project.firmware_code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }

  if (loading) return <div className="flex items-center justify-center h-64"><Loader2 className="w-8 h-8 animate-spin" /></div>;
  if (!project) return <div className="p-6 text-muted-foreground">Project not found</div>;

  const firmware = project.firmware_code || '// No firmware generated yet';

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Firmware</h1>
          <p className="text-sm text-muted-foreground">Auto-generated firmware for your project</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={copyCode}
            className="inline-flex items-center gap-2 bg-secondary px-4 py-2 rounded-lg text-sm hover:bg-secondary/80"
          >
            {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
            {copied ? 'Copied!' : 'Copy Code'}
          </button>
          <a
            href={exportAPI.firmware(projectId)}
            className="inline-flex items-center gap-2 bg-secondary px-4 py-2 rounded-lg text-sm hover:bg-secondary/80"
          >
            <Download className="w-4 h-4" />
            Download
          </a>
        </div>
      </div>

      <div className="bg-card border border-border rounded-xl overflow-hidden">
        <div className="flex items-center gap-2 px-4 py-2 border-b border-border bg-secondary/30">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500/80" />
            <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
            <div className="w-3 h-3 rounded-full bg-green-500/80" />
          </div>
          <span className="text-xs text-muted-foreground ml-2 font-mono">firmware.ino</span>
        </div>
        <pre className="p-4 overflow-x-auto text-sm font-mono leading-relaxed max-h-[calc(100vh-16rem)] overflow-y-auto">
          <code>{firmware}</code>
        </pre>
      </div>
    </div>
  );
}
