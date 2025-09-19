"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Sprout,
  TrendingUp,
  Droplets,
  Calendar,
  DollarSign,
  AlertTriangle,
  CheckCircle,
  Info,
  Star,
  Download,
  Share,
} from "lucide-react"
import type { CropRecommendation, SoilData } from "./crop-recommendation-content"

interface RecommendationResultsProps {
  recommendations: CropRecommendation[]
  soilData: SoilData | null
}

export function RecommendationResults({ recommendations, soilData }: RecommendationResultsProps) {
  const [sortBy, setSortBy] = useState("suitability")
  const [filterBy, setFilterBy] = useState("all")

  const getProfitabilityColor = (profitability: string) => {
    switch (profitability) {
      case "high":
        return "text-green-600 dark:text-green-400"
      case "medium":
        return "text-yellow-600 dark:text-yellow-400"
      case "low":
        return "text-red-600 dark:text-red-400"
      default:
        return "text-gray-600 dark:text-gray-400"
    }
  }

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "low":
        return "default"
      case "medium":
        return "secondary"
      case "high":
        return "destructive"
      default:
        return "default"
    }
  }

  const getWaterRequirementIcon = (requirement: string) => {
    const baseClass = "h-4 w-4"
    switch (requirement) {
      case "low":
        return <Droplets className={`${baseClass} text-blue-400`} />
      case "medium":
        return <Droplets className={`${baseClass} text-blue-600`} />
      case "high":
        return <Droplets className={`${baseClass} text-blue-800`} />
      default:
        return <Droplets className={baseClass} />
    }
  }

  const sortedRecommendations = [...recommendations].sort((a, b) => {
    switch (sortBy) {
      case "suitability":
        return b.suitabilityScore - a.suitabilityScore
      case "profitability":
        return b.marketPrice - a.marketPrice
      case "market-demand":
        return b.marketDemand - a.marketDemand
      default:
        return 0
    }
  })

  const filteredRecommendations = sortedRecommendations.filter((crop) => {
    if (filterBy === "all") return true
    return crop.profitability === filterBy
  })

  return (
    <div className="space-y-6">
      {/* Summary Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sprout className="h-5 w-5 text-primary" />
            Crop Recommendations Summary
          </CardTitle>
          <CardDescription>
            Based on your soil analysis and environmental conditions in {soilData?.location}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{recommendations.length}</div>
              <p className="text-sm text-muted-foreground">Suitable Crops</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {recommendations.filter((c) => c.profitability === "high").length}
              </div>
              <p className="text-sm text-muted-foreground">High Profit</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {recommendations.filter((c) => c.riskLevel === "low").length}
              </div>
              <p className="text-sm text-muted-foreground">Low Risk</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {Math.round(recommendations.reduce((acc, c) => acc + c.suitabilityScore, 0) / recommendations.length)}%
              </div>
              <p className="text-sm text-muted-foreground">Avg. Suitability</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Filters and Sorting */}
      <div className="flex flex-col sm:flex-row gap-4">
        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className="w-full sm:w-48">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="suitability">Suitability Score</SelectItem>
            <SelectItem value="profitability">Market Price</SelectItem>
            <SelectItem value="market-demand">Market Demand</SelectItem>
          </SelectContent>
        </Select>
        <Select value={filterBy} onValueChange={setFilterBy}>
          <SelectTrigger className="w-full sm:w-48">
            <SelectValue placeholder="Filter by profitability" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Crops</SelectItem>
            <SelectItem value="high">High Profitability</SelectItem>
            <SelectItem value="medium">Medium Profitability</SelectItem>
            <SelectItem value="low">Low Profitability</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Recommendations Grid */}
      <div className="grid gap-6">
        {filteredRecommendations.map((crop, index) => (
          <Card key={crop.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  {index === 0 && <Star className="h-5 w-5 text-yellow-500" />}
                  <div>
                    <CardTitle className="text-xl">{crop.name}</CardTitle>
                    <CardDescription>Expected yield: {crop.expectedYield}</CardDescription>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-primary">{crop.suitabilityScore}%</div>
                  <p className="text-sm text-muted-foreground">Suitability</p>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="overview" className="space-y-4">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="overview">Overview</TabsTrigger>
                  <TabsTrigger value="details">Details</TabsTrigger>
                  <TabsTrigger value="timeline">Timeline</TabsTrigger>
                </TabsList>

                <TabsContent value="overview" className="space-y-4">
                  {/* Key Metrics */}
                  <div className="grid gap-4 md:grid-cols-3">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">Soil Suitability</span>
                        <span className="text-sm text-muted-foreground">{crop.soilSuitability}%</span>
                      </div>
                      <Progress value={crop.soilSuitability} className="h-2" />
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">Market Demand</span>
                        <span className="text-sm text-muted-foreground">{crop.marketDemand}%</span>
                      </div>
                      <Progress value={crop.marketDemand} className="h-2" />
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">Overall Score</span>
                        <span className="text-sm text-muted-foreground">{crop.suitabilityScore}%</span>
                      </div>
                      <Progress value={crop.suitabilityScore} className="h-2" />
                    </div>
                  </div>

                  {/* Badges */}
                  <div className="flex flex-wrap gap-2">
                    <Badge variant={crop.profitability === "high" ? "default" : "secondary"}>
                      <TrendingUp className="h-3 w-3 mr-1" />
                      {crop.profitability.charAt(0).toUpperCase() + crop.profitability.slice(1)} Profit
                    </Badge>
                    <Badge variant={getRiskColor(crop.riskLevel)}>
                      <AlertTriangle className="h-3 w-3 mr-1" />
                      {crop.riskLevel.charAt(0).toUpperCase() + crop.riskLevel.slice(1)} Risk
                    </Badge>
                    <Badge variant="outline">
                      {getWaterRequirementIcon(crop.waterRequirement)}
                      <span className="ml-1">
                        {crop.waterRequirement.charAt(0).toUpperCase() + crop.waterRequirement.slice(1)} Water
                      </span>
                    </Badge>
                    <Badge variant="outline">
                      <DollarSign className="h-3 w-3 mr-1" />₹{crop.marketPrice}/kg
                    </Badge>
                  </div>

                  {/* Advantages */}
                  <div>
                    <h4 className="font-medium mb-2 flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      Key Advantages
                    </h4>
                    <ul className="space-y-1">
                      {crop.advantages.slice(0, 3).map((advantage, idx) => (
                        <li key={idx} className="text-sm text-muted-foreground flex items-start gap-2">
                          <div className="w-1 h-1 rounded-full bg-green-600 mt-2 flex-shrink-0" />
                          {advantage}
                        </li>
                      ))}
                    </ul>
                  </div>
                </TabsContent>

                <TabsContent value="details" className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <h4 className="font-medium mb-2 flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        Advantages
                      </h4>
                      <ul className="space-y-2">
                        {crop.advantages.map((advantage, idx) => (
                          <li key={idx} className="text-sm text-muted-foreground flex items-start gap-2">
                            <CheckCircle className="h-3 w-3 text-green-600 mt-0.5 flex-shrink-0" />
                            {advantage}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h4 className="font-medium mb-2 flex items-center gap-2">
                        <Info className="h-4 w-4 text-orange-600" />
                        Considerations
                      </h4>
                      <ul className="space-y-2">
                        {crop.considerations.map((consideration, idx) => (
                          <li key={idx} className="text-sm text-muted-foreground flex items-start gap-2">
                            <Info className="h-3 w-3 text-orange-600 mt-0.5 flex-shrink-0" />
                            {consideration}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="timeline" className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                      <h4 className="font-medium text-green-800 dark:text-green-200 mb-2 flex items-center gap-2">
                        <Calendar className="h-4 w-4" />
                        Best Planting Time
                      </h4>
                      <p className="text-sm text-green-700 dark:text-green-300">{crop.bestPlantingTime}</p>
                    </div>
                    <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                      <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2 flex items-center gap-2">
                        <Calendar className="h-4 w-4" />
                        Harvest Time
                      </h4>
                      <p className="text-sm text-blue-700 dark:text-blue-300">{crop.harvestTime}</p>
                    </div>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <h4 className="font-medium mb-2">Growth Period</h4>
                    <p className="text-sm text-muted-foreground">{crop.growthPeriod}</p>
                  </div>
                </TabsContent>
              </Tabs>

              <div className="flex gap-2 mt-4">
                <Button size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  Download Report
                </Button>
                <Button size="sm" variant="outline">
                  <Share className="h-4 w-4 mr-2" />
                  Share
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredRecommendations.length === 0 && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Sprout className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No crops match your filters</h3>
            <p className="text-muted-foreground text-center">Try adjusting your filter criteria to see more options.</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
