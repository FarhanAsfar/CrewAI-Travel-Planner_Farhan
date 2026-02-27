# AI Travel Planner

A multi-agent AI-powered travel planning system built with **CrewAI**, **Groq LLM**, and **Serper Dev API**. Give it a destination, dates, budget, and preferences — it returns a complete travel plan with destination research, budget breakdown, day-wise itinerary, and a validation summary.

---

## Project Overview

The planner uses **4 specialised AI agents** that work sequentially, each passing their output to the next:

| Agent | Role | Tools Used |
|---|---|---|
| Destination Researcher | Finds attractions, culture, tips | Serper Web Search |
| Budget Planner | Estimates costs per category | Serper Web Search |
| Itinerary Designer | Builds day-by-day plan | LLM only (uses prior context) |
| Validation Agent | Checks consistency & feasibility | LLM only (reviews all outputs) |

**Input:** Destination, start date, end date, budget (USD), preferences (optional)

**Output:** A structured Markdown file saved to `/output/` containing:
- Destination overview
- Budget breakdown (accommodation, food, transport, activities)
- Day-wise itinerary (morning / afternoon / evening)
- Validation summary (PASS/WARN/FAIL checks, risks, assumptions)

---


## ✅ Prerequisites

Before you begin, make sure you have the following installed on your system.

### 1. Python 3.10 or higher

```bash
python3 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/).

### 2. CrewAI

```bash
pip install crewai
```

Verify installation:

```bash
crewai --version
```

> **Note:** CrewAI uses `uv` internally to manage the project virtual environment. It will be installed automatically when you run `crewai install`.

---

## 🔑 API Keys Setup

This project requires two API keys. Both have free tiers.

### 1. Groq API Key (LLM)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to **API Keys** in the sidebar
4. Click **Create API Key**
5. Copy the key — you will only see it once

### 2. Serper Dev API Key (Web Search)

1. Go to [serper.dev](https://serper.dev)
2. Sign up or log in
3. Your API key is shown on the dashboard
4. Copy the key

### 3. Add Keys to `.env`

In the project root, copy the example file:

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```ini
GROQ_API_KEY=your_actual_groq_key_here
SERPER_API_KEY=your_actual_serper_key_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

## 🛠️ Installation

### Step 1 — Clone the repository

```bash
git clone <your-repository-url>
cd CrewAI-Travel-Planner
```

### Step 2 — Install dependencies

```bash
crewai install
```

This command:
- Creates a `.venv/` virtual environment inside the project
- Installs all dependencies listed in `pyproject.toml`
- Uses `uv.lock` to ensure exact version matches

> This may take 1–2 minutes on first run.

### Step 3 — Verify installation

```bash
source .venv/bin/activate
python3 -c "import crewai; print('CrewAI OK')"
python3 -c "import litellm; print('LiteLLM OK')"
```

Both should print without errors.

---

## ▶️ Running the Project

### Run the planner

```bash
crewai run
```

You will be prompted to enter your trip details:

```
═══════════════════════════════════════════════════════
  🌍  AI Travel Planner — CrewAI + Groq + Serper
═══════════════════════════════════════════════════════

Destination (city / country): Tokyo, Japan
Start date (YYYY-MM-DD): 2025-06-10
End date   (YYYY-MM-DD): 2025-06-17
Total budget in USD (e.g. 2000): 3000
Preferences (optional — e.g. vegetarian, no crowds): vegetarian
```

After confirming, the agents will start working. This typically takes **3–8 minutes** depending on the destination and number of days.

```
┌──────────────────────────────────────────────────┐
│  Trip Summary                                    │
│  Destination : Tokyo, Japan                      │
│  Dates       : 2025-06-10 → 2025-06-17           │
│  Duration    : 7 days                            │
│  Budget      : $3,000.00 USD                     │
│  Preferences : vegetarian                        │
└──────────────────────────────────────────────────┘

  ▶  Start planning? (y/n): y

  🚀  Starting AI agents... (this may take a few minutes)
```

When complete:

```
═══════════════════════════════════════════════════════
  ✅  Travel plan generated successfully!
  📄  Saved to: output/travel_plan_tokyo_japan_20250610_143022.md
═══════════════════════════════════════════════════════
```

---

## 📄 Sample Output

The generated Markdown file in `/output/` will look like:

