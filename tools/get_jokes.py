# @title Define the get_jokes Tool
from typing import Dict, Any, List
import json
import random

def get_jokes(category: str = "general", count: int = 1) -> Dict[str, Any]:
    """Retrieves jokes from a specified category.
    
    This tool fetches jokes from various categories and returns
    a structured response that can be processed by the ADK framework.
    
    Args:
        category (str): The category of jokes (e.g., "programming", "dad", "science", "general").
                       Defaults to "general" if not specified.
        count (int): Number of jokes to return (1-5). Defaults to 1.
    
    Returns:
        Dict[str, Any]: A dictionary containing the jokes with the following structure:
            - status (str): Either 'success' or 'error'
            - jokes (List[Dict], optional): List of joke objects when status is 'success'
            - error_message (str, optional): Error description when status is 'error'
            - category (str): The category requested
            - count (int): Number of jokes returned
    
    Example:
        >>> get_jokes("programming", 2)
        {
            'status': 'success',
            'jokes': [
                {'joke': 'Why do programmers prefer dark mode?', 'punchline': 'Because light attracts bugs!'},
                {'joke': 'How many programmers does it take to change a light bulb?', 'punchline': 'None, that\'s a hardware problem!'}
            ],
            'category': 'programming',
            'count': 2
        }
    """
    print(f"--- Tool: get_jokes called for category: {category}, count: {count} ---")  # Log tool execution
    
    # Input validation
    if not isinstance(category, str):
        return {
            "status": "error",
            "error_message": "Invalid category provided. Please provide a valid category name.",
            "category": category,
            "count": count
        }
    
    if not isinstance(count, int) or count < 1 or count > 5:
        return {
            "status": "error", 
            "error_message": "Invalid count. Please provide a number between 1 and 5.",
            "category": category,
            "count": count
        }
    
    category_normalized = category.lower().replace(" ", "")
    
    # Mock jokes database organized by category
    mock_jokes_db = {
        "programming": [
            {"joke": "Why do programmers prefer dark mode?", "punchline": "Because light attracts bugs!"},
            {"joke": "How many programmers does it take to change a light bulb?", "punchline": "None, that's a hardware problem!"},
            {"joke": "Why do Java developers wear glasses?", "punchline": "Because they can't C#!"},
            {"joke": "A SQL query goes into a bar, walks up to two tables and asks...", "punchline": "Can I join you?"},
            {"joke": "Why did the programmer quit his job?", "punchline": "Because he didn't get arrays!"},
            {"joke": "What's a programmer's favorite hangout place?", "punchline": "Foo Bar!"},
            {"joke": "Why do programmers always mix up Halloween and Christmas?", "punchline": "Because Oct 31 equals Dec 25!"}
        ],
        "dad": [
            {"joke": "I'm reading a book about anti-gravity.", "punchline": "It's impossible to put down!"},
            {"joke": "Did you hear about the mathematician who's afraid of negative numbers?", "punchline": "He'll stop at nothing to avoid them!"},
            {"joke": "Why don't scientists trust atoms?", "punchline": "Because they make up everything!"},
            {"joke": "I told my wife she was drawing her eyebrows too high.", "punchline": "She looked surprised!"},
            {"joke": "What do you call a fake noodle?", "punchline": "An impasta!"},
            {"joke": "Why did the scarecrow win an award?", "punchline": "He was outstanding in his field!"},
            {"joke": "I used to hate facial hair...", "punchline": "But then it grew on me!"}
        ],
        "science": [
            {"joke": "Two atoms are walking down the street. One says, 'I think I lost an electron!'", "punchline": "The other asks, 'Are you sure?' The first replies, 'Yes, I'm positive!'"},
            {"joke": "What did the biologist wear to impress his date?", "punchline": "Designer genes!"},
            {"joke": "Why can't you trust an atom?", "punchline": "Because they make up everything!"},
            {"joke": "What do you call an educated tube?", "punchline": "A graduated cylinder!"},
            {"joke": "Why did the physics teacher break up with the biology teacher?", "punchline": "There was no chemistry!"},
            {"joke": "What's the fastest way to determine the sex of a chromosome?", "punchline": "Pull down its genes!"},
            {"joke": "I have a new theory on inertia...", "punchline": "But it doesn't seem to be gaining momentum!"}
        ],
        "general": [
            {"joke": "Why don't eggs tell jokes?", "punchline": "They'd crack each other up!"},
            {"joke": "What do you call a sleeping bull?", "punchline": "A bulldozer!"},
            {"joke": "Why did the math book look so sad?", "punchline": "Because it was full of problems!"},
            {"joke": "What do you call a bear with no teeth?", "punchline": "A gummy bear!"},
            {"joke": "Why don't skeletons fight each other?", "punchline": "They don't have the guts!"},
            {"joke": "What's orange and sounds like a parrot?", "punchline": "A carrot!"},
            {"joke": "Why did the cookie go to the doctor?", "punchline": "Because it felt crumbly!"}
        ],
        "office": [
            {"joke": "Why did the employee get fired from the calendar factory?", "punchline": "He took a day off!"},
            {"joke": "What do you call a person who's happy on Monday?", "punchline": "Retired!"},
            {"joke": "Why don't meetings ever start on time?", "punchline": "Because punctuality is a deadline issue!"},
            {"joke": "What's the best thing about Switzerland at work?", "punchline": "I don't know, but their flag is a big plus!"},
            {"joke": "Why did the PowerPoint cross the road?", "punchline": "To get to the other slide!"},
            {"joke": "What do you call a printer that can sing?", "punchline": "A Dell!"},
            {"joke": "Why do accountants make good comedians?", "punchline": "They know how to work the numbers!"}
        ]
    }
    
    # Check if category exists
    if category_normalized not in mock_jokes_db:
        available_categories = list(mock_jokes_db.keys())
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have jokes for the category '{category}'. Available categories: {', '.join(available_categories)}",
            "category": category,
            "count": count
        }
    
    # Get jokes from the category
    category_jokes = mock_jokes_db[category_normalized]
    selected_jokes = random.sample(category_jokes, min(count, len(category_jokes)))
    
    return {
        "status": "success",
        "jokes": selected_jokes,
        "category": category,
        "count": len(selected_jokes)
    }

# Example tool usage for testing
if __name__ == "__main__":
    print("Testing get_jokes tool:")
    print(json.dumps(get_jokes("programming", 2), indent=2))
    print(json.dumps(get_jokes("dad", 1), indent=2))
    print(json.dumps(get_jokes("invalid", 1), indent=2))