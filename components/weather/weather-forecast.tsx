"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { CloudRain, Sun, Wind, Droplets, Thermometer } from "lucide-react"

interface WeatherForecastProps {
  forecast: Array<{
    date: string
    day: string
    high: number
    low: number
    humidity: number
    rainfall: number
    windSpeed: number
    condition: string
    icon: string
    rainProbability: number
  }>
}

export function WeatherForecast({ forecast }: WeatherForecastProps) {
  const getWeatherIcon = (condition: string) => {
    switch (condition.toLowerCase()) {
      case "sunny":
        return <Sun className="h-8 w-8 text-yellow-500" />
      case "partly cloudy":
        return <CloudRain className="h-8 w-8 text-blue-400" />
      case "light rain":
        return <CloudRain className="h-8 w-8 text-blue-500" />
      case "moderate rain":
        return <CloudRain className="h-8 w-8 text-blue-600" />
      case "heavy rain":
        return <CloudRain className="h-8 w-8 text-blue-700" />
      case "thunderstorm":
        return <CloudRain className="h-8 w-8 text-purple-600" />
      case "scattered showers":
        return <CloudRain className="h-8 w-8 text-blue-500" />
      default:
        return <Sun className="h-8 w-8 text-yellow-500" />
    }
  }

  const getRainProbabilityColor = (probability: number) => {
    if (probability >= 80) return "text-blue-700"
    if (probability >= 60) return "text-blue-600"
    if (probability >= 40) return "text-blue-500"
    if (probability >= 20) return "text-blue-400"
    return "text-gray-500"
  }

  const getFarmingAdvice = (item: (typeof forecast)[0]) => {
    if (item.rainfall > 20) {
      return { text: "Avoid field work", color: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200" }
    }
    if (item.rainfall > 10) {
      return {
        text: "Limited field work",
        color: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
      }
    }
    if (item.rainfall > 0) {
      return { text: "Good for planting", color: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200" }
    }
    return { text: "Ideal farming weather", color: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200" }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>7-Day Weather Forecast</CardTitle>
          <CardDescription>Detailed weather predictions with farming recommendations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            {forecast.map((item, index) => {
              const advice = getFarmingAdvice(item)
              return (
                <Card key={index} className="p-4">
                  <div className="grid gap-4 md:grid-cols-6 items-center">
                    {/* Day and Date */}
                    <div className="md:col-span-1">
                      <h3 className="font-semibold">{item.day}</h3>
                      <p className="text-sm text-muted-foreground">{new Date(item.date).toLocaleDateString()}</p>
                    </div>

                    {/* Weather Icon and Condition */}
                    <div className="md:col-span-1 flex items-center gap-3">
                      {getWeatherIcon(item.condition)}
                      <div>
                        <p className="text-sm font-medium">{item.condition}</p>
                        <p className={`text-xs ${getRainProbabilityColor(item.rainProbability)}`}>
                          {item.rainProbability}% rain
                        </p>
                      </div>
                    </div>

                    {/* Temperature */}
                    <div className="md:col-span-1">
                      <div className="flex items-center gap-2">
                        <Thermometer className="h-4 w-4 text-red-500" />
                        <div>
                          <p className="text-sm font-medium">
                            {item.high}°C / {item.low}°C
                          </p>
                          <p className="text-xs text-muted-foreground">High / Low</p>
                        </div>
                      </div>
                    </div>

                    {/* Rainfall and Humidity */}
                    <div className="md:col-span-1">
                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <CloudRain className="h-4 w-4 text-blue-500" />
                          <span className="text-sm">{item.rainfall} mm</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Droplets className="h-4 w-4 text-blue-400" />
                          <span className="text-sm">{item.humidity}%</span>
                        </div>
                      </div>
                    </div>

                    {/* Wind Speed */}
                    <div className="md:col-span-1">
                      <div className="flex items-center gap-2">
                        <Wind className="h-4 w-4 text-gray-500" />
                        <div>
                          <p className="text-sm">{item.windSpeed} km/h</p>
                          <p className="text-xs text-muted-foreground">Wind</p>
                        </div>
                      </div>
                    </div>

                    {/* Farming Advice */}
                    <div className="md:col-span-1">
                      <Badge className={advice.color}>{advice.text}</Badge>
                    </div>
                  </div>

                  {/* Additional Details for Today and Tomorrow */}
                  {index < 2 && (
                    <div className="mt-4 pt-4 border-t">
                      <div className="grid gap-4 md:grid-cols-3">
                        <div>
                          <h4 className="text-sm font-medium mb-2">Humidity Trend</h4>
                          <Progress value={item.humidity} className="h-2" />
                          <p className="text-xs text-muted-foreground mt-1">{item.humidity}% humidity</p>
                        </div>
                        <div>
                          <h4 className="text-sm font-medium mb-2">Rain Probability</h4>
                          <Progress value={item.rainProbability} className="h-2" />
                          <p className="text-xs text-muted-foreground mt-1">{item.rainProbability}% chance</p>
                        </div>
                        <div>
                          <h4 className="text-sm font-medium mb-2">Farming Suitability</h4>
                          <Progress
                            value={item.rainfall > 20 ? 20 : item.rainfall > 10 ? 50 : item.rainfall > 0 ? 80 : 100}
                            className="h-2"
                          />
                          <p className="text-xs text-muted-foreground mt-1">
                            {item.rainfall > 20
                              ? "Poor"
                              : item.rainfall > 10
                                ? "Fair"
                                : item.rainfall > 0
                                  ? "Good"
                                  : "Excellent"}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </Card>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Weekly Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Weekly Summary</CardTitle>
          <CardDescription>Key weather insights for the week ahead</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <CloudRain className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <h3 className="font-semibold text-blue-800 dark:text-blue-200">Total Rainfall</h3>
              <p className="text-2xl font-bold text-blue-600">
                {forecast.reduce((sum, day) => sum + day.rainfall, 0)} mm
              </p>
              <p className="text-xs text-muted-foreground">Expected this week</p>
            </div>
            <div className="text-center p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
              <Thermometer className="h-8 w-8 text-orange-600 mx-auto mb-2" />
              <h3 className="font-semibold text-orange-800 dark:text-orange-200">Temperature Range</h3>
              <p className="text-2xl font-bold text-orange-600">
                {Math.min(...forecast.map((d) => d.low))}° - {Math.max(...forecast.map((d) => d.high))}°C
              </p>
              <p className="text-xs text-muted-foreground">Weekly range</p>
            </div>
            <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <Wind className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <h3 className="font-semibold text-green-800 dark:text-green-200">Average Wind</h3>
              <p className="text-2xl font-bold text-green-600">
                {Math.round(forecast.reduce((sum, day) => sum + day.windSpeed, 0) / forecast.length)} km/h
              </p>
              <p className="text-xs text-muted-foreground">Weekly average</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
