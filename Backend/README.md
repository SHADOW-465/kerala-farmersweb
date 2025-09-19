# FarmersHub - AI-Powered Farming Assistant

A comprehensive backend API system for Kerala farmers, providing AI-powered features for disease detection, crop recommendations, weather analytics, market predictions, and more.

## 🌾 Features

### Core AI Features (Priority 1)
- **AI-Powered Plant Disease Detection**: Upload plant images for instant disease identification using Hugging Face models
- **Smart Crop Recommendation Engine**: ML-based recommendations considering soil, climate, and market factors
- **AI Chatbot Assistant**: Multilingual support (English, Malayalam, Tamil, Hindi) for farming queries
- **Intelligent Weather Analytics**: 7-day forecasts, farming alerts, and irrigation suggestions
- **Personal Farm Profile & Analytics**: Track farm performance, crop history, and personalized insights

### Secondary Features (Priority 2)
- **Market Price Prediction**: Real-time price data and trend analysis for Kerala markets
- **Soil Health Assessment Tool**: AI analysis of soil test results with improvement recommendations
- **Smart Government Scheme Matcher**: AI-powered matching with relevant government schemes
- **Community Knowledge Sharing**: Q&A forum, best practices, and expert network
- **Mobile-First Enhancements**: PWA support, offline functionality, and voice input

### Nice-to-Have Features (Priority 3)
- **Basic IoT Integration**: Manual sensor data entry and analytics
- **Financial Planning Assistant**: Cost calculators, ROI predictions, and budget planning
- **Insurance Advisor**: Basic crop insurance recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/farmershub-backend.git
   cd farmershub-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env file with your API keys
   ```

5. **Run the application**
   ```bash
   python main_api_server.py
   ```

The API will be available at `http://localhost:8000`

## 📋 API Documentation

### Interactive API Docs
- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`

### Key Endpoints

#### Disease Detection
- `POST /api/disease-detection` - Detect plant disease from base64 image
- `POST /api/disease-detection/upload` - Detect disease from uploaded file

#### Crop Recommendations
- `POST /api/crop-recommendations` - Get AI-powered crop recommendations
- `GET /api/crops/{crop_name}` - Get detailed crop information

#### Weather Analytics
- `POST /api/weather/current` - Get current weather
- `POST /api/weather/forecast` - Get weather forecast
- `POST /api/weather/summary` - Get comprehensive weather summary

#### AI Chatbot
- `POST /api/chatbot` - Chat with AI assistant
- `GET /api/chatbot/languages` - Get supported languages

#### Farm Management
- `POST /api/farm-profiles` - Create farm profile
- `GET /api/farm-profiles/{farm_id}` - Get farm profile
- `GET /api/farm-profiles/{farm_id}/analytics` - Get farm analytics

#### Market Prices
- `GET /api/market-prices/predict/{crop_name}` - Predict crop prices
- `GET /api/market-prices/insights` - Get market insights

#### Soil Health
- `POST /api/soil-health/assess` - Assess soil health
- `POST /api/soil-health/crop-suitability` - Check crop suitability

#### Government Schemes
- `POST /api/government-schemes/match` - Match with schemes
- `GET /api/government-schemes/search` - Search schemes

#### Community
- `POST /api/community/questions` - Post question
- `GET /api/community/questions/search` - Search questions

#### Mobile PWA
- `GET /api/mobile/manifest` - Get PWA manifest
- `GET /api/mobile/service-worker` - Get service worker
- `GET /api/mobile/offline` - Get offline page

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HUGGINGFACE_API_KEY` | Hugging Face API key for AI models | Required |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///./farmershub.db` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ENVIRONMENT` | Environment (development/production) | `development` |

### Feature Flags

Enable/disable features using environment variables:

```bash
ENABLE_DISEASE_DETECTION=true
ENABLE_CROP_RECOMMENDATIONS=true
ENABLE_WEATHER_ANALYTICS=true
ENABLE_MARKET_PREDICTIONS=true
ENABLE_SOIL_HEALTH_ASSESSMENT=true
ENABLE_GOVERNMENT_SCHEMES=true
ENABLE_COMMUNITY_FEATURES=true
ENABLE_MOBILE_PWA=true
```

## 🏗️ Architecture

