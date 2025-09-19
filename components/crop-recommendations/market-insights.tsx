"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { TrendingUp, TrendingDown, BarChart3, AlertTriangle, CheckCircle } from "lucide-react"

interface MarketData {
  crop: string
  currentPrice: number
  previousPrice: number
  trend: "up" | "down" | "stable"
  demand: number
  supply: number
  forecast: "bullish" | "bearish" | "stable"
  exportPotential: "high" | "medium" | "low"
  seasonality: string
}

const marketData: MarketData[] = [
  {
    crop: "Black Pepper",
    currentPrice: 450,
    previousPrice: 420,
    trend: "up",
    demand: 85,
    supply: 70,
    forecast: "bullish",
    exportPotential: "high",
    seasonality: "Peak: Dec-Feb",
  },
  {
    crop: "Cardamom",
    currentPrice: 1200,
    previousPrice: 1150,
    trend: "up",
    demand: 90,
    supply: 65,
    forecast: "bullish",
    exportPotential: "high",
    seasonality: "Peak: Oct-Dec",
  },
  {
    crop: "Coconut",
    currentPrice: 25,
    previousPrice: 28,
    trend: "down",
    demand: 75,
    supply: 85,
    forecast: "stable",
    exportPotential: "medium",
    seasonality: "Year-round",
  },
  {
    crop: "Rice",
    currentPrice: 20,
    previousPrice: 19,
    trend: "up",
    demand: 95,
    supply: 90,
    forecast: "stable",
    exportPotential: "low",
    seasonality: "Peak: Oct-Nov, Mar-Apr",
  },
  {
    crop: "Banana",
    currentPrice: 15,
    previousPrice: 16,
    trend: "down",
    demand: 80,
    supply: 85,
    forecast: "stable",
    exportPotential: "medium",
    seasonality: "Year-round",
  },
  {
    crop: "Ginger",
    currentPrice: 80,
    previousPrice: 75,
    trend: "up",
    demand: 85,
    supply: 75,
    forecast: "bullish",
    exportPotential: "high",
    seasonality: "Peak: Dec-Feb",
  },
]

const getTrendIcon = (trend: string) => {
  switch (trend) {
    case "up":
      return <TrendingUp className="h-4 w-4 text-green-600" />
    case "down":
      return <TrendingDown className="h-4 w-4 text-red-600" />
    default:
      return <BarChart3 className="h-4 w-4 text-gray-600" />
  }
}

const getTrendColor = (trend: string) => {
  switch (trend) {
    case "up":
      return "text-green-600 dark:text-green-400"
    case "down":
      return "text-red-600 dark:text-red-400"
    default:
      return "text-gray-600 dark:text-gray-400"
  }
}

const getForecastColor = (forecast: string) => {
  switch (forecast) {
    case "bullish":
      return "default"
    case "bearish":
      return "destructive"
    default:
      return "secondary"
  }
}

const getExportPotentialColor = (potential: string) => {
  switch (potential) {
    case "high":
      return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
    case "medium":
      return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200"
    case "low":
      return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
    default:
      return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200"
  }
}

export function MarketInsights() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Kerala Market Insights
          </CardTitle>
          <CardDescription>Current market prices, trends, and forecasts for major crops in Kerala</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            {marketData.map((item, index) => (
              <Card key={index} className="p-4">
                <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="font-semibold text-lg">{item.crop}</h3>
                      <Badge className={getExportPotentialColor(item.exportPotential)}>
                        {item.exportPotential} export
                      </Badge>
                      <Badge variant={getForecastColor(item.forecast)}>{item.forecast}</Badge>
                    </div>
                    <p className="text-sm text-muted-foreground">{item.seasonality}</p>
                  </div>

                  <div className="grid gap-4 md:grid-cols-3 lg:w-2/3">
                    <div className="text-center">
                      <div className="flex items-center justify-center gap-2 mb-1">
                        {getTrendIcon(item.trend)}
                        <span className={`text-2xl font-bold ${getTrendColor(item.trend)}`}>₹{item.currentPrice}</span>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {item.trend === "up" ? "+" : item.trend === "down" ? "-" : ""}
                        {Math.abs(((item.currentPrice - item.previousPrice) / item.previousPrice) * 100).toFixed(1)}%
                      </p>
                      <p className="text-xs text-muted-foreground">per kg</p>
                    </div>

                    <div>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-medium">Demand</span>
                          <span className="text-xs text-muted-foreground">{item.demand}%</span>
                        </div>
                        <Progress value={item.demand} className="h-1.5" />
                      </div>
                    </div>

                    <div>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-medium">Supply</span>
                          <span className="text-xs text-muted-foreground">{item.supply}%</span>
                        </div>
                        <Progress value={item.supply} className="h-1.5" />
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Market Opportunities</CardTitle>
            <CardDescription>High-potential crops for investment</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-start gap-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
              <CheckCircle className="h-5 w-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-green-800 dark:text-green-200">Cardamom</h4>
                <p className="text-sm text-green-700 dark:text-green-300">
                  Strong export demand, prices trending upward. Limited supply creates opportunity.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
              <CheckCircle className="h-5 w-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-green-800 dark:text-green-200">Black Pepper</h4>
                <p className="text-sm text-green-700 dark:text-green-300">
                  Global demand increasing, Kerala pepper commands premium prices internationally.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
              <CheckCircle className="h-5 w-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-green-800 dark:text-green-200">Ginger</h4>
                <p className="text-sm text-green-700 dark:text-green-300">
                  Rising health consciousness driving demand. Good processing opportunities.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Market Risks</CardTitle>
            <CardDescription>Factors to consider before investing</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-start gap-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
              <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-yellow-800 dark:text-yellow-200">Price Volatility</h4>
                <p className="text-sm text-yellow-700 dark:text-yellow-300">
                  Spice prices can fluctuate significantly based on global market conditions.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
              <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-yellow-800 dark:text-yellow-200">Climate Dependency</h4>
                <p className="text-sm text-yellow-700 dark:text-yellow-300">
                  Monsoon patterns and climate change can affect crop yields and quality.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
              <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-yellow-800 dark:text-yellow-200">Export Regulations</h4>
                <p className="text-sm text-yellow-700 dark:text-yellow-300">
                  Changes in export policies can impact international market access.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Price Forecast Summary</CardTitle>
          <CardDescription>Expected price movements for the next 6 months</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <TrendingUp className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <h3 className="font-semibold text-green-800 dark:text-green-200">Bullish Crops</h3>
              <p className="text-sm text-green-700 dark:text-green-300">Cardamom, Black Pepper, Ginger</p>
              <p className="text-xs text-muted-foreground mt-1">Expected 10-15% price increase</p>
            </div>
            <div className="text-center p-4 bg-gray-50 dark:bg-gray-900/20 rounded-lg">
              <BarChart3 className="h-8 w-8 text-gray-600 mx-auto mb-2" />
              <h3 className="font-semibold text-gray-800 dark:text-gray-200">Stable Crops</h3>
              <p className="text-sm text-gray-700 dark:text-gray-300">Rice, Coconut</p>
              <p className="text-xs text-muted-foreground mt-1">Expected ±5% price variation</p>
            </div>
            <div className="text-center p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
              <TrendingDown className="h-8 w-8 text-red-600 mx-auto mb-2" />
              <h3 className="font-semibold text-red-800 dark:text-red-200">Bearish Crops</h3>
              <p className="text-sm text-red-700 dark:text-red-300">Banana</p>
              <p className="text-xs text-muted-foreground mt-1">Expected 5-10% price decrease</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
