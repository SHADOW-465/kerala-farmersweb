"""
Government Scheme Matcher
AI-powered system to match farmers with relevant government schemes
"""

import json
import sqlite3
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GovernmentScheme:
    """Government scheme data structure"""
    scheme_id: str
    scheme_name: str
    department: str
    category: str
    description: str
    eligibility_criteria: List[str]
    benefits: List[str]
    required_documents: List[str]
    application_process: List[str]
    contact_info: Dict[str, str]
    validity_period: Tuple[datetime, datetime]
    budget_allocated: float
    beneficiaries_target: int
    current_beneficiaries: int
    status: str  # active, inactive, completed
    created_at: datetime
    updated_at: datetime

@dataclass
class FarmerProfile:
    """Farmer profile for scheme matching"""
    farmer_id: str
    name: str
    age: int
    gender: str
    location: Dict[str, str]  # state, district, village
    land_holding: float  # in hectares
    farming_type: str  # organic, conventional, mixed
    annual_income: float
    crops_grown: List[str]
    livestock: List[str]
    education_level: str
    caste_category: str  # general, obc, sc, st
    bank_account: bool
    aadhaar_linked: bool
    mobile_number: str
    email: str
    created_at: datetime

@dataclass
class SchemeMatch:
    """Scheme match result"""
    scheme: GovernmentScheme
    match_score: float
    eligibility_status: str  # eligible, partially_eligible, not_eligible
    missing_criteria: List[str]
    recommendations: List[str]
    application_priority: str  # high, medium, low
    estimated_benefit: float