### Project Structure
```
farmershub-backend/
├── main_api_server.py          # Main FastAPI application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── env_example.txt            # Environment variables template
├── README.md                  # This file
├── disease_detection.py       # Plant disease detection module
├── crop_recommendation.py     # Crop recommendation engine
├── ai_chatbot.py             # AI chatbot assistant
├── weather_analytics.py      # Weather analytics system
├── farm_profile.py           # Farm profile management
├── market_price_prediction.py # Market price prediction
├── soil_health_assessment.py  # Soil health assessment
├── government_scheme_matcher.py # Government scheme matching
├── community_knowledge.py    # Community knowledge sharing
├── mobile_pwa_features.py    # Mobile PWA features
└── static/                   # Static files for PWA
```

### Technology Stack

- **Backend Framework**: FastAPI
- **Database**: SQLite (development), PostgreSQL (production)
- **AI/ML**: Hugging Face Transformers, Scikit-learn
- **Image Processing**: OpenCV, Pillow
- **Weather API**: OpenWeatherMap
- **Caching**: Redis (optional)
- **Task Queue**: Celery (optional)

## 🤖 AI Models Used

### Disease Detection
- **Primary Model**: `linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification`
- **Fallback Model**: `microsoft/resnet-50`

### Chatbot
- **English**: `microsoft/DialoGPT-medium`
- **Multilingual**: `ai4bharat/indic-bert`

### Crop Recommendations
- **Algorithm**: Random Forest, Gradient Boosting
- **Features**: Soil pH, nutrients, weather, market demand

## 📱 Mobile PWA Support

The API includes comprehensive PWA support:

- **Manifest**: Auto-generated PWA manifest
- **Service Worker**: Offline functionality and caching
- **Offline Page**: Custom offline experience
- **Push Notifications**: Weather and price alerts
- **Mobile Optimization**: Responsive data formats

## 🔒 Security

- **CORS**: Configurable cross-origin resource sharing
- **Rate Limiting**: Built-in request rate limiting
- **Input Validation**: Pydantic models for request validation
- **File Upload**: Secure file upload with type validation
- **API Keys**: Environment-based API key management

## 📊 Monitoring & Analytics

- **Health Check**: `/health` endpoint
- **Usage Analytics**: Built-in usage tracking
- **Error Reporting**: Comprehensive error logging
- **Performance Metrics**: Request timing and caching stats

## 🧪 Testing

Run tests with pytest:

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## 🚀 Deployment

### Development
```bash
python main_api_server.py
```

### Production
```bash
# Using Gunicorn
gunicorn main_api_server:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker build -t farmershub-api .
docker run -p 8000:8000 farmershub-api
```

### Environment Setup
1. Set production environment variables
2. Configure database (PostgreSQL recommended)
3. Set up Redis for caching (optional)
4. Configure reverse proxy (Nginx)
5. Set up SSL certificates
6. Configure monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for providing free AI models
- **OpenWeatherMap** for weather data
- **Kerala Agriculture Department** for farming data
- **FastAPI** for the excellent web framework
- **Scikit-learn** for machine learning tools

## 📞 Support

