import os
from google import genai
from google.genai import types
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

# Initialize the router
router = APIRouter()

# Initialize the Google GenAI client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class TripRequest(BaseModel):
    destination: str
    duration_days: int
    interests: List[str] = []

# --- Structured Pydantic Schemas for Map Integration ---
class Location(BaseModel):
    name: str = Field(description="Name of the real place or real hotel")
    latitude: float = Field(description="Exact GPS latitude coordinate")
    longitude: float = Field(description="Exact GPS longitude coordinate")
    description: str = Field(description="Short engaging description")

class DayItinerary(BaseModel):
    day: int
    theme: str = Field(description="Theme for the day")
    hotel: Location = Field(description="Suggested real hotel for the night")
    activities: List[Location] = Field(description="Places to visit this day in chronological order")

class TripResponse(BaseModel):
    destination: str
    itinerary: List[DayItinerary]

@router.post("/api/v1/plan-trip")
async def plan_trip(request: TripRequest):
    if not client:
         raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable is missing.")

    prompt = (
        f"Plan a {request.duration_days}-day trip to {request.destination} focusing on "
        f"{', '.join(request.interests)}. Include real hotels, real attractions, and their exact GPS coordinates."
    )

    try:
        # Force Gemini to return a perfect JSON object matching our map schema
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TripResponse,
                temperature=0.7,
            ),
        )
        
        # 'parsed' automatically contains the validated Pydantic object
        return response.parsed.model_dump()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating itinerary: {str(e)}")
