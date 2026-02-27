import os 
from datetime import datetime
from typing import Any

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from travel_planner.logger import get_logger
from travel_planner.tools.serper_tool import SerperSearchTool


log = get_logger(__name__)
# Output directory at project root
_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..",)
)
_OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output")
os.makedirs(_OUTPUT_DIR, exist_ok=True)



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

@CrewBase
class TravelPlannerCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ---shared tool---
    def __init__(self):
        self._search_tool = SerperSearchTool()
        log.info("[Crew] TravelPlannerCrew initialised.")

    # ---agents---
    @agent
    def destination_researcher(self) -> Agent:
        """
        Loads role/goal/backstory from agents.yaml → destination_researcher.
        Assign the Serper search tool for web lookups.
        """
        log.info("[Agent] Building destination_researcher agent")
        return Agent(
            config = self.agents_config["budget_planner"],
            tools = [self._search_tool],
            llm = _get_llm(),
            verbose = True,
            allow_delegation = False,
        )
    
    @agent
    def budget_planner(self) -> Agent:
        """
        Loads config from agents.yaml → budget_planner.
        Uses Serper to fetch real price data.
        """
        log.info("[Agent] Building budget_planner")
        return Agent(
            config=self.agents_config["budget_planner"],
            tools=[self._search_tool],
            llm=_get_llm(),
            verbose=True,
            allow_delegation=False,
        )
    
    @agent
    def itinerary_designer(self) -> Agent:
        """
        Loads config from agents.yaml → itinerary_designer.
        It has the context of the prior agents.
        """
        log.info("[Agent] Building itinerary_designer")
        return Agent(
            config=self.agents_config["itinerary_designer"],
            tools=[],
            llm=_get_llm(),
            verbose=True,
            allow_delegation=False,
        )
    
    @agent
    def validation_agent(self) -> Agent:
        """
        Loads config from agents.yaml → validation_agent.
        Reviews all prior outputs.
        """
        log.info("[Agent] Building validation_agent")
        return Agent(
            config=self.agents_config["validation_agent"],
            tools=[],
            llm=_get_llm(),
            verbose=True,
            allow_delegation=False,
        )
    

    # ---tasks---
    @task
    def research_task(self) -> Task:
        """Loads description/expected_output from tasks.yaml → research_task."""
        log.info("[Task] Building research_task")
        return Task(
            config = self.tasks_config["research_task"],
            agent = self.destination_researcher(),
        )
    
    @task
    def budget_task(self) -> Task:
        """
        Loads config from tasks.yaml → budget_task.
        Context: research_task output is passed forward automatically.
        """
        log.info("[Task] Building budget_task")
        return Task(
            config = self.tasks_config["budget_task"],
            agent = self.budget_planner(),
            context = [self.research_task()],
        )
    
    @task
    def itinerary_task(self) -> Task:
        """
        Loads config from tasks.yaml → itinerary_task.
        Context: research + budget task outputs.
        """
        log.info("[Task] Building itinerary_task")
        return Task(
            config = self.tasks_config["itinerary_task"],
            agent = self.itinerary_designer(),
            context = [self.research_task(), self.budget_task()],
        )
    
    @task
    def validation_task(self) -> Task:
        """
        Loads config from tasks.yaml → validation_task.
        Context: all three prior task outputs.
        """
        log.info("[Task] Building validation_task")
        return Task(
            config = self.tasks_config["validation_task"],
            agent = self.validation_agent(),
            context = [
                self.research_task(),
                self.budget_task(),
                self.itinerary_task(),
            ],
        )
    
    # ---crew----
    @crew
    def crew(self) -> Crew:
        log.info("[Crew] Assembling crew in sequential process")
        return Crew(
            agents = self.agents, # will be auto collected by @CrewBase from @agent methods
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True,
        )


# --execute command --
def run_travel_crew(inputs: dict) -> str:
    """
    Instantiate the crew, kick it off with the given inputs dict,
    and save the result to a Markdown file.
    """
    log.info("=" * 60)
    log.info(f"[Runner] Destination : {inputs.get('destination')}")
    log.info(f"[Runner] Dates       : {inputs.get('start_date')} → {inputs.get('end_date')}")
    log.info(f"[Runner] Days        : {inputs.get('num_days')}")
    log.info(f"[Runner] Budget      : ${inputs.get('budget_usd')}")
    log.info(f"[Runner] Preferences : {inputs.get('preferences') or 'None'}")
    log.info("=" * 60)

    # -- build and run the crew --
    try:
        log.info("[Runner] Initialising TravelPlannerCrew...")
        travel_crew = TravelPlannerCrew()

        log.info("[Runner] Kicking off crew execution...")
        result = travel_crew.crew().kickoff(inputs=inputs)
        log.info("[Runner] Crew execution completed.")

    except Exception as e:
        log.exception(f"[Runner] Crew execution failed: {e}")
        raise RuntimeError(f"Crew execution error: {e}") from e
    
    # ---save Markdown output---
    try:
        output_path = _save_markdown(inputs, result)
        return output_path
    except Exception as e:
        log.exception(f"[Runner] Failed to save output: {e}")
        raise RuntimeError(f"Output saving failed: {e}") from e


def _save_markdown(inputs: dict, crew_result: Any) -> str:
    """
    Write the structured travel plan to a Markdown file in /output/.
    """
    destination = inputs.get("destination", "Unknown")
    task_outputs = getattr(crew_result, "tasks_output", [])

    def _get(index: int) -> str:
        """Safely pull raw text from a task output by index."""
        try:
            return task_outputs[index].raw if index < len(task_outputs) else "_No output available._"
        except Exception:
            return "_Output unavailable._"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_dest = destination.replace(" ", "_").replace(",", "").lower()
    filename  = f"travel_plan_{safe_dest}_{timestamp}.md"
    filepath  = os.path.join(_OUTPUT_DIR, filename)

    md = f"""# Travel Plan: {destination}

> **Generated:** {datetime.now().strftime('%d %B %Y, %H:%M')}

---

## 📋 Trip Overview

| Field        | Details                                      |
|--------------|----------------------------------------------|
| Destination  | {destination}                                
| Start Date   | {inputs.get('start_date')}                   
| End Date     | {inputs.get('end_date')}                     
| Duration     | {inputs.get('num_days')} days                
| Budget       | ${float(inputs.get('budget_usd', 0)):,.2f} USD 
| Preferences  | {inputs.get('preferences') or 'None'}        

---

## Destination Research

{_get(0)}

---

## Budget Breakdown

{_get(1)}

---

## Day-wise Itinerary

{_get(2)}

---

## Validation Summary

{_get(3)}

---
*Generated by AI Travel Planner · *
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)

    log.info(f"[Runner] Output saved → {filepath}")
    return filepath