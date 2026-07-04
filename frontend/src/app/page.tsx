import Link from 'next/link';
import { Cpu, Zap, ArrowRight } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] px-8">
      <div className="max-w-4xl text-center space-y-8">
        <div className="flex items-center justify-center gap-3">
          <div className="p-3 bg-primary/10 rounded-xl">
            <Cpu className="w-12 h-12 text-primary" />
          </div>
        </div>
        <h1 className="text-6xl font-bold tracking-tight">
          PCBMind <span className="text-primary">AI</span>
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          AI-powered PCB design platform. Describe your hardware project in natural language
          and get complete schematics, PCB layouts, BOMs, firmware, and documentation.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link
            href="/project/new"
            className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-8 py-3 rounded-lg font-medium hover:bg-primary/90 transition-colors"
          >
            <Zap className="w-5 h-5" />
            Start New Project
          </Link>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 bg-secondary text-secondary-foreground px-8 py-3 rounded-lg font-medium hover:bg-secondary/80 transition-colors"
          >
            View Dashboard
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-16 text-left">
          {[
            { label: 'Circuit Design', desc: 'AI-generated schematics' },
            { label: 'PCB Layout', desc: 'Auto placement & routing' },
            { label: 'BOM Generation', desc: 'Component selection & pricing' },
            { label: 'Firmware', desc: 'Complete code generation' },
          ].map((feature) => (
            <div key={feature.label} className="p-4 bg-card rounded-lg border border-border">
              <h3 className="font-medium text-sm">{feature.label}</h3>
              <p className="text-xs text-muted-foreground mt-1">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
