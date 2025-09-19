"""
Personal Farm Profile and Analytics Module
Manages farm data, tracks performance, and provides personalized insights
"""

import json
import sqlite3
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging
import pandas as pd
import numpy as np
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FarmProfile:
    """Farm profile data structure"""
    farm_id: str
    farmer_name: str
    farm_name: str
    location: Dict[str, str]  # state, district, village
    total_area: float  # in hectares
    soil_type: str
    soil_ph: float
    soil_nutrients: Dict[str, float]  # N, P, K levels
    irrigation_type: str
    farming_type: str  # organic, conventional, mixed
    established_year: int
    contact_info: Dict[str, str]
    created_at: datetime
    updated_at: datetime

@dataclass
class CropRecord:
    """Crop planting and harvest record"""
    record_id: str
    farm_id: str
    crop_name: str
    variety: str
    planting_date: datetime
    harvest_date: Optional[datetime]
    area_planted: float  # in hectares
    expected_yield: float  # in kg/hectare
    actual_yield: Optional[float]  # in kg/hectare
    input_costs: Dict[str, float]  # seeds, fertilizers, pesticides, labor
    selling_price: Optional[float]  # per kg
    total_revenue: Optional[float]
    profit_loss: Optional[float]
    notes: str
    created_at: datetime

@dataclass
class SoilTestRecord:
    """Soil test record"""
    test_id: str
    farm_id: str
    test_date: datetime
    ph_level: float
    nitrogen: float
    phosphorus: float
    potassium: float
    organic_matter: float
    micronutrients: Dict[str, float]
    recommendations: List[str]
    lab_name: str
    created_at: datetime

