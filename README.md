# Social Agent - Multi-Purpose AI Assistant

A sophisticated AI agent system built with Google's Agent Development Kit (ADK) that provides weather information and social media content creation capabilities. This project demonstrates how to create specialized agents that can work together to handle different types of user requests.

## 🚀 Features

### 🌤️ Weather Agent

- Provides current weather information for cities worldwide
- Supports major cities including New York, London, Tokyo, Paris, and Sydney
- Delivers weather reports in a conversational, user-friendly format

### 📱 Social Media Agent

- Creates engaging social media posts from news content
- Generates platform-specific content for:
  - **Twitter/X**: Concise posts with hashtags (280 character limit)
  - **Threads**: Conversational, longer-form content (500 character limit)
  - **Instagram**: Visual-focused content with engaging captions
- Includes image recommendations and hashtag suggestions
- Fetches real-time news using News API

### 😄 Jokes Agent

- Provides entertainment with jokes from various categories
- Supports multiple categories: programming, dad jokes, science, general, office humor
- Delivers jokes in an engaging and entertaining format
- Allows users to request specific number of jokes (1-5)

### 🎨 Image Generation Agent

- Creates high-quality images using OpenAI's DALL-E 3 API
- Supports multiple image sizes: 1024x1024, 1792x1024, 1024x1792
- Offers standard and HD quality options
- Downloads images locally for easy viewing (since ADK web doesn't have image preview yet)
- Helps users refine prompts for better image generation results

### 🎯 Host Agent

- Coordinates between specialized agents
- Routes user requests to appropriate sub-agents
- Maintains context across different types of requests
- Provides a unified interface for all capabilities

## 📁 Project Structure

```
social_agent/
├── agents/
│   ├── social_media_agent/
│   │   ├── __init__.py
│   │   └── agent.py          # Social media content creation agent
│   ├── weather_agent/
│   │   ├── __init__.py
│   │   └── agent.py          # Weather information agent
│   ├── jokes_agent/
│   │   ├── __init__.py
│   │   └── agent.py          # Jokes and entertainment agent
│   └── image_agent/
│       ├── __init__.py
│       └── agent.py          # AI image generation agent
├── host_agent/
│   ├── __init__.py
│   └── agent.py              # Main coordinator agent
├── tools/
│   ├── get_latest_news.py    # News API integration tool
│   ├── get_weather.py        # Weather data tool
│   ├── get_jokes.py          # Jokes retrieval tool
│   └── generate_image.py     # OpenAI DALL-E image generation tool
├── generated_images/         # Directory for locally downloaded images
├── .env                     # Environment variables (create from .env.example)
├── .env.example            # Template for environment variables
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Prerequisites

- Python 3.8 or higher
- Google Cloud account with access to Google ADK
- News API key (for social media content creation)
- OpenAI API key (for image generation)

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd social_agent
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env  # Create .env file from template
   ```

## 🔑 API Key Setup

### Google ADK Setup

1. **Install Google ADK**

   ```bash
   pip install google-adk
   ```

2. **Authenticate with Google Cloud**

   ```bash
   gcloud auth application-default login
   ```

3. **Set up Google Cloud project**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

### News API Setup

1. **Get a News API key**

   - Visit [NewsAPI.org](https://newsapi.org/)
   - Sign up for a free account
   - Copy your API key from the dashboard

2. **Add API key to environment**
   ```bash
   # Add to your .env file
   NEWS_API_KEY=your_news_api_key_here
   ```

### OpenAI API Setup (for Image Generation)

1. **Get an OpenAI API key**

   - Visit [OpenAI Platform](https://platform.openai.com)
   - Sign up for an account or log in
   - Go to [API Keys](https://platform.openai.com/api-keys)
   - Click "Create new secret key"
   - Give it a name and copy the key (starts with `sk-`)

2. **Add API key to environment**
   ```bash
   # Add to your .env file
   OPENAI_API_KEY=sk-your_openai_api_key_here
   ```

3. **Set up billing (Required for DALL-E)**
   - Add payment method in your [OpenAI account](https://platform.openai.com/account/billing)
   - DALL-E 3 pricing: ~$0.04 per standard image, ~$0.08 per HD image
   - Set usage limits to control costs

4. **Install OpenAI library**
   ```bash
   pip install openai>=1.3.0
   ```

## 🚀 Running the Project

### Method 1: Using ADK Web Interface

The easiest way to run your agent is using the ADK web interface:

1. **Navigate to your project directory**

   ```bash
   cd social_agent
   ```

2. **Start the ADK web interface**

   ```bash
   adk web
   ```

3. **Open your browser**

   - The web interface will typically be available at `http://localhost:8080`
   - Follow the on-screen instructions to load your agent

4. **Start chatting**
   - Use the web interface to interact with your social agent
   - Ask about weather or request social media content creation

### Method 2: Using Google ADK Runner

1. **Create a runner script**

   ```python
   # run_agent.py
   import asyncio
   from google.adk.sessions import InMemorySessionService
   from google.adk.runners import Runner
   from host_agent.agent import root_agent

   async def main():
       session_service = InMemorySessionService()
       runner = Runner(session_service)

       # Start the agent
       session = await runner.start_session(root_agent)

       # Example interactions
       response = await runner.run(session, "What's the weather in New York?")
       print(response)

       response = await runner.run(session, "Create social media posts about AI news")
       print(response)

   if __name__ == "__main__":
       asyncio.run(main())
   ```

2. **Run the script**
   ```bash
   python run_agent.py
   ```

### Method 3: Interactive Mode

1. **Create an interactive script**

   ```python
   # interactive.py
   import asyncio
   from google.adk.sessions import InMemorySessionService
   from google.adk.runners import Runner
   from host_agent.agent import root_agent

   async def interactive_session():
       session_service = InMemorySessionService()
       runner = Runner(session_service)
       session = await runner.start_session(root_agent)

       print("🤖 Social Agent is ready! Type 'quit' to exit.")
       print("Try asking about weather or requesting social media content!")

       while True:
           user_input = input("\nYou: ")
           if user_input.lower() == 'quit':
               break

           try:
               response = await runner.run(session, user_input)
               print(f"\nAgent: {response}")
           except Exception as e:
               print(f"\nError: {e}")

   if __name__ == "__main__":
       asyncio.run(interactive_session())
   ```

2. **Run interactive mode**
   ```bash
   python interactive.py
   ```

## 💬 Example Usage

### Weather Queries

```
You: What's the weather in London?
Agent: It's cloudy in London with a temperature of 15°C.

You: How's the weather in Tokyo?
Agent: Tokyo is experiencing light rain and a temperature of 18°C.
```

### Social Media Content Requests

```
You: Create social media posts about AI news
Agent: [Generates platform-specific posts with headlines, content, hashtags, and image suggestions]

You: Make posts about climate change news
Agent: [Creates engaging social media content for different platforms]
```

### Jokes Requests

```
You: Tell me a programming joke
Agent: Why do programmers prefer dark mode? Because light attracts bugs!

You: Give me 3 dad jokes
Agent: [Delivers multiple dad jokes with setup and punchline]
```

### Image Generation Requests

```
You: Generate an image of a sunset over mountains
Agent: 🖼️ **Image Generated Successfully!**

📁 **Local Path**: /Users/joshua/Desktop/agents/social_agent/generated_images/sunset_mountains_20250719_143022.png ← You can open this file to view the image

🌐 **Image URL**: https://oaidalleapi...

**Description**: I've created a beautiful sunset scene over mountains...

You: Create a futuristic city in HD quality
Agent: [Generates high-quality image with detailed specifications]
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required for social media functionality
NEWS_API_KEY=your_news_api_key_here

# Required for image generation functionality
OPENAI_API_KEY=sk-your_openai_api_key_here

# Google Cloud configuration (if needed)
GOOGLE_CLOUD_PROJECT=your_project_id
```

**⚠️ Security Important**: 
- Never commit your `.env` file to version control
- Keep your API keys private and secure
- Use the provided `.env.example` as a template

### Model Configuration

The agents use Gemini 2.0 Flash by default. You can modify the model in each agent file:

```python
# In agent.py files
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
ROOT_AGENT_MODEL = MODEL_GEMINI_2_0_FLASH
```

### Optional

You can also use the Gemini 2.5 Flash Live model to interact with the Web ADK using bidirectional streaming:

1. Update the modal

```python
MODEL_GEMINI_2_5_FLASH_LIVE ="gemini-live-2.5-flash-preview"

# Replace the Root agent
ROOT_AGENT_MODEL = MODEL_GEMINI_2_5_FLASH_LIVE

# Replace the agent model for each subagent
AGENT_MODEL = MODEL_GEMINI_2_5_FLASH_LIVE
```

2. Update the SSL certificate

```bash
export SSL_CERT_FILE=$(python -m certifi)
```

3. Run the host agent in the ADK web

```
adk web
```

## 🛠️ Customization

### Adding New Agents

1. Create a new directory in `agents/`
2. Define your agent in `agent.py`
3. Add tools in the `tools/` directory
4. Import and add to the host agent's sub-agents list

### Adding New Tools

1. Create a new tool function in the `tools/` directory
2. Follow the existing pattern with proper error handling
3. Add the tool to the appropriate agent's tools list

## 🐛 Troubleshooting

### Common Issues

1. **Google ADK Authentication Error**

   ```bash
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```

```

2. **News API Key Not Found**

   - Ensure `NEWS_API_KEY` is set in your `.env` file
   - Verify the API key is valid at [NewsAPI.org](https://newsapi.org/)

3. **Import Errors**

   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're in the correct virtual environment

4. **Model Not Available**
   - Verify your Google Cloud project has access to Gemini models
   - Check your API quotas and billing status

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🔗 Connect

Let's connect and stay updated:

- **Threads & Twitter**: [@joshuamdeguzman](https://twitter.com/joshuamdeguzman)
- **LinkedIn**: [joshuadeguzman](https://linkedin.com/in/joshuadeguzman)

---

**Note**: This project requires Google ADK access and a News API key to function properly. Make sure to set up both before running the agents.
```
