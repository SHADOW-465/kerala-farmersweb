# Kerala Farming Assistant - Complete Setup Guide

This guide will help you set up the complete Kerala Farming Assistant application with FastAPI backend, Next.js frontend, and Supabase database integration.

## 🏗️ Architecture Overview

- **Frontend**: Next.js 14 with TypeScript, shadcn/ui components
- **Backend**: FastAPI with Python
- **Database**: Supabase (PostgreSQL)
- **AI/ML**: Hugging Face models for disease detection and chatbot
- **Weather**: OpenWeatherMap API
- **Deployment**: Vercel (frontend) + Railway/Render (backend)

## 📋 Prerequisites

- Node.js 18+ and npm/pnpm
- Python 3.8+
- Supabase account
- Hugging Face account
- OpenWeatherMap account

## 🚀 Quick Start

### 1. Clone and Setup Frontend

```bash
# Navigate to project root
cd keralafarm

# Install dependencies
npm install
# or
pnpm install

# Create environment file
cp .env.example .env.local
```

### 2. Setup Supabase Database

1. **Create Supabase Project**:
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Note down your project URL and anon key

2. **Run Database Schema**:
   - Go to SQL Editor in Supabase dashboard
   - Copy and paste the contents of `Backend/supabase_schema.sql`
   - Execute the SQL to create all tables and sample data

3. **Get Supabase Credentials**:
   - Project URL: `https://your-project-id.supabase.co`
   - Anon Key: Found in Settings > API

### 3. Setup Backend

```bash
# Navigate to backend directory
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env_example.txt .env

# Edit .env file with your API keys
```

### 4. Configure Environment Variables

**Backend (.env)**:
```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key

# API Keys
HUGGINGFACE_API_KEY=your_huggingface_api_key
OPENWEATHER_API_KEY=your_openweather_api_key

# Other settings
SECRET_KEY=your_secret_key_here
ENVIRONMENT=development
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 5. Get API Keys

#### Hugging Face API Key
1. Go to [huggingface.co](https://huggingface.co)
2. Create account and go to Settings > Access Tokens
3. Create a new token with read access

#### OpenWeatherMap API Key
1. Go to [openweathermap.org](https://openweathermap.org)
2. Sign up for free account
3. Go to API keys section
4. Copy your API key

## 🏃‍♂️ Running the Application

### Start Backend Server

```bash
cd Backend
python main_api_server.py
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/api/docs`
- Health Check: `http://localhost:8000/health`

### Start Frontend Development Server

```bash
# In project root
npm run dev
# or
pnpm dev
```

The frontend will be available at `http://localhost:3000`

## 🧪 Testing the Integration

### 1. Test Backend API

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test disease detection (with base64 image)
curl -X POST "http://localhost:8000/api/disease-detection" \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "your_base64_image_data"}'

# Test crop recommendations
curl -X POST "http://localhost:8000/api/crop-recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "ph": 6.0,
    "nitrogen": 80,
    "phosphorus": 45,
    "potassium": 70,
    "rainfall": 1500,
    "temperature": 26,
    "soil_type": "Laterite",
    "season": "Kharif"
  }'
```

### 2. Test Frontend Features

1. **Disease Detection**: Upload a plant image and see AI analysis
2. **Crop Recommendations**: Fill soil analysis form and get recommendations
3. **Weather Analytics**: Enter a Kerala city and view weather data
4. **AI Chatbot**: Ask farming questions in multiple languages

## 📁 Project Structure

```
keralafarm/
├── app/                          # Next.js app directory
│   ├── chat/                    # Chat page
│   ├── crop-recommendations/    # Crop recommendations page
│   ├── disease-detection/       # Disease detection page
│   ├── farm-management/         # Farm management page
│   ├── weather/                 # Weather analytics page
│   └── community/               # Community page
├── components/                   # React components
│   ├── chat/                   # Chat components
│   ├── crop-recommendations/   # Crop recommendation components
│   ├── disease-detection/      # Disease detection components
│   ├── farm-management/        # Farm management components
│   ├── weather/                # Weather components
│   └── ui/                     # shadcn/ui components
├── lib/                        # Utility libraries
│   └── api-client.ts           # API client for backend communication
├── Backend/                    # FastAPI backend
│   ├── main_api_server.py      # Main FastAPI application
│   ├── supabase_client.py      # Supabase client configuration
│   ├── database_operations.py  # Database operations
│   ├── supabase_schema.sql     # Database schema
│   ├── disease_detection.py    # Disease detection module
│   ├── crop_recommendation.py  # Crop recommendation module
│   ├── ai_chatbot.py          # AI chatbot module
│   ├── weather_analytics.py   # Weather analytics module
│   └── requirements.txt       # Python dependencies
└── public/                     # Static assets
```

## 🔧 Key Features Implemented

### 1. AI Disease Detection
- Upload plant images for instant disease identification
- Uses Hugging Face models for accurate detection
- Provides treatment and prevention recommendations
- Saves detection history to database

### 2. Smart Crop Recommendations
- ML-based crop suggestions for Kerala farmers
- Considers soil conditions, climate, and market factors
- Provides detailed crop information and profitability analysis
- Seasonal planting recommendations

### 3. AI Chatbot Assistant
- Multilingual support (English, Malayalam, Tamil, Hindi)
- Natural language processing for farming queries
- Context-aware responses
- Integration with farming knowledge base

### 4. Weather Analytics
- Real-time weather data for Kerala cities
- 7-day weather forecasts
- Farming-specific weather recommendations
- Weather alerts and warnings

### 5. Farm Management
- Farm profile creation and management
- Crop tracking and analytics
- Soil test record keeping
- Performance metrics and insights

### 6. Community Features
- Q&A forum for farmers
- Knowledge sharing platform
- Expert advice and best practices
- Government scheme information

## 🚀 Deployment

### Frontend Deployment (Vercel)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy automatically

### Backend Deployment (Railway/Render)

1. Connect GitHub repository
2. Set environment variables
3. Deploy with automatic builds

### Database (Supabase)

- Already hosted on Supabase cloud
- No additional deployment needed

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Errors**:
   - Check if backend server is running on port 8000
   - Verify API URL in frontend environment variables
   - Check CORS settings in backend

2. **Database Connection Errors**:
   - Verify Supabase URL and API key
   - Check if database schema is properly set up
   - Ensure RLS policies are configured

3. **AI Model Errors**:
   - Verify Hugging Face API key
   - Check if models are accessible
   - Monitor API rate limits

4. **Weather API Errors**:
   - Verify OpenWeatherMap API key
   - Check API quota and limits
   - Ensure city names are correct

### Debug Mode

Enable debug logging by setting:
```env
LOG_LEVEL=DEBUG
```

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review API documentation

---

**Built with ❤️ for Kerala Farmers**

This application is designed to help Kerala farmers with AI-powered agricultural assistance, disease detection, crop recommendations, and community support.
