#!/usr/bin/env python3
"""
Social Agent Runner Script
Demonstrates how to use Google ADK Runner to interact with the agents.
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from host_agent.agent import root_agent

# Load environment variables
load_dotenv()

async def main():
    """Main function to demonstrate agent interactions."""
    
    # Check if News API key is configured
    if not os.getenv('NEWS_API_KEY'):
        print("⚠️  Warning: NEWS_API_KEY not found in environment variables.")
        print("   Social media agent functionality will be limited.")
        print("   Get a free API key from: https://newsapi.org/")
        print()
    
    # Initialize session service and runner
    session_service = InMemorySessionService()
    runner = Runner(session_service)
    
    # Start the agent session
    print("🚀 Starting Social Agent...")
    session = await runner.start_session(root_agent)
    print("✅ Agent ready!")
    print()
    
    # Example interactions
    examples = [
        "What's the weather in New York?",
        "How's the weather in London?",
        "Create social media posts about AI news",
        "Make posts about climate change news"
    ]
    
    print("📝 Running example interactions:")
    print("=" * 50)
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Query: {example}")
        print("-" * 30)
        
        try:
            response = await runner.run(session, example)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
        
        print()
    
    print("✅ Example interactions completed!")
    print("\n💡 To run interactive mode, use: python interactive.py")

if __name__ == "__main__":
    asyncio.run(main()) 