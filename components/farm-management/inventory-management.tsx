"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
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
import { Progress } from "@/components/ui/progress"
import { Plus, AlertTriangle, CheckCircle, Clock } from "lucide-react"

interface InventoryItem {
  id: string
  name: string
  category: "seeds" | "fertilizer" | "pesticide" | "equipment" | "other"
  currentStock: number
  unit: string
  minThreshold: number
  maxCapacity: number
  lastRestocked: string
  expiryDate?: string
  supplier: string
  costPerUnit: number
}

export function InventoryManagement() {
  const [inventory, setInventory] = useState<InventoryItem[]>([
    {
      id: "1",
      name: "Rice Seeds - Jyothi",
      category: "seeds",
      currentStock: 25,
      unit: "kg",
      minThreshold: 10,
      maxCapacity: 100,
      lastRestocked: "2024-06-01",
      expiryDate: "2025-06-01",
      supplier: "Kerala Seeds Corporation",
      costPerUnit: 140,
    },
    {
      id: "2",
      name: "Organic Compost",
      category: "fertilizer",
      currentStock: 150,
      unit: "kg",
      minThreshold: 50,
      maxCapacity: 500,
      lastRestocked: "2024-07-15",
      supplier: "Green Earth Fertilizers",
      costPerUnit: 18,
    },
    {
      id: "3",
      name: "Neem Oil",
      category: "pesticide",
      currentStock: 5,
      unit: "liters",
      minThreshold: 10,
      maxCapacity: 50,
      lastRestocked: "2024-05-20",
      expiryDate: "2025-05-20",
      supplier: "Bio Pesticides Ltd",
      costPerUnit: 250,
    },
    {
      id: "4",
      name: "Water Pump",
      category: "equipment",
      currentStock: 1,
      unit: "piece",
      minThreshold: 1,
      maxCapacity: 2,
      lastRestocked: "2023-12-10",
      supplier: "Farm Equipment Store",
      costPerUnit: 15000,
    },
  ])

  const [isAddingItem, setIsAddingItem] = useState(false)

  const getStockStatus = (item: InventoryItem) => {
    if (item.currentStock <= item.minThreshold) return "low"
    if (item.currentStock >= item.maxCapacity * 0.8) return "high"
    return "normal"
  }

  const getStockColor = (status: string) => {
    switch (status) {
      case "low":
        return "text-red-600"
      case "high":
        return "text-green-600"
      default:
        return "text-blue-600"
    }
  }

  const getStockIcon = (status: string) => {
    switch (status) {
      case "low":
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      case "high":
        return <CheckCircle className="h-4 w-4 text-green-500" />
      default:
        return <Clock className="h-4 w-4 text-blue-500" />
    }
  }

  const getCategoryColor = (category: string) => {
    const colors: { [key: string]: string } = {
      seeds: "bg-green-100 text-green-800",
      fertilizer: "bg-blue-100 text-blue-800",
      pesticide: "bg-orange-100 text-orange-800",
      equipment: "bg-purple-100 text-purple-800",
      other: "bg-gray-100 text-gray-800",
    }
    return colors[category] || colors["other"]
  }

  const isExpiringSoon = (expiryDate?: string) => {
    if (!expiryDate) return false
    const expiry = new Date(expiryDate)
    const today = new Date()
    const daysUntilExpiry = Math.ceil((expiry.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
    return daysUntilExpiry <= 30 && daysUntilExpiry > 0
  }

  const isExpired = (expiryDate?: string) => {
    if (!expiryDate) return false
    const expiry = new Date(expiryDate)
    const today = new Date()
    return expiry < today
  }

  const lowStockItems = inventory.filter((item) => getStockStatus(item) === "low")
  const expiringItems = inventory.filter((item) => isExpiringSoon(item.expiryDate))
  const expiredItems = inventory.filter((item) => isExpired(item.expiryDate))

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Inventory Management</h2>
          <p className="text-muted-foreground">Track your farm supplies and equipment</p>
        </div>
        <Dialog open={isAddingItem} onOpenChange={setIsAddingItem}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Item
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Add Inventory Item</DialogTitle>
              <DialogDescription>Add a new item to your farm inventory</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="itemName">Item Name</Label>
                  <Input id="itemName" placeholder="Enter item name" />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="category">Category</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="seeds">Seeds</SelectItem>
                      <SelectItem value="fertilizer">Fertilizer</SelectItem>
                      <SelectItem value="pesticide">Pesticide</SelectItem>
                      <SelectItem value="equipment">Equipment</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="currentStock">Current Stock</Label>
                  <Input id="currentStock" type="number" placeholder="0" />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="unit">Unit</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Unit" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="kg">Kg</SelectItem>
                      <SelectItem value="liters">Liters</SelectItem>
                      <SelectItem value="pieces">Pieces</SelectItem>
                      <SelectItem value="bags">Bags</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="costPerUnit">Cost per Unit (₹)</Label>
                  <Input id="costPerUnit" type="number" placeholder="0.00" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="minThreshold">Minimum Threshold</Label>
                  <Input id="minThreshold" type="number" placeholder="0" />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="maxCapacity">Maximum Capacity</Label>
                  <Input id="maxCapacity" type="number" placeholder="0" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="supplier">Supplier</Label>
                  <Input id="supplier" placeholder="Enter supplier name" />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="expiryDate">Expiry Date (Optional)</Label>
                  <Input id="expiryDate" type="date" />
                </div>
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsAddingItem(false)}>
                Cancel
              </Button>
              <Button onClick={() => setIsAddingItem(false)}>Add Item</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Alert Cards */}
      {(lowStockItems.length > 0 || expiringItems.length > 0 || expiredItems.length > 0) && (
        <div className="grid gap-4 md:grid-cols-3">
          {lowStockItems.length > 0 && (
            <Card className="border-red-200">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-red-600">Low Stock Alert</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-red-600">{lowStockItems.length}</div>
                <p className="text-xs text-muted-foreground">Items need restocking</p>
              </CardContent>
            </Card>
          )}

          {expiringItems.length > 0 && (
            <Card className="border-yellow-200">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-yellow-600">Expiring Soon</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-yellow-600">{expiringItems.length}</div>
                <p className="text-xs text-muted-foreground">Items expire within 30 days</p>
              </CardContent>
            </Card>
          )}

          {expiredItems.length > 0 && (
            <Card className="border-red-200">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-red-600">Expired Items</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-red-600">{expiredItems.length}</div>
                <p className="text-xs text-muted-foreground">Items past expiry date</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {inventory.map((item) => {
          const status = getStockStatus(item)
          const stockPercentage = (item.currentStock / item.maxCapacity) * 100

          return (
            <Card key={item.id} className="relative">
              <CardHeader className="pb-3">
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-lg">{item.name}</CardTitle>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge className={getCategoryColor(item.category)}>{item.category}</Badge>
                      {item.expiryDate && isExpiringSoon(item.expiryDate) && (
                        <Badge variant="outline" className="text-yellow-600 border-yellow-600">
                          Expiring Soon
                        </Badge>
                      )}
                      {item.expiryDate && isExpired(item.expiryDate) && (
                        <Badge variant="outline" className="text-red-600 border-red-600">
                          Expired
                        </Badge>
                      )}
                    </div>
                  </div>
                  {getStockIcon(status)}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Stock Level</span>
                    <span className={`font-medium ${getStockColor(status)}`}>
                      {item.currentStock} / {item.maxCapacity} {item.unit}
                    </span>
                  </div>
                  <Progress value={stockPercentage} className="h-2" />
                  <p className="text-xs text-muted-foreground">
                    Min threshold: {item.minThreshold} {item.unit}
                  </p>
                </div>

                <div className="grid gap-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Cost per {item.unit}:</span>
                    <span className="font-medium">₹{item.costPerUnit}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Total Value:</span>
                    <span className="font-medium">₹{(item.currentStock * item.costPerUnit).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Supplier:</span>
                    <span className="font-medium text-xs">{item.supplier}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Last Restocked:</span>
                    <span className="font-medium text-xs">{new Date(item.lastRestocked).toLocaleDateString()}</span>
                  </div>
                  {item.expiryDate && (
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Expires:</span>
                      <span
                        className={`font-medium text-xs ${isExpiringSoon(item.expiryDate) ? "text-yellow-600" : isExpired(item.expiryDate) ? "text-red-600" : ""}`}
                      >
                        {new Date(item.expiryDate).toLocaleDateString()}
                      </span>
                    </div>
                  )}
                </div>

                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                    Update Stock
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                    Reorder
                  </Button>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
