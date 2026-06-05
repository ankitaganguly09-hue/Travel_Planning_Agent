# 🌍 Travel Planning AI Agent

A simple yet powerful AI travel assistant built using LangChain, Mistral AI, OpenWeatherMap API, and Streamlit.

The agent can:
- 🌦️ Check real-time weather
- 🧠 Remember user preferences (budget, style, likes)
- 🗺️ Generate travel itineraries
- 💬 Chat with memory (multi-turn conversation)
- 🎨 Provide a clean ChatGPT-like UI

## ✨ Features

🤖 AI Agent built using LangChain `create_agent()` and powered by Mistral AI (ChatMistralAI). It uses tool-based reasoning to decide when to call external functions like weather, memory, or itinerary generation.

🌦️ Weather Tool uses OpenWeatherMap API to fetch real-time weather data like temperature and conditions for any city.

🧠 Memory System stores user preferences such as budget, travel style, and interests in an in-memory Python dictionary for personalization during the session.

🗺️ Travel Planning tool generates simple 3-day itineraries and personalizes them based on saved preferences.

💬 Chat UI is built using Streamlit with a ChatGPT-like interface and maintains session-based conversation history for a smooth chat experience.

## 🏗️ Tech Stack

LangChain, Mistral AI, OpenWeatherMap API, Streamlit, Python, dotenv

## 📁 Project Structure

travel-agent/
├── app.py              # Streamlit UI
├── .env                # API keys
├── requirements.txt
└── README.md

## ⚙️ Installation

Clone the repository:

git clone https://github.com/ankitaganguly09-hue/Travel_Planning_Agent.git  
cd Travel_Planning_Agent  

Create virtual environment:

python -m venv venv  
source venv/bin/activate   # Mac/Linux  
venv\Scripts\activate      # Windows  

Install dependencies:

pip install -r requirements.txt  

Create a `.env` file and add:

MISTRAL_API_KEY=your_mistral_api_key  
OPENWEATHER_API_KEY=your_openweather_api_key  

## ▶️ Run the App

streamlit run app.py  

Then open:

http://localhost:8501  

## 💬 Example Usage

User: I like beaches and budget travel  
User: Plan a 3-day trip to Goa  
User: What is the weather in Manali  

## 🧠 How It Works

User sends message via Streamlit UI → LangChain agent receives it → Agent decides which tool to use (weather, memory, or itinerary) → Mistral LLM generates response → Chat history is stored in session state → UI updates in real time.

## 🧩 Tools Used

Weather Tool: Fetches live weather using OpenWeatherMap API and returns temperature and condition.

Memory Tool: Stores user preferences in a Python dictionary for personalization.

Itinerary Tool: Generates a simple travel plan using stored preferences like budget and style.

## 🚀 Future Improvements

Persistent memory using SQLite or vector database, integration with Google Places API for hotels and restaurants, PDF export for itineraries, multi-city trip planning, map visualization, and streaming responses like ChatGPT typing effect.

## 🧑‍💻 Author

Built while learning LangChain Agents and AI tool-based systems.

## 📜 License

This project is open-source and free to use for learning and personal projects.
