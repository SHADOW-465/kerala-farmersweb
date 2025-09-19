"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Progress } from "@/components/ui/progress"
import { AlertTriangle, CheckCircle, Info, Download, Share, BookOpen } from "lucide-react"

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

interface DetectionResultsProps {
  result: DetectionResult
}

export function DetectionResults({ result }: DetectionResultsProps) {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "high":
        return "text-red-600 dark:text-red-400"
      case "medium":
        return "text-yellow-600 dark:text-yellow-400"
      case "low":
        return "text-green-600 dark:text-green-400"
      default:
        return "text-gray-600 dark:text-gray-400"
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case "high":
        return <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400" />
      case "medium":
        return <Info className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
      case "low":
        return <CheckCircle className="h-5 w-5 text-green-600 dark:text-green-400" />
      default:
        return <Info className="h-5 w-5" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Main Result */}
      <div className="flex items-start gap-4">
        <img
          src={result.imageUrl || "/placeholder.svg"}
          alt="Analyzed plant"
          className="w-24 h-24 object-cover rounded-lg"
        />
        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-2">
            {getSeverityIcon(result.severity)}
            <h3 className="text-xl font-semibold">{result.disease}</h3>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground">Confidence:</span>
              <div className="flex items-center gap-2">
                <Progress value={result.confidence} className="w-20 h-2" />
                <span className="text-sm font-medium">{result.confidence}%</span>
              </div>
            </div>
            <Badge variant="outline">{result.cropType}</Badge>
          </div>
          <p className={`text-sm ${getSeverityColor(result.severity)}`}>
            Severity: {result.severity.charAt(0).toUpperCase() + result.severity.slice(1)}
          </p>
        </div>
      </div>

      <Separator />

      {/* Treatment Recommendations */}
      {result.treatment.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-orange-600" />
              Immediate Treatment
            </CardTitle>
            <CardDescription>Follow these steps to treat the identified disease</CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {result.treatment.map((step, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-orange-100 dark:bg-orange-900 text-orange-600 dark:text-orange-400 text-xs font-medium">
                    {index + 1}
                  </div>
                  <p className="text-sm">{step}</p>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Prevention Tips */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <CheckCircle className="h-5 w-5 text-green-600" />
            Prevention Tips
          </CardTitle>
          <CardDescription>Prevent future occurrences with these practices</CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            {result.prevention.map((tip, index) => (
              <li key={index} className="flex items-start gap-3">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 text-xs font-medium">
                  {index + 1}
                </div>
                <p className="text-sm">{tip}</p>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-3">
        <Button>
          <Download className="h-4 w-4 mr-2" />
          Download Report
        </Button>
        <Button variant="outline">
          <Share className="h-4 w-4 mr-2" />
          Share Results
        </Button>
        <Button variant="outline">
          <BookOpen className="h-4 w-4 mr-2" />
          Learn More
        </Button>
      </div>
    </div>
  )
}
