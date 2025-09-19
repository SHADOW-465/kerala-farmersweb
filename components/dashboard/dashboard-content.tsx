"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Settings, TrendingUp, Droplets, Leaf } from "lucide-react"

export function DashboardContent() {
  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-foreground">Dashboard</h1>
        <Button className="bg-primary text-primary-foreground hover:bg-primary/90">Add Custom Widget</Button>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="kpi-card h-fit">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Soil Quality Level</CardTitle>
            <Settings className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="pb-4">
            <div className="text-3xl font-bold text-foreground">7.2 pH</div>
            <div className="flex items-center gap-2 mt-1">
              <TrendingUp className="h-4 w-4 text-green-500" />
              <span className="text-sm text-muted-foreground">vs. last soil test</span>
            </div>
            <div className="trend-chart mt-4">
              <div className="flex items-end justify-center gap-1 h-8">
                {[3, 5, 4, 6, 7, 8, 6, 7].map((height, i) => (
                  <div key={i} className="bg-green-500 rounded-sm w-3" style={{ height: `${height * 4}px` }} />
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="kpi-card h-fit">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Crop Health Index</CardTitle>
            <Settings className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="pb-4">
            <div className="text-3xl font-bold text-foreground">85.5/100%</div>
            <div className="flex items-center gap-2 mt-1">
              <TrendingUp className="h-4 w-4 text-green-500" />
              <span className="text-sm text-muted-foreground">+3% from last month</span>
            </div>
            <div className="trend-chart mt-4">
              <div className="flex items-end justify-center gap-1 h-8">
                {[4, 6, 5, 7, 8, 9, 8, 9].map((height, i) => (
                  <div key={i} className="bg-blue-500 rounded-sm w-3" style={{ height: `${height * 3.5}px` }} />
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="kpi-card h-fit">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Expected Harvest Value</CardTitle>
            <Settings className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="pb-4">
            <div className="text-3xl font-bold text-foreground">₹4,67,570</div>
            <div className="flex items-center gap-2 mt-1">
              <TrendingUp className="h-4 w-4 text-green-500" />
              <span className="text-sm text-muted-foreground">+12% from last season</span>
            </div>
            <div className="trend-chart mt-4">
              <div className="flex items-end justify-center gap-1 h-8">
                {[5, 7, 6, 8, 9, 10, 9, 10].map((height, i) => (
                  <div key={i} className="bg-green-500 rounded-sm w-3" style={{ height: `${height * 3}px` }} />
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card className="kpi-card flex flex-col">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold text-center">Irrigation Efficiency</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 flex flex-col items-center justify-center pb-4">
            <div className="gauge-chart">
              <div className="relative w-32 h-32 mx-auto">
                <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 120 120">
                  <circle cx="60" cy="60" r="50" stroke="#e5e7eb" strokeWidth="8" fill="none" />
                  <circle
                    cx="60"
                    cy="60"
                    r="50"
                    stroke="#48bb78"
                    strokeWidth="8"
                    fill="none"
                    strokeDasharray={`${72 * 3.14} ${100 * 3.14}`}
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-3xl font-bold text-foreground">72%</span>
                </div>
              </div>
              <p className="text-sm text-muted-foreground text-center mt-3">Deviation Index: 2%</p>
            </div>
          </CardContent>
        </Card>

        <Card className="kpi-card flex flex-col">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold text-center">Sustainable Practices</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 flex flex-col pb-4">
            <div className="gauge-chart flex-1">
              <div className="relative w-32 h-32 mx-auto">
                <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 120 120">
                  <circle cx="60" cy="60" r="50" stroke="#e5e7eb" strokeWidth="8" fill="none" />
                  <circle
                    cx="60"
                    cy="60"
                    r="50"
                    stroke="#4299e1"
                    strokeWidth="8"
                    fill="none"
                    strokeDasharray={`${86 * 3.14} ${100 * 3.14}`}
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-3xl font-bold text-foreground">86%</span>
                </div>
              </div>
              <div className="space-y-2 mt-4">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Organic Methods</span>
                  <span className="font-medium">34%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Water Conservation</span>
                  <span className="font-medium">28%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Crop Rotation</span>
                  <span className="font-medium">24%</span>
                </div>
              </div>
              <Button variant="outline" size="sm" className="w-full mt-4 bg-transparent">
                View Details
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="kpi-card flex flex-col">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold">Crop Distribution in Kerala</CardTitle>
            <CardDescription>Current season crop allocation</CardDescription>
          </CardHeader>
          <CardContent className="flex-1 flex flex-col pb-4">
            <div className="space-y-3 flex-1">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  <span className="text-sm">Rice - 40%</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                  <span className="text-sm">Coconut - 25%</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-orange-500"></div>
                  <span className="text-sm">Spices - 20%</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                  <span className="text-sm">Rubber - 15%</span>
                </div>
              </div>
            </div>
            <div className="mt-4 h-20 bg-gradient-to-r from-green-500 via-blue-500 via-orange-500 to-purple-500 rounded-lg opacity-20"></div>
          </CardContent>
        </Card>

        <Card className="kpi-card flex flex-col">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold">Farm Locations</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 pb-4">
            <div className="relative h-40 bg-gradient-to-br from-green-100 to-blue-100 rounded-lg overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-green-200/50 to-blue-200/50"></div>
              <div className="absolute top-3 right-3 bg-primary text-primary-foreground px-2 py-1 rounded text-xs font-medium">
                Kerala
              </div>
              <div className="absolute bottom-3 left-3 space-y-1">
                <div className="flex items-center gap-2 text-xs">
                  <div className="w-2 h-2 rounded-full bg-green-500"></div>
                  <span>Active Farms: 89%</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <div className="w-2 h-2 rounded-full bg-orange-500"></div>
                  <span>Under Development: 11%</span>
                </div>
              </div>
              <div className="absolute top-6 left-8 w-2 h-2 bg-green-500 rounded-full"></div>
              <div className="absolute top-10 right-12 w-2 h-2 bg-green-500 rounded-full"></div>
              <div className="absolute bottom-12 left-12 w-2 h-2 bg-orange-500 rounded-full"></div>
              <div className="absolute bottom-8 right-8 w-2 h-2 bg-green-500 rounded-full"></div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card className="kpi-card lg:col-span-2 flex items-center">
          <CardContent className="p-6 w-full">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-orange-100 shrink-0">
                  <span className="text-xl font-bold text-orange-600">76.2</span>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">Climate Adaptation Index</h3>
                  <p className="text-sm text-muted-foreground">Impact of climate change on Kerala farming practices</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="kpi-card flex items-center">
          <CardContent className="p-6 w-full">
            <div className="flex items-center gap-3">
              <Droplets className="h-8 w-8 text-blue-500 shrink-0" />
              <div>
                <h3 className="font-semibold text-foreground">Monsoon Water Level</h3>
                <div className="text-2xl font-bold text-foreground">57m</div>
                <p className="text-sm text-muted-foreground">Current reservoir levels</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="kpi-card bg-gradient-to-br from-green-500 to-green-600 text-white flex items-center">
          <CardContent className="p-6 w-full">
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <Leaf className="h-6 w-6" />
                <span className="font-semibold">AgroGlobal</span>
              </div>
              <h3 className="text-lg font-bold">Let's join our community</h3>
              <p className="text-sm opacity-90">Connect with fellow Kerala farmers</p>
              <div className="flex items-center gap-2">
                <div className="flex -space-x-2">
                  <div className="w-6 h-6 rounded-full bg-white/20 border-2 border-white"></div>
                  <div className="w-6 h-6 rounded-full bg-white/20 border-2 border-white"></div>
                  <div className="w-6 h-6 rounded-full bg-white/20 border-2 border-white"></div>
                </div>
                <span className="text-sm">250+ people</span>
              </div>
              <Button variant="secondary" size="sm" className="bg-white text-green-600 hover:bg-white/90">
                Join Network
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
