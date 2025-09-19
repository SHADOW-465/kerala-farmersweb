"""
Market Price Prediction System
Uses ML models to predict crop prices and provide market insights
"""

import requests
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PriceData:
    """Price data structure"""
    crop_name: str
    market_name: str
    price: float
    unit: str
    date: datetime
    quality: str
    source: str

@dataclass
class PricePrediction:
    """Price prediction structure"""
    crop_name: str
    predicted_price: float
    confidence: float
    prediction_date: datetime
    factors: Dict[str, float]
    recommendation: str

class MarketPricePredictor:
    """
    Market price prediction system for agricultural commodities
    """
    
    def __init__(self, db_path: str = "market_data.db"):
        """
        Initialize market price predictor
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.init_database()
        self.load_historical_data()
    
    def init_database(self):
        """Initialize database for market data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Market prices table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS market_prices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        crop_name TEXT NOT NULL,
                        market_name TEXT NOT NULL,
                        price REAL NOT NULL,
                        unit TEXT NOT NULL,
                        date DATE NOT NULL,
                        quality TEXT,
                        source TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Market trends table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS market_trends (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        crop_name TEXT NOT NULL,
                        trend_type TEXT NOT NULL,
                        value REAL NOT NULL,
                        date DATE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Weather impact table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS weather_impact (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        crop_name TEXT NOT NULL,
                        weather_factor TEXT NOT NULL,
                        impact_value REAL NOT NULL,
                        date DATE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                logger.info("Market database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def load_historical_data(self):
        """Load historical price data and train models"""
        try:
            # Kerala-specific crop price data (sample historical data)
            self.historical_data = {
                'Rice': self._generate_historical_prices('Rice', 25, 35, 30),
                'Coconut': self._generate_historical_prices('Coconut', 12, 22, 17),
                'Pepper': self._generate_historical_prices('Pepper', 400, 550, 475),
                'Cardamom': self._generate_historical_prices('Cardamom', 1000, 1500, 1250),
                'Rubber': self._generate_historical_prices('Rubber', 120, 180, 150),
                'Banana': self._generate_historical_prices('Banana', 20, 35, 27),
                'Ginger': self._generate_historical_prices('Ginger', 60, 120, 90),
                'Turmeric': self._generate_historical_prices('Turmeric', 80, 150, 115),
                'Tea': self._generate_historical_prices('Tea', 200, 300, 250),
                'Coffee': self._generate_historical_prices('Coffee', 300, 450, 375)
            }
            
            # Train models for each crop
            for crop_name in self.historical_data.keys():
                self._train_crop_model(crop_name)
                
            logger.info("Historical data loaded and models trained")
            
        except Exception as e:
            logger.error(f"Error loading historical data: {str(e)}")
            raise
    
    def _generate_historical_prices(self, crop_name: str, min_price: float, max_price: float, avg_price: float) -> pd.DataFrame:
        """Generate historical price data for a crop"""
        dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='D')
        prices = []
        
        for date in dates:
            # Add seasonal variation
            seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * date.dayofyear / 365)
            
            # Add random variation
            random_factor = np.random.normal(1, 0.1)
            
            # Add trend (slight upward trend over years)
            trend_factor = 1 + (date.year - 2020) * 0.02
            
            # Calculate price
            base_price = avg_price * seasonal_factor * random_factor * trend_factor
            price = max(min_price, min(max_price, base_price))
            
            prices.append({
                'date': date,
                'price': round(price, 2),
                'crop_name': crop_name,
                'market_name': 'Kerala Market',
                'unit': 'kg',
                'quality': 'Grade A',
                'source': 'Historical Data'
            })
        
        return pd.DataFrame(prices)
    
    def _train_crop_model(self, crop_name: str):
        """Train ML model for a specific crop"""
        try:
            data = self.historical_data[crop_name].copy()
            
            # Feature engineering
            data['year'] = data['date'].dt.year
            data['month'] = data['date'].dt.month
            data['day'] = data['date'].dt.day
            data['dayofyear'] = data['date'].dt.dayofyear
            data['weekday'] = data['date'].dt.weekday
            data['quarter'] = data['date'].dt.quarter
            
            # Add seasonal features
            data['sin_dayofyear'] = np.sin(2 * np.pi * data['dayofyear'] / 365)
            data['cos_dayofyear'] = np.cos(2 * np.pi * data['dayofyear'] / 365)
            
            # Add lag features
            data['price_lag_1'] = data['price'].shift(1)
            data['price_lag_7'] = data['price'].shift(7)
            data['price_lag_30'] = data['price'].shift(30)
            
            # Add rolling averages
            data['price_ma_7'] = data['price'].rolling(window=7).mean()
            data['price_ma_30'] = data['price'].rolling(window=30).mean()
            
            # Remove rows with NaN values
            data = data.dropna()
            
            if len(data) < 100:  # Need sufficient data
                logger.warning(f"Insufficient data for {crop_name}")
                return
            
            # Prepare features and target
            feature_columns = ['year', 'month', 'day', 'dayofyear', 'weekday', 'quarter',
                             'sin_dayofyear', 'cos_dayofyear', 'price_lag_1', 'price_lag_7',
                             'price_lag_30', 'price_ma_7', 'price_ma_30']
            
            X = data[feature_columns]
            y = data['price']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train multiple models and select the best one
            models = {
                'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
                'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
                'linear_regression': LinearRegression()
            }
            
            best_model = None
            best_score = -np.inf
            best_model_name = None
            
            for name, model in models.items():
                if name == 'linear_regression':
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                else:
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                
                score = r2_score(y_test, y_pred)
                if score > best_score:
                    best_score = score
                    best_model = model
                    best_model_name = name
            
            # Store the best model
            self.models[crop_name] = best_model
            self.scalers[crop_name] = scaler
            
            logger.info(f"Trained {best_model_name} model for {crop_name} with R² score: {best_score:.3f}")
            
        except Exception as e:
            logger.error(f"Error training model for {crop_name}: {str(e)}")
    
    def predict_price(self, crop_name: str, prediction_date: datetime = None) -> PricePrediction:
        """
        Predict price for a specific crop
        
        Args:
            crop_name: Name of the crop
            prediction_date: Date for prediction (default: tomorrow)
            
        Returns:
            PricePrediction object
        """
        try:
            if prediction_date is None:
                prediction_date = datetime.now() + timedelta(days=1)
            
            if crop_name not in self.models:
                raise ValueError(f"No model available for {crop_name}")
            
            # Prepare features for prediction
            features = self._prepare_prediction_features(crop_name, prediction_date)
            
            # Make prediction
            model = self.models[crop_name]
            scaler = self.scalers[crop_name]
            
            # Scale features
            features_scaled = scaler.transform(features.reshape(1, -1))
            
            # Predict price
            predicted_price = model.predict(features_scaled)[0]
            
            # Calculate confidence based on historical accuracy
            confidence = self._calculate_confidence(crop_name)
            
            # Generate factors that influenced the prediction
            factors = self._analyze_prediction_factors(crop_name, prediction_date)
            
            # Generate recommendation
            recommendation = self._generate_price_recommendation(crop_name, predicted_price, factors)
            
            return PricePrediction(
                crop_name=crop_name,
                predicted_price=round(predicted_price, 2),
                confidence=confidence,
                prediction_date=prediction_date,
                factors=factors,
                recommendation=recommendation
            )
            
        except Exception as e:
            logger.error(f"Error predicting price for {crop_name}: {str(e)}")
            raise
    
    def _prepare_prediction_features(self, crop_name: str, prediction_date: datetime) -> np.ndarray:
        """Prepare features for price prediction"""
        # Get recent price data for lag features
        recent_data = self.historical_data[crop_name].tail(30)
        
        # Basic date features
        year = prediction_date.year
        month = prediction_date.month
        day = prediction_date.day
        dayofyear = prediction_date.timetuple().tm_yday
        weekday = prediction_date.weekday()
        quarter = (prediction_date.month - 1) // 3 + 1
        
        # Seasonal features
        sin_dayofyear = np.sin(2 * np.pi * dayofyear / 365)
        cos_dayofyear = np.cos(2 * np.pi * dayofyear / 365)
        
        # Lag features (use recent prices)
        price_lag_1 = recent_data['price'].iloc[-1] if len(recent_data) > 0 else recent_data['price'].mean()
        price_lag_7 = recent_data['price'].iloc[-7] if len(recent_data) >= 7 else recent_data['price'].mean()
        price_lag_30 = recent_data['price'].iloc[-30] if len(recent_data) >= 30 else recent_data['price'].mean()
        
        # Rolling averages
        price_ma_7 = recent_data['price'].tail(7).mean()
        price_ma_30 = recent_data['price'].tail(30).mean()
        
        return np.array([year, month, day, dayofyear, weekday, quarter,
                        sin_dayofyear, cos_dayofyear, price_lag_1, price_lag_7,
                        price_lag_30, price_ma_7, price_ma_30])
    
    def _calculate_confidence(self, crop_name: str) -> float:
        """Calculate confidence score for prediction"""
        # This is a simplified confidence calculation
        # In practice, you would use cross-validation or other methods
        
        # Base confidence on data availability and model performance
        data_points = len(self.historical_data[crop_name])
        
        if data_points > 1000:
            base_confidence = 0.85
        elif data_points > 500:
            base_confidence = 0.75
        else:
            base_confidence = 0.65
        
        # Add some randomness to simulate real-world uncertainty
        confidence = base_confidence + np.random.normal(0, 0.05)
        return max(0.5, min(0.95, confidence))
    
    def _analyze_prediction_factors(self, crop_name: str, prediction_date: datetime) -> Dict[str, float]:
        """Analyze factors that influence the price prediction"""
        factors = {}
        
        # Seasonal factor
        month = prediction_date.month
        if month in [6, 7, 8, 9, 10]:  # Monsoon season
            factors['seasonal_demand'] = 0.8
        elif month in [11, 12, 1, 2]:  # Winter season
            factors['seasonal_demand'] = 1.2
        else:  # Summer season
            factors['seasonal_demand'] = 1.0
        
        # Historical trend
        recent_prices = self.historical_data[crop_name]['price'].tail(30)
        if len(recent_prices) > 1:
            trend = (recent_prices.iloc[-1] - recent_prices.iloc[0]) / recent_prices.iloc[0]
            factors['price_trend'] = trend
        else:
            factors['price_trend'] = 0.0
        
        # Market volatility
        price_std = recent_prices.std()
        price_mean = recent_prices.mean()
        volatility = price_std / price_mean if price_mean > 0 else 0
        factors['market_volatility'] = volatility
        
        # Supply and demand indicators (simplified)
        factors['supply_pressure'] = np.random.uniform(0.8, 1.2)
        factors['demand_pressure'] = np.random.uniform(0.9, 1.1)
        
        return factors
    
    def _generate_price_recommendation(self, crop_name: str, predicted_price: float, factors: Dict[str, float]) -> str:
        """Generate price recommendation for farmers"""
        recommendations = []
        
        # Price trend recommendation
        if factors['price_trend'] > 0.1:
            recommendations.append("Prices are trending upward - consider holding your produce")
        elif factors['price_trend'] < -0.1:
            recommendations.append("Prices are declining - consider selling soon")
        else:
            recommendations.append("Prices are stable - monitor market conditions")
        
        # Seasonal recommendation
        if factors['seasonal_demand'] > 1.1:
            recommendations.append("High seasonal demand expected - good time to sell")
        elif factors['seasonal_demand'] < 0.9:
            recommendations.append("Low seasonal demand - consider storing if possible")
        
        # Volatility recommendation
        if factors['market_volatility'] > 0.2:
            recommendations.append("High market volatility - consider selling in smaller batches")
        else:
            recommendations.append("Stable market conditions - normal selling strategy recommended")
        
        return " | ".join(recommendations)
    
    def get_market_insights(self, crop_name: str = None) -> Dict[str, Any]:
        """
        Get comprehensive market insights
        
        Args:
            crop_name: Specific crop name (optional)
            
        Returns:
            Dictionary with market insights
        """
        try:
            insights = {
                'market_overview': {},
                'price_trends': {},
                'seasonal_patterns': {},
                'recommendations': []
            }
            
            crops_to_analyze = [crop_name] if crop_name else list(self.historical_data.keys())
            
            for crop in crops_to_analyze:
                if crop not in self.historical_data:
                    continue
                
                data = self.historical_data[crop]
                
                # Market overview
                current_price = data['price'].iloc[-1]
                avg_price = data['price'].mean()
                price_change = ((current_price - avg_price) / avg_price) * 100
                
                insights['market_overview'][crop] = {
                    'current_price': round(current_price, 2),
                    'average_price': round(avg_price, 2),
                    'price_change_percent': round(price_change, 2),
                    'price_range': {
                        'min': round(data['price'].min(), 2),
                        'max': round(data['price'].max(), 2)
                    }
                }
                
                # Price trends
                recent_30_days = data.tail(30)
                trend_slope = np.polyfit(range(len(recent_30_days)), recent_30_days['price'], 1)[0]
                
                insights['price_trends'][crop] = {
                    'trend_direction': 'upward' if trend_slope > 0 else 'downward',
                    'trend_strength': abs(trend_slope),
                    'volatility': round(data['price'].std(), 2)
                }
                
                # Seasonal patterns
                monthly_avg = data.groupby(data['date'].dt.month)['price'].mean()
                peak_month = monthly_avg.idxmax()
                low_month = monthly_avg.idxmin()
                
                insights['seasonal_patterns'][crop] = {
                    'peak_month': peak_month,
                    'low_month': low_month,
                    'seasonal_variation': round((monthly_avg.max() - monthly_avg.min()) / monthly_avg.mean() * 100, 2)
                }
            
            # Generate overall recommendations
            insights['recommendations'] = self._generate_market_recommendations(insights)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating market insights: {str(e)}")
            return {'error': str(e)}
    
    def _generate_market_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate market recommendations based on insights"""
        recommendations = []
        
        # Analyze overall market trends
        upward_trends = sum(1 for trend in insights['price_trends'].values() if trend['trend_direction'] == 'upward')
        total_crops = len(insights['price_trends'])
        
        if upward_trends > total_crops * 0.7:
            recommendations.append("Most crops showing upward price trends - favorable market conditions")
        elif upward_trends < total_crops * 0.3:
            recommendations.append("Most crops showing downward price trends - consider holding produce")
        
        # High volatility crops
        high_volatility_crops = [crop for crop, trend in insights['price_trends'].items() 
                               if trend['volatility'] > 50]
        if high_volatility_crops:
            recommendations.append(f"High volatility detected in: {', '.join(high_volatility_crops)} - monitor closely")
        
        # Seasonal recommendations
        current_month = datetime.now().month
        seasonal_crops = [crop for crop, pattern in insights['seasonal_patterns'].items() 
                         if pattern['peak_month'] == current_month]
        if seasonal_crops:
            recommendations.append(f"Peak season for: {', '.join(seasonal_crops)} - optimal selling time")
        
        return recommendations
    
    def get_price_forecast(self, crop_name: str, days: int = 7) -> List[PricePrediction]:
        """
        Get price forecast for multiple days
        
        Args:
            crop_name: Name of the crop
            days: Number of days to forecast
            
        Returns:
            List of PricePrediction objects
        """
        forecasts = []
        
        for i in range(days):
            prediction_date = datetime.now() + timedelta(days=i+1)
            prediction = self.predict_price(crop_name, prediction_date)
            forecasts.append(prediction)
        
        return forecasts
    
    def add_price_data(self, price_data: PriceData):
        """
        Add new price data to the system
        
        Args:
            price_data: PriceData object
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO market_prices (crop_name, market_name, price, unit, date, quality, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    price_data.crop_name,
                    price_data.market_name,
                    price_data.price,
                    price_data.unit,
                    price_data.date.date(),
                    price_data.quality,
                    price_data.source
                ))
                
                conn.commit()
                logger.info(f"Added price data for {price_data.crop_name}")
                
        except Exception as e:
            logger.error(f"Error adding price data: {str(e)}")
    
    def save_models(self, filepath: str):
        """Save trained models to file"""
        try:
            model_data = {
                'models': self.models,
                'scalers': self.scalers,
                'label_encoders': self.label_encoders
            }
            joblib.dump(model_data, filepath)
            logger.info(f"Models saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving models: {str(e)}")
    
    def load_models(self, filepath: str):
        """Load trained models from file"""
        try:
            model_data = joblib.load(filepath)
            self.models = model_data['models']
            self.scalers = model_data['scalers']
            self.label_encoders = model_data['label_encoders']
            logger.info(f"Models loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize market price predictor
    predictor = MarketPricePredictor()
    
    # Test price prediction
    print("Market Price Prediction - Test Results")
    print("=" * 50)
    
    # Predict prices for different crops
    crops = ['Rice', 'Coconut', 'Pepper', 'Cardamom']
    
    for crop in crops:
        prediction = predictor.predict_price(crop)
        print(f"\n{crop} Price Prediction:")
        print(f"  Predicted Price: ₹{prediction.predicted_price}/kg")
        print(f"  Confidence: {prediction.confidence:.1%}")
        print(f"  Recommendation: {prediction.recommendation}")
        print(f"  Factors: {prediction.factors}")
    
    # Get market insights
    print("\n" + "=" * 50)
    print("Market Insights:")
    insights = predictor.get_market_insights()
    
    print("\nMarket Overview:")
    for crop, overview in insights['market_overview'].items():
        print(f"  {crop}: ₹{overview['current_price']}/kg (Change: {overview['price_change_percent']:+.1f}%)")
    
    print("\nRecommendations:")
    for rec in insights['recommendations']:
        print(f"  - {rec}")
    
    # Get 7-day forecast for Rice
    print("\n" + "=" * 50)
    print("7-Day Price Forecast for Rice:")
    rice_forecast = predictor.get_price_forecast('Rice', 7)
    
    for i, forecast in enumerate(rice_forecast, 1):
        print(f"  Day {i} ({forecast.prediction_date.strftime('%Y-%m-%d')}): ₹{forecast.predicted_price}/kg")
