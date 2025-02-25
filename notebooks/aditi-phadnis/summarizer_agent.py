import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found.")

class SummarizerAgent:

    summarizer_agent_prompt = """
    You are a helpful assistant which helps summarize sentences to extract the most relevant data.

    For example, You may receive the following sentence:
    Book your flights to Tokyo with Etihad Airways. Fly economy, business or first class with us and enjoy premium travel 
    experience to Tokyo (KHI). ... Book now From Abu Dhabi To Tokyo Fare Type Round-trip Economy Dates 9 May 2025 - 14 May 2025 
    From AED3,085 Last Seen 7 hours ago. From Abu Dhabi (AUH) To Tokyo (KHI) Round-trip / Book United Arab Emirates to Tokyo flights 
    with Etihad Airways. Fly economy, business or first class with us and enjoy premium travel experience from United Arab Emirates to Tokyo. ... 
    Book now From Abu Dhabi To Tokyo Fare Type Round-trip Economy Dates 2 Mar 2025 - 16 Mar 2025 From AED4,225 Last Seen 1 day ago.

    And you can summarize accordingly:
    The best flights from Abu Dhabi to Tokyo can be found on Etihad Airways for the price of 3,085 AED for economy tickets 
    for the dates 9 May 2025 to 14 May 2025 and 2 Mar 2025 to 16 Mar 2025 respectively.

    Another example:
    On average, a lodging in Tokyo costs $203 per night at Bulgari Hotel Tokyo (based on Booking.com Located in Tokyo, a 3-minute walk from Central Tokyo, Bulgari Hotel Tokyo 
    has accommodations with a garden, private parking, a terrace and a bar

    And you can summarize accordingly:
    The average cost of a lodging in Tokyo is $203 per night at the Bulgari Hotel Tokyo which is located in Tokyo and is a 3-minute walk from Central Tokyo.
    """.strip()

    def __init__(self, model="gpt-4o-mini", developer=summarizer_agent_prompt):
        logging.info("Summarizer agent is initializing...")
        self.model = model
        self.developer = developer
        self.client = OpenAI()
        self.messages = []
        if self.developer:
            self.messages.append({"role":"developer","content":self.developer})

    def summarize(self, prompt, max_tokens=2000):
        messages = self.messages + [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=messages
        )
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        print("\nResponse of chat: \n", response.choices[0].message.content)
        return response.choices[0].message.content