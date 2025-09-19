"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { SoilAnalysisForm } from "./soil-analysis-form"
import { RecommendationResults } from "./recommendation-results"
import { SeasonalCalendar } from "./seasonal-calendar"
import { MarketInsights } from "./market-insights"
import { Sprout, Calendar, TrendingUp, TestTube } from "lucide-react"
import { apiClient, CropRecommendation } from "@/lib/api-client"
import { useToast } from "@/hooks/use-toast"

export interface SoilData {
  ph: number
  nitrogen: number
  phosphorus: number
  potassium: number
  organicMatter: number
  soilType: string
  rainfall: number
  temperature: number
  season: string
  location: string
}

export interface CropRecommendation {
  id: string
  name: string
  suitabilityScore: number
  expectedYield: string
  marketPrice: number
  profitability: "high" | "medium" | "low"
  growthPeriod: string
  waterRequirement: "low" | "medium" | "high"
  soilSuitability: number
  marketDemand: number
  riskLevel: "low" | "medium" | "high"
  advantages: string[]
  considerations: string[]
  bestPlantingTime: string
  harvestTime: string
}

export function CropRecommendationContent() {
  const [soilData, setSoilData] = useState<SoilData | null>(null)
  const [recommendations, setRecommendations] = useState<CropRecommendation[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const { toast } = useToast()

  const handleSoilAnalysis = async (data: SoilData) => {
    setIsAnalyzing(true)
    setSoilData(data)

    try {
      // Call API for crop recommendations
      const response = await apiClient.getCropRecommendations({
        ph: data.ph,
        nitrogen: data.nitrogen,
        phosphorus: data.phosphorus,
        potassium: data.potassium,
        rainfall: data.rainfall,
        temperature: data.temperature,
        soil_type: data.soilType,
        season: data.season,
      })

      if (response.success && response.data) {
        const apiRecommendations = response.data.recommendations
        
        // Transform API response to match our interface
        const transformedRecommendations: CropRecommendation[] = apiRecommendations.map((rec, index) => ({
          id: (index + 1).toString(),
          name: rec.crop,
          suitabilityScore: rec.suitability_score,
          expectedYield: `${rec.estimated_yield} kg/hectare`,
          marketPrice: 0, // Not provided by API
          profitability: rec.suitability_score > 80 ? "high" : rec.suitability_score > 60 ? "medium" : "low",
          growthPeriod: `${rec.growth_period_days} days`,
          waterRequirement: "medium", // Not provided by API
          soilSuitability: rec.suitability_score,
          marketDemand: rec.market_demand === "Very High" ? 95 : rec.market_demand === "High" ? 80 : rec.market_demand === "Medium" ? 60 : 40,
          riskLevel: rec.suitability_score > 80 ? "low" : rec.suitability_score > 60 ? "medium" : "high",
          advantages: [
            `Suitability: ${rec.suitability_level}`,
            `Market demand: ${rec.market_demand}`,
            `Profit margin: ${(rec.profit_margin * 100).toFixed(1)}%`,
            `Optimal pH: ${rec.ph_optimal}`,
          ],
          considerations: [
            `Optimal rainfall: ${rec.rainfall_optimal}mm`,
            `Optimal temperature: ${rec.temp_optimal}°C`,
            `Recommended season: ${rec.recommended_season}`,
          ],
          bestPlantingTime: rec.recommended_season,
          harvestTime: "Varies by crop",
        }))

        setRecommendations(transformedRecommendations)
        
        toast({
          title: "Crop Recommendations Generated",
          description: `Found ${transformedRecommendations.length} suitable crops for your soil conditions`,
        })
      } else {
        throw new Error(response.error || 'Failed to get recommendations')
      }
    } catch (error) {
      console.error('Crop recommendation error:', error)
      toast({
        title: "Recommendation Failed",
        description: error instanceof Error ? error.message : 'An error occurred while generating recommendations',
        variant: "destructive",
      })
      
      // Fallback to mock data
    const mockRecommendations: CropRecommendation[] = [
      {
        id: "1",
        name: "Black Pepper",
        suitabilityScore: 92,
        expectedYield: "2-3 kg per vine",
        marketPrice: 450,
        profitability: "high",
        growthPeriod: "3-4 years to maturity",
        waterRequirement: "medium",
        soilSuitability: 95,
        marketDemand: 88,
        riskLevel: "low",
        advantages: [
          "High market value and demand",
          "Suitable for Kerala's climate",
          "Long-term profitable crop",
          "Can be intercropped with coconut",
        ],
        considerations: ["Requires initial investment", "Takes time to mature", "Needs proper support structures"],
        bestPlantingTime: "May-June (Pre-monsoon)",
        harvestTime: "December-February",
      },
      ]
    setRecommendations(mockRecommendations)
    } finally {
    setIsAnalyzing(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-balance">Crop Recommendation Engine</h1>
        <p className="text-muted-foreground text-pretty">
          Get AI-powered crop suggestions based on your soil conditions, climate, and market trends in Kerala.
        </p>
      </div>

      <Tabs defaultValue="analysis" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="analysis" className="flex items-center gap-2">
            <TestTube className="h-4 w-4" />
            Soil Analysis
          </TabsTrigger>
          <TabsTrigger value="recommendations" className="flex items-center gap-2" disabled={!recommendations.length}>
            <Sprout className="h-4 w-4" />
            Recommendations
          </TabsTrigger>
          <TabsTrigger value="calendar" className="flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            Seasonal Calendar
          </TabsTrigger>
          <TabsTrigger value="market" className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4" />
            Market Insights
          </TabsTrigger>
        </TabsList>

        <TabsContent value="analysis">
          <SoilAnalysisForm onSubmit={handleSoilAnalysis} isAnalyzing={isAnalyzing} />
        </TabsContent>

        <TabsContent value="recommendations">
          {recommendations.length > 0 ? (
            <RecommendationResults recommendations={recommendations} soilData={soilData} />
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Sprout className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No Recommendations Yet</h3>
                <p className="text-muted-foreground text-center">
                  Complete the soil analysis to get personalized crop recommendations for your farm.
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="calendar">
          <SeasonalCalendar />
        </TabsContent>

        <TabsContent value="market">
          <MarketInsights />
        </TabsContent>
      </Tabs>
    </div>
  )
}
