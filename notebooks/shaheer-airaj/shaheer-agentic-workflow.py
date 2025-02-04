import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from tavily import TavilyClient
from prompt_optimizer_agent import PromptOptimizerAgent

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found.")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found.")

MODEL = "gpt-4o-mini"
DOMAINS = [
    'https://www.expedia.ae/',
    'https://www.skyscanner.ae/',
    'https://www.etihad.com/en-ae/'
]

def search_flights(search_input):
    tavily_client = TavilyClient(TAVILY_API_KEY)
    response = tavily_client.search(search_input, include_domains=DOMAINS)
    response_list = [resp["content"] for resp in response["results"]]
    responses = " ".join(response_list)
    print("\nResponse of search_flights: \n", responses)

    return responses

def chat(MODEL):

    origin = input("Where are you flying from: ")
    destination = input("Where are you flying to: ")
    seat_class = input("Which class seats would you prefer: ")
    dep_date = input("When would you like to depart: ")
    arrival_date = input("When would you like to return: ")

    developer_message = """
    You are a helpful developer and your roles is to advice users on flight tickets and hotel bookings.
    You run in a loop of Thought, Action, PAUSE, Observation.
    At the end of the loop you output an Answer
    Use Thought to describe your thoughts about the question you have been asked.
    Use Action to run one of the actions available to you - then return PAUSE.
    Observation will be the result of running those actions.

    Your available actions are:
    
    web_search:
    e.g. Round trip flights from Abu Dhabi to Karachi in the next 7 days
    Runs a web search using Tavily to extract details of the latest flight details including ticket prices and timings

    Example Session:

    User: Please search for the latest flight details from Abu Dhabi to Morocco from the 1st of Mar to 23rd of March
    Thought: I should use web_search look up the flight ticket prices and days from Abu Dhabi to Morocco from
    the 1st of March to the 23rd of March.
    Action: web_search: Flight ticket prices from Abu Dhabi to Morocco from the 1st of Mar to 23rd of March.
    PAUSE

    You will be called again with this:
    
    Observation: The best tickets for flights from Abu Dhabi to Morocco can be found on expedia.com for the price of 2,500 AED for
    economy tickets.

    You then output:

    Answer: The best tickets for flights from Abu Dhabi to Morocco can be found on expedia.com for the price of 2,500 AED for
    economy tickets.
    """.strip()

    prompt_template = f"""
    Please search the latest flight details from {origin} to {destination}
    for {seat_class} class seats around these dates: {dep_date} to {arrival_date}.

    Include the following:
    1. What are the cheapest ticket prices
    2. When would be the best dates to travel in terms of the cheapest ticket
    """.strip()

    tools = {
        'web_search':search_flights
    }

    messages = [
    {"role":"developer","content":developer_message},
    {"role":"user", "content":prompt_template}
    ]
    
    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    ai_response = completion.choices[0].message.content
    print("\nAI: ", ai_response)

    messages.append({"role": "developer", "content": ai_response})
    
    # using regex to grab the action, the tool to use and the details of the tool input
    pattern = r"^(Action):\s(\w+):\s(.*?)(?=\.\s|$)"
    match = re.search(pattern, ai_response, re.MULTILINE)
    if match:
        action = match.group(1)
        tool = match.group(2)
        search_details = match.group(3)
    
        print("\nAction: ", action)
        print("\nTool: ", tool)
        print("\nSearch Details: ", search_details)
    else:
        print("\nNo match found")

    if 'Action' in action:
        prompt_optimizer_agent = PromptOptimizerAgent()
        optimized_prompt = prompt_optimizer_agent.optimize_prompt(search_details)
        tool_function = tools[tool]
        response = tool_function(optimized_prompt)

        messages.append({"role":"user","content":"Observation: " + response})

        client = OpenAI()
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        ai_response = completion.choices[0].message.content
        print("\nAI: ", ai_response)


def main():
    chat(MODEL=MODEL)

if __name__ == "__main__":
    main()