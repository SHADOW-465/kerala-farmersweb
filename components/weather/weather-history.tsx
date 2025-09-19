"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from "recharts"
import { Calendar, TrendingUp, CloudRain, Thermometer, Droplets } from "lucide-react"
import { useState } from "react"

interface HistoricalData {
  month: string
  rainfall: number
  temperature: number
  humidity: number
  rainyDays: number
}

export function WeatherHistory() {
  const [selectedYear, setSelectedYear] = useState("2024")
  const [selectedMetric, setSelectedMetric] = useState("rainfall")

  // Mock historical weather data for Kerala
  const historicalData: HistoricalData[] = [
    { month: "Jan", rainfall: 25, temperature: 26, humidity: 75, rainyDays: 3 },
    { month: "Feb", rainfall: 35, temperature: 28, humidity: 72, rainyDays: 4 },
    { month: "Mar", rainfall: 45, temperature: 30, humidity: 70, rainyDays: 5 },
    { month: "Apr", rainfall: 120, temperature: 31, humidity: 75, rainyDays: 8 },
    { month: "May", rainfall: 180, temperature: 30, humidity: 80, rainyDays: 12 },
    { month: "Jun", rainfall: 650, temperature: 27, humidity: 85, rainyDays: 20 },
    { month: "Jul", rainfall: 420, temperature: 26, humidity: 88, rainyDays: 18 },
    { month: "Aug", rainfall: 380, temperature: 26, humidity: 87, rainyDays: 16 },
    { month: "Sep", rainfall: 290, temperature: 27, humidity: 85, rainyDays: 14 },
    { month: "Oct", rainfall: 320, temperature: 28, humidity: 82, rainyDays: 15 },
    { month: "Nov", rainfall: 180, temperature: 27, humidity: 78, rainyDays: 10 },
    { month: "Dec", rainfall: 65, temperature: 26, humidity: 76, rainyDays: 6 },
  ]

  const yearlyStats = {
    totalRainfall: historicalData.reduce((sum, month) => sum + month.rainfall, 0),
    avgTemperature: Math.round(
      historicalData.reduce((sum, month) => sum + month.temperature, 0) / historicalData.length,
    ),
    avgHumidity: Math.round(historicalData.reduce((sum, month) => sum + month.humidity, 0) / historicalData.length),
    totalRainyDays: historicalData.reduce((sum, month) => sum + month.rainyDays, 0),
  }

  const getMetricData = () => {
    switch (selectedMetric) {
      case "temperature":
        return { dataKey: "temperature", color: "#f59e0b", unit: "°C", name: "Temperature" }
      case "humidity":
        return { dataKey: "humidity", color: "#3b82f6", unit: "%", name: "Humidity" }
      case "rainyDays":
        return { dataKey: "rainyDays", color: "#10b981", unit: " days", name: "Rainy Days" }
      default:
        return { dataKey: "rainfall", color: "#6366f1", unit: "mm", name: "Rainfall" }
    }
  }

  const metricData = getMetricData()

  const getSeasonalInsight = () => {
    const monsoonRainfall = historicalData.slice(5, 9).reduce((sum, month) => sum + month.rainfall, 0)
    const preMonsoonRainfall = historicalData.slice(2, 5).reduce((sum, month) => sum + month.rainfall, 0)
    const postMonsoonRainfall = historicalData.slice(9, 12).reduce((sum, month) => sum + month.rainfall, 0)
    const winterRainfall = historicalData.slice(0, 2).reduce((sum, month) => sum + month.rainfall, 0)

    return {
      monsoon: { amount: monsoonRainfall, percentage: Math.round((monsoonRainfall / yearlyStats.totalRainfall) * 100) },
      preMonsoon: {
        amount: preMonsoonRainfall,
        percentage: Math.round((preMonsoonRainfall / yearlyStats.totalRainfall) * 100),
      },
      postMonsoon: {
        amount: postMonsoonRainfall,
        percentage: Math.round((postMonsoonRainfall / yearlyStats.totalRainfall) * 100),
      },
      winter: { amount: winterRainfall, percentage: Math.round((winterRainfall / yearlyStats.totalRainfall) * 100) },
    }
  }

  const seasonalData = getSeasonalInsight()

  return (
    <div className="space-y-6">
      {/* Controls */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Weather History & Trends
              </CardTitle>
              <CardDescription>Historical weather data and seasonal patterns for Kerala</CardDescription>
            </div>
            <div className="flex gap-2">
              <Select value={selectedYear} onValueChange={setSelectedYear}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="2024">2024</SelectItem>
                  <SelectItem value="2023">2023</SelectItem>
                  <SelectItem value="2022">2022</SelectItem>
                </SelectContent>
              </Select>
              <Select value={selectedMetric} onValueChange={setSelectedMetric}>
                <SelectTrigger className="w-40">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="rainfall">Rainfall</SelectItem>
                  <SelectItem value="temperature">Temperature</SelectItem>
                  <SelectItem value="humidity">Humidity</SelectItem>
                  <SelectItem value="rainyDays">Rainy Days</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Yearly Statistics */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <CloudRain className="h-4 w-4 text-blue-600" />
              Total Rainfall
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{yearlyStats.totalRainfall} mm</div>
            <p className="text-sm text-muted-foreground">Annual total</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Thermometer className="h-4 w-4 text-orange-600" />
              Avg Temperature
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">{yearlyStats.avgTemperature}°C</div>
            <p className="text-sm text-muted-foreground">Annual average</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Droplets className="h-4 w-4 text-green-600" />
              Avg Humidity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{yearlyStats.avgHumidity}%</div>
            <p className="text-sm text-muted-foreground">Annual average</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Calendar className="h-4 w-4 text-purple-600" />
              Rainy Days
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">{yearlyStats.totalRainyDays}</div>
            <p className="text-sm text-muted-foreground">Total days</p>
          </CardContent>
        </Card>
      </div>

      {/* Historical Chart */}
      <Card>
        <CardHeader>
          <CardTitle>
            {metricData.name} Trends - {selectedYear}
          </CardTitle>
          <CardDescription>Monthly {metricData.name.toLowerCase()} data throughout the year</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              {selectedMetric === "rainfall" ? (
                <BarChart data={historicalData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip
                    formatter={(value) => [`${value}${metricData.unit}`, metricData.name]}
                    labelStyle={{ color: "var(--foreground)" }}
                    contentStyle={{
                      backgroundColor: "var(--background)",
                      border: "1px solid var(--border)",
                      borderRadius: "6px",
                    }}
                  />
                  <Bar dataKey={metricData.dataKey} fill={metricData.color} radius={[4, 4, 0, 0]} />
                </BarChart>
              ) : (
                <AreaChart data={historicalData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip
                    formatter={(value) => [`${value}${metricData.unit}`, metricData.name]}
                    labelStyle={{ color: "var(--foreground)" }}
                    contentStyle={{
                      backgroundColor: "var(--background)",
                      border: "1px solid var(--border)",
                      borderRadius: "6px",
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey={metricData.dataKey}
                    stroke={metricData.color}
                    fill={metricData.color}
                    fillOpacity={0.3}
                  />
                </AreaChart>
              )}
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Seasonal Analysis */}
      <Card>
        <CardHeader>
          <CardTitle>Seasonal Rainfall Distribution</CardTitle>
          <CardDescription>Breakdown of rainfall across Kerala's four seasons</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <h3 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">Monsoon</h3>
              <p className="text-sm text-muted-foreground mb-2">Jun - Sep</p>
              <div className="text-2xl font-bold text-blue-600">{seasonalData.monsoon.amount} mm</div>
              <Badge variant="outline" className="mt-2">
                {seasonalData.monsoon.percentage}% of annual
              </Badge>
            </div>
            <div className="text-center p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
              <h3 className="font-semibold text-orange-800 dark:text-orange-200 mb-2">Pre-Monsoon</h3>
              <p className="text-sm text-muted-foreground mb-2">Mar - May</p>
              <div className="text-2xl font-bold text-orange-600">{seasonalData.preMonsoon.amount} mm</div>
              <Badge variant="outline" className="mt-2">
                {seasonalData.preMonsoon.percentage}% of annual
              </Badge>
            </div>
            <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <h3 className="font-semibold text-green-800 dark:text-green-200 mb-2">Post-Monsoon</h3>
              <p className="text-sm text-muted-foreground mb-2">Oct - Dec</p>
              <div className="text-2xl font-bold text-green-600">{seasonalData.postMonsoon.amount} mm</div>
              <Badge variant="outline" className="mt-2">
                {seasonalData.postMonsoon.percentage}% of annual
              </Badge>
            </div>
            <div className="text-center p-4 bg-gray-50 dark:bg-gray-900/20 rounded-lg">
              <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">Winter</h3>
              <p className="text-sm text-muted-foreground mb-2">Jan - Feb</p>
              <div className="text-2xl font-bold text-gray-600">{seasonalData.winter.amount} mm</div>
              <Badge variant="outline" className="mt-2">
                {seasonalData.winter.percentage}% of annual
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Climate Insights */}
      <Card>
        <CardHeader>
          <CardTitle>Climate Insights</CardTitle>
          <CardDescription>Key observations from historical weather patterns</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-start gap-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
              <TrendingUp className="h-5 w-5 text-blue-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-blue-800 dark:text-blue-200">Monsoon Dominance</h4>
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  {seasonalData.monsoon.percentage}% of annual rainfall occurs during monsoon season (Jun-Sep), making
                  it crucial for crop planning and water management.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-800">
              <Thermometer className="h-5 w-5 text-orange-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-orange-800 dark:text-orange-200">Temperature Stability</h4>
                <p className="text-sm text-orange-700 dark:text-orange-300">
                  Kerala maintains relatively stable temperatures year-round (26-31°C), ideal for tropical crops like
                  coconut, pepper, and cardamom.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
              <Droplets className="h-5 w-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-green-800 dark:text-green-200">High Humidity Levels</h4>
                <p className="text-sm text-green-700 dark:text-green-300">
                  Average humidity of {yearlyStats.avgHumidity}% creates favorable conditions for spice cultivation but
                  requires careful disease management for crops.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
