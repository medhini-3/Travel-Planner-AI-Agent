import os
from google import genai
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List

# Initialize the router
router = APIRouter()

# Initialize the new Google GenAI client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class TripRequest(BaseModel):
    destination: str
    duration_days: int
    interests: List[str] = []

# Ensure the path perfectly matches what the test is requesting
@router.post("/api/v1/plan-trip")
async def plan_trip(request: TripRequest):
    if not client:
         raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable is missing.")

    def generate_streaming_itinerary():
        try:
            chat = client.chats.create(model="gemini-3.5-flash-lite")
            prompt = f"Plan a {request.duration_days} day trip to {request.destination} focusing on {', '.join(request.interests)}. Use markdown formatting with clear headings and bullet points."
            
            # Stream the response using the new SDK
            response = chat.send_message_stream(prompt)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"\n\nError generating itinerary: {str(e)}"

    return StreamingResponse(generate_streaming_itinerary(), media_type="text/plain")
