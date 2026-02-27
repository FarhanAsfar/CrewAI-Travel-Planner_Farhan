## 1. Why Multi-Agent?

A single agent processing multiple tasks can loses focus and generate low quality output. Delegating the tasks in separate agents can help provide clear role, context, and specific prompting. It can help get more clear and factual results.

---

## 2. What If Serper Returns Incorrect Data?

The agents trust search results without checking them, so incorrect prices will flow directly into the plan. The validation agent can catch inconsistencies. the system runs multiple searches per topic so the LLM can cross-reference results. 

---

## 3. What If the Budget Is Unrealistic?

The budget planner will still produce a breakdown but the validation agent will flag it as `Over Budget` with cost-saving suggestions. If the budget is severely unrealistic (e.g. $100 for 7 days in Tokyo), the agents will try their best but the validation summary will clearly state it is not feasible. The system does not block execution — it informs the user and lets them decide.

---

## 4. Hallucination Risks?

The destination researcher and budget planner are grounded by Serper search results, which significantly reduces hallucination compared to pure LLM generation. The itinerary and validation agents work only from prior task outputs with no search tool, so they can still invent plausible-sounding but incorrect details like fabricated opening hours or non-existent restaurants. Using `temperature=0.3` lowers creativity and reduces but does not eliminate this risk.

---

## 5. Token Usage?

Each run consumes roughly 10,000–20,000 tokens depending on destination complexity and trip length, spread across 6–10 LLM calls. The sequential context chaining means each agent receives all prior outputs, so token count grows with each task. This is logged after every run via `result.token_usage` and printed to console and the log file.

<img width="477" height="183" alt="token_usage" src="https://github.com/user-attachments/assets/a55fceb3-9aab-41dd-ad4e-1e99397c4a51" />

---

## 6. Scalability?

The current sequential process works well for single requests but would bottleneck under concurrent users since each run takes 2–4 minutes and holds open multiple API connections. CrewAI supports a `Process.hierarchical` mode where a manager agent delegates tasks in parallel, which would improve throughput. 
