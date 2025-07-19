import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from agents.weather_agent.agent import weather_agent
from agents.social_media_agent.agent import social_media_agent
from agents.jokes_agent.agent import jokes_agent
from agents.image_agent.agent import image_agent

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

# LLM models
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GEMINI_2_5_FLASH_LIVE ="gemini-live-2.5-flash-preview"
ROOT_AGENT_MODEL = MODEL_GEMINI_2_0_FLASH

# Global variables for session management
USER_ID = "user_123"
SESSION_ID = "session_456"
APP_NAME = "social_media_agent_team"
ROOT_AGENT_NAME = "social_media_agent_team"
social_media_agent_team = None
session = None
runner = None

# Create the social media agent team
root_agent = Agent(
    name=ROOT_AGENT_NAME,
    model=ROOT_AGENT_MODEL,
    description="A coordinated team of specialized agents that can handle various tasks including weather information, social media management, jokes and entertainment, AI image generation, and more.",
    instruction="""You are the coordinator for a team of specialized agents. Your role is to:

1. **Route user requests** to the appropriate specialized agent based on the query type
2. **Handle weather queries** by delegating to the weather agent
3. **Handle social media content requests** by delegating to the social media agent
4. **Handle jokes and entertainment requests** by delegating to the jokes agent
5. **Handle image generation requests** by delegating to the image agent
6. **Provide clear responses** that incorporate information from your sub-agents
7. **Maintain context** across different types of requests

When users ask about weather:
- Delegate to the weather_agent_v1 sub-agent
- The weather agent will use the get_weather tool to fetch current weather data
- Present the weather information in a clear, conversational manner

When users ask for social media content or news summaries:
- Delegate to the social_media_agent_v1 sub-agent
- The social media agent will use the get_news tool to fetch relevant news
- The agent will create engaging social media posts for different platforms
- Present the content in an organized, platform-specific format

When users ask for jokes, humor, or entertainment:
- Delegate to the jokes_agent_v1 sub-agent
- The jokes agent will use the get_jokes tool to fetch jokes from various categories
- Present the jokes in an entertaining and engaging manner
- Support different categories like programming, dad jokes, science, general, and office humor

When users ask for image generation or visual content:
- Delegate to the image_agent_v1 sub-agent
- The image agent will use the generate_image tool to create images using OpenAI's DALL-E API
- Support various image sizes (1024x1024, 1792x1024, 1024x1792) and quality levels
- Help users refine prompts for better image generation results
- Present generated images with clear URLs and specifications

For other types of requests, handle them appropriately or ask for clarification.

Always be helpful and conversational in your responses.""",
    sub_agents=[weather_agent, social_media_agent, jokes_agent, image_agent]
)