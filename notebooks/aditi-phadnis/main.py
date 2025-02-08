from planner_agent import PlannerAgent
from tools import SearchWeb
from dotenv import load_dotenv
from datetime import datetime


import openai
import os
import re

load_dotenv()


# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found.")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found.")



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




def query(max_turns=6):
    """Generates travel itinerary using Tavily, Amadeus, and OpenAI."""
    
    # Initialize agents
    planner = PlannerAgent()
    web_search = SearchWeb()

    # Define the user prompt
    prompt_template = """
    I want you to build an itinerary for a trip from {origin} to {destination} 
    starting from {start_month} {start_day} to {end_month} {end_day}.
    """
    
    # Sample Inputs
    origin = 'AUH'  # Abu Dhabi Airport Code
    destination = 'NRT'  # Narita Airport Code, Japan
    start_month = 'March'
    start_day = '1'
    end_month = 'March'
    end_day = '23'
    year = '2025'  # Assuming the year
    # Convert to date format
    check_in = datetime.strptime(f"{start_day} {start_month} {year}", "%d %B %Y").strftime("%Y-%m-%d")
    check_out = datetime.strptime(f"{end_day} {end_month} {year}", "%d %B %Y").strftime("%Y-%m-%d")



    # Format prompt
    prompt = prompt_template.format(
        origin=origin,
        destination=destination,
        start_month=start_month,
        start_day=start_day,
        end_month=end_month,
        end_day=end_day,
        check_out=check_out,
        check_in=check_in
        
    )

    # Step 1: Fetch Flight Data
    flights = planner.get_flight_details(origin, destination, "2025-03-01", "2025-03-23")
    
    # Step 2: Fetch Hotel Data
    hotels = planner.get_hotel_deals("TYO", "2025-03-01", "2025-03-23")  # Tokyo city code

    # Step 3: Perform Web Search (Tavily)
    web_info = web_search.search(f"Things to do in {destination} during {start_month}")

    # Step 4: Generate Final Itinerary using OpenAI
    itinerary_summary = f"Flights: {flights}\nHotels: {hotels}\nTravel Tips: {web_info}"
    itinerary = generate_itinerary(itinerary_summary)

    print("\n=== FINAL ITINERARY ===\n")
    print(itinerary)

if __name__ == "__main__":
    query()
