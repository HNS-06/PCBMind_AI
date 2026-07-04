'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Loader2, Download, FileCode, FileText, Package, Cpu, Archive } from 'lucide-react';
import { projectsAPI, exportAPI } from '@/lib/api';
import type { Project } from '@/types';

export default function ExportPage() {
  const params = useParams();
  const projectId = params.id as string;
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);

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

  if (loading) return <div className="flex items-center justify-center h-64"><Loader2 className="w-8 h-8 animate-spin" /></div>;
  if (!project) return <div className="p-6 text-muted-foreground">Project not found</div>;

  const exportFormats = [
    {
      title: 'KiCad Project',
      description: 'Complete KiCad schematic and PCB files (.kicad_sch, .kicad_pcb)',
      icon: FileCode,
      url: exportAPI.kicad(projectId),
      filename: `${project.name}_kicad.zip`,
      color: 'text-blue-400',
    },
    {
      title: 'Gerber Files',
      description: 'Manufacturing files for PCB fabrication (.gtl, .gbl, .gts, .gbs, .drl)',
      icon: Package,
      url: exportAPI.gerber(projectId),
      filename: `${project.name}_gerber.zip`,
      color: 'text-green-400',
    },
    {
      title: 'Bill of Materials',
      description: 'Component list with pricing and supplier information (.csv)',
      icon: FileText,
      url: exportAPI.bom(projectId),
      filename: `${project.name}_bom.csv`,
      color: 'text-yellow-400',
    },
    {
      title: 'Firmware Source',
      description: 'Generated firmware code ready to compile and flash',
      icon: Cpu,
      url: exportAPI.firmware(projectId),
      filename: `${project.name}_firmware.py`,
      color: 'text-purple-400',
    },
    {
      title: 'Complete Archive',
      description: 'All project files in a single ZIP archive',
      icon: Archive,
      url: exportAPI.kicad(projectId),
      filename: `${project.name}_complete.zip`,
      color: 'text-orange-400',
    },
  ];

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Export Project</h1>
        <p className="text-sm text-muted-foreground">Download your project in various formats</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {exportFormats.map((fmt) => {
          const Icon = fmt.icon;
          return (
            <a
              key={fmt.title}
              href={fmt.url}
              download={fmt.filename}
              className="flex items-start gap-4 p-4 bg-card border border-border rounded-xl hover:border-primary/50 transition-colors group"
            >
              <div className={`p-3 bg-secondary rounded-lg ${fmt.color}`}>
                <Icon className="w-6 h-6" />
              </div>
              <div className="flex-1">
                <h3 className="font-medium group-hover:text-primary transition-colors">{fmt.title}</h3>
                <p className="text-sm text-muted-foreground mt-1">{fmt.description}</p>
              </div>
              <Download className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors" />
            </a>
          );
        })}
      </div>

      <div className="p-4 bg-card border border-border rounded-xl">
        <h3 className="font-medium mb-2">Manufacturing Notes</h3>
        <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
          <li>Gerber files are ready for upload to PCB manufacturers (JLCPCB, PCBWay, OSH Park)</li>
          <li>BOM file includes manufacturer part numbers for easy ordering from DigiKey, Mouser, or LCSC</li>
          <li>KiCad files can be opened in KiCad 7+ for further editing</li>
          <li>Review the PCB design in 3D viewer before manufacturing</li>
        </ul>
      </div>
    </div>
  );
}
