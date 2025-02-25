import logging
from openai import OpenAI



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class SummarizerAgent():

    summarizer_agent_prompt = """
    You are a helpful assistant which helps summarize sentences to extract the most relevant data.

    For example, You may receive the following response:
    The cheapest flights from Los Angeles to Basel cost $364 for a one-way ticket and $627 for a round-trip, according to KAYAK. 
    Flights from Los Angeles to Zurich are available for $283 for round-trip tickets. 
    For flights from Los Angeles to Geneva, prices start at $293 for round-trip tickets. 
    Additionally, one-way flights from California to Basel can also be found, and round-trip flights from California to Zurich start at $273. 
    KAYAK aggregates price data from various airlines and utilizes historical data to forecast pricing trends.

    And you can summarize accordingly:
    The best flights from Los Angeles to Zurich can be found on Swissair for the price of USD 1500 for economy tickets 
    for the dates 3 March 2025 to 14 March 2025.
    
    Another example for flight information:
    You can find and compare cheap flights to Moscow from various cities including Los Angeles, San Francisco, Denver, Colorado Springs, and Newark on Tripadvisor for the best airfares for your trip.
    And you can summarize accordingly:
    The flight information didn't provide a specific price for the round trip from Los Angeles to Moscow, 
    but you can find and compare cheap flights to Moscow from various cities including Los Angeles, San Francisco, Denver, Colorado Springs, and Newark on Tripadvisor for the best airfares for your trip.

    Another example:
    On average, a lodging in Geneva costs $203 per night at Grand Hotel (based on Booking.com Located in Geneva, a 3-minute walk from Central Tokyo, Bulgari Hotel Tokyo 
    has accommodations with a garden, private parking, a terrace and a bar

    And you can summarize accordingly:
    The average cost of a lodging in Tokyo is $203 per night at the Bulgari Hotel Tokyo which is located in Tokyo and is a 3-minute walk from Central Tokyo.
    """.strip()

    def __init__(self, openai_api_key, tavily_api_key,  model="gpt-4o-mini", developer=summarizer_agent_prompt):
        print("\n****************") 
        logging.info("Summarizer agent is initializing...")
        self.openai_api_key = openai_api_key
        self.tavily_api_key = tavily_api_key
        self.model = model
        self.developer = developer
        self.client = OpenAI(api_key=self.openai_api_key)
        self.messages = []
        print("Summarizer agent message- ", self.messages) 
       
        if self.developer:
            self.messages.append({"role": "developer", "content": self.developer})

    def summarize(self, prompt, max_tokens=2000):
        messages = self.messages + [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=messages
        )
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        print("\nResponse of summarizer chat: \n", response.choices[0].message.content)
        return response.choices[0].message.content