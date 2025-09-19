"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { AlertTriangle, CheckCircle, Info, Search, Filter, Eye } from "lucide-react"
import { format } from "date-fns"

interface DetectionResult {
  id: string
  disease: string
  confidence: number
  severity: "low" | "medium" | "high"
  treatment: string[]
  prevention: string[]
  imageUrl: string
  timestamp: Date
  cropType: string
}

interface DetectionHistoryProps {
  history: DetectionResult[]
}

export function DetectionHistory({ history }: DetectionHistoryProps) {
  const [searchTerm, setSearchTerm] = useState("")
  const [severityFilter, setSeverityFilter] = useState<string>("all")
  const [cropFilter, setCropFilter] = useState<string>("all")

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case "high":
        return <AlertTriangle className="h-4 w-4 text-red-600 dark:text-red-400" />
      case "medium":
        return <Info className="h-4 w-4 text-yellow-600 dark:text-yellow-400" />
      case "low":
        return <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
      default:
        return <Info className="h-4 w-4" />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "high":
        return "destructive"
      case "medium":
        return "secondary"
      case "low":
        return "default"
      default:
        return "default"
    }
  }

  const filteredHistory = history.filter((item) => {
    const matchesSearch =
      item.disease.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.cropType.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesSeverity = severityFilter === "all" || item.severity === severityFilter
    const matchesCrop = cropFilter === "all" || item.cropType === cropFilter

    return matchesSearch && matchesSeverity && matchesCrop
  })

  const uniqueCrops = Array.from(new Set(history.map((item) => item.cropType)))

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Detection History</CardTitle>
          <CardDescription>View and manage your previous disease detection scans</CardDescription>
        </CardHeader>
        <CardContent>
          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search by disease or crop type..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={severityFilter} onValueChange={setSeverityFilter}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Severity" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Severities</SelectItem>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="low">Low</SelectItem>
              </SelectContent>
            </Select>
            <Select value={cropFilter} onValueChange={setCropFilter}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Crop Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Crops</SelectItem>
                {uniqueCrops.map((crop) => (
                  <SelectItem key={crop} value={crop}>
                    {crop}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Results */}
          {filteredHistory.length === 0 ? (
            <div className="text-center py-8">
              <Filter className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">No results found</h3>
              <p className="text-muted-foreground">Try adjusting your search or filter criteria</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredHistory.map((item) => (
                <Card key={item.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-4">
                      <img
                        src={item.imageUrl || "/placeholder.svg"}
                        alt={`${item.disease} detection`}
                        className="w-16 h-16 object-cover rounded-lg"
                      />
                      <div className="flex-1 space-y-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            {getSeverityIcon(item.severity)}
                            <h4 className="font-semibold">{item.disease}</h4>
                            <Badge variant={getSeverityColor(item.severity)} className="text-xs">
                              {item.severity.toUpperCase()}
                            </Badge>
                          </div>
                          <span className="text-sm text-muted-foreground">
                            {format(item.timestamp, "MMM dd, yyyy")}
                          </span>
                        </div>
                        <div className="flex items-center gap-4">
                          <Badge variant="outline">{item.cropType}</Badge>
                          <span className="text-sm text-muted-foreground">{item.confidence}% confidence</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Button size="sm" variant="outline">
                            <Eye className="h-4 w-4 mr-2" />
                            View Details
                          </Button>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
