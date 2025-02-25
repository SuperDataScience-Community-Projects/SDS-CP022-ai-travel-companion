from planner_agent import PlannerAgent
from summarizer_agent import SummarizerAgent
from tools import SearchWeb
import re
import gradio as gr
from datetime import datetime
import calendar

known_actions = {
    "web_search": SearchWeb
}

def grab_actions(response):
    pattern = r"^(Action):\s(\w+):\s(.*?)(?=\.\s|$)"
    match = re.search(pattern, response, re.MULTILINE)
    if match:
        tool = match.group(2)
        details = match.group(3)
    return tool, details

def validate_dates(start_date, end_date):
    try:
        # Convert float timestamp to datetime if necessary
        if isinstance(start_date, (int, float)):
            start = datetime.fromtimestamp(start_date)
        else:
            start = start_date

        if isinstance(end_date, (int, float)):
            end = datetime.fromtimestamp(end_date)
        else:
            end = end_date

        if start > end:
            return False, "Start date cannot be after end date"
        if start < datetime.now():
            return False, "Start date cannot be in the past"
        return True, ""
    except (ValueError, TypeError) as e:
        return False, "Please enter valid dates"

def query(origin, destination, start_date, end_date):
    # Validate inputs
    if not origin or not destination:
        return "Please enter both origin and destination"
    
    is_valid, error_message = validate_dates(start_date, end_date)
    if not is_valid:
        return error_message
    
    # No need to convert to datetime since we already have datetime objects
    start = start_date if isinstance(start_date, datetime) else datetime.fromtimestamp(start_date)
    end = end_date if isinstance(end_date, datetime) else datetime.fromtimestamp(end_date)
    
    start_month = calendar.month_name[start.month]
    start_day = start.day
    end_month = calendar.month_name[end.month]
    end_day = end.day
    
    # Initialize agents and run the query
    planner = PlannerAgent()
    summarizer = SummarizerAgent()

    prompt_template = """
    I want you to build an itinerary for me for a trip from {origin} to {destination} starting 
    from {start_month} {start_day} to {end_month} {end_day}.
    """

    prompt = prompt_template.format(
        origin=origin,
        destination=destination,
        start_month=start_month,
        start_day=start_day,
        end_month=end_month,
        end_day=end_day)
    
    i = 0
    next_prompt = prompt
    max_turns = 6
    
    while i < max_turns:
        response = planner.plan(next_prompt)
        next_prompt = response
        i += 1
        if "Action" in next_prompt:
            tool, details = grab_actions(response)
            if tool not in known_actions:
                print(f"Unknown tool: {tool}")
                break
            action = known_actions[tool]()
            search_resp = action.search(details)
            summary = summarizer.summarize(search_resp)
            next_prompt = f"Observation: {summary}"
        else:
            return response.strip("Answer:")

def main():
    with gr.Blocks(theme=gr.themes.Soft()) as iface:
        gr.Markdown("""
        # 🌍 AI Travel Companion
        Your personal AI travel planner that creates customized itineraries based on your preferences.
        """)
        
        with gr.Row():
            with gr.Column():
                origin = gr.Textbox(
                    label="Where are you traveling from?",
                    placeholder="e.g., New York, London, Tokyo",
                    info="Enter your departure city"
                )
                destination = gr.Textbox(
                    label="Where would you like to go?",
                    placeholder="e.g., France, Italy, Japan",
                    info="Enter your destination country"
                )
        
        with gr.Row():
            start_date = gr.DateTime(
                label="Start Date",
                info="When would you like to start your journey?"
            )
            end_date = gr.DateTime(
                label="End Date",
                info="When would you like to end your journey?"
            )
        
        submit_btn = gr.Button("Plan My Trip!", variant="primary")
        
        # Changed from Markdown to Textbox
        output = gr.Textbox(
            label="Your Personalized Itinerary",
            lines=10,  # Makes the textbox bigger
            interactive=False  # User can't edit the output
        )
        
        submit_btn.click(
            fn=query,
            inputs=[origin, destination, start_date, end_date],
            outputs=output
        )
        
        gr.Markdown("""
        ### Tips for better results:
        - Be specific with your departure city
        - Enter full country names for destinations
        - Plan your trip at least a few days in advance
        - Consider seasonal weather and events at your destination
        """)
    
    iface.launch()

if __name__ == "__main__":
    main()