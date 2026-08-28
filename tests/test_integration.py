import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

# Initialize FastAPI TestClient
client = TestClient(app)

def test_trip_generation_endpoint_success():
    """
    Unit test that mocks the new Google GenAI client to test 
    the streaming endpoint without live network calls.
    """
    payload = {
        "destination": "Mysore",
        "duration_days": 2,
        "interests": ["palaces", "silk markets", "local food"]
    }

    # Intercept the new 'client' object imported inside your router
    with patch("routers.trip_router.client") as mock_genai_client:

        # Create mock chunks to simulate the AI's streaming response
        chunk1 = MagicMock()
        chunk1.text = "## Day 1\n"
        chunk2 = MagicMock()
        chunk2.text = "Visit the Mysore Palace."

        # Mock the chat session and its send_message_stream generator return value
        mock_chat_session = MagicMock()
        
        # FIX: We now mock send_message_stream instead of send_message!
        mock_chat_session.send_message_stream.return_value = [chunk1, chunk2]
        
        mock_genai_client.chats.create.return_value = mock_chat_session

        # Send the POST request to your FastAPI app
        response = client.post("/api/v1/plan-trip", json=payload)

    # Assert the API contract and successful streaming response
    assert response.status_code == 200
    assert "Day 1" in response.text
    assert "Mysore Palace" in response.text
