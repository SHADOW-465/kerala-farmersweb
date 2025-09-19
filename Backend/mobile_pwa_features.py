"""
Mobile-First Enhancements and PWA Features
Provides mobile-optimized features and Progressive Web App functionality
"""

import json
import sqlite3
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
import base64
import hashlib
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PWAConfig:
    """PWA configuration structure"""
    app_name: str
    short_name: str
    description: str
    version: str
    theme_color: str
    background_color: str
    display: str
    orientation: str
    start_url: str
    scope: str
    icons: List[Dict[str, str]]
    screenshots: List[Dict[str, str]]
    categories: List[str]
    lang: str
    dir: str

@dataclass
class OfflineData:
    """Offline data structure"""
    data_id: str
    data_type: str
    content: Dict[str, Any]
    last_updated: datetime
    sync_status: str  # synced, pending, failed
    priority: int

@dataclass
class PushNotification:
    """Push notification structure"""
    notification_id: str
    user_id: str
    title: str
    body: str
    icon: str
    badge: str
    data: Dict[str, Any]
    scheduled_time: Optional[datetime]
    sent_time: Optional[datetime]
    status: str  # pending, sent, failed

class MobilePWAFeatures:
    """
    Mobile-first enhancements and PWA features for farmers' platform
    """
    
    def __init__(self, db_path: str = "mobile_pwa.db"):
        """
        Initialize mobile PWA features
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.pwa_config = self._get_default_pwa_config()
        self.init_database()
        self.init_offline_storage()
    
    def _get_default_pwa_config(self) -> PWAConfig:
        """Get default PWA configuration"""
        return PWAConfig(
            app_name="FarmersHub - AI Farming Assistant",
            short_name="FarmersHub",
            description="AI-powered farming assistant for Kerala farmers with disease detection, crop recommendations, and market insights",
            version="1.0.0",
            theme_color="#2E8B57",
            background_color="#FFFFFF",
            display="standalone",
            orientation="portrait",
            start_url="/",
            scope="/",
            icons=[
                {
                    "src": "/icons/icon-72x72.png",
                    "sizes": "72x72",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/icons/icon-96x96.png",
                    "sizes": "96x96",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/icons/icon-128x128.png",
                    "sizes": "128x128",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/icons/icon-144x144.png",
                    "sizes": "144x144",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/icons/icon-152x152.png",
                    "sizes": "152x152",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/icons/icon-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/icons/icon-384x384.png",
                    "sizes": "384x384",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/icons/icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ],
            screenshots=[
                {
                    "src": "/screenshots/mobile-home.png",
                    "sizes": "390x844",
                    "type": "image/png",
                    "form_factor": "narrow"
                },
                {
                    "src": "/screenshots/tablet-home.png",
                    "sizes": "768x1024",
                    "type": "image/png",
                    "form_factor": "wide"
                }
            ],
            categories=["agriculture", "productivity", "utilities"],
            lang="en",
            dir="ltr"
        )
    
    def init_database(self):
        """Initialize database for mobile PWA features"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Offline data table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS offline_data (
                        data_id TEXT PRIMARY KEY,
                        data_type TEXT NOT NULL,
                        content TEXT NOT NULL,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        sync_status TEXT DEFAULT 'pending',
                        priority INTEGER DEFAULT 1
                    )
                ''')
                
                # Push notifications table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS push_notifications (
                        notification_id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        title TEXT NOT NULL,
                        body TEXT NOT NULL,
                        icon TEXT,
                        badge TEXT,
                        data TEXT,
                        scheduled_time TIMESTAMP,
                        sent_time TIMESTAMP,
                        status TEXT DEFAULT 'pending'
                    )
                ''')
                
                # User preferences table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        user_id TEXT PRIMARY KEY,
                        theme TEXT DEFAULT 'light',
                        language TEXT DEFAULT 'en',
                        notifications_enabled BOOLEAN DEFAULT 1,
                        offline_mode BOOLEAN DEFAULT 1,
                        data_sync_frequency TEXT DEFAULT 'daily',
                        push_notifications BOOLEAN DEFAULT 1,
                        location_sharing BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # App usage analytics table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS app_usage_analytics (
                        session_id TEXT PRIMARY KEY,
                        user_id TEXT,
                        device_type TEXT,
                        screen_resolution TEXT,
                        user_agent TEXT,
                        session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        session_end TIMESTAMP,
                        pages_visited TEXT,
                        features_used TEXT,
                        offline_usage BOOLEAN DEFAULT 0
                    )
                ''')
                
                conn.commit()
                logger.info("Mobile PWA database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing mobile PWA database: {str(e)}")
            raise
    
    def init_offline_storage(self):
        """Initialize offline storage with essential data"""
        try:
            # Essential offline data for farmers
            offline_data = [
                {
                    'data_type': 'crop_database',
                    'content': {
                        'rice': {
                            'name': 'Rice',
                            'scientific_name': 'Oryza sativa',
                            'growing_season': 'Kharif, Rabi',
                            'water_requirement': 'High',
                            'soil_type': 'Clay, Loam',
                            'ph_range': '5.0-6.5',
                            'common_diseases': ['Blast', 'Bacterial Blight', 'Brown Spot'],
                            'common_pests': ['Stem Borer', 'Leaf Folder', 'Brown Plant Hopper']
                        },
                        'coconut': {
                            'name': 'Coconut',
                            'scientific_name': 'Cocos nucifera',
                            'growing_season': 'Year-round',
                            'water_requirement': 'Moderate',
                            'soil_type': 'Sandy, Loam, Laterite',
                            'ph_range': '5.2-8.0',
                            'common_diseases': ['Bud Rot', 'Leaf Spot', 'Root Wilt'],
                            'common_pests': ['Rhinoceros Beetle', 'Red Palm Weevil', 'Coconut Mite']
                        }
                    }
                },
                {
                    'data_type': 'weather_patterns',
                    'content': {
                        'monsoon': {
                            'months': [6, 7, 8, 9, 10],
                            'characteristics': 'Heavy rainfall, high humidity',
                            'farming_activities': 'Planting, transplanting',
                            'precautions': 'Drainage, pest control'
                        },
                        'winter': {
                            'months': [11, 12, 1, 2],
                            'characteristics': 'Cool, dry weather',
                            'farming_activities': 'Harvesting, land preparation',
                            'precautions': 'Frost protection, irrigation'
                        }
                    }
                },
                {
                    'data_type': 'emergency_contacts',
                    'content': {
                        'agriculture_department': {
                            'phone': '1800-180-1551',
                            'email': 'agri@kerala.gov.in',
                            'description': 'Kerala Agriculture Department'
                        },
                        'weather_helpline': {
                            'phone': '1800-180-1551',
                            'email': 'weather@kerala.gov.in',
                            'description': 'Weather Information Service'
                        },
                        'crop_insurance': {
                            'phone': '1800-180-1551',
                            'email': 'insurance@kerala.gov.in',
                            'description': 'Crop Insurance Helpline'
                        }
                    }
                }
            ]
            
            # Store offline data
            for data in offline_data:
                self.store_offline_data(data['data_type'], data['content'])
            
            logger.info("Offline storage initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing offline storage: {str(e)}")
    
    def generate_manifest(self) -> Dict[str, Any]:
        """Generate PWA manifest file"""
        return {
            "name": self.pwa_config.app_name,
            "short_name": self.pwa_config.short_name,
            "description": self.pwa_config.description,
            "version": self.pwa_config.version,
            "theme_color": self.pwa_config.theme_color,
            "background_color": self.pwa_config.background_color,
            "display": self.pwa_config.display,
            "orientation": self.pwa_config.orientation,
            "start_url": self.pwa_config.start_url,
            "scope": self.pwa_config.scope,
            "icons": self.pwa_config.icons,
            "screenshots": self.pwa_config.screenshots,
            "categories": self.pwa_config.categories,
            "lang": self.pwa_config.lang,
            "dir": self.pwa_config.dir,
            "shortcuts": [
                {
                    "name": "Disease Detection",
                    "short_name": "Disease",
                    "description": "Detect plant diseases using AI",
                    "url": "/disease-detection",
                    "icons": [{"src": "/icons/disease-96x96.png", "sizes": "96x96"}]
                },
                {
                    "name": "Crop Recommendations",
                    "short_name": "Crops",
                    "description": "Get AI-powered crop recommendations",
                    "url": "/crop-recommendations",
                    "icons": [{"src": "/icons/crop-96x96.png", "sizes": "96x96"}]
                },
                {
                    "name": "Weather Forecast",
                    "short_name": "Weather",
                    "description": "Check weather conditions",
                    "url": "/weather",
                    "icons": [{"src": "/icons/weather-96x96.png", "sizes": "96x96"}]
                },
                {
                    "name": "Market Prices",
                    "short_name": "Prices",
                    "description": "Check current market prices",
                    "url": "/market-prices",
                    "icons": [{"src": "/icons/price-96x96.png", "sizes": "96x96"}]
                }
            ],
            "related_applications": [
                {
                    "platform": "play",
                    "url": "https://play.google.com/store/apps/details?id=com.farmershub.app",
                    "id": "com.farmershub.app"
                }
            ],
            "prefer_related_applications": False
        }
    
    def generate_service_worker(self) -> str:
        """Generate service worker code for offline functionality"""
        return """
// Service Worker for FarmersHub PWA
const CACHE_NAME = 'farmershub-v1.0.0';
const OFFLINE_URL = '/offline.html';

// Resources to cache
const CACHE_URLS = [
    '/',
    '/offline.html',
    '/static/css/main.css',
    '/static/js/main.js',
    '/static/images/logo.png',
    '/static/images/offline-icon.png',
    '/manifest.json',
    '/icons/icon-192x192.png',
    '/icons/icon-512x512.png'
];

// Install event
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Opened cache');
                return cache.addAll(CACHE_URLS);
            })
    );
});

// Fetch event
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Return cached version or fetch from network
                if (response) {
                    return response;
                }
                
                return fetch(event.request).then((response) => {
                    // Check if valid response
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }
                    
                    // Clone the response
                    const responseToCache = response.clone();
                    
                    caches.open(CACHE_NAME)
                        .then((cache) => {
                            cache.put(event.request, responseToCache);
                        });
                    
                    return response;
                }).catch(() => {
                    // Return offline page for navigation requests
                    if (event.request.mode === 'navigate') {
                        return caches.match(OFFLINE_URL);
                    }
                });
            })
    );
});

// Activate event
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Background sync for offline data
self.addEventListener('sync', (event) => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

// Push notification handling
self.addEventListener('push', (event) => {
    const options = {
        body: event.data ? event.data.text() : 'New notification from FarmersHub',
        icon: '/icons/icon-192x192.png',
        badge: '/icons/badge-72x72.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'View Details',
                icon: '/icons/checkmark.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/icons/xmark.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('FarmersHub', options)
    );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Background sync function
async function doBackgroundSync() {
    try {
        // Sync offline data when online
        const offlineData = await getOfflineData();
        for (const data of offlineData) {
            await syncOfflineData(data);
        }
    } catch (error) {
        console.error('Background sync failed:', error);
    }
}

// Helper functions
async function getOfflineData() {
    // Implementation to get offline data from IndexedDB
    return [];
}

async function syncOfflineData(data) {
    // Implementation to sync data with server
    console.log('Syncing data:', data);
}
"""
    
    def store_offline_data(self, data_type: str, content: Dict[str, Any]) -> str:
        """
        Store data for offline access
        
        Args:
            data_type: Type of data
            content: Data content
            
        Returns:
            Data ID
        """
        try:
            data_id = f"offline_{data_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO offline_data (
                        data_id, data_type, content, sync_status, priority
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    data_id,
                    data_type,
                    json.dumps(content),
                    'synced',
                    1
                ))
                
                conn.commit()
                logger.info(f"Offline data stored: {data_id}")
                return data_id
                
        except Exception as e:
            logger.error(f"Error storing offline data: {str(e)}")
            raise
    
    def get_offline_data(self, data_type: str) -> Optional[Dict[str, Any]]:
        """
        Get offline data by type
        
        Args:
            data_type: Type of data
            
        Returns:
            Data content or None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT content FROM offline_data 
                    WHERE data_type = ? 
                    ORDER BY last_updated DESC 
                    LIMIT 1
                ''', (data_type,))
                
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
                return None
                
        except Exception as e:
            logger.error(f"Error getting offline data: {str(e)}")
            return None
    
    def schedule_push_notification(self, user_id: str, title: str, body: str, 
                                 scheduled_time: datetime = None, data: Dict[str, Any] = None) -> str:
        """
        Schedule a push notification
        
        Args:
            user_id: User ID
            title: Notification title
            body: Notification body
            scheduled_time: When to send (default: immediately)
            data: Additional data
            
        Returns:
            Notification ID
        """
        try:
            notification_id = f"notif_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO push_notifications (
                        notification_id, user_id, title, body, data, scheduled_time, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    notification_id,
                    user_id,
                    title,
                    body,
                    json.dumps(data or {}),
                    scheduled_time or datetime.now(),
                    'pending'
                ))
                
                conn.commit()
                logger.info(f"Push notification scheduled: {notification_id}")
                return notification_id
                
        except Exception as e:
            logger.error(f"Error scheduling push notification: {str(e)}")
            raise
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM user_preferences WHERE user_id = ?', (user_id,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'user_id': row[0],
                        'theme': row[1],
                        'language': row[2],
                        'notifications_enabled': bool(row[3]),
                        'offline_mode': bool(row[4]),
                        'data_sync_frequency': row[5],
                        'push_notifications': bool(row[6]),
                        'location_sharing': bool(row[7])
                    }
                else:
                    # Return default preferences
                    return {
                        'user_id': user_id,
                        'theme': 'light',
                        'language': 'en',
                        'notifications_enabled': True,
                        'offline_mode': True,
                        'data_sync_frequency': 'daily',
                        'push_notifications': True,
                        'location_sharing': True
                    }
                
        except Exception as e:
            logger.error(f"Error getting user preferences: {str(e)}")
            return {}
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user preferences"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if preferences exist
                cursor.execute('SELECT user_id FROM user_preferences WHERE user_id = ?', (user_id,))
                exists = cursor.fetchone() is not None
                
                if exists:
                    # Update existing preferences
                    update_fields = []
                    values = []
                    
                    for key, value in preferences.items():
                        if key != 'user_id':
                            update_fields.append(f"{key} = ?")
                            values.append(value)
                    
                    if update_fields:
                        update_fields.append("updated_at = CURRENT_TIMESTAMP")
                        values.append(user_id)
                        
                        query = f"UPDATE user_preferences SET {', '.join(update_fields)} WHERE user_id = ?"
                        cursor.execute(query, values)
                else:
                    # Insert new preferences
                    cursor.execute('''
                        INSERT INTO user_preferences (
                            user_id, theme, language, notifications_enabled, offline_mode,
                            data_sync_frequency, push_notifications, location_sharing
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user_id,
                        preferences.get('theme', 'light'),
                        preferences.get('language', 'en'),
                        preferences.get('notifications_enabled', True),
                        preferences.get('offline_mode', True),
                        preferences.get('data_sync_frequency', 'daily'),
                        preferences.get('push_notifications', True),
                        preferences.get('location_sharing', True)
                    ))
                
                conn.commit()
                logger.info(f"User preferences updated: {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error updating user preferences: {str(e)}")
            return False
    
    def log_app_usage(self, user_id: str, device_info: Dict[str, Any], 
                     session_data: Dict[str, Any]) -> str:
        """
        Log app usage for analytics
        
        Args:
            user_id: User ID
            device_info: Device information
            session_data: Session data
            
        Returns:
            Session ID
        """
        try:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO app_usage_analytics (
                        session_id, user_id, device_type, screen_resolution,
                        user_agent, pages_visited, features_used, offline_usage
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_id,
                    user_id,
                    device_info.get('device_type', 'unknown'),
                    device_info.get('screen_resolution', 'unknown'),
                    device_info.get('user_agent', 'unknown'),
                    json.dumps(session_data.get('pages_visited', [])),
                    json.dumps(session_data.get('features_used', [])),
                    session_data.get('offline_usage', False)
                ))
                
                conn.commit()
                logger.info(f"App usage logged: {session_id}")
                return session_id
                
        except Exception as e:
            logger.error(f"Error logging app usage: {str(e)}")
            raise
    
    def get_mobile_optimized_data(self, data_type: str, user_id: str = None) -> Dict[str, Any]:
        """
        Get mobile-optimized data for specific features
        
        Args:
            data_type: Type of data to optimize
            user_id: User ID for personalization
            
        Returns:
            Mobile-optimized data
        """
        try:
            if data_type == 'crop_recommendations':
                return self._get_mobile_crop_data()
            elif data_type == 'weather_forecast':
                return self._get_mobile_weather_data()
            elif data_type == 'disease_detection':
                return self._get_mobile_disease_data()
            elif data_type == 'market_prices':
                return self._get_mobile_market_data()
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Error getting mobile optimized data: {str(e)}")
            return {}
    
    def _get_mobile_crop_data(self) -> Dict[str, Any]:
        """Get mobile-optimized crop data"""
        return {
            'crops': [
                {
                    'name': 'Rice',
                    'icon': '/icons/crops/rice.png',
                    'season': 'Kharif, Rabi',
                    'water_need': 'High',
                    'difficulty': 'Medium'
                },
                {
                    'name': 'Coconut',
                    'icon': '/icons/crops/coconut.png',
                    'season': 'Year-round',
                    'water_need': 'Moderate',
                    'difficulty': 'Easy'
                },
                {
                    'name': 'Pepper',
                    'icon': '/icons/crops/pepper.png',
                    'season': 'Year-round',
                    'water_need': 'Moderate',
                    'difficulty': 'Hard'
                }
            ],
            'quick_actions': [
                {
                    'title': 'Get Recommendations',
                    'icon': '/icons/actions/recommend.png',
                    'action': 'crop_recommendations'
                },
                {
                    'title': 'Check Soil Health',
                    'icon': '/icons/actions/soil.png',
                    'action': 'soil_health'
                }
            ]
        }
    
    def _get_mobile_weather_data(self) -> Dict[str, Any]:
        """Get mobile-optimized weather data"""
        return {
            'current': {
                'temperature': 28,
                'humidity': 75,
                'condition': 'Partly Cloudy',
                'icon': '/icons/weather/partly-cloudy.png'
            },
            'forecast': [
                {
                    'day': 'Today',
                    'high': 30,
                    'low': 25,
                    'condition': 'Sunny',
                    'icon': '/icons/weather/sunny.png'
                },
                {
                    'day': 'Tomorrow',
                    'high': 29,
                    'low': 24,
                    'condition': 'Rainy',
                    'icon': '/icons/weather/rainy.png'
                }
            ],
            'alerts': [
                {
                    'type': 'rain',
                    'message': 'Heavy rain expected tomorrow',
                    'severity': 'medium'
                }
            ]
        }
    
    def _get_mobile_disease_data(self) -> Dict[str, Any]:
        """Get mobile-optimized disease detection data"""
        return {
            'common_diseases': [
                {
                    'name': 'Rice Blast',
                    'symptoms': ['Brown spots on leaves', 'White lesions on stems'],
                    'severity': 'High',
                    'treatment': 'Fungicide application'
                },
                {
                    'name': 'Coconut Bud Rot',
                    'symptoms': ['Yellowing fronds', 'Soft bud tissue'],
                    'severity': 'High',
                    'treatment': 'Copper fungicide'
                }
            ],
            'quick_actions': [
                {
                    'title': 'Take Photo',
                    'icon': '/icons/actions/camera.png',
                    'action': 'camera'
                },
                {
                    'title': 'Browse Gallery',
                    'icon': '/icons/actions/gallery.png',
                    'action': 'gallery'
                }
            ]
        }
    
    def _get_mobile_market_data(self) -> Dict[str, Any]:
        """Get mobile-optimized market data"""
        return {
            'prices': [
                {
                    'crop': 'Rice',
                    'price': '₹30/kg',
                    'change': '+2%',
                    'trend': 'up'
                },
                {
                    'crop': 'Coconut',
                    'price': '₹18/kg',
                    'change': '-1%',
                    'trend': 'down'
                }
            ],
            'markets': [
                {
                    'name': 'Thiruvananthapuram Market',
                    'distance': '5 km',
                    'rating': 4.5
                }
            ]
        }
    
    def generate_offline_page(self) -> str:
        """Generate offline page HTML"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FarmersHub - Offline</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #2E8B57, #3CB371);
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .offline-icon {
            width: 100px;
            height: 100px;
            margin-bottom: 20px;
            opacity: 0.8;
        }
        h1 {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        p {
            font-size: 1.1rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        .retry-btn {
            background: white;
            color: #2E8B57;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .retry-btn:hover {
            transform: scale(1.05);
        }
        .features {
            margin-top: 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            max-width: 600px;
        }
        .feature {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .feature h3 {
            margin: 0 0 10px 0;
            font-size: 1.2rem;
        }
        .feature p {
            margin: 0;
            font-size: 0.9rem;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <img src="/icons/offline-icon.png" alt="Offline" class="offline-icon">
    <h1>You're Offline</h1>
    <p>Don't worry! You can still access some features of FarmersHub.</p>
    <button class="retry-btn" onclick="window.location.reload()">Try Again</button>
    
    <div class="features">
        <div class="feature">
            <h3>📱 Offline Features</h3>
            <p>Access your saved data and basic information</p>
        </div>
        <div class="feature">
            <h3>🌾 Crop Database</h3>
            <p>Browse crop information and growing guides</p>
        </div>
        <div class="feature">
            <h3>📞 Emergency Contacts</h3>
            <p>Access important helpline numbers</p>
        </div>
        <div class="feature">
            <h3>💾 Data Sync</h3>
            <p>Your data will sync when you're back online</p>
        </div>
    </div>
    
    <script>
        // Check for online status
        window.addEventListener('online', () => {
            window.location.reload();
        });
        
        // Retry connection every 30 seconds
        setInterval(() => {
            if (navigator.onLine) {
                window.location.reload();
            }
        }, 30000);
    </script>
</body>
</html>
"""
    
    def get_pwa_analytics(self) -> Dict[str, Any]:
        """Get PWA usage analytics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total sessions
                cursor.execute('SELECT COUNT(*) FROM app_usage_analytics')
                total_sessions = cursor.fetchone()[0]
                
                # Offline usage
                cursor.execute('SELECT COUNT(*) FROM app_usage_analytics WHERE offline_usage = 1')
                offline_sessions = cursor.fetchone()[0]
                
                # Device types
                cursor.execute('''
                    SELECT device_type, COUNT(*) as count 
                    FROM app_usage_analytics 
                    GROUP BY device_type
                ''')
                device_types = dict(cursor.fetchall())
                
                # Most used features
                cursor.execute('SELECT features_used FROM app_usage_analytics')
                all_features = []
                for row in cursor.fetchall():
                    features = json.loads(row[0])
                    all_features.extend(features)
                
                feature_counts = {}
                for feature in all_features:
                    feature_counts[feature] = feature_counts.get(feature, 0) + 1
                
                return {
                    'total_sessions': total_sessions,
                    'offline_sessions': offline_sessions,
                    'offline_usage_percentage': (offline_sessions / total_sessions * 100) if total_sessions > 0 else 0,
                    'device_types': device_types,
                    'popular_features': sorted(feature_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                }
                
        except Exception as e:
            logger.error(f"Error getting PWA analytics: {str(e)}")
            return {}

# Example usage and testing
if __name__ == "__main__":
    # Initialize mobile PWA features
    mobile_pwa = MobilePWAFeatures()
    
    print("Mobile PWA Features - Test Results")
    print("=" * 50)
    
    # Generate PWA manifest
    manifest = mobile_pwa.generate_manifest()
    print("PWA Manifest generated:")
    print(f"App Name: {manifest['name']}")
    print(f"Version: {manifest['version']}")
    print(f"Theme Color: {manifest['theme_color']}")
    print(f"Shortcuts: {len(manifest['shortcuts'])}")
    
    # Test offline data storage
    test_data = {
        'crop_info': {
            'rice': 'Staple food crop requiring high water',
            'coconut': 'Important cash crop in Kerala'
        }
    }
    
    data_id = mobile_pwa.store_offline_data('test_crop_info', test_data)
    print(f"\nOffline data stored: {data_id}")
    
    # Retrieve offline data
    retrieved_data = mobile_pwa.get_offline_data('test_crop_info')
    print(f"Retrieved data: {retrieved_data}")
    
    # Test push notification
    notification_id = mobile_pwa.schedule_push_notification(
        'user_123',
        'Weather Alert',
        'Heavy rain expected tomorrow. Take necessary precautions.',
        data={'type': 'weather_alert', 'severity': 'high'}
    )
    print(f"\nPush notification scheduled: {notification_id}")
    
    # Test user preferences
    preferences = {
        'theme': 'dark',
        'language': 'ml',
        'notifications_enabled': True,
        'offline_mode': True
    }
    
    mobile_pwa.update_user_preferences('user_123', preferences)
    user_prefs = mobile_pwa.get_user_preferences('user_123')
    print(f"\nUser preferences: {user_prefs}")
    
    # Test mobile optimized data
    mobile_crop_data = mobile_pwa.get_mobile_optimized_data('crop_recommendations')
    print(f"\nMobile crop data: {len(mobile_crop_data.get('crops', []))} crops")
    
    # Test app usage logging
    device_info = {
        'device_type': 'mobile',
        'screen_resolution': '390x844',
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
    }
    
    session_data = {
        'pages_visited': ['/home', '/crops', '/weather'],
        'features_used': ['disease_detection', 'crop_recommendations'],
        'offline_usage': False
    }
    
    session_id = mobile_pwa.log_app_usage('user_123', device_info, session_data)
    print(f"\nApp usage logged: {session_id}")
    
    # Get PWA analytics
    analytics = mobile_pwa.get_pwa_analytics()
    print(f"\nPWA Analytics:")
    print(f"Total Sessions: {analytics['total_sessions']}")
    print(f"Offline Usage: {analytics['offline_usage_percentage']:.1f}%")
    print(f"Device Types: {analytics['device_types']}")
    
    print("\nPWA features initialized successfully!")
