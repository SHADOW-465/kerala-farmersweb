"""
Soil Health Assessment Tool
AI-powered soil analysis and recommendations for farmers
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SoilTestResult:
    """Soil test result structure"""
    test_id: str
    farm_id: str
    test_date: datetime
    ph_level: float
    nitrogen: float  # kg/ha
    phosphorus: float  # kg/ha
    potassium: float  # kg/ha
    organic_matter: float  # %
    carbon_content: float  # %
    bulk_density: float  # g/cm³
    water_holding_capacity: float  # %
    cation_exchange_capacity: float  # meq/100g
    micronutrients: Dict[str, float]  # mg/kg
    soil_texture: str  # clay, loam, sand, etc.
    soil_color: str
    drainage: str  # good, moderate, poor
    erosion_level: str  # low, moderate, high
    lab_name: str
    created_at: datetime

@dataclass
class SoilHealthScore:
    """Soil health score structure"""
    overall_score: float  # 0-100
    ph_score: float
    nutrient_score: float
    organic_matter_score: float
    physical_score: float
    biological_score: float
    health_level: str  # excellent, good, fair, poor
    recommendations: List[str]
    priority_actions: List[str]

class SoilHealthAssessment:
    """
    AI-powered soil health assessment tool
    """
    
    def __init__(self):
        """Initialize soil health assessment tool"""
        self.soil_health_standards = self._load_soil_health_standards()
        self.crop_requirements = self._load_crop_requirements()
        self.micronutrient_standards = self._load_micronutrient_standards()
        self.models = {}
        self.scalers = {}
        self.init_models()
    
    def _load_soil_health_standards(self) -> Dict[str, Dict[str, Tuple[float, float]]]:
        """Load soil health standards for different soil types"""
        return {
            'clay': {
                'ph': (6.0, 7.5),
                'nitrogen': (100, 200),
                'phosphorus': (40, 80),
                'potassium': (100, 200),
                'organic_matter': (3.0, 6.0),
                'carbon_content': (1.5, 3.0),
                'bulk_density': (1.0, 1.3),
                'water_holding_capacity': (40, 60),
                'cec': (15, 40)
            },
            'loam': {
                'ph': (6.0, 7.0),
                'nitrogen': (80, 150),
                'phosphorus': (30, 60),
                'potassium': (80, 150),
                'organic_matter': (2.5, 5.0),
                'carbon_content': (1.2, 2.5),
                'bulk_density': (1.2, 1.5),
                'water_holding_capacity': (30, 50),
                'cec': (10, 25)
            },
            'sandy': {
                'ph': (5.5, 7.0),
                'nitrogen': (60, 120),
                'phosphorus': (20, 50),
                'potassium': (60, 120),
                'organic_matter': (1.5, 4.0),
                'carbon_content': (0.8, 2.0),
                'bulk_density': (1.4, 1.7),
                'water_holding_capacity': (20, 40),
                'cec': (5, 15)
            },
            'laterite': {
                'ph': (5.0, 6.5),
                'nitrogen': (70, 130),
                'phosphorus': (25, 55),
                'potassium': (70, 130),
                'organic_matter': (2.0, 4.5),
                'carbon_content': (1.0, 2.2),
                'bulk_density': (1.1, 1.4),
                'water_holding_capacity': (25, 45),
                'cec': (8, 20)
            }
        }
    
    def _load_crop_requirements(self) -> Dict[str, Dict[str, Any]]:
        """Load crop-specific soil requirements"""
        return {
            'Rice': {
                'ph': (5.0, 6.5),
                'nitrogen': (100, 150),
                'phosphorus': (40, 60),
                'potassium': (60, 100),
                'organic_matter': (2.0, 4.0),
                'drainage': 'moderate',
                'soil_texture': ['clay', 'loam']
            },
            'Coconut': {
                'ph': (5.2, 8.0),
                'nitrogen': (100, 150),
                'phosphorus': (50, 80),
                'potassium': (100, 200),
                'organic_matter': (2.5, 5.0),
                'drainage': 'good',
                'soil_texture': ['loam', 'sandy', 'laterite']
            },
            'Pepper': {
                'ph': (5.5, 7.0),
                'nitrogen': (60, 100),
                'phosphorus': (30, 50),
                'potassium': (80, 120),
                'organic_matter': (3.0, 5.0),
                'drainage': 'good',
                'soil_texture': ['loam', 'laterite']
            },
            'Cardamom': {
                'ph': (5.0, 6.5),
                'nitrogen': (100, 150),
                'phosphorus': (50, 80),
                'potassium': (100, 150),
                'organic_matter': (3.0, 6.0),
                'drainage': 'good',
                'soil_texture': ['loam', 'clay']
            },
            'Rubber': {
                'ph': (5.0, 6.5),
                'nitrogen': (80, 120),
                'phosphorus': (40, 60),
                'potassium': (60, 100),
                'organic_matter': (2.5, 4.5),
                'drainage': 'good',
                'soil_texture': ['loam', 'laterite']
            },
            'Banana': {
                'ph': (5.5, 7.0),
                'nitrogen': (100, 150),
                'phosphorus': (40, 60),
                'potassium': (150, 200),
                'organic_matter': (2.0, 4.0),
                'drainage': 'good',
                'soil_texture': ['loam', 'clay']
            },
            'Ginger': {
                'ph': (5.5, 6.5),
                'nitrogen': (60, 100),
                'phosphorus': (40, 60),
                'potassium': (80, 120),
                'organic_matter': (2.5, 4.5),
                'drainage': 'good',
                'soil_texture': ['loam', 'laterite']
            },
            'Turmeric': {
                'ph': (5.0, 7.5),
                'nitrogen': (60, 100),
                'phosphorus': (40, 60),
                'potassium': (80, 120),
                'organic_matter': (2.0, 4.0),
                'drainage': 'good',
                'soil_texture': ['loam', 'laterite']
            }
        }
    
    def _load_micronutrient_standards(self) -> Dict[str, Tuple[float, float]]:
        """Load micronutrient standards (mg/kg)"""
        return {
            'zinc': (1.0, 5.0),
            'iron': (10.0, 50.0),
            'manganese': (5.0, 25.0),
            'copper': (0.5, 3.0),
            'boron': (0.5, 2.0),
            'molybdenum': (0.1, 1.0),
            'sulfur': (10.0, 30.0)
        }
    
    def init_models(self):
        """Initialize ML models for soil health prediction"""
        try:
            # Generate synthetic training data
            training_data = self._generate_training_data()
            
            # Train soil health classification model
            self._train_soil_health_model(training_data)
            
            logger.info("Soil health models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
    
    def _generate_training_data(self) -> pd.DataFrame:
        """Generate synthetic training data for model training"""
        np.random.seed(42)
        n_samples = 1000
        
        data = []
        for _ in range(n_samples):
            # Generate random soil parameters
            ph = np.random.uniform(4.0, 8.5)
            nitrogen = np.random.uniform(20, 300)
            phosphorus = np.random.uniform(10, 100)
            potassium = np.random.uniform(20, 250)
            organic_matter = np.random.uniform(0.5, 8.0)
            carbon_content = organic_matter * 0.5
            bulk_density = np.random.uniform(0.8, 1.8)
            water_holding_capacity = np.random.uniform(15, 70)
            cec = np.random.uniform(3, 50)
            
            # Generate soil texture
            soil_texture = np.random.choice(['clay', 'loam', 'sandy', 'laterite'])
            
            # Calculate soil health score
            health_score = self._calculate_health_score(
                ph, nitrogen, phosphorus, potassium, organic_matter,
                carbon_content, bulk_density, water_holding_capacity, cec, soil_texture
            )
            
            # Classify health level
            if health_score >= 80:
                health_level = 'excellent'
            elif health_score >= 60:
                health_level = 'good'
            elif health_score >= 40:
                health_level = 'fair'
            else:
                health_level = 'poor'
            
            data.append({
                'ph': ph,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'organic_matter': organic_matter,
                'carbon_content': carbon_content,
                'bulk_density': bulk_density,
                'water_holding_capacity': water_holding_capacity,
                'cec': cec,
                'soil_texture': soil_texture,
                'health_score': health_score,
                'health_level': health_level
            })
        
        return pd.DataFrame(data)
    
    def _train_soil_health_model(self, data: pd.DataFrame):
        """Train soil health classification model"""
        try:
            # Prepare features
            feature_columns = ['ph', 'nitrogen', 'phosphorus', 'potassium', 'organic_matter',
                             'carbon_content', 'bulk_density', 'water_holding_capacity', 'cec']
            
            X = data[feature_columns]
            y = data['health_level']
            
            # Encode target variable
            le = LabelEncoder()
            y_encoded = le.fit_transform(y)
            self.label_encoders['health_level'] = le
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train models
            models = {
                'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
                'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
            }
            
            best_model = None
            best_score = 0
            best_model_name = None
            
            for name, model in models.items():
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                score = accuracy_score(y_test, y_pred)
                
                if score > best_score:
                    best_score = score
                    best_model = model
                    best_model_name = name
            
            self.models['soil_health'] = best_model
            self.scalers['soil_health'] = scaler
            
            logger.info(f"Trained {best_model_name} model with accuracy: {best_score:.3f}")
            
        except Exception as e:
            logger.error(f"Error training soil health model: {str(e)}")
    
    def assess_soil_health(self, soil_test: SoilTestResult) -> SoilHealthScore:
        """
        Assess soil health based on test results
        
        Args:
            soil_test: SoilTestResult object
            
        Returns:
            SoilHealthScore object
        """
        try:
            # Calculate individual component scores
            ph_score = self._calculate_ph_score(soil_test.ph_level, soil_test.soil_texture)
            nutrient_score = self._calculate_nutrient_score(soil_test, soil_test.soil_texture)
            organic_matter_score = self._calculate_organic_matter_score(soil_test.organic_matter, soil_test.soil_texture)
            physical_score = self._calculate_physical_score(soil_test, soil_test.soil_texture)
            biological_score = self._calculate_biological_score(soil_test)
            
            # Calculate overall score
            overall_score = (ph_score * 0.2 + nutrient_score * 0.3 + 
                           organic_matter_score * 0.2 + physical_score * 0.2 + biological_score * 0.1)
            
            # Determine health level
            if overall_score >= 80:
                health_level = 'excellent'
            elif overall_score >= 60:
                health_level = 'good'
            elif overall_score >= 40:
                health_level = 'fair'
            else:
                health_level = 'poor'
            
            # Generate recommendations
            recommendations = self._generate_recommendations(soil_test, {
                'ph_score': ph_score,
                'nutrient_score': nutrient_score,
                'organic_matter_score': organic_matter_score,
                'physical_score': physical_score,
                'biological_score': biological_score
            })
            
            # Generate priority actions
            priority_actions = self._generate_priority_actions(soil_test, overall_score)
            
            return SoilHealthScore(
                overall_score=round(overall_score, 1),
                ph_score=round(ph_score, 1),
                nutrient_score=round(nutrient_score, 1),
                organic_matter_score=round(organic_matter_score, 1),
                physical_score=round(physical_score, 1),
                biological_score=round(biological_score, 1),
                health_level=health_level,
                recommendations=recommendations,
                priority_actions=priority_actions
            )
            
        except Exception as e:
            logger.error(f"Error assessing soil health: {str(e)}")
            raise
    
    def _calculate_ph_score(self, ph: float, soil_texture: str) -> float:
        """Calculate pH score (0-100)"""
        if soil_texture not in self.soil_health_standards:
            soil_texture = 'loam'  # Default
        
        ph_min, ph_max = self.soil_health_standards[soil_texture]['ph']
        ph_optimal = (ph_min + ph_max) / 2
        
        if ph_min <= ph <= ph_max:
            # Within optimal range
            distance_from_optimal = abs(ph - ph_optimal)
            max_distance = (ph_max - ph_min) / 2
            score = 100 * (1 - distance_from_optimal / max_distance)
        else:
            # Outside optimal range
            if ph < ph_min:
                distance = ph_min - ph
            else:
                distance = ph - ph_max
            
            # Penalty for being outside range
            score = max(0, 50 - distance * 10)
        
        return max(0, min(100, score))
    
    def _calculate_nutrient_score(self, soil_test: SoilTestResult, soil_texture: str) -> float:
        """Calculate nutrient score (0-100)"""
        if soil_texture not in self.soil_health_standards:
            soil_texture = 'loam'
        
        standards = self.soil_health_standards[soil_texture]
        
        # Calculate scores for each nutrient
        n_score = self._calculate_nutrient_component_score(
            soil_test.nitrogen, standards['nitrogen']
        )
        p_score = self._calculate_nutrient_component_score(
            soil_test.phosphorus, standards['phosphorus']
        )
        k_score = self._calculate_nutrient_component_score(
            soil_test.potassium, standards['potassium']
        )
        
        # Weighted average
        return (n_score * 0.4 + p_score * 0.3 + k_score * 0.3)
    
    def _calculate_nutrient_component_score(self, value: float, range_tuple: Tuple[float, float]) -> float:
        """Calculate score for a single nutrient component"""
        min_val, max_val = range_tuple
        optimal = (min_val + max_val) / 2
        
        if min_val <= value <= max_val:
            # Within optimal range
            distance_from_optimal = abs(value - optimal)
            max_distance = (max_val - min_val) / 2
            score = 100 * (1 - distance_from_optimal / max_distance)
        else:
            # Outside optimal range
            if value < min_val:
                distance = min_val - value
                penalty = distance / optimal * 50
            else:
                distance = value - max_val
                penalty = distance / optimal * 30  # Less penalty for excess
            
            score = max(0, 100 - penalty)
        
        return max(0, min(100, score))
    
    def _calculate_organic_matter_score(self, organic_matter: float, soil_texture: str) -> float:
        """Calculate organic matter score (0-100)"""
        if soil_texture not in self.soil_health_standards:
            soil_texture = 'loam'
        
        om_min, om_max = self.soil_health_standards[soil_texture]['organic_matter']
        
        if om_min <= organic_matter <= om_max:
            # Within optimal range
            score = 100
        elif organic_matter < om_min:
            # Below optimal
            deficiency = om_min - organic_matter
            score = max(0, 100 - deficiency * 20)
        else:
            # Above optimal (still good, but diminishing returns)
            excess = organic_matter - om_max
            score = max(60, 100 - excess * 5)
        
        return max(0, min(100, score))
    
    def _calculate_physical_score(self, soil_test: SoilTestResult, soil_texture: str) -> float:
        """Calculate physical properties score (0-100)"""
        if soil_texture not in self.soil_health_standards:
            soil_texture = 'loam'
        
        standards = self.soil_health_standards[soil_texture]
        
        # Bulk density score
        bd_min, bd_max = standards['bulk_density']
        if bd_min <= soil_test.bulk_density <= bd_max:
            bd_score = 100
        else:
            if soil_test.bulk_density < bd_min:
                bd_score = 80  # Too loose
            else:
                bd_score = max(0, 100 - (soil_test.bulk_density - bd_max) * 50)
        
        # Water holding capacity score
        whc_min, whc_max = standards['water_holding_capacity']
        if whc_min <= soil_test.water_holding_capacity <= whc_max:
            whc_score = 100
        else:
            if soil_test.water_holding_capacity < whc_min:
                whc_score = max(0, 100 - (whc_min - soil_test.water_holding_capacity) * 2)
            else:
                whc_score = 90  # High water holding capacity is generally good
        
        # CEC score
        cec_min, cec_max = standards['cec']
        if cec_min <= soil_test.cation_exchange_capacity <= cec_max:
            cec_score = 100
        else:
            if soil_test.cation_exchange_capacity < cec_min:
                cec_score = max(0, 100 - (cec_min - soil_test.cation_exchange_capacity) * 2)
            else:
                cec_score = 90  # High CEC is generally good
        
        return (bd_score * 0.4 + whc_score * 0.3 + cec_score * 0.3)
    
    def _calculate_biological_score(self, soil_test: SoilTestResult) -> float:
        """Calculate biological activity score (0-100)"""
        # This is a simplified calculation based on organic matter and carbon content
        # In practice, you would use actual biological indicators
        
        om_score = min(100, soil_test.organic_matter * 20)  # 5% OM = 100 points
        carbon_score = min(100, soil_test.carbon_content * 40)  # 2.5% C = 100 points
        
        # Micronutrient availability (simplified)
        micronutrient_score = 50  # Default
        if soil_test.micronutrients:
            micronutrient_scores = []
            for nutrient, value in soil_test.micronutrients.items():
                if nutrient in self.micronutrient_standards:
                    min_val, max_val = self.micronutrient_standards[nutrient]
                    if min_val <= value <= max_val:
                        micronutrient_scores.append(100)
                    else:
                        micronutrient_scores.append(50)
            
            if micronutrient_scores:
                micronutrient_score = np.mean(micronutrient_scores)
        
        return (om_score * 0.4 + carbon_score * 0.4 + micronutrient_score * 0.2)
    
    def _calculate_health_score(self, ph: float, nitrogen: float, phosphorus: float, 
                              potassium: float, organic_matter: float, carbon_content: float,
                              bulk_density: float, water_holding_capacity: float, cec: float,
                              soil_texture: str) -> float:
        """Calculate overall soil health score for training data"""
        # Create a mock SoilTestResult for calculation
        mock_soil_test = SoilTestResult(
            test_id="mock",
            farm_id="mock",
            test_date=datetime.now(),
            ph_level=ph,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            organic_matter=organic_matter,
            carbon_content=carbon_content,
            bulk_density=bulk_density,
            water_holding_capacity=water_holding_capacity,
            cation_exchange_capacity=cec,
            micronutrients={},
            soil_texture=soil_texture,
            soil_color="brown",
            drainage="good",
            erosion_level="low",
            lab_name="mock",
            created_at=datetime.now()
        )
        
        ph_score = self._calculate_ph_score(ph, soil_texture)
        nutrient_score = self._calculate_nutrient_score(mock_soil_test, soil_texture)
        organic_matter_score = self._calculate_organic_matter_score(organic_matter, soil_texture)
        physical_score = self._calculate_physical_score(mock_soil_test, soil_texture)
        biological_score = self._calculate_biological_score(mock_soil_test)
        
        return (ph_score * 0.2 + nutrient_score * 0.3 + organic_matter_score * 0.2 + 
                physical_score * 0.2 + biological_score * 0.1)
    
    def _generate_recommendations(self, soil_test: SoilTestResult, scores: Dict[str, float]) -> List[str]:
        """Generate soil improvement recommendations"""
        recommendations = []
        
        # pH recommendations
        if scores['ph_score'] < 60:
            if soil_test.ph_level < 6.0:
                recommendations.append("Add lime to increase soil pH to optimal range (6.0-7.0)")
            elif soil_test.ph_level > 7.5:
                recommendations.append("Add sulfur or organic matter to decrease soil pH")
        
        # Nutrient recommendations
        if scores['nutrient_score'] < 60:
            if soil_test.nitrogen < 80:
                recommendations.append("Apply nitrogen-rich fertilizers or organic manure")
            if soil_test.phosphorus < 30:
                recommendations.append("Add phosphorus-rich fertilizers or rock phosphate")
            if soil_test.potassium < 60:
                recommendations.append("Apply potassium-rich fertilizers or wood ash")
        
        # Organic matter recommendations
        if scores['organic_matter_score'] < 60:
            recommendations.append("Add compost, manure, or green manure to increase organic matter content")
            recommendations.append("Practice crop rotation with leguminous crops")
        
        # Physical property recommendations
        if scores['physical_score'] < 60:
            if soil_test.bulk_density > 1.5:
                recommendations.append("Improve soil structure by adding organic matter and reducing compaction")
            if soil_test.water_holding_capacity < 30:
                recommendations.append("Add organic matter to improve water holding capacity")
        
        # General recommendations
        recommendations.append("Practice conservation tillage to maintain soil structure")
        recommendations.append("Use cover crops to protect soil from erosion")
        recommendations.append("Implement crop rotation to maintain soil fertility")
        
        return recommendations
    
    def _generate_priority_actions(self, soil_test: SoilTestResult, overall_score: float) -> List[str]:
        """Generate priority actions based on soil health score"""
        actions = []
        
        if overall_score < 40:
            actions.append("URGENT: Immediate soil improvement required")
            actions.append("Test soil annually and monitor progress")
            actions.append("Consider consulting with soil specialist")
        elif overall_score < 60:
            actions.append("HIGH: Focus on major soil health issues")
            actions.append("Implement recommended soil amendments")
            actions.append("Monitor soil health every 6 months")
        elif overall_score < 80:
            actions.append("MEDIUM: Maintain current practices with minor improvements")
            actions.append("Continue regular soil testing")
        else:
            actions.append("LOW: Maintain excellent soil health practices")
            actions.append("Continue current management practices")
        
        return actions
    
    def get_crop_suitability(self, soil_test: SoilTestResult, crop_name: str) -> Dict[str, Any]:
        """
        Assess crop suitability for specific soil conditions
        
        Args:
            soil_test: SoilTestResult object
            crop_name: Name of the crop
            
        Returns:
            Dictionary with crop suitability analysis
        """
        if crop_name not in self.crop_requirements:
            return {'error': f'No requirements available for {crop_name}'}
        
        requirements = self.crop_requirements[crop_name]
        suitability_score = 0
        total_factors = 0
        issues = []
        recommendations = []
        
        # Check pH suitability
        crop_ph_min, crop_ph_max = requirements['ph']
        if crop_ph_min <= soil_test.ph_level <= crop_ph_max:
            suitability_score += 100
            total_factors += 1
        else:
            if soil_test.ph_level < crop_ph_min:
                issues.append(f"pH too low ({soil_test.ph_level:.1f}), needs to be {crop_ph_min}-{crop_ph_max}")
                recommendations.append("Add lime to increase pH")
            else:
                issues.append(f"pH too high ({soil_test.ph_level:.1f}), needs to be {crop_ph_min}-{crop_ph_max}")
                recommendations.append("Add sulfur to decrease pH")
            total_factors += 1
        
        # Check nutrient suitability
        crop_n_min, crop_n_max = requirements['nitrogen']
        if crop_n_min <= soil_test.nitrogen <= crop_n_max:
            suitability_score += 100
        else:
            if soil_test.nitrogen < crop_n_min:
                issues.append(f"Insufficient nitrogen ({soil_test.nitrogen:.1f} kg/ha)")
                recommendations.append("Apply nitrogen-rich fertilizers")
            else:
                issues.append(f"Excessive nitrogen ({soil_test.nitrogen:.1f} kg/ha)")
            total_factors += 1
        
        crop_p_min, crop_p_max = requirements['phosphorus']
        if crop_p_min <= soil_test.phosphorus <= crop_p_max:
            suitability_score += 100
        else:
            if soil_test.phosphorus < crop_p_min:
                issues.append(f"Insufficient phosphorus ({soil_test.phosphorus:.1f} kg/ha)")
                recommendations.append("Apply phosphorus-rich fertilizers")
            else:
                issues.append(f"Excessive phosphorus ({soil_test.phosphorus:.1f} kg/ha)")
            total_factors += 1
        
        crop_k_min, crop_k_max = requirements['potassium']
        if crop_k_min <= soil_test.potassium <= crop_k_max:
            suitability_score += 100
        else:
            if soil_test.potassium < crop_k_min:
                issues.append(f"Insufficient potassium ({soil_test.potassium:.1f} kg/ha)")
                recommendations.append("Apply potassium-rich fertilizers")
            else:
                issues.append(f"Excessive potassium ({soil_test.potassium:.1f} kg/ha)")
            total_factors += 1
        
        # Check soil texture suitability
        if soil_test.soil_texture in requirements['soil_texture']:
            suitability_score += 100
            total_factors += 1
        else:
            issues.append(f"Soil texture ({soil_test.soil_texture}) not ideal for {crop_name}")
            recommendations.append(f"Consider soil amendment or choose different crop")
            total_factors += 1
        
        # Calculate overall suitability
        if total_factors > 0:
            overall_suitability = suitability_score / total_factors
        else:
            overall_suitability = 0
        
        # Determine suitability level
        if overall_suitability >= 80:
            suitability_level = 'excellent'
        elif overall_suitability >= 60:
            suitability_level = 'good'
        elif overall_suitability >= 40:
            suitability_level = 'fair'
        else:
            suitability_level = 'poor'
        
        return {
            'crop_name': crop_name,
            'suitability_score': round(overall_suitability, 1),
            'suitability_level': suitability_level,
            'issues': issues,
            'recommendations': recommendations,
            'soil_requirements': requirements
        }
    
    def save_models(self, filepath: str):
        """Save trained models to file"""
        try:
            model_data = {
                'models': self.models,
                'scalers': self.scalers,
                'label_encoders': self.label_encoders
            }
            joblib.dump(model_data, filepath)
            logger.info(f"Soil health models saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving models: {str(e)}")
    
    def load_models(self, filepath: str):
        """Load trained models from file"""
        try:
            model_data = joblib.load(filepath)
            self.models = model_data['models']
            self.scalers = model_data['scalers']
            self.label_encoders = model_data['label_encoders']
            logger.info(f"Soil health models loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize soil health assessment tool
    soil_assessor = SoilHealthAssessment()
    
    # Create sample soil test result
    sample_soil_test = SoilTestResult(
        test_id="test_001",
        farm_id="farm_001",
        test_date=datetime.now(),
        ph_level=6.2,
        nitrogen=120,
        phosphorus=45,
        potassium=85,
        organic_matter=3.5,
        carbon_content=1.8,
        bulk_density=1.3,
        water_holding_capacity=45,
        cation_exchange_capacity=18,
        micronutrients={
            'zinc': 2.5,
            'iron': 25.0,
            'manganese': 15.0,
            'copper': 1.2,
            'boron': 1.0
        },
        soil_texture='loam',
        soil_color='brown',
        drainage='good',
        erosion_level='low',
        lab_name='Kerala Soil Testing Lab',
        created_at=datetime.now()
    )
    
    # Assess soil health
    print("Soil Health Assessment - Test Results")
    print("=" * 50)
    
    health_score = soil_assessor.assess_soil_health(sample_soil_test)
    
    print(f"Overall Soil Health Score: {health_score.overall_score}/100")
    print(f"Health Level: {health_score.health_level.upper()}")
    print(f"\nComponent Scores:")
    print(f"  pH Score: {health_score.ph_score}/100")
    print(f"  Nutrient Score: {health_score.nutrient_score}/100")
    print(f"  Organic Matter Score: {health_score.organic_matter_score}/100")
    print(f"  Physical Score: {health_score.physical_score}/100")
    print(f"  Biological Score: {health_score.biological_score}/100")
    
    print(f"\nRecommendations:")
    for rec in health_score.recommendations:
        print(f"  - {rec}")
    
    print(f"\nPriority Actions:")
    for action in health_score.priority_actions:
        print(f"  - {action}")
    
    # Test crop suitability
    print(f"\n" + "=" * 50)
    print("Crop Suitability Analysis:")
    
    crops = ['Rice', 'Coconut', 'Pepper', 'Cardamom']
    for crop in crops:
        suitability = soil_assessor.get_crop_suitability(sample_soil_test, crop)
        print(f"\n{crop}:")
        print(f"  Suitability: {suitability['suitability_score']}/100 ({suitability['suitability_level']})")
        if suitability['issues']:
            print(f"  Issues: {', '.join(suitability['issues'])}")
        if suitability['recommendations']:
            print(f"  Recommendations: {', '.join(suitability['recommendations'])}")
