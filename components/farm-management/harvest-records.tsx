"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Textarea } from "@/components/ui/textarea"
import { Plus, Package, TrendingUp, Calendar, Weight } from "lucide-react"

interface HarvestRecord {
  id: string
  crop: string
  variety: string
  quantity: number
  unit: string
  quality: "excellent" | "good" | "average" | "poor"
  harvestDate: string
  area: number
  pricePerUnit: number
  totalValue: number
  notes?: string
}

export function HarvestRecords() {
  const [harvests, setHarvests] = useState<HarvestRecord[]>([
    {
      id: "1",
      crop: "Rice",
      variety: "Jyothi",
      quantity: 2500,
      unit: "kg",
      quality: "excellent",
      harvestDate: "2024-10-15",
      area: 2.5,
      pricePerUnit: 25,
      totalValue: 62500,
      notes: "Good weather conditions during harvest",
    },
    {
      id: "2",
      crop: "Coconut",
      variety: "Dwarf Green",
      quantity: 800,
      unit: "pieces",
      quality: "good",
      harvestDate: "2024-07-20",
      area: 1.8,
      pricePerUnit: 18,
      totalValue: 14400,
      notes: "Regular monthly harvest",
    },
    {
      id: "3",
      crop: "Black Pepper",
      variety: "Panniyur 1",
      quantity: 45,
      unit: "kg",
      quality: "excellent",
      harvestDate: "2024-01-10",
      area: 0.5,
      pricePerUnit: 450,
      totalValue: 20250,
      notes: "Premium quality pepper, good market price",
    },
  ])

  const [isAddingHarvest, setIsAddingHarvest] = useState(false)

  const totalHarvestValue = harvests.reduce((sum, h) => sum + h.totalValue, 0)
  const totalQuantity = harvests.reduce((sum, h) => sum + h.quantity, 0)

  const getQualityColor = (quality: string) => {
    switch (quality) {
      case "excellent":
        return "bg-green-100 text-green-800"
      case "good":
        return "bg-blue-100 text-blue-800"
      case "average":
        return "bg-yellow-100 text-yellow-800"
      case "poor":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const calculateYield = (quantity: number, area: number, unit: string) => {
    const yieldPerAcre = quantity / area
    return `${yieldPerAcre.toFixed(1)} ${unit}/acre`
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Harvest Records</h2>
          <p className="text-muted-foreground">Track your harvest yields and quality</p>
        </div>
        <Dialog open={isAddingHarvest} onOpenChange={setIsAddingHarvest}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Harvest
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Record New Harvest</DialogTitle>
              <DialogDescription>Enter details of your latest harvest</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="crop">Crop</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select crop" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="rice">Rice</SelectItem>
                      <SelectItem value="coconut">Coconut</SelectItem>
                      <SelectItem value="pepper">Black Pepper</SelectItem>
                      <SelectItem value="cardamom">Cardamom</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="variety">Variety</Label>
                  <Input id="variety" placeholder="Enter variety" />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="quantity">Quantity</Label>
                  <Input id="quantity" type="number" placeholder="0" />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="unit">Unit</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Unit" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="kg">Kg</SelectItem>
                      <SelectItem value="tons">Tons</SelectItem>
                      <SelectItem value="pieces">Pieces</SelectItem>
                      <SelectItem value="bags">Bags</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="area">Area (Acres)</Label>
                  <Input id="area" type="number" placeholder="0.0" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="quality">Quality</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select quality" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="excellent">Excellent</SelectItem>
                      <SelectItem value="good">Good</SelectItem>
                      <SelectItem value="average">Average</SelectItem>
                      <SelectItem value="poor">Poor</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="harvestDate">Harvest Date</Label>
                  <Input id="harvestDate" type="date" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="pricePerUnit">Price per Unit (₹)</Label>
                  <Input id="pricePerUnit" type="number" placeholder="0.00" />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="totalValue">Total Value (₹)</Label>
                  <Input id="totalValue" type="number" placeholder="0.00" disabled />
                </div>
              </div>

              <div className="grid gap-2">
                <Label htmlFor="notes">Notes (Optional)</Label>
                <Textarea id="notes" placeholder="Any additional notes about the harvest" />
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsAddingHarvest(false)}>
                Cancel
              </Button>
              <Button onClick={() => setIsAddingHarvest(false)}>Record Harvest</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Harvest Value</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">₹{totalHarvestValue.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">This year</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Quantity</CardTitle>
            <Weight className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{totalQuantity.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">Mixed units</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Harvest Records</CardTitle>
            <Package className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">{harvests.length}</div>
            <p className="text-xs text-muted-foreground">This year</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Harvest History</CardTitle>
          <CardDescription>Detailed records of all your harvests</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {harvests.map((harvest) => (
              <div key={harvest.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-semibold text-lg">
                      {harvest.crop} - {harvest.variety}
                    </h3>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge className={getQualityColor(harvest.quality)}>{harvest.quality}</Badge>
                      <span className="text-sm text-muted-foreground flex items-center">
                        <Calendar className="h-3 w-3 mr-1" />
                        {new Date(harvest.harvestDate).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-green-600">₹{harvest.totalValue.toLocaleString()}</p>
                    <p className="text-sm text-muted-foreground">Total Value</p>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground">Quantity</p>
                    <p className="font-medium">
                      {harvest.quantity} {harvest.unit}
                    </p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Area</p>
                    <p className="font-medium">{harvest.area} acres</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Yield</p>
                    <p className="font-medium">{calculateYield(harvest.quantity, harvest.area, harvest.unit)}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Price per {harvest.unit}</p>
                    <p className="font-medium">₹{harvest.pricePerUnit}</p>
                  </div>
                </div>

                {harvest.notes && (
                  <div className="mt-3 pt-3 border-t">
                    <p className="text-sm text-muted-foreground">Notes:</p>
                    <p className="text-sm">{harvest.notes}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
