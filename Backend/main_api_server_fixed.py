"""
Main API Server for FarmersHub - Fixed Version
FastAPI-based REST API server that integrates all farming features
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import uvicorn
import logging
from datetime import datetime
import os
import json
import base64
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FarmersHub API",
    description="AI-powered farming assistant API for Kerala farmers",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class DiseaseDetectionRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image")
    crop_type: Optional[str] = Field(None, description="Type of crop")

class DiseaseDetectionResponse(BaseModel):
    disease: str
    confidence: float
    treatment: str
    prevention: str
    severity: str
    success: bool

class CropRecommendationRequest(BaseModel):
    ph: float = Field(..., ge=3.0, le=9.0, description="Soil pH level")
    nitrogen: float = Field(..., ge=0, le=300, description="Nitrogen content (kg/ha)")
    phosphorus: float = Field(..., ge=0, le=200, description="Phosphorus content (kg/ha)")
    potassium: float = Field(..., ge=0, le=200, description="Potassium content (kg/ha)")
    rainfall: float = Field(..., ge=500, le=4000, description="Annual rainfall (mm)")
    temperature: float = Field(..., ge=10, le=40, description="Temperature (°C)")
    soil_type: str = Field(..., description="Type of soil")
    season: str = Field(..., description="Planting season")

class WeatherRequest(BaseModel):
    city: str = Field(..., description="City name")
    state: str = Field("Kerala", description="State name")

class ChatbotRequest(BaseModel):
    message: str = Field(..., description="User message")
    language: Optional[str] = Field("en", description="Language code")
    user_id: Optional[str] = Field(None, description="User ID for context")

class FarmProfileRequest(BaseModel):
    farmer_name: str
    farm_name: str
    location: Dict[str, str]
    total_area: float
    soil_type: str
    soil_ph: float
    soil_nutrients: Dict[str, float]
    irrigation_type: str
    farming_type: str
    established_year: int
    contact_info: Dict[str, str]

# Mock data for testing
MOCK_DISEASES = [
    {
        "disease": "Leaf Blight",
        "confidence": 92.5,
        "treatment": "Apply copper-based fungicide. Remove affected leaves immediately. Improve air circulation around plants.",
        "prevention": "Use resistant varieties. Practice crop rotation. Avoid overhead watering during humid conditions.",
        "severity": "High"
    },
    {
        "disease": "Healthy Plant",
        "confidence": 95.0,
        "treatment": "Your plant looks healthy! Continue current care practices.",
        "prevention": "Maintain proper watering, fertilization, and pest monitoring to keep plants healthy.",
        "severity": "None"
    },
    {
        "disease": "Brown Spot",
        "confidence": 87.3,
        "treatment": "Apply propiconazole-based fungicide. Ensure proper field drainage. Remove infected plant debris.",
        "prevention": "Use resistant varieties. Maintain proper plant spacing. Apply balanced fertilization.",
        "severity": "Medium"
    }
]

MOCK_CROPS = {
    "Rice": {
        "suitability_score": 85.2,
        "suitability_level": "Excellent",
        "profit_potential": 25.5,
        "estimated_yield": 3000,
        "growth_period_days": 120,
        "market_demand": "High",
        "profit_margin": 0.25,
        "ph_optimal": 5.8,
        "rainfall_optimal": 1500,
        "temp_optimal": 26,
        "recommended_season": "Kharif"
    },
    "Coconut": {
        "suitability_score": 92.1,
        "suitability_level": "Excellent",
        "profit_potential": 35.0,
        "estimated_yield": 80,
        "growth_period_days": 365,
        "market_demand": "Very High",
        "profit_margin": 0.35,
        "ph_optimal": 6.5,
        "rainfall_optimal": 1800,
        "temp_optimal": 28,
        "recommended_season": "Year-round"
    },
    "Black Pepper": {
        "suitability_score": 88.7,
        "suitability_level": "Excellent",
        "profit_potential": 40.0,
        "estimated_yield": 200,
        "growth_period_days": 180,
        "market_demand": "Very High",
        "profit_margin": 0.40,
        "ph_optimal": 6.2,
        "rainfall_optimal": 1600,
        "temp_optimal": 25,
        "recommended_season": "Year-round"
    },
    "Cardamom": {
        "suitability_score": 82.3,
        "suitability_level": "Good",
        "profit_potential": 50.0,
        "estimated_yield": 150,
        "growth_period_days": 365,
        "market_demand": "High",
        "profit_margin": 0.50,
        "ph_optimal": 5.8,
        "rainfall_optimal": 2500,
        "temp_optimal": 23,
        "recommended_season": "Year-round"
    }
}

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "FarmersHub API - AI-Powered Farming Assistant",
        "version": "1.0.0",
        "status": "active",
        "features": [
            "Plant Disease Detection",
            "Crop Recommendations",
            "AI Chatbot",
            "Weather Analytics",
            "Farm Profile Management",
            "Market Price Prediction",
            "Soil Health Assessment",
            "Government Scheme Matching",
            "Community Knowledge Sharing",
            "Mobile PWA Features"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Disease Detection Endpoints
@app.post("/api/disease-detection", response_model=DiseaseDetectionResponse)
async def detect_disease(request: DiseaseDetectionRequest, farm_id: str = None):
    """Detect plant disease from image"""
    try:
        # Simulate AI analysis with mock data
        import random
        mock_result = random.choice(MOCK_DISEASES)
        
        return DiseaseDetectionResponse(
            disease=mock_result["disease"],
            confidence=mock_result["confidence"],
            treatment=mock_result["treatment"],
            prevention=mock_result["prevention"],
            severity=mock_result["severity"],
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error in disease detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/disease-detection/upload")
async def detect_disease_upload(file: UploadFile = File(...), farm_id: str = None):
    """Detect plant disease from uploaded file"""
    try:
        # Simulate AI analysis with mock data
        import random
        mock_result = random.choice(MOCK_DISEASES)
        
        return {
            "disease": mock_result["disease"],
            "confidence": mock_result["confidence"],
            "treatment": mock_result["treatment"],
            "prevention": mock_result["prevention"],
            "severity": mock_result["severity"],
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error in disease detection upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Crop Recommendation Endpoints
@app.post("/api/crop-recommendations")
async def get_crop_recommendations(request: CropRecommendationRequest):
    """Get AI-powered crop recommendations"""
    try:
        # Simulate ML analysis with mock data
        recommendations = []
        
        for crop_name, crop_data in MOCK_CROPS.items():
            # Simple scoring based on pH and temperature
            ph_score = max(0, 100 - abs(request.ph - crop_data["ph_optimal"]) * 10)
            temp_score = max(0, 100 - abs(request.temperature - crop_data["temp_optimal"]) * 5)
            
            # Adjust score based on soil type and season
            soil_bonus = 10 if request.soil_type.lower() in ["laterite", "alluvial"] else 0
            season_bonus = 10 if request.season.lower() in crop_data["recommended_season"].lower() else 0
            
            final_score = (ph_score + temp_score) / 2 + soil_bonus + season_bonus
            final_score = min(100, max(0, final_score))
            
            if final_score > 30:  # Only include crops with reasonable suitability
                recommendations.append({
                    "crop": crop_name,
                    "suitability_score": round(final_score, 1),
                    "suitability_level": crop_data["suitability_level"],
                    "profit_potential": round(crop_data["profit_potential"], 1),
                    "estimated_yield": crop_data["estimated_yield"],
                    "growth_period_days": crop_data["growth_period_days"],
                    "market_demand": crop_data["market_demand"],
                    "profit_margin": crop_data["profit_margin"],
                    "ph_optimal": crop_data["ph_optimal"],
                    "rainfall_optimal": crop_data["rainfall_optimal"],
                    "temp_optimal": crop_data["temp_optimal"],
                    "recommended_season": crop_data["recommended_season"]
                })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        
        return {
            "recommendations": recommendations[:5],  # Top 5 recommendations
            "total_recommendations": len(recommendations),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in crop recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/crops/{crop_name}")
async def get_crop_details(crop_name: str):
    """Get detailed information about a specific crop"""
    try:
        if crop_name in MOCK_CROPS:
            return MOCK_CROPS[crop_name]
        else:
            raise HTTPException(status_code=404, detail="Crop not found")
            
    except Exception as e:
        logger.error(f"Error getting crop details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Weather Analytics Endpoints
@app.post("/api/weather/current")
async def get_current_weather(request: WeatherRequest):
    """Get current weather information"""
    try:
        # Mock weather data
        weather_data = {
            "temperature": 28.5,
            "humidity": 75,
            "pressure": 1013.25,
            "wind_speed": 12.5,
            "description": "Partly cloudy",
            "timestamp": datetime.now().isoformat()
        }
        
        return weather_data
        
    except Exception as e:
        logger.error(f"Error getting current weather: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/weather/forecast")
async def get_weather_forecast(request: WeatherRequest, days: int = Query(7, ge=1, le=7)):
    """Get weather forecast"""
    try:
        # Mock forecast data
        forecast = []
        for i in range(days):
            forecast.append({
                "date": (datetime.now().timestamp() + i * 24 * 60 * 60),
                "temperature": 28 + (i % 3) - 1,  # Vary temperature slightly
                "humidity": 70 + (i % 10),
                "description": ["Sunny", "Partly cloudy", "Cloudy"][i % 3]
            })
        
        return {
            "forecast": forecast,
            "total_days": len(forecast)
        }
        
    except Exception as e:
        logger.error(f"Error getting weather forecast: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/weather/summary")
async def get_weather_summary(request: WeatherRequest):
    """Get comprehensive weather summary"""
    try:
        summary = {
            "current": {
                "temperature": 28.5,
                "humidity": 75,
                "pressure": 1013.25,
                "wind_speed": 12.5,
                "description": "Partly cloudy"
            },
            "forecast": [
                {"date": datetime.now().isoformat(), "temperature": 28, "humidity": 70, "description": "Sunny"},
                {"date": (datetime.now().timestamp() + 24*60*60), "temperature": 29, "humidity": 75, "description": "Partly cloudy"}
            ],
            "alerts": ["High humidity may promote fungal diseases"],
            "recommendations": [
                "Good weather for planting",
                "Ensure proper irrigation",
                "Monitor for pest activity"
            ]
        }
        
        return summary
        
    except Exception as e:
        logger.error(f"Error getting weather summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# AI Chatbot Endpoints
@app.post("/api/chatbot")
async def chat_with_bot(request: ChatbotRequest):
    """Chat with AI assistant"""
    try:
        # Simple mock responses based on keywords
        message_lower = request.message.lower()
        
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            response = "Hello! I'm your AI farming assistant. How can I help you with your farming needs today?"
        elif any(word in message_lower for word in ["disease", "sick", "problem"]):
            response = "I can help you identify plant diseases. Upload a clear photo of the affected plant part for AI analysis."
        elif any(word in message_lower for word in ["crop", "plant", "grow"]):
            response = "For crop recommendations, I need to know your soil conditions. Use the soil analysis form to get personalized suggestions."
        elif any(word in message_lower for word in ["weather", "rain", "temperature"]):
            response = "Check the weather analytics section for current conditions and farming recommendations."
        elif any(word in message_lower for word in ["soil", "fertilizer", "nutrient"]):
            response = "Healthy soil is crucial for good farming. Test your soil regularly and maintain proper pH levels."
        else:
            response = "I understand you're asking about farming. I can help with disease detection, crop recommendations, weather analysis, and general farming advice. What specific area would you like to know more about?"
        
        return {
            "response": response,
            "language": request.language,
            "intent": "general",
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error in chatbot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chatbot/languages")
async def get_supported_languages():
    """Get supported languages"""
    try:
        languages = {
            'en': 'English',
            'ml': 'Malayalam', 
            'ta': 'Tamil',
            'hi': 'Hindi',
            'te': 'Telugu',
            'kn': 'Kannada'
        }
        return {"languages": languages}
        
    except Exception as e:
        logger.error(f"Error getting supported languages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Farm Profile Endpoints
@app.post("/api/farm-profiles")
async def create_farm_profile(request: FarmProfileRequest, user_id: str = Query(...)):
    """Create a new farm profile"""
    try:
        farm_id = f"farm_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "farm_id": farm_id, 
            "message": "Farm profile created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating farm profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/farm-profiles/{farm_id}")
async def get_farm_profile(farm_id: str):
    """Get farm profile by ID"""
    try:
        # Mock farm profile
        profile = {
            "id": farm_id,
            "name": "Sample Farm",
            "location": {"district": "Thiruvananthapuram", "state": "Kerala"},
            "total_area": 5.0,
            "soil_type": "Laterite",
            "soil_ph": 6.2,
            "farming_type": "Organic",
            "created_at": datetime.now().isoformat()
        }
        
        return profile
        
    except Exception as e:
        logger.error(f"Error getting farm profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/farm-profiles/user/{user_id}")
async def get_user_farms(user_id: str):
    """Get all farms for a user"""
    try:
        farms = [
            {
                "id": "farm_1",
                "name": "Main Farm",
                "location": {"district": "Thiruvananthapuram", "state": "Kerala"},
                "total_area": 5.0,
                "soil_type": "Laterite"
            }
        ]
        
        return {"farms": farms, "total": len(farms)}
        
    except Exception as e:
        logger.error(f"Error getting user farms: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/farm-profiles/{farm_id}/analytics")
async def get_farm_analytics(farm_id: str):
    """Get farm analytics"""
    try:
        analytics = {
            "farm_id": farm_id,
            "total_crops": 3,
            "active_crops": 2,
            "total_disease_detections": 5,
            "recent_disease_detections": 1,
            "soil_tests_count": 2,
            "last_soil_test": datetime.now().isoformat(),
            "farm_area": 5.0,
            "soil_type": "Laterite",
            "farming_type": "Organic"
        }
        
        return analytics
        
    except Exception as e:
        logger.error(f"Error getting farm analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Market Price Endpoints
@app.get("/api/market-prices/predict/{crop_name}")
async def predict_crop_price(crop_name: str, days: int = Query(7, ge=1, le=30)):
    """Predict crop price"""
    try:
        # Mock price prediction
        base_prices = {
            "rice": 25.50,
            "coconut": 8.75,
            "pepper": 450.00,
            "cardamom": 1200.00,
            "rubber": 180.00
        }
        
        base_price = base_prices.get(crop_name.lower(), 50.00)
        
        prediction = {
            "crop_name": crop_name,
            "current_price": base_price,
            "predicted_price": base_price * (1 + (days * 0.01)),  # Simple trend
            "confidence": 85.5,
            "trend": "increasing" if days > 7 else "stable",
            "recommendation": "Good time to sell" if days > 14 else "Hold for better prices"
        }
        
        return prediction
        
    except Exception as e:
        logger.error(f"Error predicting crop price: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/market-prices/insights")
async def get_market_insights(crop_name: Optional[str] = None):
    """Get market insights"""
    try:
        insights = {
            "crop_name": crop_name or "General",
            "market_trend": "Bullish",
            "price_volatility": "Low",
            "demand_level": "High",
            "supply_level": "Moderate",
            "recommendation": "Favorable market conditions for selling"
        }
        
        return insights
        
    except Exception as e:
        logger.error(f"Error getting market insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Government Scheme Endpoints
@app.post("/api/government-schemes/match")
async def match_government_schemes(request: dict):
    """Match farmer with government schemes"""
    try:
        schemes = [
            {
                "name": "PM-KISAN Scheme",
                "description": "Direct income support to farmers",
                "eligibility": "Land holding up to 2 hectares",
                "benefits": ["₹6000 per year", "Direct bank transfer"],
                "application_deadline": "2024-12-31"
            },
            {
                "name": "Pradhan Mantri Fasal Bima Yojana",
                "description": "Crop insurance scheme",
                "eligibility": "All farmers",
                "benefits": ["Premium subsidy up to 90%", "Quick claim settlement"],
                "application_deadline": "2024-12-31"
            }
        ]
        
        return {
            "farmer_id": "farmer_123",
            "matches": schemes,
            "total_matches": len(schemes)
        }
        
    except Exception as e:
        logger.error(f"Error matching government schemes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/government-schemes/search")
async def search_government_schemes(query: str, category: Optional[str] = None):
    """Search government schemes"""
    try:
        schemes = [
            {
                "name": "PM-KISAN Scheme",
                "description": "Direct income support to farmers",
                "category": "Income Support"
            }
        ]
        
        return {
            "schemes": schemes,
            "total_schemes": len(schemes),
            "query": query
        }
        
    except Exception as e:
        logger.error(f"Error searching government schemes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Community Endpoints
@app.post("/api/community/questions")
async def post_question(question_data: dict):
    """Post a question to the community"""
    try:
        question_id = f"q_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "question_id": question_id, 
            "message": "Question posted successfully"
        }
        
    except Exception as e:
        logger.error(f"Error posting question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/community/questions/search")
async def search_questions(query: str, category: Optional[str] = None, limit: int = 10):
    """Search community questions"""
    try:
        questions = [
            {
                "id": "q_1",
                "title": "Best time to plant rice in Kerala?",
                "content": "When is the optimal time to plant rice in Kerala?",
                "category": "Crop Management",
                "votes": 5,
                "answers": 2
            }
        ]
        
        return {
            "questions": questions,
            "total_questions": len(questions),
            "query": query
        }
        
    except Exception as e:
        logger.error(f"Error searching questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Resource not found", "error": "Not Found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "error": "Internal Server Error"}
    )

# Main function to run the server
if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main_api_server_fixed:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
