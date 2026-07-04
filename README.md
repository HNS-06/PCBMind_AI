# PCBMind AI

**AI-powered PCB Design Platform** - Convert natural language into complete hardware projects.

## Overview

PCBMind AI is a professional-grade platform that uses multi-agent AI to transform natural language descriptions into complete hardware projects including circuit schematics, PCB layouts, bill of materials, firmware code, and manufacturing-ready files.

### What It Does

Describe your project in plain English:
> "Build an ESP32 weather station with WiFi, OLED display, BME280 sensor and battery backup"

PCBMind AI generates:
- Circuit Schematic (KiCad format)
- PCB Layout with component placement
- Bill of Materials with pricing
- Complete firmware code
- Gerber manufacturing files
- Project documentation
- Wiring diagrams

## Architecture

```
PCBMind-AI/
├── backend/          # FastAPI + Python backend
│   ├── app/
│   │   ├── api/      # REST API endpoints
│   │   ├── agents/   # AI agent system (5 specialized agents)
│   │   ├── core/     # Config, database, security
│   │   ├── models/   # SQLAlchemy ORM models
│   │   ├── schemas/  # Pydantic validation schemas
│   │   └── services/ # Business logic services
│   └── tests/
├── frontend/         # Next.js + TypeScript frontend
│   └── src/
│       ├── app/      # Next.js App Router pages
│       ├── components/ # Reusable UI components
│       ├── lib/      # API client, utilities
│       ├── stores/   # Zustand state management
│       └── types/    # TypeScript type definitions
├── ai/               # AI prompts and agent configurations
├── component-library/ # Component database (JSON)
├── eda-engine/       # EDA file generation modules
├── firmware/         # Firmware generation templates
├── storage/          # Generated files storage
├── docker/           # Docker Compose configuration
├── tests/            # Test suite
└── docs/             # Documentation
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, TailwindCSS, Three.js, ReactFlow, Monaco Editor |
| Backend | Python, FastAPI, SQLAlchemy, Celery, Redis |
| Database | PostgreSQL |
| AI Models | Google Gemini, OpenAI GPT-4o, Anthropic Claude |
| EDA | KiCad file format, Gerber generation |
| 3D | Three.js with React Three Fiber |
| DevOps | Docker Compose |

## AI Agent System

PCBMind AI uses 5 specialized AI agents working in pipeline:

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| Project Planner | Analyzes requirements | Natural language | Hardware specification |
| Circuit Designer | Designs electrical circuit | Specification + Components | Connections, voltage rails |
| PCB Expert | PCB layout & routing | Components + Connections | Placement, routing strategy |
| Firmware Engineer | Generates code | All project data | Complete firmware |
| Documentation Writer | Creates docs | All project data | README, guides |

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### 1. Clone & Install

```bash
# Backend
cd backend
py -m pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Configure Environment

```bash
cp backend/.env.example backend/.env
# Edit .env with your API keys
```

### 3. Start Services

```bash
# Start PostgreSQL and Redis (or use Docker)
docker compose -f docker/docker-compose.yml up -d postgres redis

# Backend
cd backend
py -m uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm run dev
```

### 4. Open

- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker (Full Stack)

```bash
docker compose -f docker/docker-compose.yml up -d
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/auth/me` | Get current user |
| GET | `/api/v1/projects` | List projects |
| POST | `/api/v1/projects` | Create project |
| POST | `/api/v1/projects/generate` | Generate project from prompt |
| GET | `/api/v1/projects/:id` | Get project |
| PATCH | `/api/v1/projects/:id` | Update project |
| DELETE | `/api/v1/projects/:id` | Delete project |
| GET | `/api/v1/components` | Search components |
| GET | `/api/v1/components/categories` | List categories |
| POST | `/api/v1/chat` | AI chat |
| GET | `/api/v1/export/:id/kicad` | Export KiCad files |
| GET | `/api/v1/export/:id/gerber` | Export Gerber files |
| GET | `/api/v1/export/:id/bom` | Export BOM CSV |
| GET | `/api/v1/export/:id/firmware` | Export firmware |

## Frontend Pages

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Landing page |
| Dashboard | `/dashboard` | Project listing |
| New Project | `/project/new` | AI project generator |
| Project Overview | `/project/:id` | Project details |
| AI Chat | `/project/:id/chat` | Chat with AI assistant |
| PCB Editor | `/project/:id/pcb` | Interactive PCB viewer |
| 3D Viewer | `/project/:id/viewer3d` | 3D PCB visualization |
| BOM | `/project/:id/bom` | Bill of materials |
| Firmware | `/project/:id/firmware` | Generated firmware code |
| Export | `/project/:id/export` | Download project files |
| Settings | `/settings` | API key configuration |

## Component Library

PCBMind AI includes 80+ pre-loaded components across categories:
- MCU: ESP32, STM32, Arduino, RP2040
- Sensors: BME280, MPU6050, DHT22, BH1750
- Displays: OLED SSD1306, TFT ST7789
- Power: AMS1117, TP4056, buck converters
- Passives: Resistors, capacitors, LEDs
- Connectors: USB-C, JST, headers
- Wireless: nRF24L01, HC-05 Bluetooth
- Motor Drivers: L298N, DRV8825

## Testing

```bash
# Run all tests
pytest tests/ backend/tests/ -v

# EDA engine tests
pytest tests/test_eda_engine.py -v

# Agent tests
pytest tests/test_agents.py -v

# Firmware generator tests
pytest tests/test_firmware.py -v

# API tests
cd backend && pytest tests/ -v
```

## Design Review Features

The AI Design Review agent automatically checks for:
- Missing decoupling capacitors
- Wrong pull-up/pull-down values
- Floating GPIO pins
- Reverse polarity protection
- Overcurrent protection
- EMI risks
- Ground loop issues
- Thermal management
- Manufacturing feasibility

## Manufacturing Support

Export files compatible with:
- **PCB Manufacturers**: JLCPCB, PCBWay, OSH Park, Elecrow
- **Component Suppliers**: DigiKey, Mouser, LCSC, Farnell
- **EDA Software**: KiCad 7+, EasyEDA, Altium Designer

## License

MIT License

## Built By

PCBMind AI - AI-Powered Electronic Design Automation Platform