class FarmProfileManager:
    """
    Manages farm profiles and analytics
    """
    
    def __init__(self, db_path: str = "farm_data.db"):
        """
        Initialize farm profile manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Farm profiles table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS farm_profiles (
                        farm_id TEXT PRIMARY KEY,
                        farmer_name TEXT NOT NULL,
                        farm_name TEXT NOT NULL,
                        state TEXT NOT NULL,
                        district TEXT NOT NULL,
                        village TEXT NOT NULL,
                        total_area REAL NOT NULL,
                        soil_type TEXT NOT NULL,
                        soil_ph REAL NOT NULL,
                        soil_nitrogen REAL NOT NULL,
                        soil_phosphorus REAL NOT NULL,
                        soil_potassium REAL NOT NULL,
                        irrigation_type TEXT NOT NULL,
                        farming_type TEXT NOT NULL,
                        established_year INTEGER NOT NULL,
                        phone TEXT,
                        email TEXT,
                        address TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Crop records table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS crop_records (
                        record_id TEXT PRIMARY KEY,
                        farm_id TEXT NOT NULL,
                        crop_name TEXT NOT NULL,
                        variety TEXT,
                        planting_date TIMESTAMP NOT NULL,
                        harvest_date TIMESTAMP,
                        area_planted REAL NOT NULL,
                        expected_yield REAL NOT NULL,
                        actual_yield REAL,
                        seed_cost REAL DEFAULT 0,
                        fertilizer_cost REAL DEFAULT 0,
                        pesticide_cost REAL DEFAULT 0,
                        labor_cost REAL DEFAULT 0,
                        other_costs REAL DEFAULT 0,
                        selling_price REAL,
                        total_revenue REAL,
                        profit_loss REAL,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (farm_id) REFERENCES farm_profiles (farm_id)
                    )
                ''')
                
                # Soil test records table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS soil_test_records (
                        test_id TEXT PRIMARY KEY,
                        farm_id TEXT NOT NULL,
                        test_date TIMESTAMP NOT NULL,
                        ph_level REAL NOT NULL,
                        nitrogen REAL NOT NULL,
                        phosphorus REAL NOT NULL,
                        potassium REAL NOT NULL,
                        organic_matter REAL NOT NULL,
                        micronutrients TEXT,
                        recommendations TEXT,
                        lab_name TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (farm_id) REFERENCES farm_profiles (farm_id)
                    )
                ''')
                
                # Weather records table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS weather_records (
                        record_id TEXT PRIMARY KEY,
                        farm_id TEXT NOT NULL,
                        date TIMESTAMP NOT NULL,
                        temperature REAL NOT NULL,
                        humidity REAL NOT NULL,
                        rainfall REAL NOT NULL,
                        wind_speed REAL NOT NULL,
                        pressure REAL NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (farm_id) REFERENCES farm_profiles (farm_id)
                    )
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def create_farm_profile(self, profile_data: Dict[str, Any]) -> str:
        """
        Create a new farm profile
        
        Args:
            profile_data: Dictionary containing farm profile data
            
        Returns:
            Farm ID of the created profile
        """
        try:
            farm_id = f"farm_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{profile_data.get('farmer_name', 'unknown').replace(' ', '_')}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO farm_profiles (
                        farm_id, farmer_name, farm_name, state, district, village,
                        total_area, soil_type, soil_ph, soil_nitrogen, soil_phosphorus, soil_potassium,
                        irrigation_type, farming_type, established_year, phone, email, address
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    farm_id,
                    profile_data['farmer_name'],
                    profile_data['farm_name'],
                    profile_data['location']['state'],
                    profile_data['location']['district'],
                    profile_data['location']['village'],
                    profile_data['total_area'],
                    profile_data['soil_type'],
                    profile_data['soil_ph'],
                    profile_data['soil_nutrients']['nitrogen'],
                    profile_data['soil_nutrients']['phosphorus'],
                    profile_data['soil_nutrients']['potassium'],
                    profile_data['irrigation_type'],
                    profile_data['farming_type'],
                    profile_data['established_year'],
                    profile_data.get('contact_info', {}).get('phone', ''),
                    profile_data.get('contact_info', {}).get('email', ''),
                    profile_data.get('contact_info', {}).get('address', '')
                ))
                
                conn.commit()
                logger.info(f"Farm profile created: {farm_id}")
                return farm_id
                
        except Exception as e:
            logger.error(f"Error creating farm profile: {str(e)}")
            raise
    
    def get_farm_profile(self, farm_id: str) -> Optional[FarmProfile]:
        """
        Get farm profile by ID
        
        Args:
            farm_id: Farm ID
            
        Returns:
            FarmProfile object or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM farm_profiles WHERE farm_id = ?
                ''', (farm_id,))
                
                row = cursor.fetchone()
                if row:
                    return FarmProfile(
                        farm_id=row[0],
                        farmer_name=row[1],
                        farm_name=row[2],
                        location={
                            'state': row[3],
                            'district': row[4],
                            'village': row[5]
                        },
                        total_area=row[6],
                        soil_type=row[7],
                        soil_ph=row[8],
                        soil_nutrients={
                            'nitrogen': row[9],
                            'phosphorus': row[10],
                            'potassium': row[11]
                        },
                        irrigation_type=row[12],
                        farming_type=row[13],
                        established_year=row[14],
                        contact_info={
                            'phone': row[15] or '',
                            'email': row[16] or '',
                            'address': row[17] or ''
                        },
                        created_at=datetime.fromisoformat(row[18]),
                        updated_at=datetime.fromisoformat(row[19])
                    )
                return None
                
        except Exception as e:
            logger.error(f"Error getting farm profile: {str(e)}")
            return None
    
    def update_farm_profile(self, farm_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update farm profile
        
        Args:
            farm_id: Farm ID
            update_data: Dictionary containing updated data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build update query dynamically
                update_fields = []
                values = []
                
                for key, value in update_data.items():
                    if key == 'location':
                        for loc_key, loc_value in value.items():
                            update_fields.append(f"{loc_key} = ?")
                            values.append(loc_value)
                    elif key == 'soil_nutrients':
                        for nut_key, nut_value in value.items():
                            update_fields.append(f"soil_{nut_key} = ?")
                            values.append(nut_value)
                    elif key == 'contact_info':
                        for contact_key, contact_value in value.items():
                            update_fields.append(f"{contact_key} = ?")
                            values.append(contact_value)
                    else:
                        update_fields.append(f"{key} = ?")
                        values.append(value)
                
                if update_fields:
                    update_fields.append("updated_at = CURRENT_TIMESTAMP")
                    values.append(farm_id)
                    
                    query = f"UPDATE farm_profiles SET {', '.join(update_fields)} WHERE farm_id = ?"
                    cursor.execute(query, values)
                    conn.commit()
                    
                    logger.info(f"Farm profile updated: {farm_id}")
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Error updating farm profile: {str(e)}")
            return False
    
    def add_crop_record(self, farm_id: str, crop_data: Dict[str, Any]) -> str:
        """
        Add a crop record
        
        Args:
            farm_id: Farm ID
            crop_data: Dictionary containing crop data
            
        Returns:
            Record ID of the created record
        """
        try:
            record_id = f"crop_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{crop_data.get('crop_name', 'unknown').replace(' ', '_')}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO crop_records (
                        record_id, farm_id, crop_name, variety, planting_date, harvest_date,
                        area_planted, expected_yield, actual_yield, seed_cost, fertilizer_cost,
                        pesticide_cost, labor_cost, other_costs, selling_price, total_revenue,
                        profit_loss, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record_id,
                    farm_id,
                    crop_data['crop_name'],
                    crop_data.get('variety', ''),
                    crop_data['planting_date'],
                    crop_data.get('harvest_date'),
                    crop_data['area_planted'],
                    crop_data['expected_yield'],
                    crop_data.get('actual_yield'),
                    crop_data.get('input_costs', {}).get('seed_cost', 0),
                    crop_data.get('input_costs', {}).get('fertilizer_cost', 0),
                    crop_data.get('input_costs', {}).get('pesticide_cost', 0),
                    crop_data.get('input_costs', {}).get('labor_cost', 0),
                    crop_data.get('input_costs', {}).get('other_costs', 0),
                    crop_data.get('selling_price'),
                    crop_data.get('total_revenue'),
                    crop_data.get('profit_loss'),
                    crop_data.get('notes', '')
                ))
                
                conn.commit()
                logger.info(f"Crop record added: {record_id}")
                return record_id
                
        except Exception as e:
            logger.error(f"Error adding crop record: {str(e)}")
            raise
    
    def get_crop_records(self, farm_id: str, limit: int = 50) -> List[CropRecord]:
        """
        Get crop records for a farm
        
        Args:
            farm_id: Farm ID
            limit: Maximum number of records to return
            
        Returns:
            List of CropRecord objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM crop_records 
                    WHERE farm_id = ? 
                    ORDER BY planting_date DESC 
                    LIMIT ?
                ''', (farm_id, limit))
                
                records = []
                for row in cursor.fetchall():
                    records.append(CropRecord(
                        record_id=row[0],
                        farm_id=row[1],
                        crop_name=row[2],
                        variety=row[3] or '',
                        planting_date=datetime.fromisoformat(row[4]),
                        harvest_date=datetime.fromisoformat(row[5]) if row[5] else None,
                        area_planted=row[6],
                        expected_yield=row[7],
                        actual_yield=row[8],
                        input_costs={
                            'seed_cost': row[9] or 0,
                            'fertilizer_cost': row[10] or 0,
                            'pesticide_cost': row[11] or 0,
                            'labor_cost': row[12] or 0,
                            'other_costs': row[13] or 0
                        },
                        selling_price=row[14],
                        total_revenue=row[15],
                        profit_loss=row[16],
                        notes=row[17] or '',
                        created_at=datetime.fromisoformat(row[18])
                    ))
                
                return records
                
        except Exception as e:
            logger.error(f"Error getting crop records: {str(e)}")
            return []
    
    def add_soil_test_record(self, farm_id: str, soil_data: Dict[str, Any]) -> str:
        """
        Add a soil test record
        
        Args:
            farm_id: Farm ID
            soil_data: Dictionary containing soil test data
            
        Returns:
            Test ID of the created record
        """
        try:
            test_id = f"soil_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO soil_test_records (
                        test_id, farm_id, test_date, ph_level, nitrogen, phosphorus, potassium,
                        organic_matter, micronutrients, recommendations, lab_name
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    test_id,
                    farm_id,
                    soil_data['test_date'],
                    soil_data['ph_level'],
                    soil_data['nitrogen'],
                    soil_data['phosphorus'],
                    soil_data['potassium'],
                    soil_data['organic_matter'],
                    json.dumps(soil_data.get('micronutrients', {})),
                    json.dumps(soil_data.get('recommendations', [])),
                    soil_data['lab_name']
                ))
                
                conn.commit()
                logger.info(f"Soil test record added: {test_id}")
                return test_id
                
        except Exception as e:
            logger.error(f"Error adding soil test record: {str(e)}")
            raise
    
    def get_farm_analytics(self, farm_id: str) -> Dict[str, Any]:
        """
        Get comprehensive farm analytics
        
        Args:
            farm_id: Farm ID
            
        Returns:
            Dictionary with farm analytics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get basic farm info
                farm_profile = self.get_farm_profile(farm_id)
                if not farm_profile:
                    return {'error': 'Farm profile not found'}
                
                # Get crop records
                crop_records = self.get_crop_records(farm_id, 100)
                
                # Get soil test records
                cursor.execute('''
                    SELECT * FROM soil_test_records 
                    WHERE farm_id = ? 
                    ORDER BY test_date DESC 
                    LIMIT 10
                ''', (farm_id,))
                
                soil_records = []
                for row in cursor.fetchall():
                    soil_records.append({
                        'test_date': row[2],
                        'ph_level': row[3],
                        'nitrogen': row[4],
                        'phosphorus': row[5],
                        'potassium': row[6],
                        'organic_matter': row[7],
                        'micronutrients': json.loads(row[8] or '{}'),
                        'recommendations': json.loads(row[9] or '[]'),
                        'lab_name': row[10]
                    })
                
                # Calculate analytics
                analytics = {
                    'farm_profile': asdict(farm_profile),
                    'crop_analytics': self._calculate_crop_analytics(crop_records),
                    'soil_analytics': self._calculate_soil_analytics(soil_records),
                    'financial_analytics': self._calculate_financial_analytics(crop_records),
                    'performance_metrics': self._calculate_performance_metrics(crop_records),
                    'recommendations': self._generate_recommendations(farm_profile, crop_records, soil_records)
                }
                
                return analytics
                
        except Exception as e:
            logger.error(f"Error getting farm analytics: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_crop_analytics(self, crop_records: List[CropRecord]) -> Dict[str, Any]:
        """Calculate crop-related analytics"""
        if not crop_records:
            return {}
        
        # Crop yield analysis
        completed_crops = [crop for crop in crop_records if crop.actual_yield is not None]
        
        if completed_crops:
            avg_yield = np.mean([crop.actual_yield for crop in completed_crops])
            yield_variance = np.var([crop.actual_yield for crop in completed_crops])
            
            # Best and worst performing crops
            best_crop = max(completed_crops, key=lambda x: x.actual_yield)
            worst_crop = min(completed_crops, key=lambda x: x.actual_yield)
            
            # Crop diversity
            unique_crops = len(set(crop.crop_name for crop in crop_records))
            
            return {
                'total_crops_planted': len(crop_records),
                'completed_crops': len(completed_crops),
                'average_yield': round(avg_yield, 2),
                'yield_variance': round(yield_variance, 2),
                'best_performing_crop': {
                    'crop_name': best_crop.crop_name,
                    'yield': best_crop.actual_yield,
                    'year': best_crop.planting_date.year
                },
                'worst_performing_crop': {
                    'crop_name': worst_crop.crop_name,
                    'yield': worst_crop.actual_yield,
                    'year': worst_crop.planting_date.year
                },
                'crop_diversity': unique_crops,
                'crop_frequency': self._calculate_crop_frequency(crop_records)
            }
        
        return {'total_crops_planted': len(crop_records), 'completed_crops': 0}
    
    def _calculate_soil_analytics(self, soil_records: List[Dict]) -> Dict[str, Any]:
        """Calculate soil-related analytics"""
        if not soil_records:
            return {}
        
        # Calculate trends
        ph_levels = [record['ph_level'] for record in soil_records]
        nitrogen_levels = [record['nitrogen'] for record in soil_records]
        phosphorus_levels = [record['phosphorus'] for record in soil_records]
        potassium_levels = [record['potassium'] for record in soil_records]
        
        return {
            'latest_test_date': soil_records[0]['test_date'],
            'ph_trend': self._calculate_trend(ph_levels),
            'nitrogen_trend': self._calculate_trend(nitrogen_levels),
            'phosphorus_trend': self._calculate_trend(phosphorus_levels),
            'potassium_trend': self._calculate_trend(potassium_levels),
            'current_ph': ph_levels[0] if ph_levels else None,
            'current_nitrogen': nitrogen_levels[0] if nitrogen_levels else None,
            'current_phosphorus': phosphorus_levels[0] if phosphorus_levels else None,
            'current_potassium': potassium_levels[0] if potassium_levels else None,
            'soil_health_score': self._calculate_soil_health_score(soil_records[0])
        }
    
    def _calculate_financial_analytics(self, crop_records: List[CropRecord]) -> Dict[str, Any]:
        """Calculate financial analytics"""
        completed_crops = [crop for crop in crop_records if crop.total_revenue is not None]
        
        if not completed_crops:
            return {}
        
        total_revenue = sum(crop.total_revenue for crop in completed_crops)
        total_costs = sum(
            sum(crop.input_costs.values()) for crop in completed_crops
        )
        total_profit = total_revenue - total_costs
        
        return {
            'total_revenue': round(total_revenue, 2),
            'total_costs': round(total_costs, 2),
            'total_profit': round(total_profit, 2),
            'profit_margin': round((total_profit / total_revenue * 100) if total_revenue > 0 else 0, 2),
            'average_revenue_per_crop': round(total_revenue / len(completed_crops), 2),
            'average_cost_per_crop': round(total_costs / len(completed_crops), 2),
            'most_profitable_crop': max(completed_crops, key=lambda x: x.profit_loss or 0).crop_name if completed_crops else None
        }
    
    def _calculate_performance_metrics(self, crop_records: List[CropRecord]) -> Dict[str, Any]:
        """Calculate performance metrics"""
        if not crop_records:
            return {}
        
        # Calculate success rate
        completed_crops = [crop for crop in crop_records if crop.actual_yield is not None]
        success_rate = (len(completed_crops) / len(crop_records)) * 100 if crop_records else 0
        
        # Calculate yield efficiency
        yield_efficiency = []
        for crop in completed_crops:
            if crop.expected_yield > 0:
                efficiency = (crop.actual_yield / crop.expected_yield) * 100
                yield_efficiency.append(efficiency)
        
        avg_yield_efficiency = np.mean(yield_efficiency) if yield_efficiency else 0
        
        return {
            'success_rate': round(success_rate, 2),
            'average_yield_efficiency': round(avg_yield_efficiency, 2),
            'total_area_farmed': sum(crop.area_planted for crop in crop_records),
            'crops_per_year': len(crop_records) / max(1, (datetime.now() - crop_records[0].planting_date).days / 365)
        }
    
    def _calculate_crop_frequency(self, crop_records: List[CropRecord]) -> Dict[str, int]:
        """Calculate frequency of each crop"""
        crop_counts = {}
        for crop in crop_records:
            crop_counts[crop.crop_name] = crop_counts.get(crop.crop_name, 0) + 1
        return crop_counts
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction"""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear trend
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return 'increasing'
        elif slope < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def _calculate_soil_health_score(self, soil_record: Dict) -> float:
        """Calculate soil health score (0-100)"""
        score = 0
        
        # pH score (optimal range 6.0-7.0)
        ph = soil_record['ph_level']
        if 6.0 <= ph <= 7.0:
            score += 25
        elif 5.5 <= ph <= 7.5:
            score += 20
        elif 5.0 <= ph <= 8.0:
            score += 15
        else:
            score += 5
        
        # Nutrient scores
        nitrogen = soil_record['nitrogen']
        phosphorus = soil_record['phosphorus']
        potassium = soil_record['potassium']
        
        # Nitrogen (optimal: 100-150 kg/ha)
        if 100 <= nitrogen <= 150:
            score += 25
        elif 80 <= nitrogen <= 200:
            score += 20
        else:
            score += 10
        
        # Phosphorus (optimal: 40-60 kg/ha)
        if 40 <= phosphorus <= 60:
            score += 25
        elif 30 <= phosphorus <= 80:
            score += 20
        else:
            score += 10
        
        # Potassium (optimal: 80-120 kg/ha)
        if 80 <= potassium <= 120:
            score += 25
        elif 60 <= potassium <= 150:
            score += 20
        else:
            score += 10
        
        return min(100, score)
    
    def _generate_recommendations(self, farm_profile: FarmProfile, crop_records: List[CropRecord], soil_records: List[Dict]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Soil-based recommendations
        if soil_records:
            latest_soil = soil_records[0]
            if latest_soil['ph_level'] < 6.0:
                recommendations.append("Consider adding lime to increase soil pH")
            elif latest_soil['ph_level'] > 7.5:
                recommendations.append("Consider adding sulfur to decrease soil pH")
            
            if latest_soil['nitrogen'] < 80:
                recommendations.append("Add nitrogen-rich fertilizers or organic matter")
            if latest_soil['phosphorus'] < 40:
                recommendations.append("Apply phosphorus-rich fertilizers")
            if latest_soil['potassium'] < 80:
                recommendations.append("Add potassium-rich fertilizers")
        
        # Crop-based recommendations
        if crop_records:
            # Check for low yields
            completed_crops = [crop for crop in crop_records if crop.actual_yield is not None]
            if completed_crops:
                avg_yield = np.mean([crop.actual_yield for crop in completed_crops])
                if avg_yield < 1000:  # Low yield threshold
                    recommendations.append("Consider improving farming practices to increase yield")
            
            # Check crop diversity
            unique_crops = len(set(crop.crop_name for crop in crop_records))
            if unique_crops < 3:
                recommendations.append("Consider diversifying crops to reduce risk")
        
        # General recommendations
        recommendations.append("Regular soil testing every 2-3 years is recommended")
        recommendations.append("Keep detailed records of all farming activities")
        recommendations.append("Consider crop rotation to maintain soil health")
        
        return recommendations

# Example usage and testing
if __name__ == "__main__":
    # Initialize farm profile manager
    farm_manager = FarmProfileManager()
    
    # Create a sample farm profile
    sample_farm_data = {
        'farmer_name': 'John Doe',
        'farm_name': 'Green Valley Farm',
        'location': {
            'state': 'Kerala',
            'district': 'Thiruvananthapuram',
            'village': 'Vattiyoorkavu'
        },
        'total_area': 2.5,
        'soil_type': 'Laterite',
        'soil_ph': 6.2,
        'soil_nutrients': {
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 80
        },
        'irrigation_type': 'Drip',
        'farming_type': 'Mixed',
        'established_year': 2020,
        'contact_info': {
            'phone': '+91-9876543210',
            'email': 'john@greenvalley.com',
            'address': 'Vattiyoorkavu, Thiruvananthapuram, Kerala'
        }
    }
    
    # Create farm profile
    farm_id = farm_manager.create_farm_profile(sample_farm_data)
    print(f"Created farm profile: {farm_id}")
    
    # Add sample crop record
    sample_crop_data = {
        'crop_name': 'Rice',
        'variety': 'Jaya',
        'planting_date': datetime(2024, 1, 15),
        'harvest_date': datetime(2024, 5, 15),
        'area_planted': 1.0,
        'expected_yield': 3000,
        'actual_yield': 3200,
        'input_costs': {
            'seed_cost': 2000,
            'fertilizer_cost': 5000,
            'pesticide_cost': 1500,
            'labor_cost': 8000,
            'other_costs': 1000
        },
        'selling_price': 25,
        'total_revenue': 80000,
        'profit_loss': 61500,
        'notes': 'Good harvest season'
    }
    
    crop_record_id = farm_manager.add_crop_record(farm_id, sample_crop_data)
    print(f"Added crop record: {crop_record_id}")
    
    # Get farm analytics
    analytics = farm_manager.get_farm_analytics(farm_id)
    print("\nFarm Analytics:")
    print(f"Farm Name: {analytics['farm_profile']['farm_name']}")
    print(f"Total Crops Planted: {analytics['crop_analytics']['total_crops_planted']}")
    print(f"Average Yield: {analytics['crop_analytics']['average_yield']} kg/hectare")
    print(f"Total Profit: ₹{analytics['financial_analytics']['total_profit']}")
    print(f"Soil Health Score: {analytics['soil_analytics']['soil_health_score']}")
    
    print("\nRecommendations:")
    for rec in analytics['recommendations']:
        print(f"- {rec}")
