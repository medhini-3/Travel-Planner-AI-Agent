import os
import google.generativeai as genai
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# Force Python to load your .env file locally
load_dotenv()

# Configure your Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

router = APIRouter(tags=["Trip Planner"])

class TripRequest(BaseModel):
    destination: str
    duration_days: int
    interests: List[str] = []

@router.post("/plan-trip")
async def plan_trip(request: TripRequest):
    def generate_streaming_itinerary():
        try:
            model = genai.GenerativeModel("gemini-3.5-flash-lite")
            prompt = f"Plan a detailed {request.duration_days} day trip to {request.destination} focusing on {', '.join(request.interests)}."
            
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            print(f"🚨 CRASH REASON: {str(e)}")
            yield f"\n\n### ⚠️ Connection Error\nSomething went wrong: {str(e)}"

    return StreamingResponse(generate_streaming_itinerary(), media_type="text/plain")
