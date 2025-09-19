# Kerala Farming Assistant - AI-Powered Agricultural Support

A comprehensive AI-powered farming assistant specifically designed for Kerala farmers, featuring disease detection, crop recommendations, weather analytics, and community support.

## 🌾 Features

### Core AI Features
- **AI-Powered Plant Disease Detection**: Upload plant images for instant disease identification using Hugging Face models
- **Smart Crop Recommendation Engine**: ML-based recommendations considering soil, climate, and market factors
- **AI Chatbot Assistant**: Multilingual support (English, Malayalam, Tamil, Hindi) for farming queries
- **Intelligent Weather Analytics**: 7-day forecasts, farming alerts, and irrigation suggestions
- **Personal Farm Profile & Analytics**: Track farm performance, crop history, and personalized insights

### Additional Features
- **Market Price Prediction**: Real-time price data and trend analysis for Kerala markets
- **Soil Health Assessment Tool**: AI analysis of soil test results with improvement recommendations
- **Smart Government Scheme Matcher**: AI-powered matching with relevant government schemes
- **Community Knowledge Sharing**: Q&A forum, best practices, and expert network
- **Mobile-First Design**: Responsive interface optimized for mobile devices

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.8+ (for backend)
- Supabase account
- Hugging Face API key
- OpenWeatherMap API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/keralafarm.git
   cd keralafarm
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   pnpm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API keys
   ```

4. **Set up backend** (see Backend/README.md for detailed instructions)
   ```bash
   cd Backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp env_example.txt .env
   # Edit .env with your API keys
   ```

5. **Set up database**
   - Create a Supabase project
   - Run the SQL schema from `Backend/supabase_schema.sql`
   - Update environment variables with Supabase credentials

6. **Start the application**
   ```bash
   # Terminal 1 - Backend
   cd Backend
   python main_api_server.py

   # Terminal 2 - Frontend
   npm run dev
   ```

The application will be available at `http://localhost:3000`

## 🏗️ Architecture

### Frontend Stack
- **Framework**: Next.js 14 with TypeScript
- **UI Components**: shadcn/ui component library
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React hooks and context
- **API Client**: Custom API client for backend communication

### Backend Stack
- **API Framework**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **AI/ML**: Hugging Face models, Scikit-learn
- **Image Processing**: OpenCV, Pillow
- **Weather API**: OpenWeatherMap

### Database
- **Primary Database**: Supabase (PostgreSQL)
- **Features**: Row Level Security, Real-time subscriptions
- **Tables**: Users, Farms, Crops, Disease Detections, Soil Tests, etc.

## 📱 Pages and Features

### 1. Dashboard
- Farm overview and analytics
- Quick access to all features
- Performance metrics and KPIs

### 2. Disease Detection
- Image upload for plant disease analysis
- AI-powered disease identification
- Treatment and prevention recommendations
- Detection history tracking

### 3. Crop Recommendations
- Soil analysis form
- AI-powered crop suggestions
- Detailed crop information
- Seasonal planting calendar

### 4. Weather Analytics
- Current weather conditions
- 7-day weather forecast
- Farming-specific recommendations
- Weather alerts and warnings

### 5. AI Chatbot
- Multilingual chat interface
- Natural language processing
- Quick question templates
- Context-aware responses

### 6. Farm Management
- Farm profile creation
- Crop tracking and management
- Soil test records
- Performance analytics

### 7. Community
- Q&A forum for farmers
- Knowledge sharing platform
- Expert advice and best practices
- Government scheme information

## 🔧 Configuration

### Environment Variables

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**Backend (.env)**:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

## 🧪 Testing

### Frontend Testing
```bash
npm run test
```

### Backend Testing
```bash
cd Backend
pytest
```

### API Testing
Visit `http://localhost:8000/api/docs` for interactive API documentation.

## 🚀 Deployment

### Frontend (Vercel)
1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables
4. Deploy automatically

### Backend (Railway/Render)
1. Connect GitHub repository
2. Set environment variables
3. Deploy with automatic builds

### Database (Supabase)
- Already hosted on Supabase cloud
- No additional deployment needed

## 📊 API Endpoints

### Disease Detection
- `POST /api/disease-detection` - Detect plant disease from base64 image
- `POST /api/disease-detection/upload` - Detect disease from uploaded file

### Crop Recommendations
- `POST /api/crop-recommendations` - Get AI-powered crop recommendations
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
- `GET /api/farm-profiles/{farm_id}` - Get farm profile
- `GET /api/farm-profiles/{farm_id}/analytics` - Get farm analytics

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
- **Next.js** for the React framework
- **Supabase** for the database platform

## 📞 Support

For support and questions:
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/keralafarm/issues)
- **Email**: support@keralafarm.app
- **Documentation**: [API Docs](http://localhost:8000/api/docs)

---

**Built with ❤️ for Kerala Farmers**

This application is designed to help Kerala farmers with AI-powered agricultural assistance, making farming more efficient, profitable, and sustainable.
