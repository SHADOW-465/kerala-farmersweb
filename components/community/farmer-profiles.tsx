"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Search, MapPin, Sprout, Award, MessageCircle, UserPlus, Filter } from "lucide-react"

interface Farmer {
  id: string
  name: string
  avatar?: string
  location: string
  farmSize: number
  experience: number
  specialization: string[]
  crops: string[]
  achievements: string[]
  bio: string
  isConnected: boolean
  connectionCount: number
  postsCount: number
  helpfulAnswers: number
}

export function FarmerProfiles() {
  const [farmers, setFarmers] = useState<Farmer[]>([
    {
      id: "1",
      name: "Krishnan Nair",
      avatar: "/placeholder.svg?height=60&width=60",
      location: "Alappuzha, Kerala",
      farmSize: 8.5,
      experience: 25,
      specialization: ["Organic Farming", "Rice Cultivation", "Water Management"],
      crops: ["Rice", "Coconut", "Vegetables"],
      achievements: ["Best Organic Farmer 2023", "Water Conservation Award"],
      bio: "Passionate about sustainable farming practices and helping fellow farmers adopt organic methods.",
      isConnected: false,
      connectionCount: 156,
      postsCount: 23,
      helpfulAnswers: 89,
    },
    {
      id: "2",
      name: "Priya Menon",
      avatar: "/placeholder.svg?height=60&width=60",
      location: "Wayanad, Kerala",
      farmSize: 12.0,
      experience: 18,
      specialization: ["Spice Farming", "Integrated Pest Management", "Value Addition"],
      crops: ["Black Pepper", "Cardamom", "Coffee", "Vanilla"],
      achievements: ["Spice Board Excellence Award", "Women Farmer of the Year 2022"],
      bio: "Specializing in high-value spice crops and helping farmers with value addition techniques.",
      isConnected: true,
      connectionCount: 203,
      postsCount: 45,
      helpfulAnswers: 134,
    },
    {
      id: "3",
      name: "Ravi Kumar",
      avatar: "/placeholder.svg?height=60&width=60",
      location: "Thrissur, Kerala",
      farmSize: 6.2,
      experience: 15,
      specialization: ["Coconut Farming", "Intercropping", "Farm Mechanization"],
      crops: ["Coconut", "Banana", "Turmeric", "Ginger"],
      achievements: ["Progressive Farmer Award", "Technology Adoption Leader"],
      bio: "Advocate for modern farming techniques and helping farmers increase productivity through technology.",
      isConnected: false,
      connectionCount: 98,
      postsCount: 31,
      helpfulAnswers: 67,
    },
    {
      id: "4",
      name: "Suma Krishnan",
      avatar: "/placeholder.svg?height=60&width=60",
      location: "Kottayam, Kerala",
      farmSize: 4.8,
      experience: 12,
      specialization: ["Vegetable Farming", "Greenhouse Cultivation", "Seed Production"],
      crops: ["Tomato", "Cucumber", "Leafy Greens", "Herbs"],
      achievements: ["Quality Seed Producer", "Greenhouse Innovation Award"],
      bio: "Expert in protected cultivation and quality seed production for vegetable crops.",
      isConnected: false,
      connectionCount: 87,
      postsCount: 19,
      helpfulAnswers: 52,
    },
  ])

  const [searchTerm, setSearchTerm] = useState("")
  const [selectedLocation, setSelectedLocation] = useState("all")
  const [selectedSpecialization, setSelectedSpecialization] = useState("all")

  const locations = ["All", "Alappuzha", "Wayanad", "Thrissur", "Kottayam", "Ernakulam", "Kozhikode"]
  const specializations = [
    "All",
    "Organic Farming",
    "Rice Cultivation",
    "Spice Farming",
    "Coconut Farming",
    "Vegetable Farming",
  ]

  const filteredFarmers = farmers.filter((farmer) => {
    const matchesSearch =
      farmer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      farmer.bio.toLowerCase().includes(searchTerm.toLowerCase()) ||
      farmer.specialization.some((spec) => spec.toLowerCase().includes(searchTerm.toLowerCase()))
    const matchesLocation = selectedLocation === "all" || farmer.location.includes(selectedLocation)
    const matchesSpecialization =
      selectedSpecialization === "all" || farmer.specialization.some((spec) => spec.includes(selectedSpecialization))
    return matchesSearch && matchesLocation && matchesSpecialization
  })

  const handleConnect = (farmerId: string) => {
    setFarmers(
      farmers.map((farmer) =>
        farmer.id === farmerId
          ? {
              ...farmer,
              isConnected: !farmer.isConnected,
              connectionCount: farmer.isConnected ? farmer.connectionCount - 1 : farmer.connectionCount + 1,
            }
          : farmer,
      ),
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search farmers..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="flex gap-2">
          <Select value={selectedLocation} onValueChange={setSelectedLocation}>
            <SelectTrigger className="w-48">
              <Filter className="h-4 w-4 mr-2" />
              <SelectValue placeholder="Location" />
            </SelectTrigger>
            <SelectContent>
              {locations.map((location) => (
                <SelectItem key={location} value={location.toLowerCase()}>
                  {location}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={selectedSpecialization} onValueChange={setSelectedSpecialization}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Specialization" />
            </SelectTrigger>
            <SelectContent>
              {specializations.map((spec) => (
                <SelectItem key={spec} value={spec.toLowerCase()}>
                  {spec}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredFarmers.map((farmer) => (
          <Card key={farmer.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-start gap-4">
                <Avatar className="h-16 w-16">
                  <AvatarImage src={farmer.avatar || "/placeholder.svg"} />
                  <AvatarFallback>
                    {farmer.name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <CardTitle className="text-lg">{farmer.name}</CardTitle>
                  <div className="flex items-center gap-1 text-sm text-muted-foreground mt-1">
                    <MapPin className="h-3 w-3" />
                    <span>{farmer.location}</span>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground mt-2">
                    <div className="flex items-center gap-1">
                      <Sprout className="h-3 w-3" />
                      <span>{farmer.farmSize} acres</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Award className="h-3 w-3" />
                      <span>{farmer.experience} years</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium mb-2">Specialization:</p>
                  <div className="flex flex-wrap gap-1">
                    {farmer.specialization.map((spec, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {spec}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div>
                  <p className="text-sm font-medium mb-2">Crops:</p>
                  <div className="flex flex-wrap gap-1">
                    {farmer.crops.map((crop, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {crop}
                      </Badge>
                    ))}
                  </div>
                </div>

                {farmer.achievements.length > 0 && (
                  <div>
                    <p className="text-sm font-medium mb-2">Achievements:</p>
                    <div className="space-y-1">
                      {farmer.achievements.map((achievement, index) => (
                        <div key={index} className="flex items-center gap-2">
                          <Award className="h-3 w-3 text-yellow-500" />
                          <span className="text-xs text-muted-foreground">{achievement}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <p className="text-sm text-muted-foreground line-clamp-3">{farmer.bio}</p>

                <div className="grid grid-cols-3 gap-2 text-center text-xs text-muted-foreground pt-2 border-t">
                  <div>
                    <p className="font-medium text-foreground">{farmer.connectionCount}</p>
                    <p>Connections</p>
                  </div>
                  <div>
                    <p className="font-medium text-foreground">{farmer.postsCount}</p>
                    <p>Posts</p>
                  </div>
                  <div>
                    <p className="font-medium text-foreground">{farmer.helpfulAnswers}</p>
                    <p>Helpful</p>
                  </div>
                </div>

                <div className="flex gap-2 pt-2">
                  <Button
                    variant={farmer.isConnected ? "outline" : "default"}
                    size="sm"
                    className="flex-1"
                    onClick={() => handleConnect(farmer.id)}
                  >
                    {farmer.isConnected ? (
                      <>
                        <UserPlus className="h-4 w-4 mr-1" />
                        Connected
                      </>
                    ) : (
                      <>
                        <UserPlus className="h-4 w-4 mr-1" />
                        Connect
                      </>
                    )}
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                    <MessageCircle className="h-4 w-4 mr-1" />
                    Message
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredFarmers.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <Search className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No farmers found</h3>
            <p className="text-muted-foreground">
              Try adjusting your search criteria or filters to find farmers in your area.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
