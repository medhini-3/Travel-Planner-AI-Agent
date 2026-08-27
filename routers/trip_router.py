from fastapi import APIRouter, HTTPException
from schemas.trip_schemas import TripRequest, TripResponse
from services.agent_service import generate_trip_plan

router = APIRouter(prefix="/api/v1", tags=["Travel"])

@router.post("/plan-trip", response_model=TripResponse)
async def plan_trip(request: TripRequest):
    try:
        itinerary = generate_trip_plan(
            destination=request.destination,
            duration_days=request.duration_days,
            interests=request.interests
        )
        return TripResponse(itinerary=itinerary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))