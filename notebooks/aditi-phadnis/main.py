from planner_agent import PlannerAgent
from tools import SearchWeb
from dotenv import load_dotenv
from datetime import datetime
from summarizer_agent import SummarizerAgent



import openai
import os
import re

load_dotenv()


# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")



openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Define tools available for the agent

known_actions = {
    "web_search": SearchWeb
}

def grab_actions(response):
    """Extracts the tool and details from the response using regex."""
    pattern = r"^(Action):\s(\w+):\s(.*?)(?=\.\s|$)"
    match = re.search(pattern, response, re.MULTILINE)
    if match:
        return match.group(2), match.group(3)
    return None, None

def generate_itinerary(summary):
    """Uses OpenAI to generate a structured itinerary."""
    openai.api_key = OPENAI_API_KEY
    prompt = f"Create a detailed itinerary based on the following travel details:\n{summary}"

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a travel assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# def query(max_turns=6):
#     """Generates travel itinerary using Tavily, and OpenAI."""
    
#     # Initialize agents
#     planner = PlannerAgent()
#     web_search = SearchWeb()
#     summarizer = SummarizerAgent()


#     # Define the user prompt
#     prompt_template = """
#     I want you to build an itinerary for a trip from {origin} to {destination} 
#     starting from {start_month} {start_day} to {end_month} {end_day}.
#     """
    
#     # Sample Inputs
#     origin = 'Abu Dhabi'  # Abu Dhabi Airport Code
#     destination = 'Tokyo'  # Narita Airport Code, Japan
#     start_month = 'March'
#     start_day = '1'
#     end_month = 'March'
#     end_day = '23'

#     # Format prompt
#     prompt = prompt_template.format(
#         origin=origin,
#         destination=destination,
#         start_month=start_month,
#         start_day=start_day,
#         end_month=end_month,
#         end_day=end_day,
#     )



#     i = 0
#     next_prompt = prompt
#     while i < max_turns:
#         response = planner.plan(next_prompt)
#         tool, details = grab_actions(response)
#         next_prompt = response
#         i += 1
        # if tool:
        #     if tool not in known_actions:
        #         print(f"Unknown tool: {tool}")
        #         break
        #     print("--- running {} {} ---".format(tool, details))
        #     action = known_actions[tool]()
        #     search_resp = action.search(details)
        #     print("--- summarizing results ---")
        #     summary = summarizer.summarize(search_resp)
        #     # print("--- Observation: {} ---".format(summary))
        #     next_prompt = f"Observation: {summary}"
        # else:
        #     return response
        
# if __name__ == "__main__":
#     query()

def chat_loop():
    """Runs the travel itinerary query in a loop for multiple user queries."""
    
    planner = PlannerAgent()
    web_search = SearchWeb()
    summarizer = SummarizerAgent()

    while True:
        print("\nEnter your trip details (or type 'exit' to quit):")
        
        origin = input("Enter your departure city: ")
        if origin.lower() == "exit":
            print("Goodbye!")
            break
        
        destination = input("Enter your destination: ")
        start_month = input("Enter the start month: ")
        start_day = input("Enter the start day: ")
        end_month = input("Enter the end month: ")
        end_day = input("Enter the end day: ")

        prompt_template = """
        I want you to build an itinerary for a trip from {origin} to {destination} 
        starting from {start_month} {start_day} to {end_month} {end_day}.
        """
        
        prompt = prompt_template.format(
            origin=origin,
            destination=destination,
            start_month=start_month,
            start_day=start_day,
            end_month=end_month,
            end_day=end_day,
        )

        i = 0
        next_prompt = prompt
        final_response = None  

        while i < 6:  # Limit turns to avoid infinite loops
            response = planner.plan(next_prompt)
            tool, details = grab_actions(response)
            next_prompt = response
            i += 1

            if tool:
                if tool not in known_actions:
                    print(f"Unknown tool: {tool}")
                    break
                print("--- running {} {} ---".format(tool, details))
                action = known_actions[tool]()
                search_resp = action.search(details)
                print("--- summarizing results ---")
                summary = summarizer.summarize(search_resp)
                # print("--- Observation: {} ---".format(summary))
                next_prompt = f"Observation: {summary}"
            else:
                return response


if __name__ == "__main__":
    chat_loop()
