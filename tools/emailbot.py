from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import tool
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials
import os

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=api_key) 

toolkit = GmailToolkit()

credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

tools = toolkit.get_tools()

memory = ConversationBufferMemory(memory_key = "chat_history", return_messages = True)
agent = initialize_agent(tools, llm, agent = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory = memory)
out = agent.invoke("Send an email to mmirza.bee20seecs@seecs.edu.pk saying this is a test email for the test tool")
print(out)