import sys
import os
import warnings

from datetime import datetime, date 

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from travel_planner.crew import run_travel_crew
from travel_planner.logger import get_logger


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

log = get_logger("main")

# --api key check--
def _check_env() -> bool:
    """Check env variables. Log any error and return true if all ok"""
    ok = True
    for var in ("GROQ_API_KEY", "SERPER_API_KEY"):
        if not os.getenv(var):
            log.error(f"[Env] Missing: {var}")
            print(f" {var} is not set. Add it to your .env file")
            ok = False
    return ok


# --input prompts--

def _prompt(label: str, required: bool = True) -> str:
    """Prompt a string if required field is empty"""
    while True:
        value = input(label).strip()
        if value or not required:
            return value
        print("This field is required!")

def _prompt_date(label: str) -> date:
    """Prompt for a valid date: YYYY-MM-DD"""
    while True:
        raw = _prompt(label)
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print("!! Use format YYYY-MM-DD (e.g. 2025-06-15).")

def _prompt_budget() -> float: 
    """Prompt for a positive number"""
    while True:
        raw = _prompt("Total budget in USD (e.g. 2000): ")
        try:
            val = float(raw.replace(",", ""))
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("Enter a positive nuber (e.g. 15000).")


def _collect_inputs() -> dict:
    """Collect all the trip details from the user"""

    print("\n" + "═" * 55)
    print(" AI Travel Planner ")
    print("═" * 55 + "\n")

    destination = _prompt("Destination (city / country):")

    # date validation loop
    while True: 
        start_date = _prompt_date("Start Date (YYYY-MM-DD): ")
        end_date = _prompt_date("End Date (YYYY-MM-DD): ")
        if end_date > start_date:
            break
        print("End date must be after start date. Try again.")
    
    budget_usd = _prompt_budget()
    preferences = _prompt(
        "Preferences (optional - e.g vegetarian, no crowds): ",
        required=False
    )

    num_days = (end_date - start_date).days

    inputs = {
        "destination": destination,
        "start_date":  str(start_date),
        "end_date":    str(end_date),
        "num_days":    num_days,
        "budget_usd":  budget_usd,
        "preferences": preferences or "None",
    }

    log.info(f"[Input] Collected: {inputs}")
    return inputs


def main() -> None:
    log.info("[Main] Travel Planner starting")

    # api key check
    if not _check_env():
        print("\n Missing API keys. Exiting.\n")
        sys.exit(1)
    
    # collect inputs
    try:
        inputs = _collect_inputs()
    except KeyboardInterrupt:
        print("\n\n Program Cancelled. \n")
        log.info("[Main] Cancelled during input.")
        sys.exit(0)
    except Exception as e:
        log.exception (f"[Main] Input error: {e}")
        print(f"\n Error in collecting inputs: {e}\n")
        sys.exit(1)
    
    # confirm before running
    print(f"""
    Trip Summary
    Destination : {inputs['destination']:<33} 
    Dates       : {inputs['start_date']} → {inputs['end_date']}
    Duration    : {inputs['num_days']} days{" " * (31 - len(str(inputs['num_days'])))}
    Budget      : ${inputs['budget_usd']:,.2f} USD{" " * max(0, 24 - len(f"{inputs['budget_usd']:,.2f}"))}
    Preferences : {(inputs['preferences'])[:33]:<33}  
    """)

    if input ("\n Start planning? (y/n): ").strip().lower() not in ("y", "yes", "Y", "Yes", "YES"):
        print("\n Program cancelled \n")
        log.info("[Main] User declined to start planning.")
        sys.exit(0)

    # Run the crew
    print("\n  Starting AI agents... (this may take a few minutes)\n")
    log.info("[Main] Handing off to CrewAI pipeline.")

    try:
        output_path = run_travel_crew(inputs)
        print("\n" + "═" * 55)
        print("  Travel plan generated successfully!")
        print(f"  Saved to: {output_path}")
        print("═" * 55 + "\n")
        log.info(f"[Main] Done. Output: {output_path}")

    except RuntimeError as e:
        print(f"\n  Planning failed: {e}")
        print("     Check /logs for the full error trace.\n")
        log.error(f"[Main] Pipeline error: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n  Interrupted during planning.\n")
        log.warning("[Main] Interrupted during crew execution.")
        sys.exit(0)

    except Exception as e:
        log.exception(f"[Main] Unexpected error: {e}")
        print(f"\n  Unexpected error: {e}")
        print("     Check /logs for the full error trace.\n")
        sys.exit(1)

def run():
    """crewai run"""
    main()

if __name__ == "__main__":
    main()

