"""
Smart Crop Recommendation Engine
Uses ML algorithms and Kerala-specific data for crop recommendations
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import logging
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartCropRecommender:
    """
    AI-powered crop recommendation system for Kerala farmers
    """
    
    def __init__(self):
        """Initialize the crop recommendation system"""
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        
        # Kerala-specific crop data with comprehensive requirements
        self.kerala_crops_data = {
            'Rice': {
                'ph_min': 5.0, 'ph_max': 6.5, 'ph_optimal': 5.8,
                'rainfall_min': 1000, 'rainfall_max': 2000, 'rainfall_optimal': 1500,
                'temp_min': 20, 'temp_max': 35, 'temp_optimal': 26,
                'nitrogen_min': 80, 'nitrogen_max': 120, 'nitrogen_optimal': 100,
                'phosphorus_min': 40, 'phosphorus_max': 60, 'phosphorus_optimal': 50,
                'potassium_min': 40, 'potassium_max': 80, 'potassium_optimal': 60,
                'soil_types': ['Alluvial', 'Laterite', 'Black'],
                'seasons': ['Kharif', 'Rabi'],
                'market_demand': 'High',
                'profit_margin': 0.25,
                'yield_per_hectare': 3000,
                'growth_period_days': 120
            },
            'Coconut': {
                'ph_min': 5.2, 'ph_max': 8.0, 'ph_optimal': 6.5,
                'rainfall_min': 1300, 'rainfall_max': 2300, 'rainfall_optimal': 1800,
                'temp_min': 20, 'temp_max': 35, 'temp_optimal': 28,
                'nitrogen_min': 100, 'nitrogen_max': 150, 'nitrogen_optimal': 125,
                'phosphorus_min': 50, 'phosphorus_max': 80, 'phosphorus_optimal': 65,
                'potassium_min': 100, 'potassium_max': 200, 'potassium_optimal': 150,
                'soil_types': ['Laterite', 'Alluvial', 'Coastal Sandy'],
                'seasons': ['Year-round'],
                'market_demand': 'Very High',
                'profit_margin': 0.35,
                'yield_per_hectare': 80,
                'growth_period_days': 365
            },
            'Pepper': {
                'ph_min': 5.5, 'ph_max': 7.0, 'ph_optimal': 6.2,
                'rainfall_min': 1250, 'rainfall_max': 2000, 'rainfall_optimal': 1600,
                'temp_min': 18, 'temp_max': 32, 'temp_optimal': 25,
                'nitrogen_min': 60, 'nitrogen_max': 100, 'nitrogen_optimal': 80,
                'phosphorus_min': 30, 'phosphorus_max': 50, 'phosphorus_optimal': 40,
                'potassium_min': 80, 'potassium_max': 120, 'potassium_optimal': 100,
                'soil_types': ['Laterite', 'Red'],
                'seasons': ['Year-round'],
                'market_demand': 'Very High',
                'profit_margin': 0.40,
                'yield_per_hectare': 200,
                'growth_period_days': 180
            },
            'Cardamom': {
                'ph_min': 5.0, 'ph_max': 6.5, 'ph_optimal': 5.8,
                'rainfall_min': 1500, 'rainfall_max': 4000, 'rainfall_optimal': 2500,
                'temp_min': 15, 'temp_max': 28, 'temp_optimal': 23,
                'nitrogen_min': 100, 'nitrogen_max': 150, 'nitrogen_optimal': 125,
                'phosphorus_min': 50, 'phosphorus_max': 80, 'phosphorus_optimal': 65,
                'potassium_min': 100, 'potassium_max': 150, 'potassium_optimal': 125,
                'soil_types': ['Laterite', 'Forest'],
                'seasons': ['Year-round'],
                'market_demand': 'High',
                'profit_margin': 0.50,
                'yield_per_hectare': 150,
                'growth_period_days': 365
            },
            'Rubber': {
                'ph_min': 5.0, 'ph_max': 6.5, 'ph_optimal': 5.8,
                'rainfall_min': 1500, 'rainfall_max': 2500, 'rainfall_optimal': 2000,
                'temp_min': 22, 'temp_max': 32, 'temp_optimal': 27,
                'nitrogen_min': 80, 'nitrogen_max': 120, 'nitrogen_optimal': 100,
                'phosphorus_min': 40, 'phosphorus_max': 60, 'phosphorus_optimal': 50,
                'potassium_min': 60, 'potassium_max': 100, 'potassium_optimal': 80,
                'soil_types': ['Laterite', 'Red'],
                'seasons': ['Year-round'],
                'market_demand': 'Medium',
                'profit_margin': 0.20,
                'yield_per_hectare': 2000,
                'growth_period_days': 2555  # 7 years
            },
            'Tea': {
                'ph_min': 4.5, 'ph_max': 6.0, 'ph_optimal': 5.2,
                'rainfall_min': 1200, 'rainfall_max': 2500, 'rainfall_optimal': 1800,
                'temp_min': 15, 'temp_max': 28, 'temp_optimal': 22,
                'nitrogen_min': 120, 'nitrogen_max': 180, 'nitrogen_optimal': 150,
                'phosphorus_min': 30, 'phosphorus_max': 50, 'phosphorus_optimal': 40,
                'potassium_min': 60, 'potassium_max': 100, 'potassium_optimal': 80,
                'soil_types': ['Laterite', 'Forest'],
                'seasons': ['Year-round'],
                'market_demand': 'Medium',
                'profit_margin': 0.30,
                'yield_per_hectare': 2000,
                'growth_period_days': 365
            },
            'Coffee': {
                'ph_min': 6.0, 'ph_max': 7.0, 'ph_optimal': 6.5,
                'rainfall_min': 1500, 'rainfall_max': 2000, 'rainfall_optimal': 1750,
                'temp_min': 18, 'temp_max': 28, 'temp_optimal': 24,
                'nitrogen_min': 80, 'nitrogen_max': 120, 'nitrogen_optimal': 100,
                'phosphorus_min': 40, 'phosphorus_max': 60, 'phosphorus_optimal': 50,
                'potassium_min': 80, 'potassium_max': 120, 'potassium_optimal': 100,
                'soil_types': ['Laterite', 'Forest'],
                'seasons': ['Year-round'],
                'market_demand': 'High',
                'profit_margin': 0.35,
                'yield_per_hectare': 1000,
                'growth_period_days': 365
            },
            'Banana': {
                'ph_min': 5.5, 'ph_max': 7.0, 'ph_optimal': 6.2,
                'rainfall_min': 1200, 'rainfall_max': 1800, 'rainfall_optimal': 1500,
                'temp_min': 20, 'temp_max': 35, 'temp_optimal': 27,
                'nitrogen_min': 100, 'nitrogen_max': 150, 'nitrogen_optimal': 125,
                'phosphorus_min': 40, 'phosphorus_max': 60, 'phosphorus_optimal': 50,
                'potassium_min': 150, 'potassium_max': 200, 'potassium_optimal': 175,
                'soil_types': ['Alluvial', 'Laterite', 'Black'],
                'seasons': ['Year-round'],
                'market_demand': 'High',
                'profit_margin': 0.30,
                'yield_per_hectare': 40000,
                'growth_period_days': 300
            },
            'Ginger': {
                'ph_min': 5.5, 'ph_max': 6.5, 'ph_optimal': 6.0,
                'rainfall_min': 1500, 'rainfall_max': 3000, 'rainfall_optimal': 2000,
                'temp_min': 20, 'temp_max': 30, 'temp_optimal': 25,
                'nitrogen_min': 60, 'nitrogen_max': 100, 'nitrogen_optimal': 80,
                'phosphorus_min': 40, 'phosphorus_max': 60, 'phosphorus_optimal': 50,
                'potassium_min': 80, 'potassium_max': 120, 'potassium_optimal': 100,
                'soil_types': ['Laterite', 'Red'],
                'seasons': ['Kharif', 'Rabi'],
                'market_demand': 'High',
                'profit_margin': 0.40,
                'yield_per_hectare': 15000,
                'growth_period_days': 240
            },
            'Turmeric': {
                'ph_min': 5.0, 'ph_max': 7.5, 'ph_optimal': 6.2,
                'rainfall_min': 1000, 'rainfall_max': 1500, 'rainfall_optimal': 1250,
                'temp_min': 20, 'temp_max': 32, 'temp_optimal': 26,
                'nitrogen_min': 60, 'nitrogen_max': 100, 'nitrogen_optimal': 80,
                'phosphorus_min': 40, 'phosphorus_max': 60, 'phosphorus_optimal': 50,
                'potassium_min': 80, 'potassium_max': 120, 'potassium_optimal': 100,
                'soil_types': ['Laterite', 'Red', 'Alluvial'],
                'seasons': ['Kharif', 'Rabi'],
                'market_demand': 'High',
                'profit_margin': 0.35,
                'yield_per_hectare': 20000,
                'growth_period_days': 270
            }
        }
        
        # Market demand weights (higher = more profitable)
        self.market_demand_weights = {
            'Very High': 1.0,
            'High': 0.8,
            'Medium': 0.6,
            'Low': 0.4
        }
    
    def calculate_suitability_score(self, crop: str, ph: float, nitrogen: float, 
                                  phosphorus: float, potassium: float, 
                                  rainfall: float, temperature: float, 
                                  soil_type: str, season: str) -> float:
        """
        Calculate comprehensive suitability score for a crop
        
        Args:
            crop: Name of the crop
            ph: Soil pH level
            nitrogen: Nitrogen content (kg/ha)
            phosphorus: Phosphorus content (kg/ha)
            potassium: Potassium content (kg/ha)
            rainfall: Annual rainfall (mm)
            temperature: Average temperature (°C)
            soil_type: Type of soil
            season: Planting season
            
        Returns:
            Suitability score (0-1)
        """
        if crop not in self.kerala_crops_data:
            return 0.0
        
        crop_data = self.kerala_crops_data[crop]
        
        # pH suitability (Gaussian distribution around optimal)
        ph_optimal = crop_data['ph_optimal']
        ph_range = crop_data['ph_max'] - crop_data['ph_min']
        ph_score = max(0, 1 - abs(ph - ph_optimal) / (ph_range / 2))
        
        # Temperature suitability
        temp_optimal = crop_data['temp_optimal']
        temp_range = crop_data['temp_max'] - crop_data['temp_min']
        temp_score = max(0, 1 - abs(temperature - temp_optimal) / (temp_range / 2))
        
        # Rainfall suitability
        if crop_data['rainfall_min'] <= rainfall <= crop_data['rainfall_max']:
            rainfall_score = 1.0
        else:
            rainfall_deviation = min(
                abs(rainfall - crop_data['rainfall_min']),
                abs(rainfall - crop_data['rainfall_max'])
            )
            rainfall_score = max(0, 1 - rainfall_deviation / crop_data['rainfall_optimal'])
        
        # Nutrient suitability (weighted average)
        nitrogen_score = self._calculate_nutrient_score(nitrogen, crop_data['nitrogen_min'], 
                                                      crop_data['nitrogen_max'], crop_data['nitrogen_optimal'])
        phosphorus_score = self._calculate_nutrient_score(phosphorus, crop_data['phosphorus_min'], 
                                                        crop_data['phosphorus_max'], crop_data['phosphorus_optimal'])
        potassium_score = self._calculate_nutrient_score(potassium, crop_data['potassium_min'], 
                                                       crop_data['potassium_max'], crop_data['potassium_optimal'])
        
        nutrient_score = (nitrogen_score * 0.4 + phosphorus_score * 0.3 + potassium_score * 0.3)
        
        # Soil type compatibility
        soil_score = 1.0 if soil_type in crop_data['soil_types'] else 0.5
        
        # Season compatibility
        season_score = 1.0 if season in crop_data['seasons'] or 'Year-round' in crop_data['seasons'] else 0.3
        
        # Market demand factor
        market_score = self.market_demand_weights.get(crop_data['market_demand'], 0.5)
        
        # Calculate weighted overall score
        overall_score = (
            ph_score * 0.15 +
            temp_score * 0.15 +
            rainfall_score * 0.20 +
            nutrient_score * 0.25 +
            soil_score * 0.10 +
            season_score * 0.10 +
            market_score * 0.05
        )
        
        return min(1.0, max(0.0, overall_score))
    
    def _calculate_nutrient_score(self, value: float, min_val: float, max_val: float, optimal: float) -> float:
        """Calculate nutrient suitability score"""
        if min_val <= value <= max_val:
            # Within range, calculate proximity to optimal
            range_size = max_val - min_val
            if range_size > 0:
                distance_from_optimal = abs(value - optimal) / range_size
                return max(0, 1 - distance_from_optimal)
            return 1.0
        else:
            # Outside range, penalize heavily
            deviation = min(abs(value - min_val), abs(value - max_val))
            return max(0, 1 - deviation / optimal)
    
    def get_crop_recommendations(self, ph: float, nitrogen: float, phosphorus: float, 
                               potassium: float, rainfall: float, temperature: float, 
                               soil_type: str, season: str, max_recommendations: int = 5) -> List[Dict]:
        """
        Get AI-powered crop recommendations
        
        Args:
            ph: Soil pH level
            nitrogen: Nitrogen content (kg/ha)
            phosphorus: Phosphorus content (kg/ha)
            potassium: Potassium content (kg/ha)
            rainfall: Annual rainfall (mm)
            temperature: Average temperature (°C)
            soil_type: Type of soil
            season: Planting season
            max_recommendations: Maximum number of recommendations
            
        Returns:
            List of crop recommendations with scores and details
        """
        recommendations = []
        
        for crop in self.kerala_crops_data.keys():
            score = self.calculate_suitability_score(
                crop, ph, nitrogen, phosphorus, potassium, 
                rainfall, temperature, soil_type, season
            )
            
            if score > 0.3:  # Only include crops with reasonable suitability
                crop_data = self.kerala_crops_data[crop]
                
                # Calculate additional metrics
                profit_potential = score * crop_data['profit_margin'] * 100
                yield_estimate = score * crop_data['yield_per_hectare']
                
                recommendations.append({
                    'crop': crop,
                    'suitability_score': round(score * 100, 1),
                    'suitability_level': self._get_suitability_level(score),
                    'profit_potential': round(profit_potential, 1),
                    'estimated_yield': round(yield_estimate, 0),
                    'growth_period_days': crop_data['growth_period_days'],
                    'market_demand': crop_data['market_demand'],
                    'profit_margin': crop_data['profit_margin'],
                    'ph_optimal': crop_data['ph_optimal'],
                    'rainfall_optimal': crop_data['rainfall_optimal'],
                    'temp_optimal': crop_data['temp_optimal'],
                    'recommended_season': crop_data['seasons'][0] if crop_data['seasons'] else 'Year-round'
                })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return recommendations[:max_recommendations]
    
    def _get_suitability_level(self, score: float) -> str:
        """Get suitability level based on score"""
        if score >= 0.8:
            return 'Excellent'
        elif score >= 0.6:
            return 'Good'
        elif score >= 0.4:
            return 'Fair'
        else:
            return 'Poor'
    
    def get_crop_details(self, crop: str) -> Optional[Dict]:
        """
        Get detailed information about a specific crop
        
        Args:
            crop: Name of the crop
            
        Returns:
            Dictionary with crop details or None if not found
        """
        return self.kerala_crops_data.get(crop)
    
    def get_seasonal_recommendations(self, season: str, max_recommendations: int = 5) -> List[Dict]:
        """
        Get crops suitable for a specific season
        
        Args:
            season: Planting season
            max_recommendations: Maximum number of recommendations
            
        Returns:
            List of seasonal crop recommendations
        """
        seasonal_crops = []
        
        for crop, data in self.kerala_crops_data.items():
            if season in data['seasons'] or 'Year-round' in data['seasons']:
                seasonal_crops.append({
                    'crop': crop,
                    'market_demand': data['market_demand'],
                    'profit_margin': data['profit_margin'],
                    'growth_period_days': data['growth_period_days'],
                    'yield_per_hectare': data['yield_per_hectare']
                })
        
        # Sort by market demand and profit margin
        seasonal_crops.sort(key=lambda x: (self.market_demand_weights.get(x['market_demand'], 0.5), x['profit_margin']), reverse=True)
        
        return seasonal_crops[:max_recommendations]
    
    def save_model(self, filepath: str):
        """Save the trained model to file"""
        if self.is_trained:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'label_encoders': self.label_encoders
            }, filepath)
            logger.info(f"Model saved to {filepath}")
        else:
            logger.warning("No trained model to save")
    
    def load_model(self, filepath: str):
        """Load a trained model from file"""
        try:
            data = joblib.load(filepath)
            self.model = data['model']
            self.scaler = data['scaler']
            self.label_encoders = data['label_encoders']
            self.is_trained = True
            logger.info(f"Model loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize recommender
    recommender = SmartCropRecommender()
    
    # Example recommendation
    recommendations = recommender.get_crop_recommendations(
        ph=6.0,
        nitrogen=80,
        phosphorus=45,
        potassium=70,
        rainfall=1500,
        temperature=26,
        soil_type='Laterite',
        season='Kharif'
    )
    
    print("AI Crop Recommendations:")
    print("=" * 50)
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['crop']}")
        print(f"   Suitability: {rec['suitability_score']}% ({rec['suitability_level']})")
        print(f"   Profit Potential: {rec['profit_potential']}%")
        print(f"   Estimated Yield: {rec['estimated_yield']} kg/hectare")
        print(f"   Growth Period: {rec['growth_period_days']} days")
        print(f"   Market Demand: {rec['market_demand']}")
        print()
