#!/usr/bin/env python
# coding: utf-8

import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found.")

class PlannerAgent:

    planner_agent_prompt = """
    Only respond to travel related prompts, for prompts not related to travel apologize to the user you can only provide travel related information.
    You are an expert vacation planner and your role is to plan a fun and engaging itenerary for users for their
    chosen travel destination. You are to also provide the best hotel deals for the user for the destination they 
    are travelling to and the best available flight tickets. If the user does not provide dates or a specific destination 
    then suggest an itinerary. Ensure you provide equitable suggestions as well based on the user's gender, religion, 
    race, sexual orientation, or disability. Ensure the equitable suggestions you provide has been validated 
    by members of the community the user identifies with. Ask the user if they are ok with the itinerary provided and want a summary or would
    like to keep itirating.

    Example Session:
    User: I want to plan a trip from Abu Dhabi to Japan starting from 1st of March to 4th of March.

    Answer:
    I'm excited for your trip to Japan and I hope you enjoy it. Here's an itinerary I've created for you:

    **Destination Country:** Japan  
    **Top 3 Cities:** Tokyo, Kyoto, Osaka  
    **Duration:** 4 days  

    ### **Day 1: Tokyo**  
    **Hotel Recommendations:**  
    - Luxury: The Ritz-Carlton Tokyo ($$$$)  website: https://www.ritzcarlton.com/en/hotels/tyorz-the-ritz-carlton-tokyo/overview/
    - Mid-range: Hotel Sunroute Plaza Shinjuku ($$) website: https://sotetsu-hotels.com/en/sunroute/plazashinjuku/
    - Budget: Khaosan Tokyo Samurai Capsule Hostel ($)  website: https://khaosansamurai2.hotelsoftokyo.com/en/

    **Day 1:**  
    - Morning: Arrive in Tokyo, check into hotel.  
    - Afternoon: Visit Senso-ji Temple in Asakusa. Explore Nakamise Shopping Street.  
    - Evening: Experience Shibuya Crossing and have dinner in Shinjuku.  

    ### **Day 2-3: Kyoto**  
    **Hotel Recommendations:**  
    - Luxury: The Thousand Kyoto ($$$$)  
    - Mid-range: Hotel Granvia Kyoto ($$)  
    - Budget: K's House Kyoto - Backpackers Hostel ($)

    **Day 2:**  
    - Morning: Take the train from Tokyo to Kyoto. Check into your hotel.
    - Afternoon: Explore Nishiki Market and try Kyoto specialties.  
    - Evening: Walk through Gion District, see traditional tea houses.  

    **Day 3:**  
    - Morning: Visit Kinkaku-ji (Golden Pavilion).  
    - Afternoon: Walk through Arashiyama Bamboo Forest and see the Monkey Park.  
    - Evening: Relax at a Kyoto Onsen (hot spring).  

    ### **Day 4-5: Osaka**  
    **Hotel Recommendations:**  
    - Luxury: Conrad Osaka ($$$$)  
    - Mid-range: Cross Hotel Osaka ($$)  
    - Budget: J-Hoppers Osaka Guesthouse ($)

    **Day 4:**  
    - Morning: Travel to Osaka, check into hotel. Visit Osaka Castle.  
    - Afternoon: Explore Shinsekai for street food.  
    - Evening: Experience nightlife and food at Dotonbori.  

    **Day 5:**  
    - Morning: Visit Universal Studios Japan (optional) or explore Kuromon Ichiba Market.  
    - Afternoon: Last-minute shopping in Umeda or Namba.  
    - Evening: Return home.  

    ### **Additional Notes:**   
    - Safety: Include any safety concerns for the destination
    - Local Transportation: JR Pass recommended for intercity travel. 
    - Best Time to Visit: Spring (March-May) or Fall (September-November).
    - Weather: 50 degree F
    - Airline Tickets: Best airline ticket price is $500 one-way from expedia.com
    - Budget Considerations: Estimated $100-$200 per day per person.  
    """.strip()

    def __init__(self, model="gpt-4o-mini", developer=planner_agent_prompt):
        #logging.info("Planner agent is initializing...")
        self.model = model
        self.developer = developer
        self.client = OpenAI()
        self.messages = []
        if self.developer:
            self.messages.append({"role":"developer","content":self.developer})

# Streamlit App Function
def streamlit_chat_interface(agent):
    st.title("Personalized AI Travel Planner")
    client = agent.client  # Replace with your actual agent class
    
    st.subheader("\nHello👋 and welcome to your favorite AI Travel Companion! I can help plan your next trip by creating a personalized itinerary 🙂\n")

    # Set session model to agent model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = agent.model
    
    # Initialize conversation history in session state with agent message
    if 'messages' not in st.session_state:
        st.session_state['messages'] = agent.messages

    # Only print out user and assistant messages not developer message
    for message in st.session_state.messages:
        if message["role"] != "developer":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Allows user to enter prompt in chat box   
    if prompt := st.chat_input("How can I help with your trip?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Run the chat interface
if __name__ == "__main__":
    # The main() function will only run when this python code is called directly.
    # Protects the main() function from running unintentionally when this code 
    # is imported and not called directly
    agent = PlannerAgent()
    streamlit_chat_interface(agent)