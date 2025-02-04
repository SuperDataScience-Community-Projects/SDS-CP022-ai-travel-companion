import os
from openai import OpenAI
from dotenv import load_dotenv

class PromptOptimizerAgent:
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found.")
    
    def __init__(self, model='gpt-4o-mini'):
        self.model = model

    def optimize_prompt(self, prompt, max_tokens=100):
        print("\nPrompt optimizer is called!")
        client = OpenAI()
        
        developer_prompt = """
        You are a helpful assistant and your job is to optimize a given prompt to make it more
        effective for the AI model to generate a response. If there are missing details in the prompt,
        add in the missing details.

        For example. 'User: flight details from abu dhabi' can become 'Please provide details of flights
        going out of Abu Dhabi in the next 7 days including prices and boarding times.'

        'User: What are the best hotel' can become 'Please find me the best hotel deals for the destination
        I am travelling to in the next 7 days.'
        """

        messages = [
            {"role":"developer",
             "content":developer_prompt},
            {"role": "user",
             "content": prompt}
        ]
        print("Initial Prompt: ", prompt)
        response = client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=messages
        )
        print("Optimized Prompt: ", response.choices[0].message.content)
        return response.choices[0].message.content

