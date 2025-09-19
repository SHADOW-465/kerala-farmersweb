"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Calendar, Sprout, Sun, CloudRain, Snowflake } from "lucide-react"

interface SeasonalCrop {
  name: string
  plantingMonths: string[]
  harvestMonths: string[]
  category: "spices" | "cereals" | "cash-crops" | "vegetables" | "fruits"
  difficulty: "easy" | "medium" | "hard"
}

const seasonalCrops: SeasonalCrop[] = [
  {
    name: "Rice (Kharif)",
    plantingMonths: ["May", "June", "July"],
    harvestMonths: ["September", "October", "November"],
    category: "cereals",
    difficulty: "medium",
  },
  {
    name: "Rice (Rabi)",
    plantingMonths: ["November", "December", "January"],
    harvestMonths: ["March", "April", "May"],
    category: "cereals",
    difficulty: "medium",
  },
  {
    name: "Black Pepper",
    plantingMonths: ["May", "June"],
    harvestMonths: ["December", "January", "February"],
    category: "spices",
    difficulty: "medium",
  },
  {
    name: "Cardamom",
    plantingMonths: ["April", "May", "June"],
    harvestMonths: ["October", "November", "December"],
    category: "spices",
    difficulty: "hard",
  },
  {
    name: "Coconut",
    plantingMonths: ["May", "June", "September", "October"],
    harvestMonths: ["All Year"],
    category: "cash-crops",
    difficulty: "easy",
  },
  {
    name: "Banana",
    plantingMonths: ["February", "March", "September", "October"],
    harvestMonths: ["All Year"],
    category: "fruits",
    difficulty: "easy",
  },
  {
    name: "Ginger",
    plantingMonths: ["April", "May", "June"],
    harvestMonths: ["December", "January", "February"],
    category: "spices",
    difficulty: "medium",
  },
  {
    name: "Turmeric",
    plantingMonths: ["May", "June", "July"],
    harvestMonths: ["January", "February", "March"],
    category: "spices",
    difficulty: "medium",
  },
  {
    name: "Rubber",
    plantingMonths: ["May", "June", "September", "October"],
    harvestMonths: ["All Year (after 7 years)"],
    category: "cash-crops",
    difficulty: "hard",
  },
  {
    name: "Tea",
    plantingMonths: ["May", "June", "September", "October"],
    harvestMonths: ["All Year (after 3 years)"],
    category: "cash-crops",
    difficulty: "hard",
  },
]

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
]

const getSeasonIcon = (month: string) => {
  const monthIndex = months.indexOf(month)
  if (monthIndex >= 2 && monthIndex <= 4) return <Sun className="h-4 w-4 text-yellow-500" /> // Spring
  if (monthIndex >= 5 && monthIndex <= 8) return <CloudRain className="h-4 w-4 text-blue-500" /> // Monsoon
  if (monthIndex >= 9 && monthIndex <= 11) return <Sun className="h-4 w-4 text-orange-500" /> // Post-monsoon
  return <Snowflake className="h-4 w-4 text-blue-300" /> // Winter
}

const getCategoryColor = (category: string) => {
  switch (category) {
    case "spices":
      return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
    case "cereals":
      return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200"
    case "cash-crops":
      return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
    case "vegetables":
      return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
    case "fruits":
      return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200"
    default:
      return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200"
  }
}

const getDifficultyColor = (difficulty: string) => {
  switch (difficulty) {
    case "easy":
      return "default"
    case "medium":
      return "secondary"
    case "hard":
      return "destructive"
    default:
      return "default"
  }
}

export function SeasonalCalendar() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="h-5 w-5" />
            Kerala Seasonal Planting Calendar
          </CardTitle>
          <CardDescription>Optimal planting and harvesting times for major crops in Kerala's climate</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            {seasonalCrops.map((crop, index) => (
              <Card key={index} className="p-4">
                <div className="flex flex-col md:flex-row md:items-center gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="font-semibold">{crop.name}</h3>
                      <Badge className={getCategoryColor(crop.category)}>{crop.category.replace("-", " ")}</Badge>
                      <Badge variant={getDifficultyColor(crop.difficulty)}>{crop.difficulty}</Badge>
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2 md:w-2/3">
                    <div>
                      <h4 className="text-sm font-medium mb-2 flex items-center gap-2">
                        <Sprout className="h-4 w-4 text-green-600" />
                        Planting Time
                      </h4>
                      <div className="flex flex-wrap gap-1">
                        {crop.plantingMonths.map((month) => (
                          <Badge key={month} variant="outline" className="text-xs">
                            {getSeasonIcon(month)}
                            <span className="ml-1">{month}</span>
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h4 className="text-sm font-medium mb-2 flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-orange-600" />
                        Harvest Time
                      </h4>
                      <div className="flex flex-wrap gap-1">
                        {crop.harvestMonths.map((month) => (
                          <Badge key={month} variant="outline" className="text-xs">
                            {month !== "All Year" &&
                              month !== "All Year (after 7 years)" &&
                              month !== "All Year (after 3 years)" &&
                              getSeasonIcon(month)}
                            <span className={month.includes("All Year") ? "" : "ml-1"}>{month}</span>
                          </Badge>
                        ))}
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
            <CardTitle>Kerala Seasons</CardTitle>
            <CardDescription>Understanding Kerala's agricultural seasons</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
              <Sun className="h-5 w-5 text-yellow-600" />
              <div>
                <h4 className="font-medium">Pre-Monsoon (March-May)</h4>
                <p className="text-sm text-muted-foreground">Hot and dry, prepare for planting</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <CloudRain className="h-5 w-5 text-blue-600" />
              <div>
                <h4 className="font-medium">Monsoon (June-September)</h4>
                <p className="text-sm text-muted-foreground">Heavy rainfall, main growing season</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
              <Sun className="h-5 w-5 text-orange-600" />
              <div>
                <h4 className="font-medium">Post-Monsoon (October-December)</h4>
                <p className="text-sm text-muted-foreground">Moderate rainfall, harvest time</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <Snowflake className="h-5 w-5 text-blue-400" />
              <div>
                <h4 className="font-medium">Winter (January-February)</h4>
                <p className="text-sm text-muted-foreground">Cool and dry, second planting season</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Planting Tips</CardTitle>
            <CardDescription>Best practices for seasonal planting</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="text-sm space-y-2">
              <div className="flex items-start gap-2">
                <div className="w-2 h-2 rounded-full bg-primary mt-1.5 flex-shrink-0" />
                <p>Start soil preparation 2-3 weeks before planting season</p>
              </div>
              <div className="flex items-start gap-2">
                <div className="w-2 h-2 rounded-full bg-primary mt-1.5 flex-shrink-0" />
                <p>Monitor weather forecasts for optimal planting windows</p>
              </div>
              <div className="flex items-start gap-2">
                <div className="w-2 h-2 rounded-full bg-primary mt-1.5 flex-shrink-0" />
                <p>Consider intercropping to maximize land utilization</p>
              </div>
              <div className="flex items-start gap-2">
                <div className="w-2 h-2 rounded-full bg-primary mt-1.5 flex-shrink-0" />
                <p>Plan irrigation systems before monsoon season</p>
              </div>
              <div className="flex items-start gap-2">
                <div className="w-2 h-2 rounded-full bg-primary mt-1.5 flex-shrink-0" />
                <p>Use disease-resistant varieties for better yields</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
