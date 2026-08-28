import pytest
from unittest.mock import patch, MagicMock
from main import app # Assuming your FastAPI instance is in main.py
from fastapi.testclient import TestClient

client = TestClient(app)

def test_trip_generation_endpoint_success():
    """
    Unit test that mocks the Gemini API to avoid live network calls, rate limits, 
    and long execution times.
    """
    payload = {
        "destination": "Mysore",
        "duration_days": 2,
        "interests": ["palaces", "silk markets", "local food"]
    }

    # 1. Arrange: Intercept the exact method in the google.generativeai library
    with patch("google.generativeai.GenerativeModel.generate_content") as mock_generate:
        
        # Create mock chunks to simulate the AI's streaming response
        chunk1 = MagicMock()
        chunk1.text = "## Day 1\n"
        
        chunk2 = MagicMock()
        chunk2.text = "Visit the Mysore Palace."
        
        # When the router calls generate_content, return our fake list of chunks
        mock_generate.return_value = [chunk1, chunk2]

        # 2. Act: Send the POST request to the local FastAPI app
        response = client.post("/api/v1/plan-trip", json=payload)

    # 3. Assert: Validate the API Contract and successful generation
    assert response.status_code == 200
    assert "Mysore Palace" in response.text