import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage


# =========================
# MEMORY
# =========================

memory_store = {}

chat_history = []


# =========================
# API KEYS
# =========================

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


# =========================
# TOOLS
# =========================

@tool
def save_preference(key: str, value: str) -> str:
    """Save a user preference like budget, style, etc."""
    memory_store[key] = value
    return f"Saved {key} = {value}"


@tool
def get_preferences() -> dict:
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

    return f"{city}: {res['main']['temp']}°C, {res['weather'][0]['description']}"


@tool
def suggest_itinerary(destination: str) -> str:
    """Suggest a simple 3-day itinerary based on preferences."""
    style = memory_store.get("style", "general travel")
    budget = memory_store.get("budget", "medium")

    return f"""
Trip Plan for {destination}

Style: {style}
Budget: {budget}

Day 1: Arrival + explore
Day 2: Sightseeing + food
Day 3: Relax
"""


# =========================
# LLM + AGENT
# =========================

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.7,
    api_key=MISTRAL_API_KEY
)

prompt = """
You are a Travel Planning Agent.

Use tools when needed:
- weather
- preferences
- itinerary

Be concise and helpful.
"""

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
# STREAMLIT UI CONFIG
# =========================

st.set_page_config(
    page_title="🌍 Travel AI Agent",
    page_icon="✈️",
    layout="centered"
)

st.title("🌍 Travel Planning Agent")
st.caption("Your personal AI travel assistant")


# initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================
# DISPLAY CHAT HISTORY
# =========================

for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg.content)


# =========================
# INPUT BOX
# =========================

user_input = st.chat_input("Ask me to plan your trip...")

if user_input:

    # show user message
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    # build input for agent
    messages = st.session_state.chat_history.copy()

    result = agent.invoke({"messages": messages})

    # extract response
    if isinstance(result, dict) and "messages" in result:
        reply = result["messages"][-1].content
    else:
        reply = str(result)

    # show assistant response
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.chat_history.append(AIMessage(content=reply))