import os
from google import genai
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Initialize the new Google GenAI client cleanly
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class TripRequest(BaseModel):
    destination: str
    duration_days: int
    interests: List[str] = []

@router.post("/api/v1/plan-trip")
async def plan_trip(request: TripRequest):
    def generate_streaming_itinerary():
        try:
            chat = client.chats.create(model="gemini-1.5-flash")
            prompt = f"Plan a {request.duration_days} day trip to {request.destination} focusing on {', '.join(request.interests)}. Use markdown formatting with clear headings and bullet points."
            response = chat.send_message(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"\n\nError generating itinerary: {str(e)}"

    return StreamingResponse(generate_streaming_itinerary(), media_type="text/plain")
