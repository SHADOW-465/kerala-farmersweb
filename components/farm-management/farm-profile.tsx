"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { MapPin, Edit, Save, X } from "lucide-react"

export function FarmProfile() {
  const [isEditing, setIsEditing] = useState(false)
  const [farmData, setFarmData] = useState({
    name: "Green Valley Farm",
    location: "Kottayam, Kerala",
    area: "5.2",
    soilType: "Alluvial",
    waterSource: "Borewell + Rainwater",
    primaryCrops: ["Rice", "Coconut", "Pepper"],
    description: "A sustainable farm focusing on organic farming practices with traditional Kerala crops.",
  })

  const handleSave = () => {
    setIsEditing(false)
    // Here you would typically save to a database
  }

  const handleCancel = () => {
    setIsEditing(false)
    // Reset form data if needed
  }

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>Farm Information</CardTitle>
            <CardDescription>Basic details about your farm</CardDescription>
          </div>
          {!isEditing ? (
            <Button variant="outline" size="sm" onClick={() => setIsEditing(true)}>
              <Edit className="h-4 w-4 mr-2" />
              Edit
            </Button>
          ) : (
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={handleCancel}>
                <X className="h-4 w-4 mr-2" />
                Cancel
              </Button>
              <Button size="sm" onClick={handleSave}>
                <Save className="h-4 w-4 mr-2" />
                Save
              </Button>
            </div>
          )}
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="farmName">Farm Name</Label>
              {isEditing ? (
                <Input
                  id="farmName"
                  value={farmData.name}
                  onChange={(e) => setFarmData({ ...farmData, name: e.target.value })}
                />
              ) : (
                <p className="text-sm font-medium">{farmData.name}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="location">Location</Label>
              {isEditing ? (
                <Input
                  id="location"
                  value={farmData.location}
                  onChange={(e) => setFarmData({ ...farmData, location: e.target.value })}
                />
              ) : (
                <p className="text-sm font-medium flex items-center">
                  <MapPin className="h-4 w-4 mr-1" />
                  {farmData.location}
                </p>
              )}
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="area">Total Area (Acres)</Label>
              {isEditing ? (
                <Input
                  id="area"
                  type="number"
                  value={farmData.area}
                  onChange={(e) => setFarmData({ ...farmData, area: e.target.value })}
                />
              ) : (
                <p className="text-sm font-medium">{farmData.area} acres</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="soilType">Soil Type</Label>
              {isEditing ? (
                <Select
                  value={farmData.soilType}
                  onValueChange={(value) => setFarmData({ ...farmData, soilType: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Alluvial">Alluvial</SelectItem>
                    <SelectItem value="Laterite">Laterite</SelectItem>
                    <SelectItem value="Black Cotton">Black Cotton</SelectItem>
                    <SelectItem value="Red Soil">Red Soil</SelectItem>
                    <SelectItem value="Sandy">Sandy</SelectItem>
                  </SelectContent>
                </Select>
              ) : (
                <p className="text-sm font-medium">{farmData.soilType}</p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="waterSource">Water Source</Label>
            {isEditing ? (
              <Input
                id="waterSource"
                value={farmData.waterSource}
                onChange={(e) => setFarmData({ ...farmData, waterSource: e.target.value })}
              />
            ) : (
              <p className="text-sm font-medium">{farmData.waterSource}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label>Primary Crops</Label>
            <div className="flex flex-wrap gap-2">
              {farmData.primaryCrops.map((crop, index) => (
                <Badge key={index} variant="secondary">
                  {crop}
                </Badge>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            {isEditing ? (
              <Textarea
                id="description"
                value={farmData.description}
                onChange={(e) => setFarmData({ ...farmData, description: e.target.value })}
                rows={3}
              />
            ) : (
              <p className="text-sm text-muted-foreground">{farmData.description}</p>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Farm Statistics</CardTitle>
          <CardDescription>Overview of your farm performance</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
              <span className="text-sm font-medium">Total Cultivated Area</span>
              <span className="text-lg font-bold text-primary">4.8 acres</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
              <span className="text-sm font-medium">Active Crop Seasons</span>
              <span className="text-lg font-bold text-primary">3</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
              <span className="text-sm font-medium">Total Harvest (This Year)</span>
              <span className="text-lg font-bold text-primary">12.5 tons</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
              <span className="text-sm font-medium">Revenue (This Year)</span>
              <span className="text-lg font-bold text-primary">₹2,45,000</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
