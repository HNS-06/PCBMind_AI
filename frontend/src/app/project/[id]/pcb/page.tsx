'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'next/navigation';
import { Loader2, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';
import { projectsAPI } from '@/lib/api';
import type { Project, PCBData } from '@/types';

export default function PCBEditorPage() {
  const params = useParams();
  const projectId = params.id as string;
  const [project, setProject] = useState<Project | null>(null);
  const [pcbData, setPcbData] = useState<PCBData | null>(null);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [dragging, setDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [selectedComponent, setSelectedComponent] = useState<string | null>(null);

  useEffect(() => {
    loadProject();
  }, [projectId]);

  async function loadProject() {
    try {
      const res = await projectsAPI.get(projectId);
      setProject(res.data);
      setPcbData(res.data.pcb_data);
    } catch {}
  }

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -0.1 : 0.1;
    setZoom((z) => Math.max(0.2, Math.min(3, z + delta)));
  }, []);

  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button === 1 || e.button === 2) {
      setDragging(true);
      setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (dragging) {
      setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
    }
  };

  const handleMouseUp = () => setDragging(false);

  if (!project) return <div className="flex items-center justify-center h-64"><Loader2 className="w-8 h-8 animate-spin" /></div>;

  const board = pcbData?.board;
  const components = pcbData?.components || [];
  const tracks = pcbData?.tracks || [];
  const scale = 5 * zoom;

  return (
    <div className="flex h-[calc(100vh-7rem)]">
      <div className="flex-1 relative overflow-hidden bg-[#1a1a2e]"
        onWheel={handleWheel}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onContextMenu={(e) => e.preventDefault()}
      >
        <div className="absolute top-4 left-4 z-10 flex gap-2">
          <button onClick={() => setZoom((z) => Math.min(3, z + 0.2))} className="p-2 bg-card rounded-lg border border-border hover:bg-secondary">
            <ZoomIn className="w-4 h-4" />
          </button>
          <button onClick={() => setZoom((z) => Math.max(0.2, z - 0.2))} className="p-2 bg-card rounded-lg border border-border hover:bg-secondary">
            <ZoomOut className="w-4 h-4" />
          </button>
          <button onClick={() => { setZoom(1); setPan({ x: 0, y: 0 }); }} className="p-2 bg-card rounded-lg border border-border hover:bg-secondary">
            <RotateCcw className="w-4 h-4" />
          </button>
          <span className="p-2 text-xs text-muted-foreground bg-card rounded-lg border border-border">
            {Math.round(zoom * 100)}%
          </span>
        </div>

        <svg
          width="100%" height="100%"
          style={{ transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`, transformOrigin: 'center' }}
        >
          <g transform={`translate(50, 50)`}>
            {board && (
              <rect
                x={0} y={0}
                width={board.width_mm * scale}
                height={board.height_mm * scale}
                fill="none"
                stroke="#4a9eff"
                strokeWidth={1 / zoom}
                rx={2}
              />
            )}

            {tracks.map((track, i) => (
              <line
                key={i}
                x1={track.start.x * scale}
                y1={track.start.y * scale}
                x2={track.end.x * scale}
                y2={track.end.y * scale}
                stroke={track.layer === 'B.Cu' ? '#ff6b35' : '#4a9eff'}
                strokeWidth={track.width_mm * scale * 0.5}
                opacity={0.8}
              />
            ))}

            {components.map((comp) => {
              const isSelected = selectedComponent === comp.id;
              return (
                <g key={comp.id} transform={`translate(${comp.x * scale}, ${comp.y * scale})`}
                  onClick={() => setSelectedComponent(comp.id)}
                  style={{ cursor: 'pointer' }}
                >
                  <rect
                    x={-8} y={-6}
                    width={16} height={12}
                    fill={isSelected ? '#4a9eff33' : '#2a2a4a'}
                    stroke={isSelected ? '#4a9eff' : '#666'}
                    strokeWidth={isSelected ? 2 / zoom : 1 / zoom}
                    rx={1}
                  />
                  <text
                    x={0} y={1}
                    textAnchor="middle"
                    dominantBaseline="middle"
                    fill="#fff"
                    fontSize={6 / zoom}
                    fontFamily="monospace"
                  >
                    {comp.id}
                  </text>
                  <circle cx={-6} cy={-4} r={1 / zoom} fill="#4a9eff" />
                  <circle cx={6} cy={-4} r={1 / zoom} fill="#4a9eff" />
                  <circle cx={-6} cy={4} r={1 / zoom} fill="#4a9eff" />
                  <circle cx={6} cy={4} r={1 / zoom} fill="#4a9eff" />
                </g>
              );
            })}
          </g>
        </svg>
      </div>

      <div className="w-72 bg-card border-l border-border p-4 overflow-y-auto">
        <h3 className="font-medium mb-3">Properties</h3>
        {selectedComponent ? (
          <div className="space-y-3">
            {(() => {
              const comp = components.find((c) => c.id === selectedComponent);
              if (!comp) return null;
              return (
                <>
                  <div className="p-3 bg-secondary rounded-lg">
                    <p className="font-mono text-sm font-bold text-primary">{comp.id}</p>
                    <p className="text-xs text-muted-foreground mt-1">{comp.footprint}</p>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between"><span className="text-muted-foreground">X</span><span>{comp.x}mm</span></div>
                    <div className="flex justify-between"><span className="text-muted-foreground">Y</span><span>{comp.y}mm</span></div>
                    <div className="flex justify-between"><span className="text-muted-foreground">Layer</span><span>{comp.layer}</span></div>
                    <div className="flex justify-between"><span className="text-muted-foreground">Rotation</span><span>{comp.rotation}deg</span></div>
                  </div>
                </>
              );
            })()}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">Click a component to view properties</p>
        )}

        <div className="mt-6 space-y-3">
          <h3 className="font-medium mb-2">Board Info</h3>
          {board && (
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-muted-foreground">Size</span><span>{board.width_mm} x {board.height_mm}mm</span></div>
              <div className="flex justify-between"><span className="text-muted-foreground">Layers</span><span>{board.layers}</span></div>
              <div className="flex justify-between"><span className="text-muted-foreground">Components</span><span>{components.length}</span></div>
              <div className="flex justify-between"><span className="text-muted-foreground">Tracks</span><span>{tracks.length}</span></div>
            </div>
          )}
        </div>

        <div className="mt-6 space-y-2">
          <h3 className="font-medium mb-2">Legend</h3>
          <div className="flex items-center gap-2 text-xs">
            <div className="w-3 h-3 rounded-sm bg-[#4a9eff]" /> Front Copper
          </div>
          <div className="flex items-center gap-2 text-xs">
            <div className="w-3 h-3 rounded-sm bg-[#ff6b35]" /> Back Copper
          </div>
          <div className="flex items-center gap-2 text-xs">
            <div className="w-3 h-3 rounded-sm border border-[#4a9eff]" /> Board Outline
          </div>
        </div>
      </div>
    </div>
  );
}
