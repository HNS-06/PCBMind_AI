'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  Cpu, LayoutDashboard, Plus, FolderOpen, Settings, MessageSquare,
  CircuitBoard, Box, FileText, Download, Code, ChevronLeft, ChevronRight,
  Users,
} from 'lucide-react';
import { useState } from 'react';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/project/new', label: 'New Project', icon: Plus },
  { href: '/agents', label: 'Design Agents', icon: Users },
];

const projectItems = [
  { suffix: '', label: 'Overview', icon: FolderOpen },
  { suffix: '/chat', label: 'AI Chat', icon: MessageSquare },
  { suffix: '/pcb', label: 'PCB Editor', icon: CircuitBoard },
  { suffix: '/viewer3d', label: '3D Viewer', icon: Box },
  { suffix: '/bom', label: 'BOM', icon: FileText },
  { suffix: '/firmware', label: 'Firmware', icon: Code },
  { suffix: '/export', label: 'Export', icon: Download },
];

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const projectIdMatch = pathname.match(/^\/project\/([a-f0-9-]+)/);
  const projectId = projectIdMatch ? projectIdMatch[1] : null;

  return (
    <aside className={cn(
      'flex flex-col border-r border-border bg-card transition-all duration-300',
      collapsed ? 'w-16' : 'w-64'
    )}>
      <div className="flex items-center gap-2 px-4 py-4 border-b border-border">
        <Cpu className="w-8 h-8 text-primary shrink-0" />
        {!collapsed && <span className="font-bold text-lg">PCBMind</span>}
      </div>

      <nav className="flex-1 p-2 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors',
                active ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-secondary hover:text-foreground'
              )}
            >
              <Icon className="w-5 h-5 shrink-0" />
              {!collapsed && <span>{item.label}</span>}
            </Link>
          );
        })}

        {projectId && (
          <>
            <div className="pt-4 pb-2">
              {!collapsed && <p className="px-3 text-xs font-medium text-muted-foreground uppercase">Project</p>}
            </div>
            {projectItems.map((item) => {
              const Icon = item.icon;
              const href = `/project/${projectId}${item.suffix}`;
              const active = pathname === href;
              return (
                <Link
                  key={href}
                  href={href}
                  className={cn(
                    'flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors',
                    active ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-secondary hover:text-foreground'
                  )}
                >
                  <Icon className="w-5 h-5 shrink-0" />
                  {!collapsed && <span>{item.label}</span>}
                </Link>
              );
            })}
          </>
        )}
      </nav>

      <div className="p-2 border-t border-border">
        <Link
          href="/settings"
          className={cn(
            'flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors',
            pathname === '/settings' ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-secondary hover:text-foreground'
          )}
        >
          <Settings className="w-5 h-5 shrink-0" />
          {!collapsed && <span>Settings</span>}
        </Link>
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="flex items-center justify-center w-full py-2 text-muted-foreground hover:text-foreground"
        >
          {collapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
        </button>
      </div>
    </aside>
  );
}
