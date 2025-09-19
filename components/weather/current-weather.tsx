"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Droplets, Wind, Gauge, Sun, CloudRain, MapPin, Clock, Eye } from "lucide-react"

interface CurrentWeatherProps {
  data: {
    temperature: number
    humidity: number
    rainfall: number
    windSpeed: number
    pressure: number
    uvIndex: number
    condition: string
    icon: string
    location: string
    lastUpdated: string
  }
}

export function CurrentWeather({ data }: CurrentWeatherProps) {
  const getWeatherIcon = (condition: string) => {
    switch (condition.toLowerCase()) {
      case "sunny":
        return <Sun className="h-12 w-12 text-yellow-500" />
      case "partly cloudy":
        return <CloudRain className="h-12 w-12 text-blue-400" />
      case "cloudy":
        return <CloudRain className="h-12 w-12 text-gray-500" />
      case "rainy":
      case "light rain":
      case "moderate rain":
      case "heavy rain":
        return <CloudRain className="h-12 w-12 text-blue-600" />
      default:
        return <Sun className="h-12 w-12 text-yellow-500" />
    }
  }

  const getUVLevel = (uvIndex: number) => {
    if (uvIndex <= 2) return { level: "Low", color: "text-green-600" }
    if (uvIndex <= 5) return { level: "Moderate", color: "text-yellow-600" }
    if (uvIndex <= 7) return { level: "High", color: "text-orange-600" }
    if (uvIndex <= 10) return { level: "Very High", color: "text-red-600" }
    return { level: "Extreme", color: "text-purple-600" }
  }

  const uvLevel = getUVLevel(data.uvIndex)

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="h-5 w-5" />
              Current Weather
            </CardTitle>
            <CardDescription className="flex items-center gap-2 mt-1">
              <Clock className="h-4 w-4" />
              {data.location} • Updated {data.lastUpdated}
            </CardDescription>
          </div>
          <Badge variant="outline" className="text-sm">
            Live Data
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {/* Main Weather Display */}
          <div className="md:col-span-2 lg:col-span-1">
            <div className="flex items-center gap-4">
              {getWeatherIcon(data.condition)}
              <div>
                <div className="text-4xl font-bold">{data.temperature}°C</div>
                <p className="text-muted-foreground">{data.condition}</p>
              </div>
            </div>
          </div>

          {/* Weather Metrics */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <Droplets className="h-5 w-5 text-blue-500" />
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Humidity</span>
                  <span className="text-sm text-muted-foreground">{data.humidity}%</span>
                </div>
                <Progress value={data.humidity} className="h-2 mt-1" />
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Wind className="h-5 w-5 text-gray-500" />
              <div>
                <p className="text-sm font-medium">Wind Speed</p>
                <p className="text-sm text-muted-foreground">{data.windSpeed} km/h</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <Gauge className="h-5 w-5 text-purple-500" />
              <div>
                <p className="text-sm font-medium">Pressure</p>
                <p className="text-sm text-muted-foreground">{data.pressure} hPa</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Sun className="h-5 w-5 text-orange-500" />
              <div>
                <p className="text-sm font-medium">UV Index</p>
                <p className={`text-sm ${uvLevel.color}`}>
                  {data.uvIndex} ({uvLevel.level})
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <CloudRain className="h-5 w-5 text-blue-600" />
              <div>
                <p className="text-sm font-medium">Rainfall Today</p>
                <p className="text-sm text-muted-foreground">{data.rainfall} mm</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Eye className="h-5 w-5 text-gray-600" />
              <div>
                <p className="text-sm font-medium">Visibility</p>
                <p className="text-sm text-muted-foreground">10 km</p>
              </div>
            </div>
          </div>
        </div>

        {/* Farming Conditions Summary */}
        <div className="mt-6 p-4 bg-muted rounded-lg">
          <h4 className="font-medium mb-2">Farming Conditions</h4>
          <div className="grid gap-2 md:grid-cols-3">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500" />
              <span className="text-sm">Good for outdoor work</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-yellow-500" />
              <span className="text-sm">Moderate UV exposure</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-500" />
              <span className="text-sm">Adequate soil moisture</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
