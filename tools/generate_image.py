# @title Define the generate_image Tool
from typing import Dict, Any
import json
import os
import requests
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_image(prompt: str, size: str = "1024x1024", quality: str = "standard") -> Dict[str, Any]:
    """Generates an image using OpenAI's DALL-E API.
    
    This tool creates images based on text descriptions using OpenAI's DALL-E model
    and returns a structured response that can be processed by the ADK framework.
    
    Args:
        prompt (str): A detailed description of the image to generate.
                     Should be clear and descriptive (e.g., "A sunset over mountains with purple clouds").
        size (str): The size of the image. Options: "1024x1024", "1792x1024", "1024x1792".
                   Defaults to "1024x1024".
        quality (str): The quality of the image. Options: "standard", "hd".
                      Defaults to "standard".
    
    Returns:
        Dict[str, Any]: A dictionary containing the image generation result with the following structure:
            - status (str): Either 'success' or 'error'
            - image_url (str, optional): URL to the generated image when status is 'success'
            - local_path (str, optional): Local file path to downloaded image when status is 'success'
            - prompt (str): The original prompt used
            - size (str): The size of the generated image
            - quality (str): The quality setting used
            - error_message (str, optional): Error description when status is 'error'
    
    Example:
        >>> generate_image("A futuristic city with flying cars", "1024x1024", "standard")
        {
            'status': 'success',
            'image_url': 'https://oaidalleapiprodscus.blob.core.windows.net/...',
            'local_path': '/Users/joshua/Desktop/agents/social_agent/generated_images/futuristic_city_20240119_143022.png',
            'prompt': 'A futuristic city with flying cars',
            'size': '1024x1024',
            'quality': 'standard'
        }
    """
    print(f"--- Tool: generate_image called with prompt: {prompt[:50]}... ---")  # Log tool execution
    
    # Input validation
    if not prompt or not isinstance(prompt, str):
        return {
            "status": "error",
            "error_message": "Invalid prompt provided. Please provide a valid text description.",
            "prompt": prompt,
            "size": size,
            "quality": quality
        }
    
    if prompt.strip() == "":
        return {
            "status": "error",
            "error_message": "Empty prompt provided. Please provide a descriptive text for image generation.",
            "prompt": prompt,
            "size": size,
            "quality": quality
        }
    
    # Validate size parameter
    valid_sizes = ["1024x1024", "1792x1024", "1024x1792"]
    if size not in valid_sizes:
        return {
            "status": "error",
            "error_message": f"Invalid size '{size}'. Valid options: {', '.join(valid_sizes)}",
            "prompt": prompt,
            "size": size,
            "quality": quality
        }
    
    # Validate quality parameter
    valid_qualities = ["standard", "hd"]
    if quality not in valid_qualities:
        return {
            "status": "error",
            "error_message": f"Invalid quality '{quality}'. Valid options: {', '.join(valid_qualities)}",
            "prompt": prompt,
            "size": size,
            "quality": quality
        }
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "OpenAI API key not found. Please set OPENAI_API_KEY environment variable.",
            "prompt": prompt,
            "size": size,
            "quality": quality
        }
    
    try:
        # Try to import OpenAI client
        try:
            from openai import OpenAI
        except ImportError:
            return {
                "status": "error",
                "error_message": "OpenAI library not installed. Please install it with: pip install openai",
                "prompt": prompt,
                "size": size,
                "quality": quality
            }
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Generate image using DALL-E
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1
        )
        
        # Extract image URL from response
        image_url = response.data[0].url
        
        # Download image locally
        try:
            # Create a safe filename based on prompt and timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            # Clean prompt for filename (remove special characters)
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '_')).rstrip()
            safe_prompt = safe_prompt.replace(' ', '_').lower()
            filename = f"{safe_prompt}_{timestamp}.png"
            
            # Ensure the directory exists
            images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_images")
            os.makedirs(images_dir, exist_ok=True)
            
            local_path = os.path.join(images_dir, filename)
            
            # Download the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                f.write(image_response.content)
            
            print(f"Image downloaded to: {local_path}")
            
            return {
                "status": "success",
                "image_url": image_url,
                "local_path": local_path,
                "prompt": prompt,
                "size": size,
                "quality": quality
            }
            
        except Exception as download_error:
            # If download fails, still return the URL
            print(f"Warning: Failed to download image locally: {download_error}")
            return {
                "status": "success",
                "image_url": image_url,
                "local_path": None,
                "download_error": str(download_error),
                "prompt": prompt,
                "size": size,
                "quality": quality
            }
        
    except Exception as e:
        # Handle any errors during image generation
        error_message = str(e)
        
        # Provide more user-friendly error messages for common issues
        if "API key" in error_message.lower():
            error_message = "Invalid OpenAI API key. Please check your OPENAI_API_KEY environment variable."
        elif "content policy" in error_message.lower():
            error_message = "The prompt violates OpenAI's content policy. Please try a different description."
        elif "rate limit" in error_message.lower():
            error_message = "Rate limit exceeded. Please try again in a moment."
        elif "insufficient" in error_message.lower() and "quota" in error_message.lower():
            error_message = "OpenAI account quota exceeded. Please check your OpenAI account billing."
        
        return {
            "status": "error",
            "error_message": f"Image generation failed: {error_message}",
            "prompt": prompt,
            "size": size,
            "quality": quality
        }

# Example tool usage for testing
if __name__ == "__main__":
    print("Testing generate_image tool:")
    print(json.dumps(generate_image("A peaceful lake with mountains in the background"), indent=2))
    print(json.dumps(generate_image(""), indent=2))  # Test empty prompt
    print(json.dumps(generate_image("A cat", "invalid_size"), indent=2))  # Test invalid size