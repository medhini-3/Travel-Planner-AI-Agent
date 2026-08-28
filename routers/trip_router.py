import os
import requests
from google import genai
from google.genai import types
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()

# Load API Keys
api_key = os.getenv("GEMINI_API_KEY")
serpapi_key = os.getenv("SERPAPI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class TripRequest(BaseModel):
    destination: str
    duration_days: int
    interests: List[str] = []

class Location(BaseModel):
    name: str = Field(description="Name of the real place")
    latitude: float = Field(description="Exact GPS latitude coordinate")
    longitude: float = Field(description="Exact GPS longitude coordinate")
    description: str = Field(description="Short engaging description")

class DayItinerary(BaseModel):
    day: int
    theme: str = Field(description="Theme for the day")
    hotel: Location = Field(description="Suggested real hotel for the night")
    meals: List[Location] = Field(description="Real restaurants or cafes to eat at")
    activities: List[Location] = Field(description="Places to visit this day in chronological order")

class TripResponse(BaseModel):
    destination: str
    itinerary: List[DayItinerary]

def fetch_real_places(destination: str, search_type: str) -> str:
    """Agentic Tool: Fetches live data and exact GPS coordinates from Google Maps via SerpApi."""
    if not serpapi_key:
        return f"No SerpApi key found for {search_type}."
        
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_maps",
        "q": f"top-rated {search_type} in {destination}",
        "type": "search",
        "api_key": serpapi_key
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        local_results = data.get("local_results", [])
        
        context = f"LIVE {search_type.upper()} DATA FROM GOOGLE MAPS:\n"
        # Grab the top 5 real places and their verified coordinates
        for place in local_results[:5]: 
            name = place.get("title")
            rating = place.get("rating", "N/A")
            gps = place.get("gps_coordinates", {})
            lat = gps.get("latitude")
            lng = gps.get("longitude")
            
            if name and lat and lng:
                context += f"- {name} (Rating: {rating} stars), GPS: {lat}, {lng}\n"
                
        return context
    except Exception as e:
        print(f"SerpApi Error: {e}")
        return ""

@router.post("/api/v1/plan-trip")
async def plan_trip(request: TripRequest):
    if not client:
         raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable is missing.")

    # 1. Agentic Action: Fetch Live Data First (Multiple Tool Calls)
    live_hotels = fetch_real_places(request.destination, "hotels")
    live_restaurants = fetch_real_places(request.destination, "restaurants")

    # 2. Inject the live data into the prompt as strict instructions
    prompt = (
        f"Plan a {request.duration_days}-day trip to {request.destination} focusing on {', '.join(request.interests)}.\n\n"
        f"CRITICAL INSTRUCTIONS:\n"
        f"1. You MUST use the following real hotels for the accommodations. Do not invent your own.\n"
        f"2. You MUST use the following real restaurants for the meals. Do not invent your own.\n"
        f"3. You MUST use the exact GPS coordinates provided below.\n\n"
        f"{live_hotels}\n\n"
        f"{live_restaurants}\n\n"
        f"Include real attractions for the daily activities with their estimated GPS coordinates."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TripResponse,
                temperature=0.7,
            ),
        )
        return response.parsed.model_dump()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating itinerary: {str(e)}")
