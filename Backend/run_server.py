#!/usr/bin/env python3
"""
Simple script to run the FarmersHub API server
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

if __name__ == "__main__":
    print("🌾 Starting FarmersHub API Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🔧 Health Check: http://localhost:8000/health")
    print("\n" + "="*50)
    
    try:
        uvicorn.run(
            "main_api_server_fixed:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
