"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertTriangle, CloudRain, Droplets, CheckCircle, Clock, X } from "lucide-react"

interface FarmingAlertsProps {
  alerts: Array<{
    id: string
    type: "weather" | "farming" | "irrigation"
    severity: "low" | "medium" | "high"
    title: string
    description: string
    action: string
    validUntil: string
  }>
}

export function FarmingAlerts({ alerts }: FarmingAlertsProps) {
  const getAlertIcon = (type: string) => {
    switch (type) {
      case "weather":
        return <CloudRain className="h-5 w-5" />
      case "farming":
        return <AlertTriangle className="h-5 w-5" />
      case "irrigation":
        return <Droplets className="h-5 w-5" />
      default:
        return <AlertTriangle className="h-5 w-5" />
    }
  }

  const getAlertVariant = (severity: string) => {
    switch (severity) {
      case "high":
        return "destructive"
      case "medium":
        return "default"
      case "low":
        return "secondary"
      default:
        return "default"
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "high":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
      case "medium":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200"
      case "low":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200"
    }
  }

  const formatValidUntil = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffHours = Math.ceil((date.getTime() - now.getTime()) / (1000 * 60 * 60))

    if (diffHours < 24) {
      return `${diffHours} hours`
    }
    return `${Math.ceil(diffHours / 24)} days`
  }

  const activeAlerts = alerts.filter((alert) => new Date(alert.validUntil) > new Date())
  const expiredAlerts = alerts.filter((alert) => new Date(alert.validUntil) <= new Date())

  return (
    <div className="space-y-6">
      {/* Active Alerts */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-orange-600" />
                Active Farm Alerts
              </CardTitle>
              <CardDescription>Important weather and farming notifications requiring attention</CardDescription>
            </div>
            <Badge variant="outline">{activeAlerts.length} active</Badge>
          </div>
        </CardHeader>
        <CardContent>
          {activeAlerts.length === 0 ? (
            <div className="text-center py-8">
              <CheckCircle className="h-12 w-12 text-green-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-green-800 mb-2">No Active Alerts</h3>
              <p className="text-muted-foreground">All clear! No weather or farming alerts at this time.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {activeAlerts.map((alert) => (
                <Alert key={alert.id} variant={getAlertVariant(alert.severity)}>
                  <div className="flex items-start gap-3">
                    {getAlertIcon(alert.type)}
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <AlertTitle>{alert.title}</AlertTitle>
                        <Badge className={getSeverityColor(alert.severity)}>{alert.severity.toUpperCase()}</Badge>
                        <Badge variant="outline" className="text-xs">
                          {alert.type}
                        </Badge>
                      </div>
                      <AlertDescription className="mb-3">{alert.description}</AlertDescription>
                      <div className="space-y-2">
                        <div className="p-3 bg-muted rounded-lg">
                          <h4 className="text-sm font-medium mb-1">Recommended Action:</h4>
                          <p className="text-sm">{alert.action}</p>
                        </div>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <Clock className="h-4 w-4" />
                            Valid for {formatValidUntil(alert.validUntil)}
                          </div>
                          <Button size="sm" variant="outline">
                            <X className="h-4 w-4 mr-2" />
                            Dismiss
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </Alert>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Alert Statistics */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <CloudRain className="h-4 w-4 text-blue-600" />
              Weather Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{alerts.filter((a) => a.type === "weather").length}</div>
            <p className="text-sm text-muted-foreground">This week</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-orange-600" />
              Farming Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">
              {alerts.filter((a) => a.type === "farming").length}
            </div>
            <p className="text-sm text-muted-foreground">This week</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Droplets className="h-4 w-4 text-green-600" />
              Irrigation Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {alerts.filter((a) => a.type === "irrigation").length}
            </div>
            <p className="text-sm text-muted-foreground">This week</p>
          </CardContent>
        </Card>
      </div>

      {/* Recent Alerts History */}
      {expiredAlerts.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recent Alert History</CardTitle>
            <CardDescription>Previously active alerts for reference</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {expiredAlerts.slice(0, 3).map((alert) => (
                <div key={alert.id} className="flex items-center gap-3 p-3 bg-muted/50 rounded-lg opacity-60">
                  {getAlertIcon(alert.type)}
                  <div className="flex-1">
                    <h4 className="text-sm font-medium">{alert.title}</h4>
                    <p className="text-xs text-muted-foreground">{alert.description}</p>
                  </div>
                  <Badge variant="outline" className="text-xs">
                    Expired
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Alert Preferences */}
      <Card>
        <CardHeader>
          <CardTitle>Alert Preferences</CardTitle>
          <CardDescription>Customize which alerts you want to receive</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 border rounded-lg">
              <div className="flex items-center gap-3">
                <CloudRain className="h-5 w-5 text-blue-600" />
                <div>
                  <h4 className="text-sm font-medium">Weather Warnings</h4>
                  <p className="text-xs text-muted-foreground">Heavy rain, storms, extreme temperatures</p>
                </div>
              </div>
              <Badge variant="default">Enabled</Badge>
            </div>
            <div className="flex items-center justify-between p-3 border rounded-lg">
              <div className="flex items-center gap-3">
                <AlertTriangle className="h-5 w-5 text-orange-600" />
                <div>
                  <h4 className="text-sm font-medium">Farming Advisories</h4>
                  <p className="text-xs text-muted-foreground">Planting, harvesting, pest management</p>
                </div>
              </div>
              <Badge variant="default">Enabled</Badge>
            </div>
            <div className="flex items-center justify-between p-3 border rounded-lg">
              <div className="flex items-center gap-3">
                <Droplets className="h-5 w-5 text-green-600" />
                <div>
                  <h4 className="text-sm font-medium">Irrigation Reminders</h4>
                  <p className="text-xs text-muted-foreground">Water scheduling, drought conditions</p>
                </div>
              </div>
              <Badge variant="secondary">Disabled</Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
