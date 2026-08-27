import pytest
from fastapi.testclient import TestClient
from main import app

# Initialize the test client to talk to the local FastAPI application
client = TestClient(app)

@pytest.mark.integration
def test_live_trip_generation_contract():
    """
    Integration test that hits the live Gemini and SerpAPI endpoints.
    Validates the API contract and performs dynamic assertions on the non-deterministic AI output.
    """
    
    # 1. Arrange: Setup a real payload for a weekend getaway
    payload = {
        "destination": "Mysore",
        "duration_days": 2,
        "interests": ["palaces", "silk markets", "local food"]
    }

    # 2. Act: Send the POST request (This will take 5-10 seconds as it hits the live internet)
    response = client.post("/api/v1/plan-trip", json=payload)
    
    # 3. Assert: Validate the API Contract
    assert response.status_code == 200, f"Integration failure: Expected HTTP 200, got {response.status_code}"
    
    data = response.json()
    assert "itinerary" in data, "Contract violation: Response JSON is missing the 'itinerary' key"
    
    # 4. Assert: Validate the AI output quality dynamically
    itinerary = data["itinerary"]
    
    # We can't check for exact strings, but we can verify it generated a substantial response
    assert len(itinerary) > 150, "Quality failure: The generated itinerary is suspiciously short."
    
    # Do a fuzzy check to ensure the LLM didn't hallucinate a completely different location
    assert "mysore" in itinerary.lower(), "Quality failure: The AI failed to mention the requested destination."