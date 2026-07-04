export interface Project {
  id: string;
  name: string;
  description: string;
  prompt: string;
  status: 'draft' | 'generating' | 'completed' | 'error' | 'archived';
  components: Component[];
  connections: Connection[];
  netlist: NetEntry[];
  bom: BOMItem[];
  pcb_data: PCBData;
  schematic_data: SchematicData;
  firmware_code: string;
  documentation: string;
  metadata: Record<string, unknown>;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface Component {
  ref: string;
  type: string;
  name: string;
  value: string;
  package: string;
  quantity: number;
  manufacturer: string;
  part_number: string;
  price: number;
  supplier: string;
  datasheet: string;
  alternatives: string[];
  pins: string[];
  description: string;
  specs: Record<string, unknown>;
}

export interface Connection {
  net_name: string;
  description: string;
  type: string;
  pins: PinConnection[];
  pull_up?: { pin: string; value: string; voltage: number };
}

export interface PinConnection {
  component: string;
  pin: string;
  side: string;
}

export interface NetEntry {
  net_name: string;
  components: PinConnection[];
}

export interface BOMItem {
  ref: string;
  name: string;
  value: string;
  package: string;
  quantity: number;
  manufacturer: string;
  part_number: string;
  price: number;
  supplier: string;
  datasheet: string;
  alternatives: string[];
}

export interface PCBData {
  board: { width_mm: number; height_mm: number; layers: number; thickness_mm?: number };
  components: PCBComponent[];
  tracks: PCBTrack[];
  vias: PCBVia[];
  copper_pours: CopperPour[];
}

export interface PCBComponent {
  id: string;
  footprint: string;
  x: number;
  y: number;
  rotation: number;
  layer: string;
}

export interface PCBTrack {
  start: { x: number; y: number };
  end: { x: number; y: number };
  width_mm: number;
  net: string;
  layer: string;
}

export interface PCBVia {
  x: number;
  y: number;
  diameter_mm: number;
  drill_mm: number;
  net: string;
}

export interface CopperPour {
  net: string;
  layer: string;
  clearance_mm: number;
}

export interface SchematicData {
  components: SchematicComponent[];
  connections: Connection[];
}

export interface SchematicComponent {
  id: string;
  type: string;
  value: string;
  package: string;
  x: number;
  y: number;
  rotation: number;
  pins: string[];
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
}

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}
