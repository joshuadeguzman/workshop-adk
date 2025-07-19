# @title Define the get_news Tool
from typing import Dict, Any
import json
import requests
import os
from datetime import datetime

def get_news(topic: str, max_articles: int = 5) -> Dict[str, Any]:
    """Retrieves news articles for a specified topic using News API.
    
    This tool fetches news information for a given topic and returns
    a structured response that can be processed by the ADK framework.
    
    Args:
        topic (str): The topic to search for news (e.g., "technology", "climate change", "AI").
        max_articles (int): Maximum number of articles to return (default: 5).
    
    Returns:
        Dict[str, Any]: A dictionary containing the news information with the following structure:
            - status (str): Either 'success' or 'error'
            - articles (list, optional): List of news articles when status is 'success'
            - error_message (str, optional): Error description when status is 'error'
            - topic (str): The original topic requested
            - total_results (int, optional): Total number of articles found
    
    Example:
        >>> get_news("artificial intelligence")
        {
            'status': 'success',
            'topic': 'artificial intelligence',
            'total_results': 3,
            'articles': [
                {
                    'title': 'AI Breakthrough in Healthcare',
                    'description': 'New AI system improves diagnosis accuracy...',
                    'url': 'https://example.com/article1',
                    'published_at': '2024-01-15T10:30:00Z'
                }
            ]
        }
    """
    print(f"--- Tool: get_news called for topic: {topic} ---")  # Log tool execution
    
    # Input validation
    if not topic or not isinstance(topic, str):
        return {
            "status": "error",
            "error_message": "Invalid topic provided. Please provide a valid topic.",
            "topic": topic
        }
    
    if max_articles < 1 or max_articles > 10:
        max_articles = 5  # Default to 5 if invalid
    
    # Get API key from environment
    api_key = os.getenv('NEWS_API_KEY')
    
    if not api_key:
        return {
            "status": "error",
            "error_message": "News API key not found. Please set NEWS_API_KEY in your .env file.",
            "topic": topic
        }
    
    # News API configuration
    base_url = "https://newsapi.org/v2/everything"
    params = {
        'q': topic,
        'apiKey': api_key,
        'pageSize': min(max_articles, 10),  # News API max is 100, but we limit to 10
        'language': 'en',
        'sortBy': 'publishedAt',
        'searchIn': 'title,description'
    }
    
    try:
        # Make API request
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if request was successful
        if data.get('status') != 'ok':
            return {
                "status": "error",
                "error_message": f"News API error: {data.get('message', 'Unknown error')}",
                "topic": topic
            }
        
        articles = data.get('articles', [])
        total_results = data.get('totalResults', 0)
        
        # Process and format articles
        formatted_articles = []
        for article in articles[:max_articles]:
            formatted_article = {
                "title": article.get('title', 'No title available'),
                "description": article.get('description', 'No description available'),
                "url": article.get('url', ''),
                "published_at": article.get('publishedAt', ''),
                "source": article.get('source', {}).get('name', 'Unknown source'),
                "author": article.get('author', 'Unknown author'),
                "content": article.get('content', '')[:200] + '...' if article.get('content') else ''
            }
            formatted_articles.append(formatted_article)
        
        return {
            "status": "success",
            "topic": topic,
            "total_results": len(formatted_articles),
            "total_available": total_results,
            "articles": formatted_articles
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Network error: {str(e)}",
            "topic": topic
        }
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "error_message": f"Invalid response format: {str(e)}",
            "topic": topic
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error: {str(e)}",
            "topic": topic
        }

# Example tool usage for testing
if __name__ == "__main__":
    print("Testing get_news tool:")
    print(json.dumps(get_news("technology"), indent=2))
    print(json.dumps(get_news("climate change"), indent=2))
    print(json.dumps(get_news("artificial intelligence"), indent=2))
    print(json.dumps(get_news("invalid topic"), indent=2)) 