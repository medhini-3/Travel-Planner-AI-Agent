import os
from serpapi import GoogleSearch

def search_live_flights(departure_id: str, arrival_id: str, date: str) -> str:
    """
    Searches Google Flights for live ticket prices. Use this tool specifically 
    when the user asks for flight costs, airlines, or travel times.
    
    Args:
        departure_id: The 3-letter IATA airport code you are leaving from (e.g., 'BLR', 'JFK', 'DEL').
        arrival_id: The 3-letter IATA airport code you are going to.
        date: The date of the flight in YYYY-MM-DD format.
    """
    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": date,
        "currency": "USD",
        "hl": "en",
        "api_key": os.getenv("SERPAPI_KEY")
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        best_flights = results.get("best_flights", [])
        if not best_flights:
            return "No flight data found for these dates/locations."
            
        flight_info = []
        # Grab the top 3 best flights
        for flight in best_flights[:3]:
            price = flight.get("price", "Unknown price")
            # Extract the airline name from the first leg of the flight
            airline = flight.get("flights", [{}])[0].get("airline", "Unknown airline")
            duration = flight.get("total_duration", 0)
            
            flight_info.append(f"{airline}: {price} (Duration: {duration} minutes)")
            
        return "Live flight options: " + " | ".join(flight_info)
    except Exception as e:
        return f"Error fetching flights: {str(e)}"