"""
Database operations using Supabase
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from supabase_client import supabase_client, User, Farm, Crop, DiseaseDetection, SoilTest, MarketPrice, ChatSession, GovernmentScheme, CommunityQuestion

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseOperations:
    """Database operations wrapper for Supabase"""
    
    def __init__(self):
        self.client = supabase_client.client
    
    # User Operations
    def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        """Create a new user"""
        try:
            result = self.client.table("users").insert(user_data).execute()
            if result.data:
                return result.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return None
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            result = self.client.table("users").select("*").eq("id", user_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """Update user data"""
        try:
            result = self.client.table("users").update(user_data).eq("id", user_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return False
    
    # Farm Operations
    def create_farm(self, farm_data: Dict[str, Any]) -> Optional[str]:
        """Create a new farm"""
        try:
            result = self.client.table("farms").insert(farm_data).execute()
            if result.data:
                return result.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating farm: {str(e)}")
            return None
    
    def get_farm(self, farm_id: str) -> Optional[Dict[str, Any]]:
        """Get farm by ID"""
        try:
            result = self.client.table("farms").select("*").eq("id", farm_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting farm: {str(e)}")
            return None
    
    def get_user_farms(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all farms for a user"""
        try:
            result = self.client.table("farms").select("*").eq("user_id", user_id).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting user farms: {str(e)}")
            return []
    
    def update_farm(self, farm_id: str, farm_data: Dict[str, Any]) -> bool:
        """Update farm data"""
        try:
            result = self.client.table("farms").update(farm_data).eq("id", farm_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error updating farm: {str(e)}")
            return False
    
    # Crop Operations
    def create_crop(self, crop_data: Dict[str, Any]) -> Optional[str]:
        """Create a new crop record"""
        try:
            result = self.client.table("crops").insert(crop_data).execute()
            if result.data:
                return result.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating crop: {str(e)}")
            return None
    
    def get_farm_crops(self, farm_id: str) -> List[Dict[str, Any]]:
        """Get all crops for a farm"""
        try:
            result = self.client.table("crops").select("*").eq("farm_id", farm_id).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting farm crops: {str(e)}")
            return []
    
    def update_crop(self, crop_id: str, crop_data: Dict[str, Any]) -> bool:
        """Update crop data"""
        try:
            result = self.client.table("crops").update(crop_data).eq("id", crop_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error updating crop: {str(e)}")
            return False
    
    # Disease Detection Operations
    def create_disease_detection(self, detection_data: Dict[str, Any]) -> Optional[str]:
        """Create a new disease detection record"""
        try:
            result = self.client.table("disease_detections").insert(detection_data).execute()
            if result.data:
                return result.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating disease detection: {str(e)}")
            return None
    
    def get_farm_disease_detections(self, farm_id: str) -> List[Dict[str, Any]]:
        """Get all disease detections for a farm"""
        try:
            result = self.client.table("disease_detections").select("*").eq("farm_id", farm_id).order("detection_date", desc=True).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting farm disease detections: {str(e)}")
            return []
    
    # Soil Test Operations
    def create_soil_test(self, soil_test_data: Dict[str, Any]) -> Optional[str]:
        """Create a new soil test record"""
        try:
            result = self.client.table("soil_tests").insert(soil_test_data).execute()
            if result.data:
                return result.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating soil test: {str(e)}")
            return None
    
    def get_farm_soil_tests(self, farm_id: str) -> List[Dict[str, Any]]:
        """Get all soil tests for a farm"""
        try:
            result = self.client.table("soil_tests").select("*").eq("farm_id", farm_id).order("test_date", desc=True).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting farm soil tests: {str(e)}")
            return []
    
    # Market Price Operations
    def create_market_price(self, price_data: Dict[str, Any]) -> Optional[str]:
        """Create a new market price record"""
        try:
            result = self.client.table("market_prices").insert(price_data).execute()
            if result.data:
                return result.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating market price: {str(e)}")
            return None
    
    def get_market_prices(self, crop_name: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get market prices, optionally filtered by crop"""
        try:
            query = self.client.table("market_prices").select("*")
            if crop_name:
                query = query.eq("crop_name", crop_name)
            result = query.order("date", desc=True).limit(limit).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting market prices: {str(e)}")
            return []
    
    # Chat Session Operations
    def create_chat_session(self, session_data: Dict[str, Any]) -> Optional[str]:
        """Create a new chat session"""
        try:
            result = self.client.table("chat_sessions").insert(session_data).execute()
            if result.data:
                return result.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating chat session: {str(e)}")
            return None
    
    def get_user_chat_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all chat sessions for a user"""
        try:
            result = self.client.table("chat_sessions").select("*").eq("user_id", user_id).order("updated_at", desc=True).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting user chat sessions: {str(e)}")
            return []
    
    def update_chat_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Update chat session"""
        try:
            result = self.client.table("chat_sessions").update(session_data).eq("id", session_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error updating chat session: {str(e)}")
            return False
    
    # Government Scheme Operations
    def get_government_schemes(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get government schemes, optionally filtered by category"""
        try:
            query = self.client.table("government_schemes").select("*").eq("is_active", True)
            if category:
                query = query.eq("category", category)
            result = query.order("created_at", desc=True).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting government schemes: {str(e)}")
            return []
    
    def search_government_schemes(self, query: str) -> List[Dict[str, Any]]:
        """Search government schemes by name or description"""
        try:
            result = self.client.table("government_schemes").select("*").or_(f"name.ilike.%{query}%,description.ilike.%{query}%").eq("is_active", True).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error searching government schemes: {str(e)}")
            return []
    
    # Community Question Operations
    def create_community_question(self, question_data: Dict[str, Any]) -> Optional[str]:
        """Create a new community question"""
        try:
            result = self.client.table("community_questions").insert(question_data).execute()
            if result.data:
                return result.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating community question: {str(e)}")
            return None
    
    def get_community_questions(self, category: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get community questions, optionally filtered by category"""
        try:
            query = self.client.table("community_questions").select("*")
            if category:
                query = query.eq("category", category)
            result = query.order("created_at", desc=True).limit(limit).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting community questions: {str(e)}")
            return []
    
    def search_community_questions(self, query: str) -> List[Dict[str, Any]]:
        """Search community questions by title or content"""
        try:
            result = self.client.table("community_questions").select("*").or_(f"title.ilike.%{query}%,content.ilike.%{query}%").order("created_at", desc=True).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error searching community questions: {str(e)}")
            return []
    
    def update_community_question(self, question_id: str, question_data: Dict[str, Any]) -> bool:
        """Update community question"""
        try:
            result = self.client.table("community_questions").update(question_data).eq("id", question_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error updating community question: {str(e)}")
            return False

# Initialize global database operations
db_ops = DatabaseOperations()

# Export the operations
__all__ = ["DatabaseOperations", "db_ops"]
