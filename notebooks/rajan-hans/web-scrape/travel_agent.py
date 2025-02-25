import re
import os
from dotenv import load_dotenv
import wikipedia
from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool
from langchain_community.chat_models import ChatOpenAI
from tavily import TavilyClient
import streamlit as st

class TravelAgent():
    def __init__(self, openai_key, tavily_key):
        """
        Initialize the TravelAgent by loading API keys, setting up the chat model,
        and initializing the agent with its tools.
        """
        
        self.openai_api_key = openai_key
        self.tavily_key = tavily_key
        #print(f"OpenAI API key: {self.openai_api_key}")
        #print(f"Tavily API key: {self.tavily_key}")

        if not self.tavily_key:
            st.error("Tavily API key not found. Please set it in your environment or .env file.")
            raise ValueError("Missing Tavily API key")
        if not self.openai_api_key:
            st.error("OpenAI API key not found. Please set it in your environment or .env file.")
            raise ValueError("Missing OpenAI API key")
        
        # Initialize clients and LLM
        self.tav_client1 = TavilyClient() # For weather
        self.tav_client2 = TavilyClient() # For tickets
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=self.openai_api_key)
        self.agent = self.initialize_agent()

    def get_weather(self, query):
        """
        Parses the query to extract city and travel month, then returns weather information.
        """
        try:
            city_match = re.search(r"City:\s*([^\.]+)\.", query)
            month_match = re.search(r"Travel month:\s*([^\.]+)\.", query)
            city = city_match.group(1).strip() if city_match else query.strip()
            month = month_match.group(1).strip() if month_match else "Anytime"
            if month == "Anytime":
                return f"No specific travel month provided for {city}; weather forecast not requested."
            # Use Tavily API client to get weather information.
            tav_resp1 = self.tav_client1.search(f"What is the average temperature in {city} for the {month}?")
            return tav_resp1
        except Exception as e:
            return f"Error retrieving weather information: {str(e)}"

    def search_wikipedia(self, query):
        """
        Returns a brief summary of the city using Wikipedia.
        """
        try:
            summary = wikipedia.summary(query, sentences=2)
            return summary
        except Exception as e:
            return f"Error retrieving Wikipedia summary: {str(e)}"

    def search_tickets(self, query):
        """
        Parses the query for city and month then returns airline ticket pricing information.
        """
        try:
            city_match = re.search(r"City:\s*([^\.]+)\.", query)
            month_match = re.search(r"Travel month:\s*([^\.]+)\.", query)
            city = city_match.group(1).strip() if city_match else query.strip()
            month = month_match.group(1).strip() if month_match else "Anytime"
            if month == "Anytime":
                return f"No specific travel month provided for {city}; ticket search not requested."
            tav_resp2 = self.tav_client2.search(
                f"Find the best airline ticket price (in USD) from Los Angeles to {city} for the {month}?"
            )
            return tav_resp2
        except Exception as e:
            return f"Error retrieving ticket information: {str(e)}"

    def initialize_agent(self):
        """
        Sets up the LangChain agent with the necessary tools.
        """
        weather_tool = Tool(
            name="WeatherTool",
            func=self.get_weather,
            description="Use this tool to get real weather information for a city given a specific travel month. " +
                        "The query should include 'City: <city>. Travel month: <month>.'"
        )
        wiki_tool = Tool(
            name="WikipediaTool",
            func=self.search_wikipedia,
            description="Use this tool to get a detailed summary and description of the city including airport, sights, and local cuisine."
        )
        ticket_tool = Tool(
            name="TicketTool",
            func=self.search_tickets,
            description="Use this tool to get airline ticket pricing information."
        )

        tools = [weather_tool, wiki_tool, ticket_tool]
        agent = initialize_agent(
            tools, self.llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True, handle_parsing_errors=True
        )
        return agent

    def run_query(self, query):
        """
        Runs the composite query through the agent and returns its response.
        """
        return self.agent.run(query)