For support and questions:
- **Email**: support@farmershub.app
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/farmershub-backend/issues)
- **Documentation**: [API Docs](http://localhost:8000/api/docs)

## 🔮 Roadmap

### Phase 1 (Completed)
- ✅ Core AI features implementation
- ✅ API server setup
- ✅ Database integration
- ✅ Mobile PWA support

### Phase 2 (In Progress)
- 🔄 Advanced ML models
- 🔄 Real-time notifications
- 🔄 Advanced analytics
- 🔄 Performance optimization

### Phase 3 (Planned)
- 📋 IoT sensor integration
- 📋 Advanced financial tools
- 📋 Blockchain integration
- 📋 Multi-language expansion

---

**Built with ❤️ for Kerala Farmers**


AI-Powered Personal Farming Assistant for Kerala Farmers - V0 WebApp Prompt
Project Overview
Build a comprehensive AI-powered farming assistant web application specifically designed for Kerala farmers. This platform combines machine learning, real-time data analytics, and user-friendly interfaces to revolutionize agricultural practices in Kerala.
Core Features to Implement
1. AI Plant Disease Detection System

Image Upload Interface: Drag-and-drop file upload component for plant/crop images
Real-time Disease Classification: Integration with Hugging Face API for plant disease detection
Treatment Recommendations: Dynamic treatment suggestions based on detected diseases
Confidence Score Visualization: Progress bars and confidence indicators
Disease History Tracking: Store and track past disease detections per farm

2. Smart Crop Recommendation Engine

Multi-factor Input Form: pH, soil type, nutrients (NPK), rainfall, temperature, season
ML-based Recommendations: Algorithm considering Kerala-specific crops (rice, coconut, pepper, cardamom, rubber, tea, coffee, banana, ginger, turmeric)
Suitability Scoring: Visual score cards with color-coded recommendations
Seasonal Calendar: Interactive crop planting timeline
Market Demand Integration: Consider current market prices in recommendations

3. AI Chatbot Assistant

Chat Interface: Modern chat UI with message bubbles
Natural Language Processing: Handle farming queries in multiple languages
Quick Action Buttons: Pre-defined common questions
Voice Input: Speech-to-text functionality
Expert Escalation: Hand-off to human experts when needed
Chat History: Persistent conversation tracking

4. Weather Analytics Dashboard

7-Day Forecast: Weather cards with icons and detailed metrics
Farm-specific Alerts: Location-based notifications
Irrigation Recommendations: Smart watering suggestions
Pest/Disease Risk Warnings: Weather-based risk indicators
Historical Weather Data: Charts and trends

5. Personal Farm Management

Farm Registration: Multi-step onboarding form
Crop History Timeline: Visual crop rotation tracking
Yield Analytics: Interactive charts and performance metrics
Personalized Dashboard: Customized widgets based on farm data
Photo Documentation: Before/after crop growth images

6. Market Price Intelligence

Real-time Price Dashboard: Live price feeds from Kerala markets
Price Trend Charts: Historical price analysis with Chart.js
Best Selling Time Predictor: AI-powered timing recommendations
Market Locator: Interactive map of nearby markets
Price Alerts: Notification system for price targets

7. Soil Health Assessment

Soil Test Data Input: Form for lab test results
Nutrient Deficiency Analysis: Visual health indicators
Custom Fertilizer Recommendations: NPK calculator
Soil Health Score: Overall rating with improvement tips
Test Reminder System: Scheduled soil testing notifications

8. Government Scheme Matcher

Eligibility Checker: Dynamic form-based qualification assessment
Scheme Recommendation Cards: Visual scheme suggestions
Application Assistant: Step-by-step application guidance
Document Manager: Upload and track required documents
Application Status Tracker: Progress monitoring system

9. Community Platform

Q&A Forum: Question and answer interface
Success Stories: Blog-style success case studies
Expert Network: Directory of agricultural extension officers
Knowledge Base: Searchable farming tips and techniques
Farmer Profiles: Community member profiles and connections

10. Mobile-First Design

Progressive Web App: Offline functionality with service workers
Responsive Layout: Mobile-optimized interface
Camera Integration: Native camera access for plant photos
Voice Commands: Speech recognition for hands-free operation
Push Notifications: Real-time alerts and reminders

Technical Architecture
Frontend Stack

Framework: Next.js 14 with TypeScript
UI Components: shadcn/ui component library
Styling: Tailwind CSS for responsive design
State Management: Zustand for global state
Forms: React Hook Form with Zod validation
Charts: Chart.js and Recharts for data visualization
Maps: Mapbox or Google Maps integration
PWA: Next.js PWA plugin for offline functionality

Backend Stack

API Framework: Node.js with Express.js or Next.js API routes
Database: PostgreSQL with Prisma ORM
Authentication: NextAuth.js with multiple providers
File Storage: AWS S3 or Cloudinary for image uploads
Caching: Redis for session and API caching
Queue System: Bull.js for background job processing

AI/ML Integration

Disease Detection: Hugging Face Inference API
Crop Recommendation: Custom ML model with scikit-learn
Chatbot: OpenAI API or Google Dialogflow
Image Processing: Sharp.js for image optimization
Weather API: OpenWeatherMap or AccuWeather

Database Schema
Users Table
sql- id (UUID primary key)
- email (unique)
- name
- phone
- preferred_language (enum)
- created_at
- updated_at
Farms Table
sql- id (UUID primary key)
- user_id (foreign key)
- name
- location (coordinates)
- area_acres
- soil_type
- created_at
- updated_at
Crops Table
sql- id (UUID primary key)
- farm_id (foreign key)
- crop_name
- planting_date
- expected_harvest
- area_acres
- status (planted/growing/harvested)
- yield_actual
- created_at
Disease_Detections Table
sql- id (UUID primary key)
- farm_id (foreign key)
- crop_id (foreign key)
- image_url
- disease_name
- confidence_score
- treatment_applied
- detection_date
Soil_Tests Table
sql- id (UUID primary key)
- farm_id (foreign key)
- ph_level
- nitrogen
- phosphorus
- potassium
- organic_matter
- test_date
- recommendations
Market_Prices Table
sql- id (UUID primary key)
- crop_name
- market_location
- price_per_kg
- date
- source
Chat_Sessions Table
sql- id (UUID primary key)
- user_id (foreign key)
- messages (JSONB)
- created_at
- updated_at
Key Pages and Layouts
1. Dashboard Layout

Sidebar Navigation: Collapsible menu with feature icons
Header: User profile, notifications, language selector
Main Content Area: Grid-based widget layout
Quick Actions: Floating action button for common tasks

2. Disease Detection Page

Image Upload Area: Drag-and-drop with preview
Results Display: Disease name, confidence, treatment cards
History Section: Past detections with filtering
Export Options: PDF reports and image downloads

3. Crop Recommendation Page

Input Form: Multi-step wizard with validation
Results Dashboard: Score cards with visual indicators
Comparison Table: Side-by-side crop analysis
Save Options: Bookmark recommendations

4. Weather Dashboard

Current Weather Card: Large display with key metrics
7-Day Forecast: Horizontal scroll cards
Alerts Section: Notification banners
Historical Charts: Interactive weather trends

5. Farm Management Page

Farm Overview: Statistics and quick metrics
Crop Calendar: Timeline view of planted crops
Performance Charts: Yield and profitability analysis
Photo Gallery: Crop progress documentation

6. Community Forum

Question Feed: Card-based layout with voting
Categories: Filterable topic tags
Expert Answers: Highlighted responses
Search Functionality: Full-text search with filters

Styling and UX Requirements
Design System

Color Palette: Green primary (#2E8B57), Earth tones, High contrast
Typography: Inter font family, Clear hierarchy
Spacing: 8px grid system
Shadows: Subtle depth with box-shadows
Border Radius: 8px for cards, 4px for buttons

Responsive Breakpoints

Mobile: 320px - 768px
Tablet: 768px - 1024px
Desktop: 1024px+

Accessibility Features

WCAG 2.1 AA Compliance: Color contrast, keyboard navigation
Screen Reader Support: Semantic HTML, ARIA labels
Multi-language Support: i18n with English, Malayalam, Tamil, Hindi
Offline Functionality: Service worker for core features

Performance Requirements

Page Load Time: < 3 seconds on 3G networks
Image Optimization: WebP format with fallbacks
Database Queries: Optimized with indexing and caching
API Response Time: < 500ms for core endpoints
Lighthouse Score: > 90 for Performance, Accessibility, SEO

Security Implementation

Authentication: JWT tokens with refresh mechanism
Data Encryption: TLS 1.3 for data in transit
Input Validation: Server-side validation for all inputs
File Upload Security: Type validation and malware scanning
Rate Limiting: API endpoint protection
GDPR Compliance: Data privacy and user consent

Deployment Configuration

Hosting: Vercel or AWS with CDN
Database: PostgreSQL on AWS RDS or Supabase
Environment Variables: Secure API key management
Monitoring: Error tracking with Sentry
Analytics: User behavior tracking with privacy focus
CI/CD: GitHub Actions for automated deployment

Success Metrics

User Engagement: 5+ page views per session
Feature Adoption: 80% users try disease detection
AI Accuracy: >85% disease detection accuracy
Response Time: <2 seconds for AI predictions
User Retention: 60% monthly active users
Mobile Usage: 70% traffic from mobile devices

Additional Integrations

Payment Gateway: For premium features (Razorpay/Stripe)
SMS Service: OTP and alerts (Twilio)
Email Service: Notifications (SendGrid)
Maps API: Location services (Google Maps)
Weather API: Real-time data (OpenWeatherMap)
Translation API: Multi-language support (Google Translate)

Build this as a modern, scalable, and user-friendly web application that can serve thousands of Kerala farmers with reliable AI-powered agricultural assistance.


Feature list:
MVP Core Features (Priority 1 - Must Have)
1. AI-Powered Plant Disease Detection

Image Upload Feature: Allow farmers to upload photos of crops/leaves
Disease Classification Model: Pre-trained CNN model to identify common Kerala crop diseases
Treatment Recommendations: Automated suggestions for identified diseases
Confidence Score Display: Show prediction accuracy to build trust

2. Smart Crop Recommendation Engine

Enhanced Algorithm: Replace basic pH logic with ML-based recommendations
Multi-factor Analysis: Consider soil type, climate, season, market demand
Kerala-Specific Crops: Focus on rice, coconut, spices, vegetables
Seasonal Recommendations: Time-based crop suggestions

3. AI Chatbot Assistant

Basic NLP Integration: Simple question-answering system
Multilingual Support: English, Malayalam, Tamil, Hindi
Common Query Handling: Weather, crop care, disease symptoms
Fallback to Human Expert: When AI can't answer

4. Intelligent Weather Analytics

7-Day Forecast: Enhanced weather predictions
Farm-Specific Alerts: Weather-based farming recommendations
Irrigation Suggestions: Water management based on weather
Pest/Disease Warnings: Weather-related risk alerts

5. Personal Farm Profile & Analytics

Farm Registration: Detailed farm information collection
Crop History Tracking: Record past crops and outcomes
Performance Analytics: Yield trends and insights
Personalized Dashboard: Customized recommendations based on farm data

MVP Secondary Features (Priority 2 - Should Have)
6. Market Price Prediction

Real-time Price Data: Live market prices from major Kerala markets
Price Trend Analysis: Historical price charts and patterns
Best Selling Time Predictions: When to sell for maximum profit
Nearby Market Locator: Find best markets to sell produce

7. Soil Health Assessment Tool

Nutrient Deficiency Detection: AI analysis of soil test results
Fertilizer Recommendations: Customized NPK suggestions
Soil Health Score: Overall soil condition rating
Improvement Action Plan: Step-by-step soil enhancement guide

8. Smart Government Scheme Matcher

Eligibility Checker: AI determines which schemes farmer qualifies for
Application Assistance: Guided scheme application process
Document Checklist: Required documents for each scheme
Status Tracking: Track application progress

9. Community Knowledge Sharing

Farmer Q&A Forum: Peer-to-peer problem solving
Success Stories: Share and learn from successful farmers
Local Expert Network: Connect with agricultural extension officers
Best Practices Library: Curated farming tips and techniques

10. Mobile-First Enhancements

Progressive Web App (PWA): Offline functionality
Voice Input: Speech-to-text for queries
Camera Integration: Easy photo capture for disease detection
Push Notifications: Timely alerts and reminders

MVP Nice-to-Have Features (Priority 3 - Could Have)
11. Basic IoT Integration

Manual Sensor Data Entry: Input soil moisture, temperature readings
Simple Analytics: Basic charts and trends
Alert System: Notifications based on sensor thresholds

12. Financial Planning Assistant

Crop Cost Calculator: Estimate farming costs
ROI Predictions: Expected returns on investment
Budget Planner: Monthly farming budget management
Insurance Advisor: Basic crop insurance recommendations

Technical Implementation Priority for MVP
Phase 1 (2-3 weeks): Core AI Features

Plant disease detection model integration
Enhanced crop recommendation system
Basic AI chatbot implementation
Personal farm profile setup

Phase 2 (2-3 weeks): Data Intelligence

Weather analytics enhancement
Market price prediction system
Soil health assessment tool
Government scheme matcher

Phase 3 (1-2 weeks): User Experience

Community features
Mobile optimizations
Voice and camera integration
PWA implementation

Phase 4 (1 week): Polish & Testing

Performance optimization
User interface improvements
Testing and bug fixes
Demo preparation

Recommended Tech Stack for MVP
AI/ML Components:

TensorFlow Lite or PyTorch Mobile for plant disease detection
Scikit-learn for crop recommendation algorithms
Rasa or Dialogflow for chatbot functionality
OpenCV for image processing

Backend Services:

FastAPI or Flask for AI model serving
PostgreSQL for user and farm data
Redis for caching and real-time features
Celery for background tasks

Frontend Enhancements:

Streamlit (current) with custom components
JavaScript for camera and voice features
Service Workers for PWA functionality
WebRTC for real-time features

Success Metrics for MVP

AI Accuracy: >85% disease detection accuracy
User Engagement: Average 5+ interactions per session
Query Resolution: 70% of questions answered by AI
Feature Adoption: 80% users try disease detection
User Satisfaction: 4+ star rating from test users