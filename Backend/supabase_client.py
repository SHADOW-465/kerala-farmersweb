"""
Supabase client configuration and database models
"""

import os
from supabase import create_client, Client
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseClient:
    """Supabase client wrapper for database operations"""
    
    def __init__(self):
        """Initialize Supabase client"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required")
        
        self.client: Client = create_client(self.url, self.key)
        logger.info("Supabase client initialized successfully")
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            # Simple query to test connection
            result = self.client.table("users").select("id").limit(1).execute()
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            return False

# Database Models
class User(BaseModel):
    id: str
    email: str
    name: str
    phone: Optional[str] = None
    preferred_language: str = "en"
    created_at: datetime
    updated_at: datetime

class Farm(BaseModel):
    id: str
    user_id: str
    name: str
    location: Dict[str, Any]
    total_area: float
    soil_type: str
    soil_ph: float
    soil_nutrients: Dict[str, float]
    irrigation_type: str
    farming_type: str
    established_year: int
    contact_info: Dict[str, str]
    created_at: datetime
    updated_at: datetime

class Crop(BaseModel):
    id: str
    farm_id: str
    crop_name: str
    planting_date: datetime
    expected_harvest: datetime
    area_acres: float
    status: str  # planted/growing/harvested
    yield_actual: Optional[float] = None
    created_at: datetime

class DiseaseDetection(BaseModel):
    id: str
    farm_id: str
    crop_id: Optional[str] = None
    image_url: str
    disease_name: str
    confidence_score: float
    treatment_applied: Optional[str] = None
    detection_date: datetime

class SoilTest(BaseModel):
    id: str
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
    test_date: datetime
    recommendations: Optional[str] = None

class MarketPrice(BaseModel):
    id: str
    crop_name: str
    market_location: str
    price_per_kg: float
    date: datetime
    source: str

class ChatSession(BaseModel):
    id: str
    user_id: str
    messages: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

class GovernmentScheme(BaseModel):
    id: str
    name: str
    description: str
    category: str
    eligibility_criteria: Dict[str, Any]
    benefits: List[str]
    application_process: List[str]
    required_documents: List[str]
    contact_info: Dict[str, str]
    is_active: bool
    created_at: datetime

class CommunityQuestion(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    category: str
    tags: List[str]
    answers: List[Dict[str, Any]]
    votes: int
    is_resolved: bool
    created_at: datetime
    updated_at: datetime

# Initialize global Supabase client
supabase_client = SupabaseClient()

# Export the client and models
__all__ = [
    "SupabaseClient",
    "supabase_client",
    "User",
    "Farm", 
    "Crop",
    "DiseaseDetection",
    "SoilTest",
    "MarketPrice",
    "ChatSession",
    "GovernmentScheme",
    "CommunityQuestion"
]
