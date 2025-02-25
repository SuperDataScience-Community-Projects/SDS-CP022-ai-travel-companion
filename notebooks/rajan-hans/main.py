# main.py
from planner_agent import PlannerAgent
from summarizer_agent import SummarizerAgent
from tools import SearchWeb
import re

known_actions = {
    "web_search":  lambda tavily_api_key: SearchWeb(tavily_api_key)
}


def grab_actions(response):
    pattern = r"^(Action):\s(\w+):\s(.*?)(?=\.\s|$)"
    tool = None
    details = None
    match = re.search(pattern, response, re.MULTILINE)
    if match:
        tool = match.group(2)
        details = match.group(3)
    return tool, details

class TravelPlanner():
    def __init__(self, openai_api_key, tavily_api_key, origin, destination, start_date, end_date):

        self.openai_api_key = openai_api_key
        self.tavily_api_key = tavily_api_key
        self.planner = PlannerAgent(openai_api_key, tavily_api_key)
        self.summarizer = SummarizerAgent(openai_api_key, tavily_api_key)
        self.prompt_template = ("""
            "I want you to build an itinerary for me for a trip from {origin} to {destination} starting "
            "from {start_month} {start_day} to {end_month} {end_day}."
            """
        )
        print("TravelPlanner initialized with Origin, Destination as : ",origin, destination)
        print("TravelPlanner initialized with Start Date, End Date as : ",start_date, end_date)   
    def plan_itinerary(self, origin, destination, start_date, end_date, max_turns=6):
        # Convert dates to month name and day number
        start_month = start_date.strftime("%B")
        start_day = start_date.day
        end_month = end_date.strftime("%B")
        end_day = end_date.day

        prompt = self.prompt_template.format(
            origin=origin,
            destination=destination,
            start_month=start_month,
            start_day=start_day,
            end_month=end_month,
            end_day=end_day
        )
        
        next_prompt = prompt
        for i in range(max_turns):
            response = self.planner.plan(next_prompt)
            tool, details = grab_actions(response)
            next_prompt = response  # feed the previous response into the next prompt
            if tool:
                if tool not in known_actions:
                    print(f"Unknown tool: {tool}")
                    break
                print(f"--- running {tool} {details} ---")
                action = known_actions[tool](self.tavily_api_key)
                search_resp = action.search(details)
                print("--- summarizing results ---")
                summary = self.summarizer.summarize(search_resp)
                next_prompt = f"Observation: {summary}"
            else:
                return response
        return response

# Optional: if you still want to run main.py directly
if __name__ == "__main__":
    planner = TravelPlanner()
    # Example hardcoded dates if running directly:
    from datetime import date
    itinerary = planner.plan_itinerary("New Delhi", "Japan", date(2023, 6, 1), date(2023, 6, 23))
    print("\nFinal Itinerary:\n", itinerary)
