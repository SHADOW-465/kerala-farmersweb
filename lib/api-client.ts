/**
 * API Client for FarmersHub Backend
 * Handles all API calls to the FastAPI backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '/api';

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  success: boolean;
}

export interface DiseaseDetectionRequest {
  image_base64: string;
  crop_type?: string;
}

export interface DiseaseDetectionResponse {
  disease: string;
  confidence: number;
  treatment: string;
  prevention: string;
  severity: string;
  success: boolean;
}

export interface CropRecommendationRequest {
  ph: number;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  rainfall: number;
  temperature: number;
  soil_type: string;
  season: string;
}

export interface CropRecommendation {
  crop: string;
  suitability_score: number;
  suitability_level: string;
  profit_potential: number;
  estimated_yield: number;
  growth_period_days: number;
  market_demand: string;
  profit_margin: number;
  ph_optimal: number;
  rainfall_optimal: number;
  temp_optimal: number;
  recommended_season: string;
}

export interface WeatherRequest {
  city: string;
  state: string;
}

export interface WeatherData {
  temperature: number;
  humidity: number;
  pressure: number;
  wind_speed: number;
  description: string;
  timestamp: string;
}

export interface ChatbotRequest {
  message: string;
  language?: string;
  user_id?: string;
}

export interface ChatbotResponse {
  response: string;
  language: string;
  intent: string;
  timestamp: string;
  success: boolean;
}

export interface FarmProfileRequest {
  farmer_name: string;
  farm_name: string;
  location: {
    district: string;
    state: string;
    coordinates?: {
      lat: number;
      lng: number;
    };
    address: string;
  };
  total_area: number;
  soil_type: string;
  soil_ph: number;
  soil_nutrients: {
    nitrogen: number;
    phosphorus: number;
    potassium: number;
    organic_matter: number;
  };
  irrigation_type: string;
  farming_type: string;
  established_year: number;
  contact_info: {
    phone: string;
    email: string;
    address: string;
  };
}

export interface FarmProfile {
  id: string;
  user_id: string;
  name: string;
  location: any;
  total_area: number;
  soil_type: string;
  soil_ph: number;
  soil_nutrients: any;
  irrigation_type: string;
  farming_type: string;
  established_year: number;
  contact_info: any;
  created_at: string;
  updated_at: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      console.log(`API Request: ${options.method || 'GET'} ${url}`);
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      console.log(`API Response: ${response.status} ${response.statusText}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('API Error:', errorData);
        return {
          success: false,
          error: errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      const data = await response.json();
      console.log('API Success:', data);
      return {
        success: true,
        data,
      };
    } catch (error) {
      console.error('API Request Error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  // Disease Detection APIs
  async detectDisease(
    request: DiseaseDetectionRequest,
    farmId?: string
  ): Promise<ApiResponse<DiseaseDetectionResponse>> {
    const params = farmId ? `?farm_id=${farmId}` : '';
    return this.request<DiseaseDetectionResponse>(
      `/api/disease-detection${params}`,
      {
        method: 'POST',
        body: JSON.stringify(request),
      }
    );
  }

  async detectDiseaseUpload(
    file: File,
    farmId?: string
  ): Promise<ApiResponse<DiseaseDetectionResponse>> {
    const formData = new FormData();
    formData.append('file', file);
    
    const params = farmId ? `?farm_id=${farmId}` : '';
    try {
      const response = await fetch(`${this.baseUrl}/api/disease-detection/upload${params}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          success: false,
          error: errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      const data = await response.json();
      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  // Crop Recommendation APIs
  async getCropRecommendations(
    request: CropRecommendationRequest
  ): Promise<ApiResponse<{ recommendations: CropRecommendation[]; total_recommendations: number; timestamp: string }>> {
    return this.request('/api/crop-recommendations', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getCropDetails(cropName: string): Promise<ApiResponse<any>> {
    return this.request(`/api/crops/${encodeURIComponent(cropName)}`);
  }

  // Weather APIs
  async getCurrentWeather(request: WeatherRequest): Promise<ApiResponse<WeatherData>> {
    return this.request('/api/weather/current', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getWeatherForecast(
    request: WeatherRequest,
    days: number = 7
  ): Promise<ApiResponse<{ forecast: any[]; total_days: number }>> {
    return this.request(`/api/weather/forecast?days=${days}`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getWeatherSummary(request: WeatherRequest): Promise<ApiResponse<any>> {
    return this.request('/api/weather/summary', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Chatbot APIs
  async chatWithBot(request: ChatbotRequest): Promise<ApiResponse<ChatbotResponse>> {
    return this.request('/api/chatbot', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getSupportedLanguages(): Promise<ApiResponse<{ languages: Record<string, string> }>> {
    return this.request('/api/chatbot/languages');
  }

  // Farm Profile APIs
  async createFarmProfile(
    request: FarmProfileRequest,
    userId: string
  ): Promise<ApiResponse<{ farm_id: string; message: string }>> {
    return this.request(`/api/farm-profiles?user_id=${userId}`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getFarmProfile(farmId: string): Promise<ApiResponse<FarmProfile>> {
    return this.request(`/api/farm-profiles/${farmId}`);
  }

  async getUserFarms(userId: string): Promise<ApiResponse<{ farms: FarmProfile[]; total: number }>> {
    return this.request(`/api/farm-profiles/user/${userId}`);
  }

  async getFarmAnalytics(farmId: string): Promise<ApiResponse<any>> {
    return this.request(`/api/farm-profiles/${farmId}/analytics`);
  }

  // Market Price APIs
  async predictCropPrice(
    cropName: string,
    days: number = 7
  ): Promise<ApiResponse<any>> {
    return this.request(`/api/market-prices/predict/${encodeURIComponent(cropName)}?days=${days}`);
  }

  async getMarketInsights(cropName?: string): Promise<ApiResponse<any>> {
    const params = cropName ? `?crop_name=${encodeURIComponent(cropName)}` : '';
    return this.request(`/api/market-prices/insights${params}`);
  }

  // Soil Health APIs
  async assessSoilHealth(request: any): Promise<ApiResponse<any>> {
    return this.request('/api/soil-health/assess', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async checkCropSuitability(request: any, cropName: string): Promise<ApiResponse<any>> {
    return this.request(`/api/soil-health/crop-suitability?crop_name=${encodeURIComponent(cropName)}`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Government Scheme APIs
  async matchGovernmentSchemes(request: any): Promise<ApiResponse<any>> {
    return this.request('/api/government-schemes/match', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async searchGovernmentSchemes(
    query: string,
    category?: string
  ): Promise<ApiResponse<any>> {
    const params = new URLSearchParams({ query });
    if (category) params.append('category', category);
    return this.request(`/api/government-schemes/search?${params}`);
  }

  // Community APIs
  async postQuestion(questionData: any): Promise<ApiResponse<{ question_id: string; message: string }>> {
    return this.request('/api/community/questions', {
      method: 'POST',
      body: JSON.stringify(questionData),
    });
  }

  async searchQuestions(
    query: string,
    category?: string,
    limit: number = 10
  ): Promise<ApiResponse<any>> {
    const params = new URLSearchParams({ query, limit: limit.toString() });
    if (category) params.append('category', category);
    return this.request(`/api/community/questions/search?${params}`);
  }

  // Mobile PWA APIs
  async getPWAManifest(): Promise<ApiResponse<any>> {
    return this.request('/api/mobile/manifest');
  }

  async getServiceWorker(): Promise<ApiResponse<{ code: string }>> {
    return this.request('/api/mobile/service-worker');
  }

  async getOfflinePage(): Promise<ApiResponse<{ html: string }>> {
    return this.request('/api/mobile/offline');
  }

  // Health Check
  async healthCheck(): Promise<ApiResponse<{ status: string; timestamp: string }>> {
    return this.request('/health');
  }
}

// Export singleton instance
export const apiClient = new ApiClient();

// Export types
export type {
  DiseaseDetectionRequest,
  DiseaseDetectionResponse,
  CropRecommendationRequest,
  CropRecommendation,
  WeatherRequest,
  WeatherData,
  ChatbotRequest,
  ChatbotResponse,
  FarmProfileRequest,
  FarmProfile,
};
