"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Droplets, Calendar, Clock, Pause, Play, Settings, TrendingDown, TrendingUp } from "lucide-react"
import type { WeatherData } from "./weather-analytics-content"

interface IrrigationRecommendationsProps {
  weatherData: WeatherData
}

interface IrrigationZone {
  id: string
  name: string
  cropType: string
  area: number
  soilMoisture: number
  lastWatered: string
  nextScheduled: string
  waterRequirement: "low" | "medium" | "high"
  status: "active" | "paused" | "scheduled"
  efficiency: number
}

export function IrrigationRecommendations({ weatherData }: IrrigationRecommendationsProps) {
  // Mock irrigation zones data
  const irrigationZones: IrrigationZone[] = [
    {
      id: "1",
      name: "Rice Field A",
      cropType: "Rice",
      area: 2.5,
      soilMoisture: 85,
      lastWatered: "2024-01-14T06:00:00Z",
      nextScheduled: "2024-01-16T06:00:00Z",
      waterRequirement: "high",
      status: "paused",
      efficiency: 78,
    },
    {
      id: "2",
      name: "Pepper Garden",
      cropType: "Black Pepper",
      area: 1.2,
      soilMoisture: 65,
      lastWatered: "2024-01-13T18:00:00Z",
      nextScheduled: "2024-01-15T18:00:00Z",
      waterRequirement: "medium",
      status: "scheduled",
      efficiency: 85,
    },
    {
      id: "3",
      name: "Coconut Grove",
      cropType: "Coconut",
      area: 3.0,
      soilMoisture: 45,
      lastWatered: "2024-01-12T07:00:00Z",
      nextScheduled: "2024-01-15T07:00:00Z",
      waterRequirement: "medium",
      status: "active",
      efficiency: 72,
    },
    {
      id: "4",
      name: "Vegetable Plot",
      cropType: "Mixed Vegetables",
      area: 0.8,
      soilMoisture: 55,
      lastWatered: "2024-01-14T17:00:00Z",
      nextScheduled: "2024-01-16T17:00:00Z",
      waterRequirement: "high",
      status: "paused",
      efficiency: 90,
    },
  ]

  const totalRainfall = weatherData.forecast.reduce((sum, day) => sum + day.rainfall, 0)
  const avgHumidity = Math.round(
    weatherData.forecast.reduce((sum, day) => sum + day.humidity, 0) / weatherData.forecast.length,
  )

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "default"
      case "paused":
        return "secondary"
      case "scheduled":
        return "outline"
      default:
        return "outline"
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "active":
        return <Play className="h-4 w-4" />
      case "paused":
        return <Pause className="h-4 w-4" />
      case "scheduled":
        return <Clock className="h-4 w-4" />
      default:
        return <Clock className="h-4 w-4" />
    }
  }

  const getWaterRequirementColor = (requirement: string) => {
    switch (requirement) {
      case "high":
        return "text-red-600"
      case "medium":
        return "text-yellow-600"
      case "low":
        return "text-green-600"
      default:
        return "text-gray-600"
    }
  }

  const getMoistureStatus = (moisture: number) => {
    if (moisture >= 80) return { status: "Optimal", color: "text-green-600" }
    if (moisture >= 60) return { status: "Good", color: "text-blue-600" }
    if (moisture >= 40) return { status: "Moderate", color: "text-yellow-600" }
    return { status: "Low", color: "text-red-600" }
  }

  return (
    <div className="space-y-6">
      {/* Irrigation Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Droplets className="h-5 w-5 text-blue-600" />
            Smart Irrigation Recommendations
          </CardTitle>
          <CardDescription>
            AI-powered irrigation scheduling based on weather forecasts and soil conditions
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <Droplets className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <h3 className="font-semibold text-blue-800 dark:text-blue-200">Expected Rainfall</h3>
              <p className="text-2xl font-bold text-blue-600">{totalRainfall} mm</p>
              <p className="text-xs text-muted-foreground">Next 7 days</p>
            </div>
            <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <TrendingUp className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <h3 className="font-semibold text-green-800 dark:text-green-200">Water Savings</h3>
              <p className="text-2xl font-bold text-green-600">35%</p>
              <p className="text-xs text-muted-foreground">This month</p>
            </div>
            <div className="text-center p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
              <Settings className="h-8 w-8 text-orange-600 mx-auto mb-2" />
              <h3 className="font-semibold text-orange-800 dark:text-orange-200">System Efficiency</h3>
              <p className="text-2xl font-bold text-orange-600">
                {Math.round(irrigationZones.reduce((sum, zone) => sum + zone.efficiency, 0) / irrigationZones.length)}%
              </p>
              <p className="text-xs text-muted-foreground">Average across zones</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Weekly Irrigation Plan */}
      <Card>
        <CardHeader>
          <CardTitle>Weekly Irrigation Plan</CardTitle>
          <CardDescription>Optimized watering schedule based on weather forecast</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {weatherData.forecast.slice(0, 7).map((day, index) => {
              const shouldIrrigate = day.rainfall < 5 && day.humidity < 70
              return (
                <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="text-center">
                      <p className="text-sm font-medium">{day.day}</p>
                      <p className="text-xs text-muted-foreground">{new Date(day.date).toLocaleDateString()}</p>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-sm">
                        <p>Rain: {day.rainfall}mm</p>
                        <p className="text-muted-foreground">Humidity: {day.humidity}%</p>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {shouldIrrigate ? (
                      <Badge
                        variant="default"
                        className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
                      >
                        <Droplets className="h-3 w-3 mr-1" />
                        Irrigate
                      </Badge>
                    ) : (
                      <Badge variant="secondary">
                        <Pause className="h-3 w-3 mr-1" />
                        Skip
                      </Badge>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Irrigation Zones */}
      <Card>
        <CardHeader>
          <CardTitle>Irrigation Zones</CardTitle>
          <CardDescription>Monitor and control individual irrigation zones</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            {irrigationZones.map((zone) => {
              const moistureStatus = getMoistureStatus(zone.soilMoisture)
              return (
                <Card key={zone.id} className="p-4">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="font-semibold">{zone.name}</h3>
                      <p className="text-sm text-muted-foreground">
                        {zone.cropType} • {zone.area} hectares
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={getStatusColor(zone.status)} className="flex items-center gap-1">
                        {getStatusIcon(zone.status)}
                        {zone.status.charAt(0).toUpperCase() + zone.status.slice(1)}
                      </Badge>
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-4">
                    <div>
                      <h4 className="text-sm font-medium mb-2">Soil Moisture</h4>
                      <div className="space-y-1">
                        <Progress value={zone.soilMoisture} className="h-2" />
                        <p className={`text-sm ${moistureStatus.color}`}>
                          {zone.soilMoisture}% ({moistureStatus.status})
                        </p>
                      </div>
                    </div>

                    <div>
                      <h4 className="text-sm font-medium mb-2">Water Requirement</h4>
                      <p className={`text-sm font-medium ${getWaterRequirementColor(zone.waterRequirement)}`}>
                        {zone.waterRequirement.charAt(0).toUpperCase() + zone.waterRequirement.slice(1)}
                      </p>
                      <p className="text-xs text-muted-foreground">Based on crop type</p>
                    </div>

                    <div>
                      <h4 className="text-sm font-medium mb-2">System Efficiency</h4>
                      <div className="flex items-center gap-2">
                        {zone.efficiency >= 80 ? (
                          <TrendingUp className="h-4 w-4 text-green-600" />
                        ) : (
                          <TrendingDown className="h-4 w-4 text-red-600" />
                        )}
                        <span className="text-sm font-medium">{zone.efficiency}%</span>
                      </div>
                    </div>

                    <div>
                      <h4 className="text-sm font-medium mb-2">Next Scheduled</h4>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <span className="text-sm">{new Date(zone.nextScheduled).toLocaleDateString()}</span>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {new Date(zone.nextScheduled).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-2 mt-4">
                    <Button size="sm" variant="outline">
                      <Settings className="h-4 w-4 mr-2" />
                      Configure
                    </Button>
                    {zone.status === "paused" ? (
                      <Button size="sm">
                        <Play className="h-4 w-4 mr-2" />
                        Resume
                      </Button>
                    ) : (
                      <Button size="sm" variant="outline">
                        <Pause className="h-4 w-4 mr-2" />
                        Pause
                      </Button>
                    )}
                  </div>
                </Card>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Smart Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle>Smart Recommendations</CardTitle>
          <CardDescription>AI-powered irrigation insights for optimal water management</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
              <div className="flex items-start gap-3">
                <Droplets className="h-5 w-5 text-blue-600 mt-0.5" />
                <div>
                  <h4 className="font-medium text-blue-800 dark:text-blue-200">Pause Irrigation Systems</h4>
                  <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                    Expected rainfall of {totalRainfall}mm over the next 7 days will provide sufficient water for most
                    crops. Consider pausing automated irrigation to save water and prevent overwatering.
                  </p>
                </div>
              </div>
            </div>

            <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
              <div className="flex items-start gap-3">
                <Settings className="h-5 w-5 text-yellow-600 mt-0.5" />
                <div>
                  <h4 className="font-medium text-yellow-800 dark:text-yellow-200">Optimize Coconut Grove</h4>
                  <p className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                    Coconut Grove shows low soil moisture (45%) and lower efficiency (72%). Consider checking for system
                    leaks or adjusting irrigation timing for better water retention.
                  </p>
                </div>
              </div>
            </div>

            <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
              <div className="flex items-start gap-3">
                <TrendingUp className="h-5 w-5 text-green-600 mt-0.5" />
                <div>
                  <h4 className="font-medium text-green-800 dark:text-green-200">Excellent Water Management</h4>
                  <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                    Your Vegetable Plot shows optimal efficiency (90%) and good soil moisture levels. Continue current
                    irrigation schedule for best results.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
