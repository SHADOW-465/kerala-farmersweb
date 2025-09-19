# 🌾 Kerala Farming Assistant

A comprehensive AI-powered farming assistant designed specifically for Kerala farmers. This application provides intelligent crop recommendations, disease detection, weather analytics, and community support to help farmers make informed decisions.

## ✨ Features

### 🤖 AI-Powered Features
- **Plant Disease Detection**: Upload images to identify plant diseases with AI
- **Smart Crop Recommendations**: Get personalized crop suggestions based on soil and weather conditions
- **AI Chatbot**: Multilingual support (English, Malayalam, Tamil, Hindi) for farming queries
- **Weather Analytics**: Real-time weather data and farming recommendations

### 🏡 Farm Management
- **Farm Profile Management**: Create and manage multiple farm profiles
- **Crop Tracking**: Monitor crop growth and health
- **Expense Tracking**: Track farming expenses and budget
- **Harvest Records**: Record and analyze harvest data
- **Inventory Management**: Manage seeds, fertilizers, and equipment

### 🌐 Community Platform
- **Discussion Forum**: Ask questions and share knowledge
- **Expert Advice**: Connect with agricultural experts
- **Knowledge Sharing**: Access farming guides and best practices
- **Local Events**: Stay updated with agricultural events

### 📊 Market Intelligence
- **Price Predictions**: AI-powered crop price forecasting
- **Market Insights**: Real-time market trends and analysis
- **Government Schemes**: Find and apply for relevant schemes

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **UI Components**: shadcn/ui with Tailwind CSS
- **State Management**: React Hooks
- **Forms**: React Hook Form with Zod validation
- **Charts**: Recharts for data visualization
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **AI/ML**: Hugging Face Transformers, scikit-learn
- **Image Processing**: OpenCV, Pillow
- **Weather Data**: OpenWeatherMap API

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
# Double-click start_dev.bat or run in Command Prompt
start_dev.bat
```

**Linux/Mac:**
```bash
# Make executable and run
chmod +x start_dev.sh
./start_dev.sh
```

### Option 2: Manual Setup

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd keralafarm
```

#### 2. Setup Backend
```bash
cd Backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python run_server.py
```

#### 3. Setup Frontend
```bash
# In a new terminal
npm install
npm run dev
```

#### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the root directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

### Backend Configuration

Create a `.env` file in the `Backend` directory:
```env
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# API Keys (Optional - app works with mock data)
HUGGINGFACE_API_KEY=your_huggingface_key
OPENWEATHER_API_KEY=your_openweather_key

# Other settings
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## 📱 Mobile Support

The application is fully responsive and optimized for mobile devices. It includes:
- Progressive Web App (PWA) features
- Touch-friendly interface
- Offline capabilities
- Mobile-optimized forms

## 🌾 Kerala-Specific Features

### Crops Supported
- Rice (Kerala varieties)
- Coconut
- Black Pepper
- Cardamom
- Rubber
- Cashew
- Banana
- Tapioca

### Languages
- English
- Malayalam (മലയാളം)
- Tamil (தமிழ்)
- Hindi (हिन्दी)

### Regions
- Coastal Kerala
- Midland Kerala
- Highland Kerala

## 🔍 API Endpoints

### Disease Detection
- `POST /api/disease-detection` - Detect plant diseases from images
- `POST /api/disease-detection/upload` - Upload image file for detection

### Crop Recommendations
- `POST /api/crop-recommendations` - Get AI-powered crop suggestions
- `GET /api/crops/{crop_name}` - Get detailed crop information

### Weather Analytics
- `POST /api/weather/current` - Get current weather
- `POST /api/weather/forecast` - Get weather forecast
- `POST /api/weather/summary` - Get comprehensive weather summary

### AI Chatbot
- `POST /api/chatbot` - Chat with AI assistant
- `GET /api/chatbot/languages` - Get supported languages

### Farm Management
- `POST /api/farm-profiles` - Create farm profile
- `GET /api/farm-profiles/{farm_id}` - Get farm details
- `GET /api/farm-profiles/user/{user_id}` - Get user's farms
- `GET /api/farm-profiles/{farm_id}/analytics` - Get farm analytics

## 🧪 Testing

### Backend Testing
```bash
cd Backend
python -m pytest tests/
```

### Frontend Testing
```bash
npm run test
```

### API Testing
Visit http://localhost:8000/api/docs for interactive API documentation.

## 📦 Deployment

### Backend Deployment
1. Set up Supabase database
2. Configure environment variables
3. Deploy to your preferred platform (Railway, Heroku, etc.)

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy to Vercel, Netlify, or your preferred platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Basic AI features
- ✅ Farm management
- ✅ Community platform
- ✅ Mobile responsiveness

### Phase 2 (Planned)
- 🔄 Advanced AI models
- 🔄 Real-time notifications
- 🔄 Offline support
- 🔄 Advanced analytics

### Phase 3 (Future)
- 📋 IoT integration
- 📋 Drone support
- 📋 Blockchain integration
- 📋 Advanced ML models

---

**Built with ❤️ for Kerala Farmers**