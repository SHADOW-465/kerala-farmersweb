#!/usr/bin/env python3
"""
FarmersHub API Runner Script
Provides easy commands to run the application in different modes
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_development():
    """Run the application in development mode"""
    print("🚀 Starting FarmersHub API in development mode...")
    os.system("uvicorn main_api_server:app --host 0.0.0.0 --port 8000 --reload --log-level debug")

def run_production():
    """Run the application in production mode"""
    print("🚀 Starting FarmersHub API in production mode...")
    os.system("gunicorn main_api_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000")

def run_docker():
    """Run the application using Docker"""
    print("🐳 Starting FarmersHub API with Docker...")
    os.system("docker-compose up --build")

def run_tests():
    """Run tests"""
    print("🧪 Running tests...")
    os.system("pytest -v --cov=. --cov-report=html")

def install_dependencies():
    """Install dependencies"""
    print("📦 Installing dependencies...")
    os.system("pip install -r requirements.txt")

def setup_environment():
    """Set up environment"""
    print("⚙️ Setting up environment...")
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        if Path("env_example.txt").exists():
            os.system("cp env_example.txt .env")
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your API keys")
        else:
            print("❌ env_example.txt not found")
    
    # Create necessary directories
    directories = ["uploads", "static", "logs", "data"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory} directory")
    
    print("✅ Environment setup complete")

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    print("✅ requirements.txt found")
    
    # Check if main_api_server.py exists
    if not Path("main_api_server.py").exists():
        print("❌ main_api_server.py not found")
        return False
    
    print("✅ main_api_server.py found")
    
    print("✅ All requirements met")
    return True

def show_help():
    """Show help information"""
    print("""
🌾 FarmersHub API Runner

Usage: python run.py [command]

Commands:
  dev, development    Run in development mode (with auto-reload)
  prod, production    Run in production mode (with Gunicorn)
  docker             Run with Docker Compose
  test               Run tests
  install            Install dependencies
  setup              Set up environment
  check              Check requirements
  help               Show this help message

Examples:
  python run.py dev          # Start development server
  python run.py prod         # Start production server
  python run.py docker       # Start with Docker
  python run.py test         # Run tests
  python run.py setup        # Set up environment

Environment Variables:
  HUGGINGFACE_API_KEY        Required for AI features
  OPENWEATHER_API_KEY        Required for weather features
  DATABASE_URL              Database connection string
  LOG_LEVEL                 Logging level (DEBUG, INFO, WARNING, ERROR)

For more information, see README.md
""")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="FarmersHub API Runner")
    parser.add_argument("command", nargs="?", default="help", 
                       choices=["dev", "development", "prod", "production", 
                               "docker", "test", "install", "setup", "check", "help"],
                       help="Command to run")
    
    args = parser.parse_args()
    
    if args.command in ["dev", "development"]:
        if check_requirements():
            run_development()
    elif args.command in ["prod", "production"]:
        if check_requirements():
            run_production()
    elif args.command == "docker":
        run_docker()
    elif args.command == "test":
        run_tests()
    elif args.command == "install":
        install_dependencies()
    elif args.command == "setup":
        setup_environment()
    elif args.command == "check":
        check_requirements()
    elif args.command == "help":
        show_help()
    else:
        show_help()

if __name__ == "__main__":
    main()
