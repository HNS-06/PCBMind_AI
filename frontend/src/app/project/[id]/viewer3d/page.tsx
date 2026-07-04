'use client';

import { useEffect, useState, useRef, Suspense } from 'react';
import { useParams } from 'next/navigation';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Environment } from '@react-three/drei';
import { Loader2 } from 'lucide-react';
import { projectsAPI } from '@/lib/api';
import * as THREE from 'three';

function PCBBoard({ pcbData }: { pcbData: any }) {
  const board = pcbData?.board;
  const components = pcbData?.components || [];
  const w = (board?.width_mm || 80) / 100;
  const h = (board?.height_mm || 60) / 100;
  const t = 0.016;

  return (
    <group>
      <mesh position={[0, 0, -t / 2]}>
        <boxGeometry args={[w, h, t]} />
        <meshStandardMaterial color="#1a5c1a" roughness={0.3} metalness={0.1} />
      </mesh>

      <mesh position={[0, 0, t / 2 + 0.001]}>
        <boxGeometry args={[w - 0.005, h - 0.005, 0.001]} />
        <meshStandardMaterial color="#cc7722" roughness={0.4} metalness={0.6} transparent opacity={0.6} />
      </mesh>

      {components.map((comp: any, i: number) => {
        const x = ((comp.x || 0) / 100) - w / 2;
        const y = ((comp.y || 0) / 100) - h / 2;
        const isSMD = comp.footprint?.includes('SMD') || comp.footprint?.includes('0402') || comp.footprint?.includes('0603');
        const compH = isSMD ? 0.008 : 0.03;

        return (
          <group key={i} position={[x, y, t / 2 + compH / 2]}>
            <mesh>
              <boxGeometry args={[0.015, 0.01, compH]} />
              <meshStandardMaterial color="#1a1a1a" roughness={0.5} />
            </mesh>
            {(comp.id?.startsWith('R') || comp.id?.startsWith('C')) && (
              <mesh position={[0, 0, compH / 2 + 0.002]}>
                <boxGeometry args={[0.012, 0.006, 0.002]} />
                <meshStandardMaterial color="#2a2a2a" roughness={0.3} />
              </mesh>
            )}
            {comp.id?.startsWith('U') && (
              <>
                <mesh position={[0, 0, compH / 2 + 0.001]}>
                  <boxGeometry args={[0.02, 0.015, 0.002]} />
                  <meshStandardMaterial color="#0a0a0a" roughness={0.2} metalness={0.3} />
                </mesh>
                {[...Array(4)].map((_, j) => (
                  <mesh key={j} position={[
                    (j % 2 === 0 ? -1 : 1) * 0.012,
                    (j < 2 ? -1 : 1) * 0.006,
                    0
                  ]}>
                    <boxGeometry args={[0.002, 0.004, 0.001]} />
                    <meshStandardMaterial color="#c0a050" metalness={0.8} roughness={0.2} />
                  </mesh>
                ))}
              </>
            )}
          </group>
        );
      })}
    </group>
  );
}

function Scene({ pcbData }: { pcbData: any }) {
  const controlsRef = useRef<any>(null);
  return (
    <>
      <PerspectiveCamera makeDefault position={[0.3, -0.2, 0.3]} />
      <OrbitControls ref={controlsRef} enableDamping dampingFactor={0.05} />
      <ambientLight intensity={0.5} />
      <directionalLight position={[1, 1, 1]} intensity={1} />
      <pointLight position={[-0.5, -0.5, 0.5]} intensity={0.3} color="#4a9eff" />
      <Environment preset="studio" />
      <PCBBoard pcbData={pcbData} />
      <gridHelper args={[1, 20, '#333', '#222']} position={[0, 0, -0.02]} />
    </>
  );
}

export default function Viewer3DPage() {
  const params = useParams();
  const projectId = params.id as string;
  const [pcbData, setPcbData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProject();
  }, [projectId]);

  async function loadProject() {
    try {
      const res = await projectsAPI.get(projectId);
      setPcbData(res.data.pcb_data);
    } catch {} finally {
      setLoading(false);
    }
  }

  if (loading) return <div className="flex items-center justify-center h-64"><Loader2 className="w-8 h-8 animate-spin" /></div>;

  return (
    <div className="h-[calc(100vh-7rem)] relative">
      <div className="absolute top-4 left-4 z-10 space-y-2">
        <div className="bg-card border border-border rounded-lg p-3 text-sm">
          <p className="font-medium">3D PCB Viewer</p>
          <p className="text-xs text-muted-foreground mt-1">Drag to rotate, scroll to zoom, right-click to pan</p>
        </div>
      </div>
      <Canvas>
        <Scene pcbData={pcbData} />
      </Canvas>
    </div>
  );
}