```
# ✈️ Travel Plan: Tokyo, Japan

## 📋 Trip Overview
| Field       | Details       |
|-------------|---------------|
| Destination | Tokyo, Japan  |
| Duration    | 7 days        |
| Budget      | $3,000.00 USD |

## 🗺️ Destination Research
Top attractions, local culture, practical tips, best areas to stay...

## 💰 Budget Breakdown
| Category      | Cost      |
|---------------|-----------|
| Accommodation | $840.00   |
| Food          | $350.00   |
| Transport     | $200.00   |
| Activities    | $300.00   |
| Total         | $1,690.00 ✅ Within Budget |

## 📅 Day-wise Itinerary
Day 1 — Arrival & Shinjuku
- Morning: Arrive at Narita, check in (~$0)
- Afternoon: Explore Shinjuku Gyoen (~$5)
- Evening: Dinner at local ramen restaurant (~$15)
...

## ✅ Validation Summary
- Budget Alignment:        PASS
- Scheduling Feasibility:  PASS
- Consistency Check:       PASS
- Overall Verdict:         APPROVED ✅
```

---

## 🏗️ Architecture

```
User Input (CLI)
      │
      ▼
┌─────────────────────────────────────────────────────┐
│                    Crew Manager                     │
│                                                     │
│  Task 1: Destination Researcher  ── Serper API      │
│       │                                             │
│  Task 2: Budget Planner          ── Serper API      │
│       │                                             │
│  Task 3: Itinerary Designer      ── LLM only        │
│       │                                             │
│  Task 4: Validation Agent        ── LLM only        │
└─────────────────────────────────────────────────────┘
      │
      ▼
output/travel_plan_<destination>_<timestamp>.md
```

Each task passes its output as context to the next task — no information is lost between agents.

---

## 📁 Project Structure

```
CrewAI-Travel-Planner/
│
├── pyproject.toml                   # Project metadata and dependencies
├── uv.lock                          # Locked dependency versions (commit this)
├── .env                             # Your API keys (never commit this)
├── .env.example                     # API key template
├── .gitignore
├── README.md
│
├── knowledge/                       # Reserved for CrewAI knowledge sources
├── logs/                            # Auto-created — one timestamped .log per run
├── output/                          # Auto-created — Markdown travel plans saved here
│
└── src/
    └── travel_planner/
        │
        ├── __init__.py
        ├── main.py                  # CLI prompts + calls run_travel_crew()
        ├── crew.py                  # @agent / @task / @crew decorators + output writer
        ├── logger.py                # Centralised logging (console + file)
        │
        ├── config/
        │   ├── agents.yaml          # Agent definitions (role, goal, backstory)
        │   └── tasks.yaml           # Task definitions (description, expected_output)
        │
        └── tools/
            ├── __init__.py
            ├── serper_tool.py       # Serper Dev API wrapper
            └── calculator_tool.py   # Budget calculator utility
```

---

## 📋 Logs

Every run creates a timestamped log file in `/logs/`:

```bash
# View the latest log
cat logs/travel_planner_*.log

# Follow a live run in real time
tail -f logs/travel_planner_*.log
```

Log levels:
- **Console** → INFO and above (clean progress messages)
- **File** → DEBUG and above (full execution trace including every agent step and tool call)

---

## 🔧 Troubleshooting

### `ModuleNotFoundError: No module named 'travel_planner'`
You are running `python3 main.py` directly. Always use `crewai run` instead:
```bash
crewai run
```

### `Model decommissioned error`
The Groq model name is outdated. Open `src/travel_planner/crew.py` and update:
```python
model="groq/llama3-8b-8192"           # ❌ old
model="groq/llama-3.3-70b-versatile"  # ✅ new
```
Check currently available models at [console.groq.com/docs/models](https://console.groq.com/docs/models).

### `Fallback to LiteLLM is not available`
LiteLLM is missing from the virtual environment:
```bash
source .venv/bin/activate
uv pip install litellm --frozen
crewai run
```

### `GROQ_API_KEY is not set`
Your `.env` file is missing or the key is not filled in:
```bash
cat .env
```
Make sure both keys have real values and not the placeholder text.

### `ImportError: Missing dependency apscheduler`
This is a harmless warning from litellm's proxy module — your project does not use the proxy. The agents will still run correctly. To suppress the warning, add this to your `.env`:
```ini
LITELLM_LOG=ERROR
```

### Agents produce incomplete or cut-off output
The Groq free tier rate limit was likely hit mid-run. Wait 1–2 minutes and run again:
```bash
crewai run
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `crewai` | Multi-agent framework — includes LiteLLM for Groq LLM connectivity |
| `requests` | HTTP calls to Serper Dev API for web search |
| `python-dotenv` | Loads API keys from `.env` file at runtime |
