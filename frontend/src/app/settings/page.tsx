'use client';

import { Settings as SettingsIcon, Key, Server, Database, Cpu } from 'lucide-react';

export default function SettingsPage() {
  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-sm text-muted-foreground">Configure your PCBMind AI platform</p>
      </div>

      <div className="space-y-4">
        {[
          {
            title: 'AI Model Configuration',
            icon: Cpu,
            fields: [
              { label: 'Gemini API Key', type: 'password', placeholder: 'Enter your Gemini API key' },
              { label: 'OpenAI API Key', type: 'password', placeholder: 'Enter your OpenAI API key' },
              { label: 'Claude API Key', type: 'password', placeholder: 'Enter your Claude API key' },
            ],
          },
          {
            title: 'Component Supplier APIs',
            icon: Key,
            fields: [
              { label: 'Octopart API Key', type: 'password', placeholder: 'Enter your Octopart API key' },
              { label: 'Mouser API Key', type: 'password', placeholder: 'Enter your Mouser API key' },
              { label: 'DigiKey Client ID', type: 'text', placeholder: 'Enter DigiKey Client ID' },
              { label: 'DigiKey Client Secret', type: 'password', placeholder: 'Enter DigiKey Client Secret' },
            ],
          },
          {
            title: 'Server Configuration',
            icon: Server,
            fields: [
              { label: 'Backend URL', type: 'text', placeholder: 'http://localhost:8000', value: 'http://localhost:8000' },
              { label: 'Redis URL', type: 'text', placeholder: 'redis://localhost:6379', value: 'redis://localhost:6379' },
            ],
          },
          {
            title: 'Database',
            icon: Database,
            fields: [
              { label: 'PostgreSQL URL', type: 'text', placeholder: 'postgresql://...', value: 'postgresql+asyncpg://postgres:postgres@localhost:5432/pcbmind' },
            ],
          },
        ].map((section) => {
          const Icon = section.icon;
          return (
            <div key={section.title} className="p-4 bg-card border border-border rounded-xl space-y-4">
              <div className="flex items-center gap-3">
                <Icon className="w-5 h-5 text-primary" />
                <h2 className="font-medium">{section.title}</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {section.fields.map((field) => (
                  <div key={field.label}>
                    <label className="block text-sm text-muted-foreground mb-1">{field.label}</label>
                    <input
                      type={field.type}
                      placeholder={field.placeholder}
                      defaultValue={(field as any).value}
                      className="w-full bg-secondary border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                    />
                  </div>
                ))}
              </div>
            </div>
          );
        })}

        <button className="bg-primary text-primary-foreground px-6 py-2 rounded-lg font-medium hover:bg-primary/90">
          Save Settings
        </button>
      </div>
    </div>
  );
}
