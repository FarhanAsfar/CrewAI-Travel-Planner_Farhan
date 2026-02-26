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