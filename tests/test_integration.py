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

    # Intercept both the GenAI client AND the requests library
    with patch("routers.trip_router.client") as mock_genai_client, \
         patch("routers.trip_router.requests.get") as mock_requests_get:

        # 1. Mock the SerpApi response
        mock_serpapi_response = MagicMock()
        mock_serpapi_response.json.return_value = {
            "local_results": [
                {"title": "Real Taj Exotica", "rating": 4.8, "gps_coordinates": {"latitude": 15.2, "longitude": 73.9}}
            ]
        }
        mock_requests_get.return_value = mock_serpapi_response

        # 2. Mock the Gemini structured JSON response
        mock_parsed_response = MagicMock()
        mock_parsed_response.model_dump.return_value = {
            "destination": "Goa",
            "itinerary": [
                {
                    "day": 1,
                    "theme": "Beach Day",
                    "hotel": {"name": "Real Taj Exotica", "latitude": 15.2, "longitude": 73.9, "description": "Luxury stay"},
                    "activities": [
                        {"name": "Baga Beach", "latitude": 15.5, "longitude": 73.7, "description": "Sunny"}
                    ]
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.parsed = mock_parsed_response
        mock_genai_client.models.generate_content.return_value = mock_response

        # Send request
        response = client.post("/api/v1/plan-trip", json=payload)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["destination"] == "Goa"
    assert data["itinerary"][0]["hotel"]["name"] == "Real Taj Exotica"
