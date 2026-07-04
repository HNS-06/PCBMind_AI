'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Loader2, Download } from 'lucide-react';
import { projectsAPI, exportAPI } from '@/lib/api';
import { formatCurrency } from '@/lib/utils';
import type { Project, BOMItem } from '@/types';

export default function BOMPage() {
  const params = useParams();
  const projectId = params.id as string;
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<'name' | 'price' | 'quantity'>('name');

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

  const bom = project.bom || [];
  const sorted = [...bom].sort((a, b) => {
    if (sortBy === 'price') return b.price - a.price;
    if (sortBy === 'quantity') return b.quantity - a.quantity;
    return a.name.localeCompare(b.name);
  });

  const totalCost = bom.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const totalQty = bom.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Bill of Materials</h1>
          <p className="text-sm text-muted-foreground">{bom.length} unique components, {totalQty} total parts</p>
        </div>
        <a
          href={exportAPI.bom(projectId)}
          className="inline-flex items-center gap-2 bg-secondary px-4 py-2 rounded-lg text-sm hover:bg-secondary/80"
        >
          <Download className="w-4 h-4" />
          Export CSV
        </a>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 bg-card border border-border rounded-xl">
          <p className="text-2xl font-bold text-primary">{formatCurrency(totalCost)}</p>
          <p className="text-sm text-muted-foreground">Total Cost</p>
        </div>
        <div className="p-4 bg-card border border-border rounded-xl">
          <p className="text-2xl font-bold">{totalQty}</p>
          <p className="text-sm text-muted-foreground">Total Components</p>
        </div>
        <div className="p-4 bg-card border border-border rounded-xl">
          <p className="text-2xl font-bold">{bom.length}</p>
          <p className="text-sm text-muted-foreground">Unique Parts</p>
        </div>
      </div>

      <div className="flex gap-2">
        {(['name', 'price', 'quantity'] as const).map((s) => (
          <button
            key={s}
            onClick={() => setSortBy(s)}
            className={`px-3 py-1.5 rounded-lg text-sm ${sortBy === s ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'}`}
          >
            Sort by {s}
          </button>
        ))}
      </div>

      <div className="bg-card border border-border rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Ref</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Component</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Value</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Package</th>
              <th className="text-right px-4 py-3 font-medium text-muted-foreground">Qty</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Manufacturer</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Part Number</th>
              <th className="text-right px-4 py-3 font-medium text-muted-foreground">Unit Price</th>
              <th className="text-right px-4 py-3 font-medium text-muted-foreground">Total</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Supplier</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((item, i) => (
              <tr key={i} className="border-b border-border/50 hover:bg-secondary/30">
                <td className="px-4 py-3 font-mono text-primary">{item.ref}</td>
                <td className="px-4 py-3">{item.name}</td>
                <td className="px-4 py-3 font-mono">{item.value}</td>
                <td className="px-4 py-3">{item.package}</td>
                <td className="px-4 py-3 text-right">{item.quantity}</td>
                <td className="px-4 py-3 text-muted-foreground">{item.manufacturer}</td>
                <td className="px-4 py-3 font-mono text-xs">{item.part_number}</td>
                <td className="px-4 py-3 text-right font-mono">{formatCurrency(item.price)}</td>
                <td className="px-4 py-3 text-right font-mono">{formatCurrency(item.price * item.quantity)}</td>
                <td className="px-4 py-3 text-muted-foreground">{item.supplier}</td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr className="border-t border-border font-medium">
              <td className="px-4 py-3" colSpan={4}>Total</td>
              <td className="px-4 py-3 text-right">{totalQty}</td>
              <td className="px-4 py-3" colSpan={3}></td>
              <td className="px-4 py-3 text-right font-mono text-primary">{formatCurrency(totalCost)}</td>
              <td className="px-4 py-3"></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
}
