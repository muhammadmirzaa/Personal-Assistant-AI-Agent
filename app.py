import langchain_community
import openai
import numpy as np
import os 
import dotenv
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_community.utilities.steam import SteamWebAPIWrapper
from langchain_community.agent_toolkits.steam.toolkit import SteamToolkit
from langchain.memory import ConversationBufferMemory
from steam.client import SteamClient
import streamlit as st
import pywhatkit as kit
import json
import requests

load_dotenv()
llm_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = "gpt-3.5-turbo", temperature = 0.8, openai_api_key = llm_key )

# Define Weather tool
weather_key = os.getenv("OPENWEATHER_API_KEY")
weather = OpenWeatherMapAPIWrapper()

# Define Steam Tool
steam_api = os.getenv("STEAM_KEY")
steam_id = os.getenv("STEAM_ID")

# try:
#     Steam = SteamClient()
#     Steam.login(username=steam_api, password=steam_id)  # Example login, adjust as needed
#     toolkit = SteamToolkit.from_steam_api_wrapper(Steam)
# except ImportError as e:
#     print(f"Error initializing SteamClient: {e}")
#     toolkit = None
# except Exception as e:
#     print(f"An error occurred during SteamClient initialization: {e}")
#     toolkit = None

tools = load_tools(["openweathermap-api"], llm)
tools = [toolkit] + standard_tools if toolkit else standard_tools

# Agent Initialization
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(
    tools,
    llm,
    agent="chat-conversational-react-description",
    memory=memory,
    verbose=True
)

# Interaction Loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "end"]:
        print("Goodbye")
        break
    response = agent.invoke({"input": user_input})
    print(f"Agent: {response}")