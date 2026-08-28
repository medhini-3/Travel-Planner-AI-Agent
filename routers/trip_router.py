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

# --- Detailed Schemas for Rich Information ---
class ActivityLocation(BaseModel):
    time_slot: str = Field(description="Scheduled time slot, e.g., '09:30 AM - 11:30 AM'")
    name: str = Field(description="Name of the attraction or activity")
    estimated_duration: str = Field(description="Estimated duration, e.g., '2 hours'")
    estimated_cost: str = Field(description="Entry fee or cost, e.g., '₹100 per person' or 'Free entry'")
    insider_tip: str = Field(description="Short, high-value local tip or best photo spot")
    latitude: float = Field(description="Exact GPS latitude coordinate")
    longitude: float = Field(description="Exact GPS longitude coordinate")
    description: str = Field(description="Engaging 1-2 sentence description of what to do")

class MealLocation(BaseModel):
    meal_type: str = Field(description="Type of meal: 'Breakfast', 'Lunch', 'Sunset Drinks', or 'Dinner'")
    time_slot: str = Field(description="Scheduled time slot, e.g., '01:00 PM - 02:30 PM'")
    name: str = Field(description="Name of the restaurant, cafe, or shack")
    must_try: str = Field(description="Must-try dish or specialty beverage")
    estimated_cost: str = Field(description="Estimated budget, e.g., '₹1,200 for two'")
    latitude: float = Field(description="Exact GPS latitude coordinate")
    longitude: float = Field(description="Exact GPS longitude coordinate")
    description: str = Field(description="Vibe and dining recommendation")

class HotelLocation(BaseModel):
    name: str = Field(description="Name of the hotel")
    rating: str = Field(description="Rating score, e.g., '4.6 ★'")
    price_tier: str = Field(description="Estimated price tier, e.g., 'Mid-Range (₹4,000/night)'")
    check_in_note: str = Field(description="Check-in time or notable amenity, e.g., 'Check-in 02:00 PM | Pool & Spa'")
    latitude: float = Field(description="Exact GPS latitude coordinate")
    longitude: float = Field(description="Exact GPS longitude coordinate")
    description: str = Field(description="Short description of location and stay vibe")

class DayItinerary(BaseModel):
    day: int
    theme: str = Field(description="Theme for the day, e.g., 'Coastal Heritage & Sunset Dining'")
    hotel: HotelLocation = Field(description="Suggested real hotel for the night")
    activities: List[ActivityLocation] = Field(description="Sightseeing activities in chronological order")
    meals: List[MealLocation] = Field(description="Curated restaurant stops across the day")

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

    # 1. Fetch Live SerpApi Data
    live_hotels = fetch_real_places(request.destination, "hotels")
    live_restaurants = fetch_real_places(request.destination, "restaurants")

    # 2. Structured Prompt with Timings & Rich Context
    prompt = (
        f"Create a comprehensive, time-stamped {request.duration_days}-day travel itinerary for {request.destination} "
        f"tailored to interests: {', '.join(request.interests)}.\n\n"
        f"CRITICAL REQUIREMENTS:\n"
        f"1. Schedule realistic chronological time slots for each activity (morning, afternoon, evening) and meal.\n"
        f"2. Provide estimated budget/costs and high-value insider tips for each stop.\n"
        f"3. You MUST use these real hotels from Google Maps with their exact GPS coordinates:\n{live_hotels}\n"
        f"4. You MUST use these real restaurants from Google Maps with their exact GPS coordinates:\n{live_restaurants}\n"
        f"5. Provide accurate GPS coordinates for all sightseeing locations."
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
