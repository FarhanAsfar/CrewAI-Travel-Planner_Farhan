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

## Run the Project With Only One Command
**What You Need: An api key from https://serper.dev/api-keys, the LLM Model name and the API_KEY.**

**1. Clone the Project**
```bash
git clone <your-repository-url>
cd CrewAI-Travel-Planner
```

**2. Then create a .env file and add the LLM MODEL and API_KEYS**
Example:
```ini
MODEL=groq/meta-llama/llama-4-scout-17b-16e-instruct
GROQ_API_KEY=gsk_95PDP7Agkwrsf------b3FYNSrgNtsabEPu8ipKM0hdWbPz
SERPER_API_KEY=295c2-------87790b833cd6d9f151eea117
```

**You also need to add your LLM Model in `crew.py` file**
```python
def _get_llm() -> LLM:
    """
    CrewAI LLM pointed at Groq via LiteLLM.
    """
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        log.error("GROQ_API_KEY is not set.")
        raise EnvironmentError(
            "GROQ_API_KEY is missing. Add it to the .env file"
        )
    return LLM(
        model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
        api_key=api_key,
        temperature=0.3,
    )
```
**Add your model name here:**
```
model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
```
**3. Then run the following command in the terminal:**
```bash
./run.sh
```
**You should see the project running and asking for user input**

<img width="731" height="251" alt="run" src="https://github.com/user-attachments/assets/c76da812-3771-47d9-a5ff-3226508cadf3" />

---

> **You may see an error saying `litellm[proxy]` is not installed, you can ignore this error as the project runs successfully without it.**

---

## Project Installation in the Typical Manner:

##E ✅ Prerequisites

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


##  Installation

### Step 1 — Clone the repository

```bash
git clone <your-repository-url>
cd CrewAI-Travel-Planner
```

### Step 2 - Create a .env file in the project root and add your api keys and llm model name:
```ini
MODEL=groq/meta-llama/llama-4-scout-17b-16e-instruct
GROQ_API_KEY=gsk_95PDP7Agkwrsf------b3FYNSrgNtsabEPu8ipKM0hdWbPz
SERPER_API_KEY=295c2-------87790b833cd6d9f151eea117
```
**Also update the model name in the `crew.py` file:**
```
model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
```

### Step 3 — Install dependencies

```bash
crewai install
```

### Step 4 - Run the following command in your terminal
```
crewai run
```
**You should see the project running and asking for user input**

---


## Running the Project

### Run the planner

```bash
crewai run
```

You will be prompted to enter your trip details:

```
═══════════════════════════════════════════════════════
    AI Travel Planner 
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
