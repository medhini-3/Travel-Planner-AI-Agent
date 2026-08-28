from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_trip_generation_endpoint_success():
    payload = {
        "destination": "Goa",
        "duration_days": 1,
        "interests": ["beaches"]
    }

    # Intercept the new 'client' object
    with patch("routers.trip_router.client") as mock_genai_client:

        # Create a fake Pydantic dictionary that matches our new schema
        mock_parsed_response = MagicMock()
        mock_parsed_response.model_dump.return_value = {
            "destination": "Goa",
            "itinerary": [
                {
                    "day": 1,
                    "theme": "Beach Day",
                    "hotel": {"name": "Taj Exotica", "latitude": 15.2, "longitude": 73.9, "description": "Luxury"},
                    "activities": [
                        {"name": "Baga Beach", "latitude": 15.5, "longitude": 73.7, "description": "Sunny"}
                    ]
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.parsed = mock_parsed_response
        
        # We mock generate_content (since we use structured output now)
        mock_genai_client.models.generate_content.return_value = mock_response

        response = client.post("/api/v1/plan-trip", json=payload)

    # Assert JSON response
    assert response.status_code == 200
    data = response.json()
    assert data["destination"] == "Goa"
    assert data["itinerary"][0]["activities"][0]["name"] == "Baga Beach"
    assert data["itinerary"][0]["hotel"]["name"] == "Taj Exotica"
