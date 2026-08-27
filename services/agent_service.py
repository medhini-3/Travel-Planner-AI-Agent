import os
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError
from tools.search_tool import search_web_for_travel
from tools.flight_tool import search_live_flights
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_trip_plan(destination: str, duration_days: int, interests: list[str]) -> str:
    prompt = f"Plan a {duration_days}-day trip to {destination}. Interests: {', '.join(interests)}. Include live flight estimates if possible."
    
    max_retries = 2
    for attempt in range(max_retries):
        try:
            chat = client.chats.create(
                model='gemini-3.6-flash',
                config=types.GenerateContentConfig(
                    tools=[search_web_for_travel, search_live_flights],
                    system_instruction="You are an expert travel agent. Use search tools for live details."
                )
            )
            response = chat.send_message(prompt)
            return response.text

        except APIError as e:
            # Check for 429 Rate Limit
            if e.code == 429 and attempt < max_retries - 1:
                time.sleep(35)  # Wait for the quota window to clear
                continue
            raise RuntimeError("API quota temporarily exceeded. Please wait a minute and try again.")