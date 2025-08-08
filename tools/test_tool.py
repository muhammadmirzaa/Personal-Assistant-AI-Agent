from langchain.agents import AgentType, initialize_agent, Tool
from langchain_community.agent_toolkits.steam.toolkit import SteamToolkit
from langchain_community.utilities.steam import SteamWebAPIWrapper
from langchain_openai import ChatOpenAI
import os
from steam.client import SteamClient
from bs4 import BeautifulSoup
import requests
from langchain_core.tools import tool
from langchain.memory import ConversationBufferMemory


steam_api = os.getenv("STEAM_KEY")
steam_id = os.getenv("STEAM_ID")
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model= "gpt-3.5-turbo", temperature=0, openai_api_key=api_key)
try:
    Steam = SteamClient()
    Steam.login(username=steam_api, password=steam_id)
except Exception as e:
    print(f"Error initializing SteamClient: {e}")
    Steam = None
def get_game(game_name):
    url = f"https://store.steampowered.com/search/?term={game_name.replace(' ', '+')}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find("a", class_ = 'search_result_row')
        if result:
            game_id = result['data-ds-appid']
            return game_id
    return None

def get_game_info(game_id):
    api_url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data and data[str(game_id)]["success"]:
            game_info = data[str(game_id)]["data"]
            formatted_info = {
                    "Name": game_info.get("name"),
                    "Steam URL": f"https://store.steampowered.com/app/{game_info.get('steam_appid')}",
                    "Price": game_info.get("price_overview", {}).get("final_formatted", "N/A"),
                    "Description": game_info.get("short_description"),
                    "Metacritic Score": game_info.get("metacritic", {}).get("score", "N/A"),
                    "Genres": ", ".join([genre["description"] for genre in game_info.get("genres", [])]),
            }
            return formatted_info
    return None

@tool
def get_game_data(game_name):
    """
    Get the game data from Steam using its name
    """
    game_id = get_game(game_name)
    if game_id:
        game_info = get_game_info(game_id)
        return game_info
    return None

tools = [Tool(
    name="GetGameInfo",
    func=get_game_data,
    description="Get the game data and steam url from Steam by using its name as input"
)]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory, 
    verbose=True
)

out = agent("can you give the information about the game Elden Ring")
print(out)