class GovernmentSchemeMatcher:
    """
    AI-powered government scheme matching system
    """
    
    def __init__(self, db_path: str = "schemes.db"):
        """
        Initialize government scheme matcher
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.schemes = {}
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.scaler = StandardScaler()
        self.init_database()
        self.load_schemes()
    
    def init_database(self):
        """Initialize database for schemes and farmer profiles"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Government schemes table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS government_schemes (
                        scheme_id TEXT PRIMARY KEY,
                        scheme_name TEXT NOT NULL,
                        department TEXT NOT NULL,
                        category TEXT NOT NULL,
                        description TEXT NOT NULL,
                        eligibility_criteria TEXT NOT NULL,
                        benefits TEXT NOT NULL,
                        required_documents TEXT NOT NULL,
                        application_process TEXT NOT NULL,
                        contact_info TEXT NOT NULL,
                        validity_start DATE NOT NULL,
                        validity_end DATE NOT NULL,
                        budget_allocated REAL NOT NULL,
                        beneficiaries_target INTEGER NOT NULL,
                        current_beneficiaries INTEGER DEFAULT 0,
                        status TEXT DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Farmer profiles table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS farmer_profiles (
                        farmer_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        gender TEXT NOT NULL,
                        state TEXT NOT NULL,
                        district TEXT NOT NULL,
                        village TEXT NOT NULL,
                        land_holding REAL NOT NULL,
                        farming_type TEXT NOT NULL,
                        annual_income REAL NOT NULL,
                        crops_grown TEXT NOT NULL,
                        livestock TEXT NOT NULL,
                        education_level TEXT NOT NULL,
                        caste_category TEXT NOT NULL,
                        bank_account BOOLEAN DEFAULT 0,
                        aadhaar_linked BOOLEAN DEFAULT 0,
                        mobile_number TEXT,
                        email TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Scheme applications table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS scheme_applications (
                        application_id TEXT PRIMARY KEY,
                        farmer_id TEXT NOT NULL,
                        scheme_id TEXT NOT NULL,
                        application_date DATE NOT NULL,
                        status TEXT DEFAULT 'pending',
                        documents_submitted TEXT,
                        application_notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (farmer_id) REFERENCES farmer_profiles (farmer_id),
                        FOREIGN KEY (scheme_id) REFERENCES government_schemes (scheme_id)
                    )
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def load_schemes(self):
        """Load government schemes from database and initialize matching system"""
        try:
            # Load schemes from database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM government_schemes WHERE status = "active"')
                rows = cursor.fetchall()
                
                for row in rows:
                    scheme = GovernmentScheme(
                        scheme_id=row[0],
                        scheme_name=row[1],
                        department=row[2],
                        category=row[3],
                        description=row[4],
                        eligibility_criteria=json.loads(row[5]),
                        benefits=json.loads(row[6]),
                        required_documents=json.loads(row[7]),
                        application_process=json.loads(row[8]),
                        contact_info=json.loads(row[9]),
                        validity_period=(datetime.fromisoformat(row[10]), datetime.fromisoformat(row[11])),
                        budget_allocated=row[12],
                        beneficiaries_target=row[13],
                        current_beneficiaries=row[14],
                        status=row[15],
                        created_at=datetime.fromisoformat(row[16]),
                        updated_at=datetime.fromisoformat(row[17])
                    )
                    self.schemes[scheme.scheme_id] = scheme
                
                # If no schemes in database, load default schemes
                if not self.schemes:
                    self._load_default_schemes()
                
                logger.info(f"Loaded {len(self.schemes)} government schemes")
                
        except Exception as e:
            logger.error(f"Error loading schemes: {str(e)}")
            self._load_default_schemes()
    
    def _load_default_schemes(self):
        """Load default government schemes for Kerala"""
        default_schemes = [
            {
                'scheme_id': 'pm_kisan_2024',
                'scheme_name': 'PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)',
                'department': 'Ministry of Agriculture & Farmers Welfare',
                'category': 'Income Support',
                'description': 'Direct income support of ₹6000 per year to all farmer families',
                'eligibility_criteria': [
                    'Landholding farmers',
                    'Small and marginal farmers',
                    'Must have valid land records',
                    'Aadhaar linked bank account required'
                ],
                'benefits': [
                    '₹6000 per year in 3 installments of ₹2000 each',
                    'Direct bank transfer',
                    'No middlemen involved'
                ],
                'required_documents': [
                    'Aadhaar card',
                    'Land records (7/12 extract)',
                    'Bank account details',
                    'Mobile number linked to Aadhaar'
                ],
                'application_process': [
                    'Visit nearest Common Service Centre (CSC)',
                    'Submit required documents',
                    'Verification by local authorities',
                    'Approval and fund transfer'
                ],
                'contact_info': {
                    'phone': '1800-180-1551',
                    'email': 'pmkisan@gov.in',
                    'website': 'https://pmkisan.gov.in'
                },
                'validity_period': (datetime(2024, 1, 1), datetime(2024, 12, 31)),
                'budget_allocated': 75000.0,
                'beneficiaries_target': 12000000,
                'current_beneficiaries': 10000000
            },
            {
                'scheme_id': 'pmfby_2024',
                'scheme_name': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
                'department': 'Ministry of Agriculture & Farmers Welfare',
                'category': 'Crop Insurance',
                'description': 'Comprehensive crop insurance scheme with low premium rates',
                'eligibility_criteria': [
                    'All farmers growing notified crops',
                    'Must have insurable interest in the crop',
                    'Crop should be grown in notified area',
                    'Must have valid land records'
                ],
                'benefits': [
                    'Low premium rates (1.5% for Kharif, 2% for Rabi)',
                    'Comprehensive coverage against natural calamities',
                    'Quick claim settlement',
                    'Use of technology for assessment'
                ],
                'required_documents': [
                    'Aadhaar card',
                    'Land records',
                    'Bank account details',
                    'Crop details and area'
                ],
                'application_process': [
                    'Visit nearest bank or insurance company',
                    'Fill application form',
                    'Pay premium',
                    'Receive insurance certificate'
                ],
                'contact_info': {
                    'phone': '1800-180-1551',
                    'email': 'pmfby@gov.in',
                    'website': 'https://pmfby.gov.in'
                },
                'validity_period': (datetime(2024, 1, 1), datetime(2024, 12, 31)),
                'budget_allocated': 15000.0,
                'beneficiaries_target': 50000000,
                'current_beneficiaries': 35000000
            },
            {
                'scheme_id': 'soil_health_card',
                'scheme_name': 'Soil Health Card Scheme',
                'department': 'Ministry of Agriculture & Farmers Welfare',
                'category': 'Soil Testing',
                'description': 'Free soil testing and recommendations for farmers',
                'eligibility_criteria': [
                    'All farmers',
                    'Must have valid land records',
                    'Land should be cultivable'
                ],
                'benefits': [
                    'Free soil testing',
                    'Personalized recommendations',
                      'Crop-specific fertilizer advice',
                    'Regular monitoring'
                ],
                'required_documents': [
                    'Aadhaar card',
                    'Land records',
                    'Mobile number'
                ],
                'application_process': [
                    'Visit nearest soil testing lab',
                    'Submit soil sample',
                    'Receive soil health card',
                    'Follow recommendations'
                ],
                'contact_info': {
                    'phone': '1800-180-1551',
                    'email': 'soilhealth@gov.in',
                    'website': 'https://soilhealth.dac.gov.in'
                },
                'validity_period': (datetime(2024, 1, 1), datetime(2025, 12, 31)),
                'budget_allocated': 5000.0,
                'beneficiaries_target': 10000000,
                'current_beneficiaries': 8000000
            },
            {
                'scheme_id': 'kisan_credit_card',
                'scheme_name': 'Kisan Credit Card (KCC)',
                'department': 'Ministry of Agriculture & Farmers Welfare',
                'category': 'Credit',
                'description': 'Credit card for farmers with low interest rates',
                'eligibility_criteria': [
                    'All farmers including tenant farmers',
                    'Must have valid land records or lease agreement',
                    'Good credit history preferred',
                    'Must have bank account'
                ],
                'benefits': [
                    'Low interest rates (4% per annum)',
                    'Flexible repayment options',
                    'Credit limit up to ₹3 lakh',
                    'Insurance coverage included'
                ],
                'required_documents': [
                    'Aadhaar card',
                    'Land records or lease agreement',
                    'Bank account details',
                    'Income certificate'
                ],
                'application_process': [
                    'Visit nearest bank',
                    'Fill application form',
                    'Submit required documents',
                    'Credit assessment and approval'
                ],
                'contact_info': {
                    'phone': '1800-180-1551',
                    'email': 'kcc@gov.in',
                    'website': 'https://kcc.gov.in'
                },
                'validity_period': (datetime(2024, 1, 1), datetime(2026, 12, 31)),
                'budget_allocated': 20000.0,
                'beneficiaries_target': 20000000,
                'current_beneficiaries': 15000000
            },
            {
                'scheme_id': 'organic_farming_scheme',
                'scheme_name': 'Paramparagat Krishi Vikas Yojana (PKVY)',
                'department': 'Ministry of Agriculture & Farmers Welfare',
                'category': 'Organic Farming',
                'description': 'Promotion of organic farming with financial assistance',
                'eligibility_criteria': [
                    'Farmers interested in organic farming',
                    'Must have minimum 0.5 hectares of land',
                    'Should be willing to follow organic practices',
                    'Must have valid land records'
                ],
                'benefits': [
                    'Financial assistance of ₹50,000 per hectare',
                    'Training and capacity building',
                    'Certification support',
                    'Market linkage assistance'
                ],
                'required_documents': [
                    'Aadhaar card',
                    'Land records',
                    'Bank account details',
                    'Organic farming plan'
                ],
                'application_process': [
                    'Visit nearest agriculture office',
                    'Submit application with plan',
                    'Field verification',
                    'Approval and fund disbursement'
                ],
                'contact_info': {
                    'phone': '1800-180-1551',
                    'email': 'pkvy@gov.in',
                    'website': 'https://pkvy.gov.in'
                },
                'validity_period': (datetime(2024, 1, 1), datetime(2025, 12, 31)),
                'budget_allocated': 10000.0,
                'beneficiaries_target': 1000000,
                'current_beneficiaries': 750000
            }
        ]
        
        # Add schemes to database
        for scheme_data in default_schemes:
            self._add_scheme_to_database(scheme_data)
        
        # Reload schemes
        self.load_schemes()
    
    def _add_scheme_to_database(self, scheme_data: Dict[str, Any]):
        """Add scheme to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO government_schemes (
                        scheme_id, scheme_name, department, category, description,
                        eligibility_criteria, benefits, required_documents, application_process,
                        contact_info, validity_start, validity_end, budget_allocated,
                        beneficiaries_target, current_beneficiaries, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    scheme_data['scheme_id'],
                    scheme_data['scheme_name'],
                    scheme_data['department'],
                    scheme_data['category'],
                    scheme_data['description'],
                    json.dumps(scheme_data['eligibility_criteria']),
                    json.dumps(scheme_data['benefits']),
                    json.dumps(scheme_data['required_documents']),
                    json.dumps(scheme_data['application_process']),
                    json.dumps(scheme_data['contact_info']),
                    scheme_data['validity_period'][0].date(),
                    scheme_data['validity_period'][1].date(),
                    scheme_data['budget_allocated'],
                    scheme_data['beneficiaries_target'],
                    scheme_data['current_beneficiaries'],
                    'active'
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error adding scheme to database: {str(e)}")
    
    def add_farmer_profile(self, farmer_data: Dict[str, Any]) -> str:
        """
        Add farmer profile to the system
        
        Args:
            farmer_data: Dictionary containing farmer profile data
            
        Returns:
            Farmer ID of the created profile
        """
        try:
            farmer_id = f"farmer_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{farmer_data.get('name', 'unknown').replace(' ', '_')}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO farmer_profiles (
                        farmer_id, name, age, gender, state, district, village,
                        land_holding, farming_type, annual_income, crops_grown, livestock,
                        education_level, caste_category, bank_account, aadhaar_linked,
                        mobile_number, email
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    farmer_id,
                    farmer_data['name'],
                    farmer_data['age'],
                    farmer_data['gender'],
                    farmer_data['location']['state'],
                    farmer_data['location']['district'],
                    farmer_data['location']['village'],
                    farmer_data['land_holding'],
                    farmer_data['farming_type'],
                    farmer_data['annual_income'],
                    json.dumps(farmer_data['crops_grown']),
                    json.dumps(farmer_data['livestock']),
                    farmer_data['education_level'],
                    farmer_data['caste_category'],
                    farmer_data.get('bank_account', False),
                    farmer_data.get('aadhaar_linked', False),
                    farmer_data.get('mobile_number', ''),
                    farmer_data.get('email', '')
                ))
                
                conn.commit()
                logger.info(f"Farmer profile added: {farmer_id}")
                return farmer_id
                
        except Exception as e:
            logger.error(f"Error adding farmer profile: {str(e)}")
            raise
    
    def get_farmer_profile(self, farmer_id: str) -> Optional[FarmerProfile]:
        """Get farmer profile by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM farmer_profiles WHERE farmer_id = ?', (farmer_id,))
                row = cursor.fetchone()
                
                if row:
                    return FarmerProfile(
                        farmer_id=row[0],
                        name=row[1],
                        age=row[2],
                        gender=row[3],
                        location={
                            'state': row[4],
                            'district': row[5],
                            'village': row[6]
                        },
                        land_holding=row[7],
                        farming_type=row[8],
                        annual_income=row[9],
                        crops_grown=json.loads(row[10]),
                        livestock=json.loads(row[11]),
                        education_level=row[12],
                        caste_category=row[13],
                        bank_account=bool(row[14]),
                        aadhaar_linked=bool(row[15]),
                        mobile_number=row[16] or '',
                        email=row[17] or '',
                        created_at=datetime.fromisoformat(row[18])
                    )
                return None
                
        except Exception as e:
            logger.error(f"Error getting farmer profile: {str(e)}")
            return None
    
    def find_matching_schemes(self, farmer_id: str, max_results: int = 10) -> List[SchemeMatch]:
        """
        Find matching government schemes for a farmer
        
        Args:
            farmer_id: Farmer ID
            max_results: Maximum number of results to return
            
        Returns:
            List of SchemeMatch objects
        """
        try:
            farmer = self.get_farmer_profile(farmer_id)
            if not farmer:
                return []
            
            matches = []
            
            for scheme in self.schemes.values():
                match = self._evaluate_scheme_match(farmer, scheme)
                if match.match_score > 0:  # Only include schemes with some match
                    matches.append(match)
            
            # Sort by match score and return top results
            matches.sort(key=lambda x: x.match_score, reverse=True)
            return matches[:max_results]
            
        except Exception as e:
            logger.error(f"Error finding matching schemes: {str(e)}")
            return []
    
    def _evaluate_scheme_match(self, farmer: FarmerProfile, scheme: GovernmentScheme) -> SchemeMatch:
        """Evaluate how well a scheme matches a farmer's profile"""
        match_score = 0
        total_criteria = 0
        missing_criteria = []
        recommendations = []
        
        # Basic eligibility checks
        eligibility_checks = {
            'land_holding': self._check_land_holding_eligibility(farmer, scheme),
            'income': self._check_income_eligibility(farmer, scheme),
            'documents': self._check_document_eligibility(farmer, scheme),
            'location': self._check_location_eligibility(farmer, scheme),
            'farming_type': self._check_farming_type_eligibility(farmer, scheme),
            'crops': self._check_crop_eligibility(farmer, scheme)
        }
        
        # Calculate match score
        for check_name, (eligible, weight) in eligibility_checks.items():
            total_criteria += weight
            if eligible:
                match_score += weight
            else:
                missing_criteria.append(check_name)
        
        # Normalize score
        if total_criteria > 0:
            match_score = (match_score / total_criteria) * 100
        
        # Determine eligibility status
        if match_score >= 80:
            eligibility_status = 'eligible'
        elif match_score >= 50:
            eligibility_status = 'partially_eligible'
        else:
            eligibility_status = 'not_eligible'
        
        # Generate recommendations
        recommendations = self._generate_scheme_recommendations(farmer, scheme, missing_criteria)
        
        # Determine application priority
        application_priority = self._determine_application_priority(match_score, scheme)
        
        # Estimate benefit
        estimated_benefit = self._estimate_scheme_benefit(scheme, farmer)
        
        return SchemeMatch(
            scheme=scheme,
            match_score=round(match_score, 1),
            eligibility_status=eligibility_status,
            missing_criteria=missing_criteria,
            recommendations=recommendations,
            application_priority=application_priority,
            estimated_benefit=estimated_benefit
        )
    
    def _check_land_holding_eligibility(self, farmer: FarmerProfile, scheme: GovernmentScheme) -> Tuple[bool, float]:
        """Check land holding eligibility"""
        # Most schemes don't have strict land holding requirements
        # But some schemes favor small and marginal farmers
        if 'small' in scheme.description.lower() or 'marginal' in scheme.description.lower():
            if farmer.land_holding <= 2.0:  # Small and marginal farmers
                return True, 10
            else:
                return False, 5
        return True, 5  # Default eligibility
    
    def _check_income_eligibility(self, farmer: FarmerProfile, scheme: GovernmentScheme) -> Tuple[bool, float]:
        """Check income eligibility"""
        # Most schemes don't have strict income limits
        # But some schemes target low-income farmers
        if 'income' in scheme.description.lower() or 'poor' in scheme.description.lower():
            if farmer.annual_income < 100000:  # Low income threshold
                return True, 10
            else:
                return False, 5
        return True, 5  # Default eligibility
    
    def _check_document_eligibility(self, farmer: FarmerProfile, scheme: GovernmentScheme) -> Tuple[bool, float]:
        """Check document eligibility"""
        required_docs = set()
        for doc in scheme.required_documents:
            doc_lower = doc.lower()
            if 'aadhaar' in doc_lower:
                required_docs.add('aadhaar')
            elif 'bank' in doc_lower:
                required_docs.add('bank_account')
            elif 'land' in doc_lower:
                required_docs.add('land_records')
        
        available_docs = set()
        if farmer.aadhaar_linked:
            available_docs.add('aadhaar')
        if farmer.bank_account:
            available_docs.add('bank_account')
        if farmer.land_holding > 0:
            available_docs.add('land_records')
        
        if required_docs.issubset(available_docs):
            return True, 10
        else:
            return False, 5
    
    def _check_location_eligibility(self, farmer: FarmerProfile, scheme: GovernmentScheme) -> Tuple[bool, float]:
        """Check location eligibility"""
        # Most schemes are available nationwide
        # Some schemes might be state-specific
        if 'kerala' in scheme.description.lower() or 'state' in scheme.description.lower():
            if farmer.location['state'].lower() == 'kerala':
                return True, 10
            else:
                return False, 5
        return True, 5  # Default eligibility
    
    def _check_farming_type_eligibility(self, farmer: FarmerProfile, scheme: GovernmentScheme) -> Tuple[bool, float]:
        """Check farming type eligibility"""
        if 'organic' in scheme.description.lower():
            if farmer.farming_type.lower() == 'organic':
                return True, 10
            else:
                return False, 5
        return True, 5  # Default eligibility
    
    def _check_crop_eligibility(self, farmer: FarmerProfile, scheme: GovernmentScheme) -> Tuple[bool, float]:
        """Check crop eligibility"""
        # Some schemes are crop-specific
        scheme_crops = set()
        for crop in ['rice', 'wheat', 'cotton', 'sugarcane', 'pulses', 'oilseeds']:
            if crop in scheme.description.lower():
                scheme_crops.add(crop)
        
        if scheme_crops:
            farmer_crops = set(crop.lower() for crop in farmer.crops_grown)
            if scheme_crops.intersection(farmer_crops):
                return True, 10
            else:
                return False, 5
        return True, 5  # Default eligibility
    
    def _generate_scheme_recommendations(self, farmer: FarmerProfile, scheme: GovernmentScheme, missing_criteria: List[str]) -> List[str]:
        """Generate recommendations for scheme application"""
        recommendations = []
        
        if 'documents' in missing_criteria:
            if not farmer.aadhaar_linked:
                recommendations.append("Link your Aadhaar card to your bank account")
            if not farmer.bank_account:
                recommendations.append("Open a bank account and link it with Aadhaar")
            recommendations.append("Ensure you have valid land records")
        
        if 'income' in missing_criteria:
            recommendations.append("Consider applying for income-based schemes")
        
        if 'farming_type' in missing_criteria:
            recommendations.append("Consider transitioning to organic farming for better scheme eligibility")
        
        # General recommendations
        recommendations.append(f"Contact {scheme.contact_info.get('phone', 'helpline')} for more information")
        recommendations.append(f"Visit {scheme.contact_info.get('website', 'official website')} for online application")
        
        return recommendations
    
    def _determine_application_priority(self, match_score: float, scheme: GovernmentScheme) -> str:
        """Determine application priority based on match score and scheme characteristics"""
        if match_score >= 80:
            return 'high'
        elif match_score >= 60:
            return 'medium'
        else:
            return 'low'
    
    def _estimate_scheme_benefit(self, scheme: GovernmentScheme, farmer: FarmerProfile) -> float:
        """Estimate potential benefit from scheme"""
        # This is a simplified calculation
        # In practice, you would use more sophisticated models
        
        if 'pm-kisan' in scheme.scheme_id.lower():
            return 6000.0  # Fixed annual benefit
        elif 'pmfby' in scheme.scheme_id.lower():
            return 5000.0  # Estimated insurance benefit
        elif 'kcc' in scheme.scheme_id.lower():
            return 300000.0  # Credit limit
        elif 'organic' in scheme.scheme_id.lower():
            return farmer.land_holding * 50000  # Per hectare benefit
        else:
            return 10000.0  # Default estimated benefit
    
    def apply_for_scheme(self, farmer_id: str, scheme_id: str, application_notes: str = "") -> str:
        """
        Apply for a government scheme
        
        Args:
            farmer_id: Farmer ID
            scheme_id: Scheme ID
            application_notes: Additional notes
            
        Returns:
            Application ID
        """
        try:
            application_id = f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{farmer_id}_{scheme_id}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO scheme_applications (
                        application_id, farmer_id, scheme_id, application_date,
                        status, application_notes
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    application_id,
                    farmer_id,
                    scheme_id,
                    datetime.now().date(),
                    'pending',
                    application_notes
                ))
                
                conn.commit()
                logger.info(f"Scheme application submitted: {application_id}")
                return application_id
                
        except Exception as e:
            logger.error(f"Error applying for scheme: {str(e)}")
            raise
    
    def get_scheme_statistics(self) -> Dict[str, Any]:
        """Get statistics about government schemes"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total schemes
                cursor.execute('SELECT COUNT(*) FROM government_schemes WHERE status = "active"')
                total_schemes = cursor.fetchone()[0]
                
                # Total beneficiaries
                cursor.execute('SELECT SUM(current_beneficiaries) FROM government_schemes')
                total_beneficiaries = cursor.fetchone()[0] or 0
                
                # Total budget
                cursor.execute('SELECT SUM(budget_allocated) FROM government_schemes')
                total_budget = cursor.fetchone()[0] or 0
                
                # Schemes by category
                cursor.execute('''
                    SELECT category, COUNT(*) as count 
                    FROM government_schemes 
                    WHERE status = "active" 
                    GROUP BY category
                ''')
                schemes_by_category = dict(cursor.fetchall())
                
                # Recent applications
                cursor.execute('''
                    SELECT COUNT(*) 
                    FROM scheme_applications 
                    WHERE application_date >= date('now', '-30 days')
                ''')
                recent_applications = cursor.fetchone()[0]
                
                return {
                    'total_schemes': total_schemes,
                    'total_beneficiaries': total_beneficiaries,
                    'total_budget': total_budget,
                    'schemes_by_category': schemes_by_category,
                    'recent_applications': recent_applications
                }
                
        except Exception as e:
            logger.error(f"Error getting scheme statistics: {str(e)}")
            return {}
    
    def search_schemes(self, query: str, category: str = None) -> List[GovernmentScheme]:
        """
        Search for schemes based on query
        
        Args:
            query: Search query
            category: Optional category filter
            
        Returns:
            List of matching schemes
        """
        try:
            results = []
            query_lower = query.lower()
            
            for scheme in self.schemes.values():
                if category and scheme.category.lower() != category.lower():
                    continue
                
                # Search in scheme name, description, and benefits
                searchable_text = f"{scheme.scheme_name} {scheme.description} {' '.join(scheme.benefits)}".lower()
                
                if query_lower in searchable_text:
                    results.append(scheme)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching schemes: {str(e)}")
            return []

# Example usage and testing
if __name__ == "__main__":
    # Initialize government scheme matcher
    matcher = GovernmentSchemeMatcher()
    
    # Create sample farmer profile
    sample_farmer_data = {
        'name': 'Rajesh Kumar',
        'age': 45,
        'gender': 'Male',
        'location': {
            'state': 'Kerala',
            'district': 'Thiruvananthapuram',
            'village': 'Vattiyoorkavu'
        },
        'land_holding': 1.5,
        'farming_type': 'conventional',
        'annual_income': 80000,
        'crops_grown': ['Rice', 'Coconut', 'Banana'],
        'livestock': ['Cows', 'Goats'],
        'education_level': 'High School',
        'caste_category': 'OBC',
        'bank_account': True,
        'aadhaar_linked': True,
        'mobile_number': '+91-9876543210',
        'email': 'rajesh@example.com'
    }
    
    # Add farmer profile
    farmer_id = matcher.add_farmer_profile(sample_farmer_data)
    print(f"Created farmer profile: {farmer_id}")
    
    # Find matching schemes
    print("\nGovernment Scheme Matcher - Test Results")
    print("=" * 50)
    
    matches = matcher.find_matching_schemes(farmer_id, 5)
    
    print(f"Found {len(matches)} matching schemes:")
    print()
    
    for i, match in enumerate(matches, 1):
        print(f"{i}. {match.scheme.scheme_name}")
        print(f"   Department: {match.scheme.department}")
        print(f"   Category: {match.scheme.category}")
        print(f"   Match Score: {match.match_score}%")
        print(f"   Eligibility: {match.eligibility_status}")
        print(f"   Priority: {match.application_priority}")
        print(f"   Estimated Benefit: ₹{match.estimated_benefit:,.0f}")
        
        if match.missing_criteria:
            print(f"   Missing Criteria: {', '.join(match.missing_criteria)}")
        
        print(f"   Recommendations:")
        for rec in match.recommendations[:3]:  # Show first 3 recommendations
            print(f"     - {rec}")
        
        print(f"   Contact: {match.scheme.contact_info.get('phone', 'N/A')}")
        print()
    
    # Get scheme statistics
    stats = matcher.get_scheme_statistics()
    print("Scheme Statistics:")
    print(f"  Total Active Schemes: {stats['total_schemes']}")
    print(f"  Total Beneficiaries: {stats['total_beneficiaries']:,}")
    print(f"  Total Budget: ₹{stats['total_budget']:,.0f} crores")
    print(f"  Recent Applications (30 days): {stats['recent_applications']}")
    
    print("\nSchemes by Category:")
    for category, count in stats['schemes_by_category'].items():
        print(f"  {category}: {count}")
