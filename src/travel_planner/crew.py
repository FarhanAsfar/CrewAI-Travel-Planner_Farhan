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
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
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
        model="groq/llama3-8b-8192",
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
            tools = [self._search_tool]
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
    


