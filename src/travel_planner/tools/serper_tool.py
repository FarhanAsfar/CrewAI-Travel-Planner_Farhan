import os
import requests
from crewai.tools import BaseTool
from pydantic import Field

from travel_planner.logger import get_logger

log = get_logger(__name__)


class SerperSearchTool(BaseTool):
    """
    Searches the web via Serper Dev API (https://serper.dev).
    Input: a plain-text search query string.
    Output: top 5 organic results as formatted text.
    """

    name: str = "web_search"
    description: str = (
        "Search the web for up-to-date travel information such as attractions, "
        "hotel prices, transport costs, visa requirements, and local tips. "
        "Input must be a clear search query string."
    )

    api_key: str = Field(default="")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.getenv("SERPER_API_KEY", "")
        if not self.api_key:
            log.warning(
                "SERPER_API_KEY is not set — web_search tool will return errors."
            )

    def _run(self, query: str) -> str:
        """Hit the Serper API and return formatted results."""
        log.info(f"[SerperSearchTool] Query: '{query}'")

        if not self.api_key:
            msg = "ERROR: SERPER_API_KEY is missing. Cannot perform web search."
            log.error(msg)
            return msg  

        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {"q": query, "num": 5}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            results = response.json().get("organic", [])

            if not results:
                log.warning(f"[SerperSearchTool] No results for: '{query}'")
                return "No results found for this query."

            lines = []
            for i, item in enumerate(results, start=1):
                lines.append(
                    f"{i}. {item.get('title', 'No Title')}\n"
                    f"   {item.get('snippet', 'No description.')}\n"
                    f"   Source: {item.get('link', '')}"
                )

            output = "\n\n".join(lines)
            log.debug(f"[SerperSearchTool] Results:\n{output}")
            return output

        except requests.exceptions.Timeout:
            msg = f"ERROR: Serper API request timed out for query: '{query}'"
            log.error(msg)
            return msg

        except requests.exceptions.HTTPError as e:
            msg = f"ERROR: Serper API HTTP error: {e}"
            log.error(msg)
            return msg

        except requests.exceptions.RequestException as e:
            msg = f"ERROR: Serper API request failed: {e}"
            log.error(msg)
            return msg

        except Exception as e:
            msg = f"ERROR: Unexpected error in web_search: {e}"
            log.exception(msg)
            return msg