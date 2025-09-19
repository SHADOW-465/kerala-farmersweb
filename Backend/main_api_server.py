"""
Main API Server for FarmersHub
FastAPI-based REST API server that integrates all farming features
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import uvicorn
import logging
from datetime import datetime
import os
import json
from pathlib import Path

# Import all feature modules
from disease_detection import PlantDiseaseDetector
from crop_recommendation import SmartCropRecommender
from ai_chatbot import AIChatbotAssistant
from weather_analytics import IntelligentWeatherAnalytics
from farm_profile import FarmProfileManager
from market_price_prediction import MarketPricePredictor
from soil_health_assessment import SoilHealthAssessment, SoilTestResult
from government_scheme_matcher import GovernmentSchemeMatcher
from community_knowledge import CommunityKnowledgePlatform
from mobile_pwa_features import MobilePWAFeatures
from database_operations import db_ops
from supabase_client import supabase_client

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

# Global variables for feature modules
disease_detector = None
crop_recommender = None
chatbot = None
weather_analytics = None
farm_manager = None
market_predictor = None
soil_assessor = None
scheme_matcher = None
community_platform = None
mobile_pwa = None

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

class SoilTestRequest(BaseModel):
    farm_id: str
    ph_level: float
    nitrogen: float
    phosphorus: float
    potassium: float
    organic_matter: float
    carbon_content: float
    bulk_density: float
    water_holding_capacity: float
    cation_exchange_capacity: float
    micronutrients: Dict[str, float]
    soil_texture: str
    soil_color: str
    drainage: str
    erosion_level: str
    lab_name: str

class GovernmentSchemeRequest(BaseModel):
    farmer_id: str
    land_holding: float
    annual_income: float
    farming_type: str
    crops_grown: List[str]
    location: Dict[str, str]

# Dependency to get API key
def get_api_key():
    return os.getenv("HUGGINGFACE_API_KEY", "your_api_key_here")

def get_weather_api_key():
    return os.getenv("OPENWEATHER_API_KEY", "your_weather_api_key_here")

# Initialize feature modules
@app.on_event("startup")
async def startup_event():
    """Initialize all feature modules on startup"""
    global disease_detector, crop_recommender, chatbot, weather_analytics
    global farm_manager, market_predictor, soil_assessor, scheme_matcher
    global community_platform, mobile_pwa
    
    try:
        # Test Supabase connection
        if not supabase_client.test_connection():
            logger.warning("Supabase connection test failed, but continuing...")
        
        # Initialize feature modules
        disease_detector = PlantDiseaseDetector(get_api_key())
        crop_recommender = SmartCropRecommender()
        chatbot = AIChatbotAssistant(get_api_key())
        weather_analytics = IntelligentWeatherAnalytics(get_weather_api_key())
        farm_manager = FarmProfileManager()
        market_predictor = MarketPricePredictor()
        soil_assessor = SoilHealthAssessment()
        scheme_matcher = GovernmentSchemeMatcher()
        community_platform = CommunityKnowledgePlatform()
        mobile_pwa = MobilePWAFeatures()
        
        logger.info("All feature modules initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing feature modules: {str(e)}")
        raise

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
        # Decode base64 image
        import base64
        image_bytes = base64.b64decode(request.image_base64)
        
        # Detect disease
        result = disease_detector.detect_disease(image_bytes)
        
        if result['success']:
            # Save to database if farm_id provided
            if farm_id:
                detection_data = {
                    'farm_id': farm_id,
                    'crop_id': None,  # Could be enhanced to include crop_id
                    'image_url': f"data:image/jpeg;base64,{request.image_base64}",  # Store as data URL for now
                    'disease_name': result['disease'],
                    'confidence_score': result['confidence'],
                    'treatment_applied': None,
                    'detection_date': datetime.now().isoformat()
                }
                db_ops.create_disease_detection(detection_data)
            
            return DiseaseDetectionResponse(
                disease=result['disease'],
                confidence=result['confidence'],
                treatment=result['treatment'],
                prevention=result['prevention'],
                severity=result['severity'],
                success=True
            )
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Error in disease detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/disease-detection/upload")
async def detect_disease_upload(file: UploadFile = File(...)):
    """Detect plant disease from uploaded file"""
    try:
        # Read file content
        image_bytes = await file.read()
        
        # Detect disease
        result = disease_detector.detect_disease(image_bytes)
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Error in disease detection upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Crop Recommendation Endpoints
@app.post("/api/crop-recommendations")
async def get_crop_recommendations(request: CropRecommendationRequest):
    """Get AI-powered crop recommendations"""
    try:
        recommendations = crop_recommender.get_crop_recommendations(
            ph=request.ph,
            nitrogen=request.nitrogen,
            phosphorus=request.phosphorus,
            potassium=request.potassium,
            rainfall=request.rainfall,
            temperature=request.temperature,
            soil_type=request.soil_type,
            season=request.season
        )
        
        return {
            "recommendations": recommendations,
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
        details = crop_recommender.get_crop_details(crop_name)
        if details:
            return details
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
        weather_data = weather_analytics.get_current_weather(request.city, request.state)
        if weather_data:
            return {
                "temperature": weather_data.temperature,
                "humidity": weather_data.humidity,
                "pressure": weather_data.pressure,
                "wind_speed": weather_data.wind_speed,
                "description": weather_data.description,
                "timestamp": weather_data.timestamp.isoformat()
            }
        else:
            raise HTTPException(status_code=404, detail="Weather data not found")
            
    except Exception as e:
        logger.error(f"Error getting current weather: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/weather/forecast")
async def get_weather_forecast(request: WeatherRequest, days: int = Query(7, ge=1, le=7)):
    """Get weather forecast"""
    try:
        forecast = weather_analytics.get_weather_forecast(request.city, request.state, days)
        return {
            "forecast": [
                {
                    "date": w.timestamp.isoformat(),
                    "temperature": w.temperature,
                    "humidity": w.humidity,
                    "description": w.description
                } for w in forecast
            ],
            "total_days": len(forecast)
        }
        
    except Exception as e:
        logger.error(f"Error getting weather forecast: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/weather/summary")
async def get_weather_summary(request: WeatherRequest):
    """Get comprehensive weather summary"""
    try:
        summary = weather_analytics.get_weather_summary(request.city, request.state)
        return summary
        
    except Exception as e:
        logger.error(f"Error getting weather summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# AI Chatbot Endpoints
@app.post("/api/chatbot")
async def chat_with_bot(request: ChatbotRequest):
    """Chat with AI assistant"""
    try:
        response = chatbot.generate_response(request.message, request.language)
        return response
        
    except Exception as e:
        logger.error(f"Error in chatbot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chatbot/languages")
async def get_supported_languages():
    """Get supported languages"""
    try:
        languages = chatbot.get_supported_languages()
        return {"languages": languages}
        
    except Exception as e:
        logger.error(f"Error getting supported languages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Farm Profile Endpoints
@app.post("/api/farm-profiles")
async def create_farm_profile(request: FarmProfileRequest, user_id: str):
    """Create a new farm profile"""
    try:
        farm_data = {
            'user_id': user_id,
            'name': request.farm_name,
            'location': request.location,
            'total_area': request.total_area,
            'soil_type': request.soil_type,
            'soil_ph': request.soil_ph,
            'soil_nutrients': request.soil_nutrients,
            'irrigation_type': request.irrigation_type,
            'farming_type': request.farming_type,
            'established_year': request.established_year,
            'contact_info': request.contact_info,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        farm_id = db_ops.create_farm(farm_data)
        if farm_id:
            return {"farm_id": farm_id, "message": "Farm profile created successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to create farm profile")
        
    except Exception as e:
        logger.error(f"Error creating farm profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/farm-profiles/{farm_id}")
async def get_farm_profile(farm_id: str):
    """Get farm profile by ID"""
    try:
        profile = db_ops.get_farm(farm_id)
        if profile:
            return profile
        else:
            raise HTTPException(status_code=404, detail="Farm profile not found")
            
    except Exception as e:
        logger.error(f"Error getting farm profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/farm-profiles/user/{user_id}")
async def get_user_farms(user_id: str):
    """Get all farms for a user"""
    try:
        farms = db_ops.get_user_farms(user_id)
        return {"farms": farms, "total": len(farms)}
        
    except Exception as e:
        logger.error(f"Error getting user farms: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/farm-profiles/{farm_id}/analytics")
async def get_farm_analytics(farm_id: str):
    """Get farm analytics"""
    try:
        # Get farm data
        farm = db_ops.get_farm(farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")
        
        # Get crops
        crops = db_ops.get_farm_crops(farm_id)
        
        # Get disease detections
        disease_detections = db_ops.get_farm_disease_detections(farm_id)
        
        # Get soil tests
        soil_tests = db_ops.get_farm_soil_tests(farm_id)
        
        analytics = {
            'farm_id': farm_id,
            'total_crops': len(crops),
            'active_crops': len([c for c in crops if c['status'] in ['planted', 'growing']]),
            'total_disease_detections': len(disease_detections),
            'recent_disease_detections': len([d for d in disease_detections if d['detection_date'] > (datetime.now().timestamp() - 30*24*60*60)]),
            'soil_tests_count': len(soil_tests),
            'last_soil_test': soil_tests[0]['test_date'] if soil_tests else None,
            'farm_area': farm['total_area'],
            'soil_type': farm['soil_type'],
            'farming_type': farm['farming_type']
        }
        
        return analytics
        
    except Exception as e:
        logger.error(f"Error getting farm analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Market Price Prediction Endpoints
@app.get("/api/market-prices/predict/{crop_name}")
async def predict_crop_price(crop_name: str, days: int = Query(7, ge=1, le=30)):
    """Predict crop price"""
    try:
        prediction = market_predictor.predict_price(crop_name)
        return prediction
        
    except Exception as e:
        logger.error(f"Error predicting crop price: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/market-prices/insights")
async def get_market_insights(crop_name: Optional[str] = None):
    """Get market insights"""
    try:
        insights = market_predictor.get_market_insights(crop_name)
        return insights
        
    except Exception as e:
        logger.error(f"Error getting market insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Soil Health Assessment Endpoints
@app.post("/api/soil-health/assess")
async def assess_soil_health(request: SoilTestRequest):
    """Assess soil health"""
    try:
        # Create SoilTestResult object
        soil_test = SoilTestResult(
            test_id=f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            farm_id=request.farm_id,
            test_date=datetime.now(),
            ph_level=request.ph_level,
            nitrogen=request.nitrogen,
            phosphorus=request.phosphorus,
            potassium=request.potassium,
            organic_matter=request.organic_matter,
            carbon_content=request.carbon_content,
            bulk_density=request.bulk_density,
            water_holding_capacity=request.water_holding_capacity,
            cation_exchange_capacity=request.cation_exchange_capacity,
            micronutrients=request.micronutrients,
            soil_texture=request.soil_texture,
            soil_color=request.soil_color,
            drainage=request.drainage,
            erosion_level=request.erosion_level,
            lab_name=request.lab_name,
            created_at=datetime.now()
        )
        
        # Assess soil health
        health_score = soil_assessor.assess_soil_health(soil_test)
        return health_score
        
    except Exception as e:
        logger.error(f"Error assessing soil health: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/soil-health/crop-suitability")
async def check_crop_suitability(request: SoilTestRequest, crop_name: str):
    """Check crop suitability for soil"""
    try:
        # Create SoilTestResult object
        soil_test = SoilTestResult(
            test_id=f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            farm_id=request.farm_id,
            test_date=datetime.now(),
            ph_level=request.ph_level,
            nitrogen=request.nitrogen,
            phosphorus=request.phosphorus,
            potassium=request.potassium,
            organic_matter=request.organic_matter,
            carbon_content=request.carbon_content,
            bulk_density=request.bulk_density,
            water_holding_capacity=request.water_holding_capacity,
            cation_exchange_capacity=request.cation_exchange_capacity,
            micronutrients=request.micronutrients,
            soil_texture=request.soil_texture,
            soil_color=request.soil_color,
            drainage=request.drainage,
            erosion_level=request.erosion_level,
            lab_name=request.lab_name,
            created_at=datetime.now()
        )
        
        # Check crop suitability
        suitability = soil_assessor.get_crop_suitability(soil_test, crop_name)
        return suitability
        
    except Exception as e:
        logger.error(f"Error checking crop suitability: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Government Scheme Endpoints
@app.post("/api/government-schemes/match")
async def match_government_schemes(request: GovernmentSchemeRequest):
    """Match farmer with government schemes"""
    try:
        # Create farmer profile
        farmer_data = {
            'name': f"Farmer_{request.farmer_id}",
            'age': 35,
            'gender': 'Male',
            'location': request.location,
            'land_holding': request.land_holding,
            'farming_type': request.farming_type,
            'annual_income': request.annual_income,
            'crops_grown': request.crops_grown,
            'livestock': [],
            'education_level': 'High School',
            'caste_category': 'General',
            'bank_account': True,
            'aadhaar_linked': True
        }
        
        farmer_id = scheme_matcher.add_farmer_profile(farmer_data)
        matches = scheme_matcher.find_matching_schemes(farmer_id)
        
        return {
            "farmer_id": farmer_id,
            "matches": matches,
            "total_matches": len(matches)
        }
        
    except Exception as e:
        logger.error(f"Error matching government schemes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/government-schemes/search")
async def search_government_schemes(query: str, category: Optional[str] = None):
    """Search government schemes"""
    try:
        schemes = scheme_matcher.search_schemes(query, category)
        return {
            "schemes": schemes,
            "total_schemes": len(schemes),
            "query": query
        }
        
    except Exception as e:
        logger.error(f"Error searching government schemes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Community Knowledge Endpoints
@app.post("/api/community/questions")
async def post_question(question_data: dict):
    """Post a question to the community"""
    try:
        question_id = community_platform.post_question(
            question_data['user_id'],
            question_data
        )
        return {"question_id": question_id, "message": "Question posted successfully"}
        
    except Exception as e:
        logger.error(f"Error posting question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/community/questions/search")
async def search_questions(query: str, category: Optional[str] = None, limit: int = 10):
    """Search community questions"""
    try:
        questions = community_platform.search_questions(query, category, limit)
        return {
            "questions": questions,
            "total_questions": len(questions),
            "query": query
        }
        
    except Exception as e:
        logger.error(f"Error searching questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Mobile PWA Endpoints
@app.get("/api/mobile/manifest")
async def get_pwa_manifest():
    """Get PWA manifest"""
    try:
        manifest = mobile_pwa.generate_manifest()
        return manifest
        
    except Exception as e:
        logger.error(f"Error getting PWA manifest: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mobile/service-worker")
async def get_service_worker():
    """Get service worker code"""
    try:
        service_worker = mobile_pwa.generate_service_worker()
        return {"code": service_worker}
        
    except Exception as e:
        logger.error(f"Error getting service worker: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mobile/offline")
async def get_offline_page():
    """Get offline page"""
    try:
        offline_page = mobile_pwa.generate_offline_page()
        return {"html": offline_page}
        
    except Exception as e:
        logger.error(f"Error getting offline page: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Static files (for serving PWA assets)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    # Create static directory if it doesn't exist
    Path("static").mkdir(exist_ok=True)
    
    # Run the server
    uvicorn.run(
        "main_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
