#!/usr/bin/env python3
"""
Test script to verify backend connection and API endpoints
"""

import requests
import json
import time
import sys

def test_backend_connection():
    """Test if backend is running and responding"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Backend Connection...")
    print("=" * 40)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check: FAILED (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check: FAILED (Error: {e})")
        return False
    
    # Test 2: Root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint: PASSED")
            data = response.json()
            print(f"   App: {data.get('message', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
        else:
            print(f"❌ Root endpoint: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint: FAILED (Error: {e})")
    
    # Test 3: Disease detection endpoint
    try:
        test_data = {
            "image_base64": "test_image_data",
            "crop_type": "rice"
        }
        response = requests.post(f"{base_url}/api/disease-detection", json=test_data, timeout=10)
        if response.status_code == 200:
            print("✅ Disease detection: PASSED")
            data = response.json()
            print(f"   Detected disease: {data.get('disease', 'Unknown')}")
            print(f"   Confidence: {data.get('confidence', 0)}%")
        else:
            print(f"❌ Disease detection: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Disease detection: FAILED (Error: {e})")
    
    # Test 4: Crop recommendations endpoint
    try:
        test_data = {
            "ph": 6.5,
            "nitrogen": 50,
            "phosphorus": 30,
            "potassium": 40,
            "rainfall": 2500,
            "temperature": 28,
            "soil_type": "laterite",
            "season": "monsoon"
        }
        response = requests.post(f"{base_url}/api/crop-recommendations", json=test_data, timeout=10)
        if response.status_code == 200:
            print("✅ Crop recommendations: PASSED")
            data = response.json()
            print(f"   Recommendations: {len(data.get('recommendations', []))} crops")
        else:
            print(f"❌ Crop recommendations: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Crop recommendations: FAILED (Error: {e})")
    
    # Test 5: Weather endpoint
    try:
        test_data = {
            "city": "Kochi",
            "state": "Kerala"
        }
        response = requests.post(f"{base_url}/api/weather/current", json=test_data, timeout=10)
        if response.status_code == 200:
            print("✅ Weather API: PASSED")
            data = response.json()
            print(f"   Temperature: {data.get('temperature', 'Unknown')}°C")
        else:
            print(f"❌ Weather API: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Weather API: FAILED (Error: {e})")
    
    # Test 6: Chatbot endpoint
    try:
        test_data = {
            "message": "Hello, how can you help with farming?",
            "language": "en"
        }
        response = requests.post(f"{base_url}/api/chatbot", json=test_data, timeout=10)
        if response.status_code == 200:
            print("✅ Chatbot API: PASSED")
            data = response.json()
            print(f"   Response: {data.get('response', 'Unknown')[:50]}...")
        else:
            print(f"❌ Chatbot API: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Chatbot API: FAILED (Error: {e})")
    
    print("\n" + "=" * 40)
    print("🎉 Backend testing completed!")
    return True

def test_frontend_connection():
    """Test if frontend is accessible"""
    print("\n🌐 Testing Frontend Connection...")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: PASSED")
            print("   Frontend is accessible at http://localhost:3000")
        else:
            print(f"❌ Frontend: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend: FAILED (Error: {e})")
        print("   Make sure to run 'npm run dev' in the frontend directory")

if __name__ == "__main__":
    print("🚀 Kerala Farming Assistant - Connection Test")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_backend_connection()
    
    # Test frontend
    test_frontend_connection()
    
    print("\n" + "=" * 50)
    if backend_ok:
        print("✅ Backend is running correctly!")
        print("📍 API Documentation: http://localhost:8000/api/docs")
    else:
        print("❌ Backend has issues. Please check the logs.")
        print("💡 Try running: cd Backend && python run_server.py")
    
    print("\n📱 Frontend should be accessible at: http://localhost:3000")
    print("🔧 If frontend is not running, try: npm run dev")
