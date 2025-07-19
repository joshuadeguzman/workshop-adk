#!/usr/bin/env python3
"""
Social Agent Setup Script
Helps users set up the project dependencies and configuration.
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print setup header."""
    print("🚀 Social Agent Setup")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible.")
    return True

def install_dependencies():
    """Install project dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    print("\n🔧 Setting up environment configuration...")
    
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists.")
        return True
    
    # Create .env file with template
    env_content = """# Social Agent Environment Configuration

# News API Configuration
# Get your API key from: https://newsapi.org/
NEWS_API_KEY=your_news_api_key_here

# Google Cloud Configuration (optional)
# Set your Google Cloud project ID if needed
GOOGLE_CLOUD_PROJECT=your_project_id_here

# Additional Configuration (optional)
# Set to true for debug logging
DEBUG=false

# Model Configuration (optional)
# Default is gemini-2.0-flash, you can change this if needed
AGENT_MODEL=gemini-2.0-flash
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with template configuration.")
        print("   Please edit .env and add your API keys.")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_google_adk():
    """Check if Google ADK is properly configured."""
    print("\n🔍 Checking Google ADK configuration...")
    
    try:
        import google.adk
        print("✅ Google ADK is installed.")
        
        # Check if user is authenticated
        try:
            import google.auth
            credentials, project = google.auth.default()
            print("✅ Google Cloud authentication is configured.")
            return True
        except Exception:
            print("⚠️  Google Cloud authentication not configured.")
            print("   Run: gcloud auth application-default login")
            return False
            
    except ImportError:
        print("❌ Google ADK not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "google-adk"])
            print("✅ Google ADK installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Google ADK.")
            return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n🎉 Setup completed!")
    print("=" * 50)
    print("Next steps:")
    print()
    print("1. 🔑 Configure API Keys:")
    print("   - Edit .env file")
    print("   - Add your News API key from https://newsapi.org/")
    print()
    print("2. ☁️  Set up Google Cloud (if not done):")
    print("   - Run: gcloud auth application-default login")
    print("   - Run: gcloud config set project YOUR_PROJECT_ID")
    print()
    print("3. 🚀 Run the agent:")
    print("   - For examples: python run_agent.py")
    print("   - For interactive mode: python interactive.py")
    print()
    print("4. 📚 Read the README.md for more information")
    print()
    print("Happy coding! 🎊")

def main():
    """Main setup function."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Check Google ADK
    check_google_adk()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 