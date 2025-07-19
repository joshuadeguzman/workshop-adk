# @title Define the get_weather Tool
from typing import Dict, Any
import json

def get_weather(city: str) -> Dict[str, Any]:
    """Retrieves the current weather report for a specified city.
    
    This tool fetches weather information for a given city and returns
    a structured response that can be processed by the ADK framework.
    
    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").
                   The city name will be normalized for lookup.
    
    Returns:
        Dict[str, Any]: A dictionary containing the weather information with the following structure:
            - status (str): Either 'success' or 'error'
            - report (str, optional): Weather details when status is 'success'
            - error_message (str, optional): Error description when status is 'error'
            - city (str): The original city name requested
            - temperature (str, optional): Temperature information when available
            - conditions (str, optional): Weather conditions when available
    
    Example:
        >>> get_weather("New York")
        {
            'status': 'success',
            'report': 'The weather in New York is sunny with a temperature of 25°C.',
            'city': 'New York',
            'temperature': '25°C',
            'conditions': 'sunny'
        }
    """
    print(f"--- Tool: get_weather called for city: {city} ---")  # Log tool execution
    
    # Input validation
    if not city or not isinstance(city, str):
        return {
            "status": "error",
            "error_message": "Invalid city name provided. Please provide a valid city name.",
            "city": city
        }
    
    city_normalized = city.lower().replace(" ", "")  # Basic normalization

    # Mock weather database with more detailed information
    mock_weather_db = {
        "newyork": {
            "status": "success",
            "report": "The weather in New York is sunny with a temperature of 25°C.",
            "city": "New York",
            "temperature": "25°C",
            "conditions": "sunny"
        },
        "london": {
            "status": "success", 
            "report": "It's cloudy in London with a temperature of 15°C.",
            "city": "London",
            "temperature": "15°C",
            "conditions": "cloudy"
        },
        "tokyo": {
            "status": "success",
            "report": "Tokyo is experiencing light rain and a temperature of 18°C.",
            "city": "Tokyo", 
            "temperature": "18°C",
            "conditions": "light rain"
        },
        "paris": {
            "status": "success",
            "report": "Paris has partly cloudy skies with a temperature of 22°C.",
            "city": "Paris",
            "temperature": "22°C", 
            "conditions": "partly cloudy"
        },
        "sydney": {
            "status": "success",
            "report": "Sydney is clear and sunny with a temperature of 28°C.",
            "city": "Sydney",
            "temperature": "28°C",
            "conditions": "clear and sunny"
        }
    }

    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {
            "status": "error", 
            "error_message": f"Sorry, I don't have weather information for '{city}'. Please try another city.",
            "city": city
        }

# Example tool usage for testing
if __name__ == "__main__":
    print("Testing get_weather tool:")
    print(json.dumps(get_weather("New York"), indent=2))
    print(json.dumps(get_weather("Paris"), indent=2))
    print(json.dumps(get_weather("Invalid City"), indent=2))