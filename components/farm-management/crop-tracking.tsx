"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Plus, Droplets, Thermometer, TrendingUp } from "lucide-react"

interface Crop {
  id: string
  name: string
  variety: string
  area: number
  plantingDate: string
  expectedHarvest: string
  stage: string
  progress: number
  status: "healthy" | "attention" | "critical"
}

export function CropTracking() {
  const [crops, setCrops] = useState<Crop[]>([
    {
      id: "1",
      name: "Rice",
      variety: "Jyothi",
      area: 2.5,
      plantingDate: "2024-06-15",
      expectedHarvest: "2024-10-15",
      stage: "Flowering",
      progress: 65,
      status: "healthy",
    },
    {
      id: "2",
      name: "Coconut",
      variety: "Dwarf Green",
      area: 1.8,
      plantingDate: "2023-03-20",
      expectedHarvest: "2024-12-20",
      stage: "Fruiting",
      progress: 80,
      status: "healthy",
    },
    {
      id: "3",
      name: "Black Pepper",
      variety: "Panniyur 1",
      area: 0.5,
      plantingDate: "2024-05-10",
      expectedHarvest: "2025-01-10",
      stage: "Vegetative",
      progress: 35,
      status: "attention",
    },
  ])

  const [isAddingCrop, setIsAddingCrop] = useState(false)

  const getStatusColor = (status: string) => {
    switch (status) {
      case "healthy":
        return "bg-green-100 text-green-800"
      case "attention":
        return "bg-yellow-100 text-yellow-800"
      case "critical":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return "bg-green-500"
    if (progress >= 50) return "bg-yellow-500"
    return "bg-blue-500"
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Crop Tracking</h2>
          <p className="text-muted-foreground">Monitor your crops throughout their growth cycle</p>
        </div>
        <Dialog open={isAddingCrop} onOpenChange={setIsAddingCrop}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Crop
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add New Crop</DialogTitle>
              <DialogDescription>Enter details for the new crop you want to track</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="cropName">Crop Name</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select crop" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="rice">Rice</SelectItem>
                    <SelectItem value="coconut">Coconut</SelectItem>
                    <SelectItem value="pepper">Black Pepper</SelectItem>
                    <SelectItem value="cardamom">Cardamom</SelectItem>
                    <SelectItem value="banana">Banana</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="variety">Variety</Label>
                <Input id="variety" placeholder="Enter variety name" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="area">Area (Acres)</Label>
                <Input id="area" type="number" placeholder="0.0" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="plantingDate">Planting Date</Label>
                <Input id="plantingDate" type="date" />
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsAddingCrop(false)}>
                Cancel
              </Button>
              <Button onClick={() => setIsAddingCrop(false)}>Add Crop</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {crops.map((crop) => (
          <Card key={crop.id} className="relative">
            <CardHeader className="pb-3">
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-lg">{crop.name}</CardTitle>
                  <CardDescription>{crop.variety}</CardDescription>
                </div>
                <Badge className={getStatusColor(crop.status)}>{crop.status}</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-2">
                <div className="flex justify-between text-sm">
                  <span>Growth Progress</span>
                  <span className="font-medium">{crop.progress}%</span>
                </div>
                <Progress value={crop.progress} className="h-2" />
                <p className="text-xs text-muted-foreground">Current Stage: {crop.stage}</p>
              </div>

              <div className="grid gap-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Area:</span>
                  <span className="font-medium">{crop.area} acres</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Planted:</span>
                  <span className="font-medium">{new Date(crop.plantingDate).toLocaleDateString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Expected Harvest:</span>
                  <span className="font-medium">{new Date(crop.expectedHarvest).toLocaleDateString()}</span>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2 pt-2 border-t">
                <div className="text-center">
                  <Droplets className="h-4 w-4 mx-auto mb-1 text-blue-500" />
                  <p className="text-xs text-muted-foreground">Irrigation</p>
                  <p className="text-xs font-medium">Good</p>
                </div>
                <div className="text-center">
                  <Thermometer className="h-4 w-4 mx-auto mb-1 text-orange-500" />
                  <p className="text-xs text-muted-foreground">Temperature</p>
                  <p className="text-xs font-medium">Optimal</p>
                </div>
                <div className="text-center">
                  <TrendingUp className="h-4 w-4 mx-auto mb-1 text-green-500" />
                  <p className="text-xs text-muted-foreground">Growth</p>
                  <p className="text-xs font-medium">Normal</p>
                </div>
              </div>

              <Button variant="outline" className="w-full bg-transparent" size="sm">
                View Details
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
