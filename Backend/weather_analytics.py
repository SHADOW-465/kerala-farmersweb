"""
Intelligent Weather Analytics System
Provides weather forecasts, alerts, and farming recommendations
"""

import requests
import json
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from dataclasses import dataclass
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WeatherData:
    """Weather data structure"""
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    wind_direction: float
    visibility: float
    uv_index: float
    description: str
    timestamp: datetime

@dataclass
class WeatherAlert:
    """Weather alert structure"""
    alert_type: str
    severity: str
    description: str
    start_time: datetime
    end_time: datetime
    recommendation: str

class IntelligentWeatherAnalytics:
    """
    Intelligent weather analytics system for farmers
    """
    
    def __init__(self, api_key: str):
        """
        Initialize weather analytics system
        
        Args:
            api_key: OpenWeatherMap API key
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Kerala-specific weather patterns and thresholds
        self.kerala_weather_patterns = {
            'monsoon_season': {
                'months': [6, 7, 8, 9, 10],  # June to October
                'avg_rainfall': 2000,  # mm
                'avg_humidity': 85,
                'avg_temperature': 26
            },
            'winter_season': {
                'months': [11, 12, 1, 2],  # November to February
                'avg_rainfall': 200,  # mm
                'avg_humidity': 70,
                'avg_temperature': 24
            },
            'summer_season': {
                'months': [3, 4, 5],  # March to May
                'avg_rainfall': 300,  # mm
                'avg_humidity': 75,
                'avg_temperature': 30
            }
        }
        
        # Weather alert thresholds
        self.alert_thresholds = {
            'heavy_rain': {'rainfall': 50, 'duration_hours': 3},
            'drought': {'rainfall': 5, 'duration_days': 7},
            'high_temperature': {'temperature': 35, 'duration_hours': 6},
            'low_temperature': {'temperature': 15, 'duration_hours': 6},
            'high_humidity': {'humidity': 90, 'duration_hours': 12},
            'low_humidity': {'humidity': 40, 'duration_hours': 12},
            'strong_wind': {'wind_speed': 15, 'duration_hours': 3},
            'high_uv': {'uv_index': 8, 'duration_hours': 4}
        }
        
        # Farming recommendations based on weather
        self.farming_recommendations = {
            'irrigation': {
                'high_temperature': "Increase irrigation frequency. Water early morning or late evening to reduce evaporation.",
                'low_humidity': "Consider mulching to retain soil moisture. Increase irrigation if needed.",
                'drought': "Implement water conservation measures. Use drip irrigation for efficiency.",
                'heavy_rain': "Reduce irrigation. Ensure proper drainage to prevent waterlogging."
            },
            'pest_control': {
                'high_humidity': "High humidity increases pest activity. Monitor crops closely and apply preventive measures.",
                'rainy_weather': "Fungal diseases are more likely. Apply fungicides preventively.",
                'dry_weather': "Spider mites and aphids thrive in dry conditions. Check for infestations."
            },
            'harvesting': {
                'clear_weather': "Ideal conditions for harvesting. Plan harvesting activities.",
                'rainy_weather': "Avoid harvesting during rain. Wait for dry conditions.",
                'high_humidity': "Delay harvesting if possible. High humidity can affect crop quality."
            },
            'planting': {
                'moderate_rain': "Good conditions for planting. Soil moisture is adequate.",
                'heavy_rain': "Avoid planting. Wait for better conditions to prevent seed rot.",
                'drought': "Delay planting until adequate moisture is available."
            }
        }
    
    def get_current_weather(self, city: str, state: str = "Kerala") -> Optional[WeatherData]:
        """
        Get current weather data for a location
        
        Args:
            city: City name
            state: State name
            
        Returns:
            WeatherData object or None if failed
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': f"{city},{state}",
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                main = data['main']
                weather = data['weather'][0]
                wind = data.get('wind', {})
                visibility = data.get('visibility', 0) / 1000  # Convert to km
                
                return WeatherData(
                    temperature=main['temp'],
                    humidity=main['humidity'],
                    pressure=main['pressure'],
                    wind_speed=wind.get('speed', 0),
                    wind_direction=wind.get('deg', 0),
                    visibility=visibility,
                    uv_index=data.get('uv', 0),
                    description=weather['description'],
                    timestamp=datetime.now()
                )
            else:
                logger.error(f"Weather API error: {data.get('message', 'Unknown error')}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching current weather: {str(e)}")
            return None
    
    def get_weather_forecast(self, city: str, state: str = "Kerala", days: int = 7) -> List[WeatherData]:
        """
        Get weather forecast for specified days
        
        Args:
            city: City name
            state: State name
            days: Number of days to forecast (max 5 for free API)
            
        Returns:
            List of WeatherData objects
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': f"{city},{state}",
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                forecast_data = []
                for item in data['list'][:days * 8]:  # 8 forecasts per day (3-hour intervals)
                    main = item['main']
                    weather = item['weather'][0]
                    wind = item.get('wind', {})
                    visibility = item.get('visibility', 0) / 1000
                    
                    forecast_data.append(WeatherData(
                        temperature=main['temp'],
                        humidity=main['humidity'],
                        pressure=main['pressure'],
                        wind_speed=wind.get('speed', 0),
                        wind_direction=wind.get('deg', 0),
                        visibility=visibility,
                        uv_index=0,  # Not available in forecast
                        description=weather['description'],
                        timestamp=datetime.fromtimestamp(item['dt'])
                    ))
                
                return forecast_data
            else:
                logger.error(f"Weather forecast API error: {data.get('message', 'Unknown error')}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching weather forecast: {str(e)}")
            return []
    
    def analyze_weather_patterns(self, weather_data: List[WeatherData]) -> Dict:
        """
        Analyze weather patterns and provide insights
        
        Args:
            weather_data: List of weather data points
            
        Returns:
            Dictionary with weather analysis
        """
        if not weather_data:
            return {}
        
        # Calculate statistics
        temperatures = [w.temperature for w in weather_data]
        humidities = [w.humidity for w in weather_data]
        pressures = [w.pressure for w in weather_data]
        wind_speeds = [w.wind_speed for w in weather_data]
        
        analysis = {
            'temperature': {
                'current': temperatures[0] if temperatures else 0,
                'average': np.mean(temperatures),
                'min': np.min(temperatures),
                'max': np.max(temperatures),
                'trend': self._calculate_trend(temperatures)
            },
            'humidity': {
                'current': humidities[0] if humidities else 0,
                'average': np.mean(humidities),
                'min': np.min(humidities),
                'max': np.max(humidities),
                'trend': self._calculate_trend(humidities)
            },
            'pressure': {
                'current': pressures[0] if pressures else 0,
                'average': np.mean(pressures),
                'min': np.min(pressures),
                'max': np.max(pressures),
                'trend': self._calculate_trend(pressures)
            },
            'wind': {
                'current_speed': wind_speeds[0] if wind_speeds else 0,
                'average_speed': np.mean(wind_speeds),
                'max_speed': np.max(wind_speeds),
                'trend': self._calculate_trend(wind_speeds)
            },
            'season': self._identify_season(datetime.now().month),
            'weather_conditions': self._analyze_weather_conditions(weather_data)
        }
        
        return analysis
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction for a series of values"""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear trend calculation
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return 'increasing'
        elif slope < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def _identify_season(self, month: int) -> str:
        """Identify current season based on month"""
        for season, data in self.kerala_weather_patterns.items():
            if month in data['months']:
                return season.replace('_', ' ').title()
        return 'Unknown'
    
    def _analyze_weather_conditions(self, weather_data: List[WeatherData]) -> Dict:
        """Analyze overall weather conditions"""
        conditions = {
            'rainy_days': 0,
            'sunny_days': 0,
            'cloudy_days': 0,
            'stormy_days': 0,
            'foggy_days': 0
        }
        
        for data in weather_data:
            desc = data.description.lower()
            if 'rain' in desc or 'drizzle' in desc:
                conditions['rainy_days'] += 1
            elif 'clear' in desc or 'sunny' in desc:
                conditions['sunny_days'] += 1
            elif 'cloud' in desc:
                conditions['cloudy_days'] += 1
            elif 'storm' in desc or 'thunder' in desc:
                conditions['stormy_days'] += 1
            elif 'fog' in desc or 'mist' in desc:
                conditions['foggy_days'] += 1
        
        return conditions
    
    def generate_weather_alerts(self, weather_data: List[WeatherData]) -> List[WeatherAlert]:
        """
        Generate weather alerts based on current conditions
        
        Args:
            weather_data: List of weather data points
            
        Returns:
            List of WeatherAlert objects
        """
        alerts = []
        
        if not weather_data:
            return alerts
        
        current_weather = weather_data[0]
        
        # Check for various alert conditions
        if current_weather.temperature > self.alert_thresholds['high_temperature']['temperature']:
            alerts.append(WeatherAlert(
                alert_type="High Temperature",
                severity="Warning",
                description=f"Temperature is {current_weather.temperature}°C, above normal levels",
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(hours=6),
                recommendation="Increase irrigation and provide shade for sensitive crops"
            ))
        
        if current_weather.humidity > self.alert_thresholds['high_humidity']['humidity']:
            alerts.append(WeatherAlert(
                alert_type="High Humidity",
                severity="Info",
                description=f"Humidity is {current_weather.humidity}%, very high",
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(hours=12),
                recommendation="Monitor for fungal diseases and ensure good air circulation"
            ))
        
        if current_weather.wind_speed > self.alert_thresholds['strong_wind']['wind_speed']:
            alerts.append(WeatherAlert(
                alert_type="Strong Wind",
                severity="Warning",
                description=f"Wind speed is {current_weather.wind_speed} m/s, very strong",
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(hours=3),
                recommendation="Secure loose items and avoid outdoor activities"
            ))
        
        if current_weather.uv_index > self.alert_thresholds['high_uv']['uv_index']:
            alerts.append(WeatherAlert(
                alert_type="High UV Index",
                severity="Warning",
                description=f"UV index is {current_weather.uv_index}, very high",
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(hours=4),
                recommendation="Avoid outdoor work during peak hours (10 AM - 4 PM)"
            ))
        
        return alerts
    
    def get_farming_recommendations(self, weather_data: List[WeatherData]) -> Dict[str, List[str]]:
        """
        Get farming recommendations based on weather conditions
        
        Args:
            weather_data: List of weather data points
            
        Returns:
            Dictionary of farming recommendations by category
        """
        if not weather_data:
            return {}
        
        current_weather = weather_data[0]
        recommendations = {
            'irrigation': [],
            'pest_control': [],
            'harvesting': [],
            'planting': [],
            'general': []
        }
        
        # Temperature-based recommendations
        if current_weather.temperature > 32:
            recommendations['irrigation'].append(
                self.farming_recommendations['irrigation']['high_temperature']
            )
            recommendations['general'].append(
                "High temperature detected. Consider working early morning or late evening."
            )
        elif current_weather.temperature < 18:
            recommendations['general'].append(
                "Low temperature detected. Protect sensitive crops from cold stress."
            )
        
        # Humidity-based recommendations
        if current_weather.humidity > 85:
            recommendations['pest_control'].append(
                self.farming_recommendations['pest_control']['high_humidity']
            )
        elif current_weather.humidity < 50:
            recommendations['irrigation'].append(
                self.farming_recommendations['irrigation']['low_humidity']
            )
            recommendations['pest_control'].append(
                self.farming_recommendations['pest_control']['dry_weather']
            )
        
        # Weather condition-based recommendations
        weather_desc = current_weather.description.lower()
        if 'rain' in weather_desc:
            recommendations['irrigation'].append(
                self.farming_recommendations['irrigation']['heavy_rain']
            )
            recommendations['harvesting'].append(
                self.farming_recommendations['harvesting']['rainy_weather']
            )
            recommendations['planting'].append(
                self.farming_recommendations['planting']['heavy_rain']
            )
            recommendations['pest_control'].append(
                self.farming_recommendations['pest_control']['rainy_weather']
            )
        elif 'clear' in weather_desc or 'sunny' in weather_desc:
            recommendations['harvesting'].append(
                self.farming_recommendations['harvesting']['clear_weather']
            )
            recommendations['planting'].append(
                self.farming_recommendations['planting']['moderate_rain']
            )
        
        # Wind-based recommendations
        if current_weather.wind_speed > 10:
            recommendations['general'].append(
                "Strong wind detected. Secure loose items and avoid spraying operations."
            )
        
        return recommendations
    
    def get_irrigation_schedule(self, weather_data: List[WeatherData], soil_moisture: float = 50) -> Dict:
        """
        Generate irrigation schedule based on weather and soil moisture
        
        Args:
            weather_data: List of weather data points
            soil_moisture: Current soil moisture percentage
            
        Returns:
            Dictionary with irrigation recommendations
        """
        if not weather_data:
            return {}
        
        current_weather = weather_data[0]
        forecast = weather_data[1:3] if len(weather_data) > 1 else []
        
        # Calculate irrigation needs
        irrigation_needs = {
            'immediate': False,
            'next_24h': False,
            'next_3days': False,
            'recommendation': '',
            'schedule': []
        }
        
        # Check immediate needs
        if soil_moisture < 30 or current_weather.temperature > 30:
            irrigation_needs['immediate'] = True
            irrigation_needs['recommendation'] = "Immediate irrigation required"
        
        # Check 24-hour forecast
        if forecast:
            avg_temp_24h = np.mean([w.temperature for w in forecast])
            avg_humidity_24h = np.mean([w.humidity for w in forecast])
            
            if avg_temp_24h > 28 and avg_humidity_24h < 70:
                irrigation_needs['next_24h'] = True
                irrigation_needs['recommendation'] = "Irrigation recommended within 24 hours"
        
        # Generate schedule
        schedule = []
        for i, weather in enumerate(weather_data[:7]):  # Next 7 days
            if weather.temperature > 28 and weather.humidity < 70:
                schedule.append({
                    'date': weather.timestamp.strftime('%Y-%m-%d'),
                    'time': 'Early morning (6-8 AM)',
                    'duration': '30-45 minutes',
                    'reason': f"High temperature ({weather.temperature}°C) and low humidity ({weather.humidity}%)"
                })
        
        irrigation_needs['schedule'] = schedule
        
        return irrigation_needs
    
    def get_weather_summary(self, city: str, state: str = "Kerala") -> Dict:
        """
        Get comprehensive weather summary for a location
        
        Args:
            city: City name
            state: State name
            
        Returns:
            Dictionary with complete weather summary
        """
        # Get current weather and forecast
        current_weather = self.get_current_weather(city, state)
        forecast = self.get_weather_forecast(city, state, 5)
        
        if not current_weather:
            return {'error': 'Unable to fetch weather data'}
        
        # Combine current and forecast data
        all_weather_data = [current_weather] + forecast
        
        # Analyze patterns
        analysis = self.analyze_weather_patterns(all_weather_data)
        
        # Generate alerts
        alerts = self.generate_weather_alerts(all_weather_data)
        
        # Get farming recommendations
        recommendations = self.get_farming_recommendations(all_weather_data)
        
        # Get irrigation schedule
        irrigation = self.get_irrigation_schedule(all_weather_data)
        
        return {
            'current_weather': {
                'temperature': current_weather.temperature,
                'humidity': current_weather.humidity,
                'pressure': current_weather.pressure,
                'wind_speed': current_weather.wind_speed,
                'description': current_weather.description,
                'timestamp': current_weather.timestamp.isoformat()
            },
            'forecast': [
                {
                    'date': w.timestamp.strftime('%Y-%m-%d %H:%M'),
                    'temperature': w.temperature,
                    'humidity': w.humidity,
                    'description': w.description
                } for w in forecast
            ],
            'analysis': analysis,
            'alerts': [
                {
                    'type': alert.alert_type,
                    'severity': alert.severity,
                    'description': alert.description,
                    'recommendation': alert.recommendation,
                    'start_time': alert.start_time.isoformat(),
                    'end_time': alert.end_time.isoformat()
                } for alert in alerts
            ],
            'farming_recommendations': recommendations,
            'irrigation_schedule': irrigation
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize weather analytics (replace with your API key)
    weather_analytics = IntelligentWeatherAnalytics("your_openweathermap_api_key_here")
    
    # Test weather summary
    print("Weather Analytics - Test Results")
    print("=" * 50)
    
    summary = weather_analytics.get_weather_summary("Thiruvananthapuram", "Kerala")
    
    if 'error' not in summary:
        print(f"Current Temperature: {summary['current_weather']['temperature']}°C")
        print(f"Current Humidity: {summary['current_weather']['humidity']}%")
        print(f"Weather Description: {summary['current_weather']['description']}")
        print(f"Season: {summary['analysis']['season']}")
        
        print("\nFarming Recommendations:")
        for category, recs in summary['farming_recommendations'].items():
            if recs:
                print(f"\n{category.title()}:")
                for rec in recs:
                    print(f"  - {rec}")
        
        print(f"\nActive Alerts: {len(summary['alerts'])}")
        for alert in summary['alerts']:
            print(f"  - {alert['type']}: {alert['description']}")
    else:
        print(f"Error: {summary['error']}")
