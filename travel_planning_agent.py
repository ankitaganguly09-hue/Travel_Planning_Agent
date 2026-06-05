import os
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.messages import HumanMessage, AIMessage


# =========================
# SIMPLE MEMORY
# =========================

memory_store = {}

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


# =========================
# CHAT HISTORY STORE
# =========================

chat_history = []


# =========================
# TOOLS
# =========================

@tool
def save_preference(key: str, value: str) -> str:
    """Save a user preference like budget, style, etc."""
    memory_store[key] = value
    return f"Saved {key} = {value}"


@tool
def get_preferences() -> Dict:
    """Return all stored preferences."""
    return memory_store


@tool
def get_weather(city: str) -> str:
    """Get current weather from OpenWeatherMap."""

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )

    res = requests.get(url).json()

    if res.get("cod") != 200:
        return f"Error: {res.get('message')}"

    temp = res["main"]["temp"]
    desc = res["weather"][0]["description"]

    return f"{city}: {temp}°C, {desc}"


@tool
def suggest_itinerary(destination: str) -> str:
    """Create a simple travel itinerary using stored preferences."""

    style = memory_store.get("style", "general travel")
    budget = memory_store.get("budget", "medium")

    return f"""
Trip Plan for {destination}

Style: {style}
Budget: {budget}

Day 1: Arrival + explore local spots
Day 2: Sightseeing + food exploration
Day 3: Relax + shopping
"""


# =========================
# LLM (MISTRAL)
# =========================

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.7,
    api_key=MISTRAL_API_KEY
)


# =========================
# PROMPT
# =========================

prompt = """
You are a Travel Planning Agent.

You help users:
- Save preferences
- Check weather
- Create itineraries

Always use tools when needed.
Keep answers simple and useful.
"""


# =========================
# AGENT
# =========================

tools = [
    save_preference,
    get_preferences,
    get_weather,
    suggest_itinerary
]

agent = create_agent(
    llm,
    tools=tools,
    system_prompt=prompt
)


# =========================
# RUN LOOP (WITH CHAT HISTORY)
# =========================

print("🌍 Travel Agent Running (with chat history)...\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    # -------------------------
    # Build message-based input
    # -------------------------

    messages = []

    # add previous chat history
    messages.extend(chat_history)

    # add new user message
    messages.append(HumanMessage(content=user_input))

    # invoke agent
    result = agent.invoke({"messages": messages})

    # extract response (robust handling)
    if isinstance(result, dict) and "output" in result:
        output = result["output"]
    else:
        output = str(result)

    

    # -------------------------
    # update history
    # -------------------------

    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=output))

    print("\nAgent:", result["messages"][-1].content, "\n")