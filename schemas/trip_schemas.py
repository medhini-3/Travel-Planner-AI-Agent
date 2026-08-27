from pydantic import BaseModel, Field

class TripRequest(BaseModel):
    destination: str = Field(..., description="The city or country to visit")
    duration_days: int = Field(..., ge=1, le=30, description="Length of the trip")
    interests: list[str] = Field(default=[], description="User preferences like 'food', 'history'")

class TripResponse(BaseModel):
    itinerary: str