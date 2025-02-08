from dotenv import load_dotenv
import os

def main():
    # Load environment variables from the .env file located in the current directory.
    load_dotenv()

    # Retrieve the API keys from the environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    # Check if both keys were loaded successfully
    if openai_api_key is None or tavily_api_key is None:
        print("Error: One or more API keys are missing in the .env file.")
    else:
        print("OPENAI_API_KEY:", openai_api_key)
        print("TAVILY_API_KEY:", tavily_api_key)

if __name__ == "__main__":
    main()
