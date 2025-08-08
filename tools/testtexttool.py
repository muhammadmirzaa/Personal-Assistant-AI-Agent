import pywhatkit as kit
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_openai import ChatOpenAI
import os
from langchain_core.tools import tool
from langchain.memory import ConversationBufferMemory
import re
import time
import pyautogui

api_key = os.getenv("OPENAI_API_KEY")

@tool
def send_text(input_text: str):
    """
    Send a text message to a contact number using WhatsApp.
    The input_text should contain both the contact number and the message/topic.
    Tool takes single argument: input_text.
    """
    # Extract the contact number
    contact_no_match = re.search(r'\+?\d+', input_text)
    if not contact_no_match:
        print("Invalid contact number")
        return None

    contact_no = contact_no_match.group()  # Extract the matched string

    topic = re.sub(r'\+?\d+', '', input_text).strip()

    if topic:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        message = llm.invoke(f"Write a short and friendly WhatsApp message about: {topic} Just write the text nothing additional as if you were chatting directly to that person").content
    else:
        message = "Hello! This is an automated message."

    kit.sendwhatmsg_instantly(contact_no, message, wait_time = 20)
    time.sleep(5)
    pyautogui.press('enter')

    print(f"Message sent successfully to {contact_no}: {message}")
    return None

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)

tools = [Tool(
    name="send_text", 
    func=send_text, 
    description=(
            "Send a WhatsApp message to a contact number. "
            "Provide 'contact_no' (e.g., +1234567890) and 'message' (e.g., 'Hello, how are you?') as a single argument."
            )
        )
    ]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=memory)

prompt = "Send a text message to +923407988714 saying go to sleep'"

out = agent.invoke(prompt)
print(out) 