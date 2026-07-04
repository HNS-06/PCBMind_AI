'use client';

import { useState, useEffect } from 'react';
import { Search, Send, Loader2, ArrowRight, Sparkles, Users } from 'lucide-react';

interface Agent {
  id: string;
  name: string;
  title: string;
  domain: string;
  avatar: string;
  color: string;
  description: string;
  capabilities: { name: string; description: string }[];
  keywords: string[];
}

const EXAMPLE_QUERIES = [
  { text: "Design a 3.3V power supply from 5V USB with battery backup", agents: ["power_systems"] },
  { text: "Help me select an ESP32 module for a weather station", agents: ["digital_logic"] },
  { text: "Why is my I2C bus not working? SDA and SCL are floating", agents: ["digital_logic", "signal_integrity"] },
  { text: "How can I reduce the BOM cost below $10?", agents: ["cost_optimization"] },
  { text: "Check my PCB design for thermal issues", agents: ["thermal_management"] },
  { text: "Add ESD protection to my USB connector", agents: ["safety_protection"] },
  { text: "Design a low-pass filter for my ADC input", agents: ["analog_design"] },
  { text: "What antenna should I use for LoRa 433MHz?", agents: ["rf_wireless"] },
  { text: "Is my design ready for manufacturing at JLCPCB?", agents: ["design_for_manufacturing"] },
  { text: "Review this entire circuit for issues", agents: ["multi_agent"] },
];

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [multiAgent, setMultiAgent] = useState(false);
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);

  useEffect(() => {
    fetchAgents();
  }, []);

  async function fetchAgents() {
    try {
      const res = await fetch('http://localhost:8000/api/v1/agents');
      const data = await res.json();
      setAgents(data);
    } catch {
      setAgents(getDefaultAgents());
    }
  }

  function getDefaultAgents(): Agent[] {
    return [
      { id: "system_architecture", name: "System Architect", title: "System Architecture Designer", domain: "system_architecture", avatar: "🏗️", color: "#a855f7", description: "Expert in overall system design, component selection, and high-level architecture.", capabilities: [{ name: "Requirements Analysis", description: "Analyze and decompose requirements" }, { name: "Block Diagram", description: "Create system block diagrams" }, { name: "Component Selection", description: "Select optimal components" }], keywords: ["system", "architecture", "design"] },
      { id: "power_systems", name: "Power Systems Engineer", title: "Power Systems Engineer", domain: "power_systems", avatar: "⚡", color: "#f59e0b", description: "Expert in power supply design, voltage regulation, battery management, and power distribution.", capabilities: [{ name: "Voltage Regulation", description: "Design LDO and switching regulator circuits" }, { name: "Battery Management", description: "Design charging and fuel gauge circuits" }, { name: "Power Budget", description: "Calculate power consumption and battery life" }], keywords: ["power", "voltage", "battery"] },
      { id: "signal_integrity", name: "Signal Integrity Expert", title: "Signal Integrity Engineer", domain: "signal_integrity", avatar: "📡", color: "#3b82f6", description: "Expert in high-speed signal routing, impedance matching, EMI/EMC, and noise reduction.", capabilities: [{ name: "Impedance Matching", description: "Calculate trace impedance and termination" }, { name: "EMI Analysis", description: "Identify and mitigate EMI sources" }], keywords: ["signal", "impedance", "emi"] },
      { id: "analog_design", name: "Analog Circuit Designer", title: "Analog Design Specialist", domain: "analog_design", avatar: "🔬", color: "#8b5cf6", description: "Expert in analog circuit design: op-amps, filters, sensor interfaces, ADC/DAC circuits.", capabilities: [{ name: "Op-Amp Design", description: "Design amplifier circuits with precise gain" }, { name: "Filter Design", description: "Design active and passive filters" }], keywords: ["analog", "op-amp", "filter"] },
      { id: "digital_logic", name: "Digital Logic Designer", title: "Digital Systems Architect", domain: "digital_logic", avatar: "🔲", color: "#10b981", description: "Expert in MCU selection, digital interfaces, communication protocols, and GPIO mapping.", capabilities: [{ name: "MCU Selection", description: "Choose the right microcontroller" }, { name: "Pin Mapping", description: "Allocate and map GPIO pins" }], keywords: ["digital", "mcu", "gpio"] },
      { id: "rf_wireless", name: "RF/Wireless Expert", title: "RF & Wireless Engineer", domain: "rf_wireless", avatar: "📻", color: "#ec4899", description: "Expert in wireless design: WiFi, Bluetooth, LoRa, Zigbee, antenna matching, and RF layout.", capabilities: [{ name: "Antenna Design", description: "Design PCB and chip antennas" }, { name: "Wireless Selection", description: "Choose WiFi, BLE, LoRa, Zigbee" }], keywords: ["rf", "wireless", "antenna"] },
      { id: "thermal_management", name: "Thermal Management Engineer", title: "Thermal Design Specialist", domain: "thermal_management", avatar: "🌡️", color: "#ef4444", description: "Expert in thermal analysis, heat dissipation, copper pours, and thermal vias.", capabilities: [{ name: "Thermal Analysis", description: "Calculate junction temperatures" }, { name: "Copper Pour Design", description: "Design ground and power copper pours" }], keywords: ["thermal", "heat", "temperature"] },
      { id: "design_for_manufacturing", name: "DFM Expert", title: "Design for Manufacturing Engineer", domain: "design_for_manufacturing", avatar: "🏭", color: "#06b6d4", description: "Expert in PCB manufacturing constraints, assembly rules, and production-ready design.", capabilities: [{ name: "DFM Check", description: "Verify design meets manufacturing rules" }, { name: "Cost Estimation", description: "Estimate PCB manufacturing cost" }], keywords: ["dfm", "manufacturing", "assembly"] },
      { id: "cost_optimization", name: "Cost Optimization Engineer", title: "Cost & Procurement Specialist", domain: "cost_optimization", avatar: "💰", color: "#84cc16", description: "Expert in component cost optimization, alternative sourcing, and BOM optimization.", capabilities: [{ name: "BOM Cost Analysis", description: "Analyze and reduce BOM cost" }, { name: "Alternative Sourcing", description: "Find alternative components and suppliers" }], keywords: ["cost", "price", "budget"] },
      { id: "safety_protection", name: "Safety & Protection Expert", title: "Circuit Protection Specialist", domain: "safety_protection", avatar: "🛡️", color: "#f97316", description: "Expert in circuit protection: ESD, overcurrent, overvoltage, reverse polarity, and isolation.", capabilities: [{ name: "ESD Protection", description: "Design ESD protection circuits" }, { name: "Overcurrent Protection", description: "Design fuse and PTC circuits" }], keywords: ["protection", "esd", "fuse"] },
    ];
  }

  async function handleSend() {
    if (!input.trim() || loading) return;
    setLoading(true);
    setResponse('');

    try {
      const res = await fetch('http://localhost:8000/api/v1/agents/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          agent_id: multiAgent ? null : selectedAgent,
          multi_agent: multiAgent,
        }),
      });
      const data = await res.json();
      setResponse(data.response || data.error || 'No response');
    } catch {
      setResponse('Error connecting to backend. Make sure the backend is running on port 8000.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-[calc(100vh-7rem)]">
      {/* Agent Sidebar */}
      <div className="w-80 bg-card border-r border-border overflow-y-auto">
        <div className="p-4 border-b border-border">
          <h2 className="font-bold flex items-center gap-2">
            <Users className="w-5 h-5 text-primary" />
            Design Agents
          </h2>
          <p className="text-xs text-muted-foreground mt-1">{agents.length} specialized AI agents</p>
        </div>

        <div className="p-3">
          <label className="flex items-center gap-2 p-2 bg-secondary rounded-lg cursor-pointer mb-3">
            <input type="checkbox" checked={multiAgent} onChange={(e) => setMultiAgent(e.target.checked)} className="rounded" />
            <span className="text-sm">Multi-Agent Mode</span>
            <Sparkles className="w-4 h-4 text-primary ml-auto" />
          </label>
        </div>

        <div className="p-2 space-y-1">
          {agents.map((agent) => (
            <button
              key={agent.id}
              onClick={() => { setSelectedAgent(agent.id); setMultiAgent(false); }}
              className={`w-full text-left p-3 rounded-lg transition-colors ${
                selectedAgent === agent.id && !multiAgent
                  ? 'bg-primary/10 border border-primary/30'
                  : 'hover:bg-secondary border border-transparent'
              }`}
            >
              <div className="flex items-center gap-2 mb-1">
                <span className="text-lg">{agent.avatar}</span>
                <span className="font-medium text-sm">{agent.name}</span>
              </div>
              <p className="text-xs text-muted-foreground line-clamp-2">{agent.description}</p>
              <div className="flex flex-wrap gap-1 mt-2">
                {agent.capabilities.slice(0, 2).map((cap) => (
                  <span key={cap.name} className="text-[10px] px-1.5 py-0.5 bg-secondary rounded">
                    {cap.name}
                  </span>
                ))}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {!response && !loading && (
            <div className="text-center py-12 space-y-6">
              <div className="text-6xl">🏗️</div>
              <h2 className="text-2xl font-bold">AI Design Agents</h2>
              <p className="text-muted-foreground max-w-lg mx-auto">
                Choose a specialized agent or enable Multi-Agent mode to get expert advice
                from multiple domains simultaneously.
              </p>

              <div className="grid grid-cols-2 gap-3 max-w-2xl mx-auto mt-8">
                {EXAMPLE_QUERIES.map((eq, i) => (
                  <button
                    key={i}
                    onClick={() => setInput(eq.text)}
                    className="text-left p-3 bg-card border border-border rounded-lg text-sm hover:border-primary/50 transition-colors"
                  >
                    {eq.text}
                  </button>
                ))}
              </div>
            </div>
          )}

          {response && (
            <div className="max-w-4xl">
              <div className="p-4 bg-card border border-border rounded-xl">
                <div className="flex items-center gap-2 mb-3 text-sm text-muted-foreground">
                  <Sparkles className="w-4 h-4 text-primary" />
                  AI Response
                  {selectedAgent && !multiAgent && (
                    <span className="px-2 py-0.5 bg-primary/10 text-primary rounded text-xs">
                      {agents.find(a => a.id === selectedAgent)?.avatar} {agents.find(a => a.id === selectedAgent)?.name}
                    </span>
                  )}
                  {multiAgent && (
                    <span className="px-2 py-0.5 bg-primary/10 text-primary rounded text-xs">
                      Multi-Agent
                    </span>
                  )}
                </div>
                <div className="whitespace-pre-wrap text-sm leading-relaxed">{response}</div>
              </div>
            </div>
          )}

          {loading && (
            <div className="flex items-center gap-3 p-4 bg-card border border-border rounded-xl">
              <Loader2 className="w-5 h-5 animate-spin text-primary" />
              <span className="text-sm text-muted-foreground">
                {multiAgent ? 'Multiple agents analyzing...' : 'Agent thinking...'}
              </span>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="p-4 border-t border-border">
          <div className="flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
              placeholder={
                multiAgent
                  ? "Ask any design question (all agents will analyze)..."
                  : selectedAgent
                    ? `Ask the ${agents.find(a => a.id === selectedAgent)?.name}...`
                    : "Select an agent or type your question..."
              }
              className="flex-1 bg-secondary border border-border rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="bg-primary text-primary-foreground px-5 py-2.5 rounded-lg hover:bg-primary/90 disabled:opacity-50 flex items-center gap-2"
            >
              <Send className="w-4 h-4" />
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
