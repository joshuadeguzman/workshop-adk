#!/usr/bin/env python3
"""
Interactive Social Agent
Allows real-time conversation with the agents using Google ADK Runner.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from host_agent.agent import root_agent

# Load environment variables
load_dotenv()

async def interactive_session():
    """Run an interactive session with the agent."""
    
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
    
    # Display welcome message and instructions
    print("🤖 Welcome to Social Agent!")
    print("=" * 50)
    print("I can help you with:")
    print("• Weather information for cities worldwide")
    print("• Creating social media posts from news content")
    print("• And much more!")
    print()
    print("💡 Try asking:")
    print("  - 'What's the weather in Tokyo?'")
    print("  - 'Create social media posts about AI news'")
    print("  - 'How's the weather in Paris?'")
    print("  - 'Make posts about climate change'")
    print()
    print("Type 'quit', 'exit', or 'bye' to end the session.")
    print("Type 'help' for this message again.")
    print("=" * 50)
    print()
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye! Thanks for using Social Agent!")
                break
            
            # Check for help command
            if user_input.lower() == 'help':
                print("\n💡 Available commands:")
                print("  - Weather queries: 'What's the weather in [city]?'")
                print("  - Social media: 'Create posts about [topic]'")
                print("  - 'help' - Show this help message")
                print("  - 'quit', 'exit', 'bye' - End session")
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Process the request
            print("\n🤖 Agent: ", end="", flush=True)
            
            try:
                response = await runner.run(session, user_input)
                print(response)
            except Exception as e:
                print(f"❌ Error: {e}")
                print("💡 Try rephrasing your question or check your API configuration.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except EOFError:
            print("\n\n👋 End of input. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("💡 Please try again or type 'quit' to exit.")

def main():
    """Main entry point."""
    try:
        asyncio.run(interactive_session())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main() 