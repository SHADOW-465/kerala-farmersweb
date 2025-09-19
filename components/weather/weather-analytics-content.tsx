"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { 
  Cloud, 
  Sun, 
  Droplets, 
  Wind, 
  Thermometer, 
  Eye, 
  Calendar,
  MapPin,
  AlertTriangle,
  TrendingUp,
  TrendingDown
} from "lucide-react"
import { apiClient, WeatherData } from "@/lib/api-client"
import { useToast } from "@/hooks/use-toast"

interface WeatherForecast {
  date: string
  temperature: number
  humidity: number
  description: string
}

interface WeatherSummary {
  current: WeatherData
  forecast: WeatherForecast[]
  alerts: string[]
  recommendations: string[]
}

export function WeatherAnalyticsContent() {
  const [location, setLocation] = useState("Thiruvananthapuram")
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null)
  const [forecast, setForecast] = useState<WeatherForecast[]>([])
  const [summary, setSummary] = useState<WeatherSummary | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const { toast } = useToast()

  // Load weather data on component mount
  useEffect(() => {
    loadWeatherData()
  }, [])

  const loadWeatherData = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.getCurrentWeather({
        city: location,
        state: "Kerala"
      })

      if (response.success && response.data) {
        setWeatherData(response.data)
        setLastUpdated(new Date())
      } else {
        throw new Error(response.error || "Failed to load weather data")
      }
    } catch (error) {
      console.error("Weather loading error:", error)
      toast({
        title: "Weather Loading Failed",
        description: error instanceof Error ? error.message : "Failed to load weather data",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const loadForecast = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.getWeatherForecast({
        city: location,
        state: "Kerala"
      }, 7)

      if (response.success && response.data) {
        setForecast(response.data.forecast)
      } else {
        throw new Error(response.error || "Failed to load forecast")
      }
    } catch (error) {
      console.error("Forecast loading error:", error)
      toast({
        title: "Forecast Loading Failed",
        description: error instanceof Error ? error.message : "Failed to load weather forecast",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const loadWeatherSummary = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.getWeatherSummary({
        city: location,
        state: "Kerala"
      })

      if (response.success && response.data) {
        setSummary(response.data)
      } else {
        throw new Error(response.error || "Failed to load weather summary")
      }
    } catch (error) {
      console.error("Weather summary error:", error)
      toast({
        title: "Summary Loading Failed",
        description: error instanceof Error ? error.message : "Failed to load weather summary",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const getWeatherIcon = (description: string) => {
    const desc = description.toLowerCase()
    if (desc.includes("rain") || desc.includes("drizzle")) return <Droplets className="h-6 w-6 text-blue-500" />
    if (desc.includes("cloud")) return <Cloud className="h-6 w-6 text-gray-500" />
    if (desc.includes("sun") || desc.includes("clear")) return <Sun className="h-6 w-6 text-yellow-500" />
    return <Cloud className="h-6 w-6 text-gray-500" />
  }

  const getTemperatureColor = (temp: number) => {
    if (temp > 35) return "text-red-600"
    if (temp > 30) return "text-orange-600"
    if (temp > 25) return "text-yellow-600"
    if (temp > 20) return "text-green-600"
    return "text-blue-600"
  }

  const getFarmingRecommendation = (weather: WeatherData) => {
    const temp = weather.temperature
    const humidity = weather.humidity
    const description = weather.description.toLowerCase()

    if (description.includes("rain")) {
      return "Good time for planting. Avoid heavy field work during heavy rain."
    }
    if (temp > 35) {
      return "High temperature - ensure adequate irrigation and shade for sensitive crops."
    }
    if (temp < 20) {
      return "Cool weather - good for root vegetables and leafy greens."
    }
    if (humidity > 80) {
      return "High humidity - watch for fungal diseases. Ensure good air circulation."
    }
    return "Favorable weather conditions for most farming activities."
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-balance">Weather Analytics</h1>
        <p className="text-muted-foreground text-pretty">
          Get real-time weather data, forecasts, and farming recommendations for your location in Kerala.
        </p>
      </div>

      {/* Location Input */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <Input
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="Enter city name (e.g., Thiruvananthapuram, Kochi, Kozhikode)"
                className="w-full"
              />
            </div>
            <Button onClick={loadWeatherData} disabled={isLoading}>
              {isLoading ? "Loading..." : "Get Weather"}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="current" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="current">Current Weather</TabsTrigger>
          <TabsTrigger value="forecast">7-Day Forecast</TabsTrigger>
          <TabsTrigger value="summary">Farming Summary</TabsTrigger>
          <TabsTrigger value="alerts">Weather Alerts</TabsTrigger>
        </TabsList>

        <TabsContent value="current" className="space-y-6">
          {weatherData ? (
            <>
              {/* Current Weather Card */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <MapPin className="h-5 w-5" />
                      <CardTitle>{location}, Kerala</CardTitle>
                    </div>
                    <Badge variant="outline">
                      {lastUpdated?.toLocaleTimeString()}
                    </Badge>
                  </div>
                  <CardDescription>
                    Current weather conditions and farming recommendations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                    <div className="text-center">
                      <div className="flex items-center justify-center mb-2">
                        {getWeatherIcon(weatherData.description)}
                      </div>
                      <div className={`text-4xl font-bold ${getTemperatureColor(weatherData.temperature)}`}>
                        {Math.round(weatherData.temperature)}°C
                      </div>
                      <div className="text-sm text-muted-foreground capitalize">
                        {weatherData.description}
                      </div>
                    </div>

                    <div className="space-y-4">
                      <div className="flex items-center gap-2">
                        <Droplets className="h-4 w-4 text-blue-500" />
                        <span className="text-sm">Humidity: {weatherData.humidity}%</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Wind className="h-4 w-4 text-gray-500" />
                        <span className="text-sm">Wind: {weatherData.wind_speed} km/h</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Eye className="h-4 w-4 text-gray-500" />
                        <span className="text-sm">Pressure: {weatherData.pressure} hPa</span>
                      </div>
                    </div>

                    <div className="lg:col-span-2">
                      <Alert>
                        <AlertTriangle className="h-4 w-4" />
                        <AlertDescription>
                          <strong>Farming Recommendation:</strong> {getFarmingRecommendation(weatherData)}
                        </AlertDescription>
                      </Alert>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Weather Details */}
              <div className="grid gap-4 md:grid-cols-3">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm flex items-center gap-2">
                      <Thermometer className="h-4 w-4" />
                      Temperature
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{Math.round(weatherData.temperature)}°C</div>
                    <div className="text-xs text-muted-foreground">
                      {weatherData.temperature > 30 ? "Hot" : weatherData.temperature > 25 ? "Warm" : "Cool"}
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm flex items-center gap-2">
                      <Droplets className="h-4 w-4" />
                      Humidity
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{weatherData.humidity}%</div>
                    <div className="text-xs text-muted-foreground">
                      {weatherData.humidity > 70 ? "High" : weatherData.humidity > 40 ? "Moderate" : "Low"}
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm flex items-center gap-2">
                      <Wind className="h-4 w-4" />
                      Wind Speed
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{weatherData.wind_speed} km/h</div>
                    <div className="text-xs text-muted-foreground">
                      {weatherData.wind_speed > 20 ? "Strong" : weatherData.wind_speed > 10 ? "Moderate" : "Light"}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Cloud className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No Weather Data</h3>
                <p className="text-muted-foreground text-center">
                  Enter a location and click "Get Weather" to load current weather conditions.
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="forecast" className="space-y-6">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">7-Day Weather Forecast</h3>
            <Button onClick={loadForecast} disabled={isLoading}>
              {isLoading ? "Loading..." : "Load Forecast"}
            </Button>
          </div>

          {forecast.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-7">
              {forecast.map((day, index) => (
                <Card key={index}>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm">
                      {new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' })}
                    </CardTitle>
                    <CardDescription className="text-xs">
                      {new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex items-center justify-center">
                      {getWeatherIcon(day.description)}
                    </div>
                    <div className="text-center">
                      <div className={`text-lg font-bold ${getTemperatureColor(day.temperature)}`}>
                        {Math.round(day.temperature)}°C
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {day.humidity}% humidity
                      </div>
                    </div>
                    <div className="text-xs text-center capitalize">
                      {day.description}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Calendar className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No Forecast Data</h3>
                <p className="text-muted-foreground text-center">
                  Click "Load Forecast" to get 7-day weather predictions.
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="summary" className="space-y-6">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Farming Weather Summary</h3>
            <Button onClick={loadWeatherSummary} disabled={isLoading}>
              {isLoading ? "Loading..." : "Load Summary"}
            </Button>
          </div>

          {summary ? (
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Current Conditions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <h4 className="font-semibold mb-2">Weather Status</h4>
                      <p className="text-sm text-muted-foreground">
                        Temperature: {Math.round(summary.current.temperature)}°C | 
                        Humidity: {summary.current.humidity}% | 
                        {summary.current.description}
                      </p>
                    </div>
                    <div>
                      <h4 className="font-semibold mb-2">Farming Impact</h4>
                      <p className="text-sm text-muted-foreground">
                        {getFarmingRecommendation(summary.current)}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {summary.recommendations.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Farming Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {summary.recommendations.map((rec, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <TrendingUp className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                          <span className="text-sm">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <TrendingUp className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No Summary Available</h3>
                <p className="text-muted-foreground text-center">
                  Click "Load Summary" to get detailed farming weather analysis.
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="alerts" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Weather Alerts & Warnings</CardTitle>
              <CardDescription>
                Important weather information that may affect your farming activities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Alert>
                  <AlertTriangle className="h-4 w-4" />
                  <AlertDescription>
                    <strong>Monsoon Season:</strong> Kerala experiences heavy rainfall during June-September. 
                    Plan irrigation accordingly and watch for waterlogging.
                  </AlertDescription>
                </Alert>
                
                <Alert>
                  <AlertTriangle className="h-4 w-4" />
                  <AlertDescription>
                    <strong>Temperature Alert:</strong> High temperatures above 35°C can stress crops. 
                    Ensure adequate irrigation and consider shade nets for sensitive plants.
                  </AlertDescription>
                </Alert>

                <Alert>
                  <AlertTriangle className="h-4 w-4" />
                  <AlertDescription>
                    <strong>Humidity Warning:</strong> High humidity levels can promote fungal diseases. 
                    Maintain good air circulation and consider preventive fungicide applications.
                  </AlertDescription>
                </Alert>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}