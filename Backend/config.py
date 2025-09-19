"""
Configuration file for FarmersHub API
Contains all configuration settings and environment variables
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

class Config:
    """Base configuration class"""
    
    # API Configuration
    API_TITLE = "FarmersHub API"
    API_DESCRIPTION = "AI-powered farming assistant API for Kerala farmers"
    API_VERSION = "1.0.0"
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farmershub.db")
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "farmershub.db")
    
    # API Keys
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    
    # CORS Configuration
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "https://farmershub.app",
        "https://www.farmershub.app"
    ]
    
    # Security Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALGORITHM = "HS256"
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "farmershub.log")
    
    # File Upload Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]
    UPLOAD_DIRECTORY = "uploads"
    
    # Cache Configuration
    CACHE_TTL = 300  # 5 minutes
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = 60
    RATE_LIMIT_BURST = 10
    
    # Feature Flags
    ENABLE_DISEASE_DETECTION = True
    ENABLE_CROP_RECOMMENDATIONS = True
    ENABLE_WEATHER_ANALYTICS = True
    ENABLE_MARKET_PREDICTIONS = True
    ENABLE_SOIL_HEALTH_ASSESSMENT = True
    ENABLE_GOVERNMENT_SCHEMES = True
    ENABLE_COMMUNITY_FEATURES = True
    ENABLE_MOBILE_PWA = True
    
    # AI Model Configuration
    DISEASE_DETECTION_MODEL = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
    CHATBOT_MODEL = "microsoft/DialoGPT-medium"
    CROP_RECOMMENDATION_MODEL = "random_forest"
    
    # Kerala-specific Configuration
    KERALA_STATE = "Kerala"
    KERALA_DISTRICTS = [
        "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha",
        "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad",
        "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"
    ]
    
    # Crop Configuration
    KERALA_CROPS = [
        "Rice", "Coconut", "Pepper", "Cardamom", "Rubber", "Tea",
        "Coffee", "Banana", "Ginger", "Turmeric", "Cashew", "Tapioca"
    ]
    
    # Soil Types
    SOIL_TYPES = [
        "Laterite", "Alluvial", "Black", "Red", "Coastal Sandy", "Clay", "Loam"
    ]
    
    # Seasons
    SEASONS = ["Kharif", "Rabi", "Zaid", "Year-round"]
    
    # Farming Types
    FARMING_TYPES = ["Organic", "Conventional", "Mixed", "Natural"]
    
    # Irrigation Types
    IRRIGATION_TYPES = [
        "Drip", "Sprinkler", "Flood", "Furrow", "Basin", "Manual"
    ]
    
    # Weather Configuration
    WEATHER_UPDATE_INTERVAL = 3600  # 1 hour
    WEATHER_CACHE_TTL = 1800  # 30 minutes
    
    # Market Price Configuration
    PRICE_UPDATE_INTERVAL = 7200  # 2 hours
    PRICE_CACHE_TTL = 3600  # 1 hour
    
    # Soil Health Configuration
    SOIL_HEALTH_STANDARDS = {
        "ph_optimal": (6.0, 7.0),
        "nitrogen_optimal": (80, 150),
        "phosphorus_optimal": (40, 60),
        "potassium_optimal": (80, 120),
        "organic_matter_optimal": (2.0, 4.0)
    }
    
    # Government Scheme Configuration
    SCHEME_CATEGORIES = [
        "Income Support", "Crop Insurance", "Credit", "Soil Testing",
        "Organic Farming", "Irrigation", "Technology", "Training"
    ]
    
    # Community Configuration
    MAX_QUESTION_LENGTH = 1000
    MAX_ANSWER_LENGTH = 2000
    MAX_ARTICLE_LENGTH = 5000
    REPUTATION_THRESHOLDS = {
        "expert": 1000,
        "experienced": 500,
        "intermediate": 100,
        "beginner": 0
    }
    
    # Mobile PWA Configuration
    PWA_NAME = "FarmersHub - AI Farming Assistant"
    PWA_SHORT_NAME = "FarmersHub"
    PWA_THEME_COLOR = "#2E8B57"
    PWA_BACKGROUND_COLOR = "#FFFFFF"
    PWA_DISPLAY = "standalone"
    PWA_ORIENTATION = "portrait"
    
    # Notification Configuration
    PUSH_NOTIFICATION_ENABLED = True
    NOTIFICATION_TYPES = [
        "weather_alert", "price_alert", "disease_alert", "scheme_alert"
    ]
    
    # Analytics Configuration
    ANALYTICS_ENABLED = True
    ANALYTICS_RETENTION_DAYS = 365
    
    # Performance Configuration
    MAX_CONCURRENT_REQUESTS = 100
    REQUEST_TIMEOUT = 30
    RESPONSE_CACHE_TTL = 300
    
    # Error Configuration
    ERROR_REPORTING_ENABLED = True
    ERROR_REPORTING_EMAIL = os.getenv("ERROR_REPORTING_EMAIL", "")
    
    # Backup Configuration
    BACKUP_ENABLED = True
    BACKUP_INTERVAL = 86400  # 24 hours
    BACKUP_RETENTION_DAYS = 30
    
    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            "url": cls.DATABASE_URL,
            "sqlite_path": cls.SQLITE_DB_PATH,
            "echo": cls.LOG_LEVEL == "DEBUG"
        }
    
    @classmethod
    def get_ai_config(cls) -> Dict[str, Any]:
        """Get AI configuration"""
        return {
            "huggingface_api_key": cls.HUGGINGFACE_API_KEY,
            "disease_detection_model": cls.DISEASE_DETECTION_MODEL,
            "chatbot_model": cls.CHATBOT_MODEL,
            "crop_recommendation_model": cls.CROP_RECOMMENDATION_MODEL
        }
    
    @classmethod
    def get_weather_config(cls) -> Dict[str, Any]:
        """Get weather configuration"""
        return {
            "api_key": cls.OPENWEATHER_API_KEY,
            "update_interval": cls.WEATHER_UPDATE_INTERVAL,
            "cache_ttl": cls.WEATHER_CACHE_TTL
        }
    
    @classmethod
    def get_mobile_config(cls) -> Dict[str, Any]:
        """Get mobile PWA configuration"""
        return {
            "name": cls.PWA_NAME,
            "short_name": cls.PWA_SHORT_NAME,
            "theme_color": cls.PWA_THEME_COLOR,
            "background_color": cls.PWA_BACKGROUND_COLOR,
            "display": cls.PWA_DISPLAY,
            "orientation": cls.PWA_ORIENTATION
        }
    
    @classmethod
    def get_feature_flags(cls) -> Dict[str, bool]:
        """Get feature flags"""
        return {
            "disease_detection": cls.ENABLE_DISEASE_DETECTION,
            "crop_recommendations": cls.ENABLE_CROP_RECOMMENDATIONS,
            "weather_analytics": cls.ENABLE_WEATHER_ANALYTICS,
            "market_predictions": cls.ENABLE_MARKET_PREDICTIONS,
            "soil_health_assessment": cls.ENABLE_SOIL_HEALTH_ASSESSMENT,
            "government_schemes": cls.ENABLE_GOVERNMENT_SCHEMES,
            "community_features": cls.ENABLE_COMMUNITY_FEATURES,
            "mobile_pwa": cls.ENABLE_MOBILE_PWA
        }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    CORS_ORIGINS = ["*"]
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = "INFO"
    CORS_ORIGINS = [
        "https://farmershub.app",
        "https://www.farmershub.app"
    ]

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = "sqlite:///./test_farmershub.db"
    SQLITE_DB_PATH = "test_farmershub.db"
    LOG_LEVEL = "WARNING"

# Configuration mapping
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}

def get_config(environment: str = None) -> Config:
    """Get configuration based on environment"""
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")
    
    config_class = config_map.get(environment, DevelopmentConfig)
    return config_class()

# Environment-specific settings
def get_environment_settings() -> Dict[str, Any]:
    """Get environment-specific settings"""
    environment = os.getenv("ENVIRONMENT", "development")
    
    settings = {
        "development": {
            "reload": True,
            "log_level": "debug",
            "workers": 1
        },
        "production": {
            "reload": False,
            "log_level": "info",
            "workers": 4
        },
        "testing": {
            "reload": False,
            "log_level": "warning",
            "workers": 1
        }
    }
    
    return settings.get(environment, settings["development"])

# Validation functions
def validate_config(config: Config) -> bool:
    """Validate configuration settings"""
    errors = []
    
    # Check required API keys
    if not config.HUGGINGFACE_API_KEY:
        errors.append("HUGGINGFACE_API_KEY is required")
    
    if not config.OPENWEATHER_API_KEY:
        errors.append("OPENWEATHER_API_KEY is required")
    
    # Check file paths
    if not Path(config.UPLOAD_DIRECTORY).exists():
        try:
            Path(config.UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create upload directory: {e}")
    
    # Check database URL
    if not config.DATABASE_URL:
        errors.append("DATABASE_URL is required")
    
    if errors:
        for error in errors:
            print(f"Configuration Error: {error}")
        return False
    
    return True

# Export configuration
__all__ = [
    "Config",
    "DevelopmentConfig", 
    "ProductionConfig",
    "TestingConfig",
    "get_config",
    "get_environment_settings",
    "validate_config"
]
