'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Zap, Sparkles, Loader2 } from 'lucide-react';
import { projectsAPI } from '@/lib/api';

const EXAMPLE_PROMPTS = [
  "Build an ESP32 weather station with WiFi, OLED display, BME280 sensor and battery backup.",
  "Design a home automation controller with relay module, IR sensor, and Bluetooth connectivity.",
  "Create a robot car controller with motor driver, ultrasonic sensor, and line following sensors.",
  "Build a DNA data storage reader with SD card, LCD display, and temperature monitoring.",
  "Design a smart plant monitoring system with soil moisture, light sensor, and MQTT connectivity.",
];

export default function NewProjectPage() {
  const router = useRouter();
  const [prompt, setPrompt] = useState('');
  const [modelName, setModelName] = useState('groq');
  const [generating, setGenerating] = useState(false);

  async function handleGenerate() {
    if (!prompt.trim()) return;
    setGenerating(true);
    try {
      const res = await projectsAPI.generate({ prompt: prompt.trim(), model: modelName });
      router.push(`/project/${res.data.project_id}`);
    } catch {
      alert('Generation failed. Please try again.');
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <div className="text-center space-y-4">
        <div className="inline-flex items-center gap-2 bg-primary/10 px-4 py-2 rounded-full">
          <Sparkles className="w-5 h-5 text-primary" />
          <span className="text-sm font-medium text-primary">AI Project Generator</span>
        </div>
        <h1 className="text-3xl font-bold">Describe Your Hardware Project</h1>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Tell PCBMind AI what you want to build in natural language. The AI will analyze your
          requirements, select components, design the circuit, generate PCB layout, and create firmware.
        </p>
      </div>

      <div className="space-y-4">
        <div className="relative">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your hardware project...&#10;&#10;Example: Build an ESP32 weather station with WiFi, OLED display, BME280 sensor and battery backup."
            className="w-full h-40 bg-card border border-border rounded-xl p-4 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary placeholder:text-muted-foreground"
          />
          <div className="absolute bottom-3 right-3 text-xs text-muted-foreground">
            {prompt.length} characters
          </div>
        </div>

        <div className="flex items-center gap-4">
          <select
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
            className="bg-card border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="groq">Groq Llama 3.1 (Fastest - Free)</option>
            <option value="gemini">Gemini 1.5 Flash</option>
            <option value="openai">GPT-4o</option>
            <option value="claude">Claude</option>
          </select>

          <button
            onClick={handleGenerate}
            disabled={!prompt.trim() || generating}
            className="flex items-center gap-2 bg-primary text-primary-foreground px-6 py-2 rounded-lg font-medium hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed ml-auto"
          >
            {generating ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                Generate Project
              </>
            )}
          </button>
        </div>
      </div>

      <div className="space-y-3">
        <h3 className="text-sm font-medium text-muted-foreground">Example Projects</h3>
        <div className="grid grid-cols-1 gap-2">
          {EXAMPLE_PROMPTS.map((example, i) => (
            <button
              key={i}
              onClick={() => setPrompt(example)}
              className="text-left p-3 bg-card border border-border rounded-lg text-sm hover:border-primary/50 transition-colors"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
