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

    with patch("routers.trip_router.client") as mock_genai_client, \
         patch("routers.trip_router.requests.get") as mock_requests_get:

        # 1. Mock SerpApi responses (Hotels, then Restaurants)
        mock_hotel_response = MagicMock()
        mock_hotel_response.json.return_value = {
            "local_results": [{"title": "Real Taj Exotica", "rating": 4.8, "gps_coordinates": {"latitude": 15.2, "longitude": 73.9}}]
        }
        
        mock_restaurant_response = MagicMock()
        mock_restaurant_response.json.return_value = {
            "local_results": [{"title": "Real Britto's", "rating": 4.5, "gps_coordinates": {"latitude": 15.55, "longitude": 73.75}}]
        }
        
        mock_requests_get.side_effect = [mock_hotel_response, mock_restaurant_response]

        # 2. Mock Gemini response with timings and budget
        mock_parsed_response = MagicMock()
        mock_parsed_response.model_dump.return_value = {
            "destination": "Goa",
            "itinerary": [
                {
                    "day": 1,
                    "theme": "Beach Day",
                    "hotel": {
                        "name": "Real Taj Exotica",
                        "rating": "4.8 ★",
                        "price_tier": "Luxury (₹15,000/night)",
                        "check_in_note": "Check-in 02:00 PM",
                        "latitude": 15.2,
                        "longitude": 73.9,
                        "description": "Luxury beachfront resort"
                    },
                    "activities": [
                        {
                            "time_slot": "09:30 AM - 12:00 PM",
                            "name": "Baga Beach",
                            "estimated_duration": "2.5 hours",
                            "estimated_cost": "Free entry",
                            "insider_tip": "Visit early to avoid peak heat",
                            "latitude": 15.5,
                            "longitude": 73.7,
                            "description": "Popular sandy beach with water sports"
                        }
                    ],
                    "meals": [
                        {
                            "meal_type": "Lunch",
                            "time_slot": "01:00 PM - 02:30 PM",
                            "name": "Real Britto's",
                            "must_try": "Butter Garlic Prawns",
                            "estimated_cost": "₹1,200 for two",
                            "latitude": 15.55,
                            "longitude": 73.75,
                            "description": "Iconic beach shack dining"
                        }
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
    assert data["itinerary"][0]["activities"][0]["time_slot"] == "09:30 AM - 12:00 PM"
    assert data["itinerary"][0]["meals"][0]["must_try"] == "Butter Garlic Prawns"
