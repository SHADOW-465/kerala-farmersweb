"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Star, MessageCircle, Award, Plus, CheckCircle } from "lucide-react"

interface Expert {
  id: string
  name: string
  avatar?: string
  title: string
  specialization: string[]
  experience: number
  rating: number
  totalConsultations: number
  location: string
  languages: string[]
  availability: "available" | "busy" | "offline"
  bio: string
}

interface Consultation {
  id: string
  expertId: string
  question: string
  category: string
  status: "pending" | "answered" | "in-progress"
  createdAt: string
  answer?: string
  answeredAt?: string
}

export function ExpertAdvice() {
  const [experts] = useState<Expert[]>([
    {
      id: "1",
      name: "Dr. Rajesh Kumar",
      avatar: "/placeholder.svg?height=60&width=60",
      title: "Agricultural Scientist",
      specialization: ["Plant Pathology", "Organic Farming", "Soil Science"],
      experience: 15,
      rating: 4.8,
      totalConsultations: 245,
      location: "Thiruvananthapuram, Kerala",
      languages: ["Malayalam", "English", "Hindi"],
      availability: "available",
      bio: "Specialized in plant diseases and organic farming methods. Former researcher at Kerala Agricultural University.",
    },
    {
      id: "2",
      name: "Prof. Meera Nair",
      avatar: "/placeholder.svg?height=60&width=60",
      title: "Horticulture Expert",
      specialization: ["Coconut Cultivation", "Spice Farming", "Integrated Pest Management"],
      experience: 20,
      rating: 4.9,
      totalConsultations: 312,
      location: "Kochi, Kerala",
      languages: ["Malayalam", "English"],
      availability: "available",
      bio: "Expert in coconut and spice cultivation with extensive field experience across Kerala.",
    },
    {
      id: "3",
      name: "Sunil Varma",
      avatar: "/placeholder.svg?height=60&width=60",
      title: "Farm Management Consultant",
      specialization: ["Farm Economics", "Market Analysis", "Crop Planning"],
      experience: 12,
      rating: 4.7,
      totalConsultations: 189,
      location: "Kozhikode, Kerala",
      languages: ["Malayalam", "English"],
      availability: "busy",
      bio: "Helps farmers optimize their farm operations and market strategies for better profitability.",
    },
  ])

  const [consultations] = useState<Consultation[]>([
    {
      id: "1",
      expertId: "1",
      question: "My rice plants are showing brown spots on leaves. What could be the cause?",
      category: "Plant Diseases",
      status: "answered",
      createdAt: "2024-01-15",
      answer:
        "Based on your description, this appears to be brown spot disease caused by Bipolaris oryzae. I recommend applying organic fungicides like neem oil spray and ensuring proper field drainage.",
      answeredAt: "2024-01-15",
    },
    {
      id: "2",
      expertId: "2",
      question: "When is the best time to harvest coconuts for maximum oil content?",
      category: "Harvesting",
      status: "answered",
      createdAt: "2024-01-14",
      answer:
        "For maximum oil content, harvest coconuts when they are 11-12 months old. The husk should be brown and the coconut should sound full when tapped.",
      answeredAt: "2024-01-14",
    },
    {
      id: "3",
      expertId: "3",
      question: "What are the current market trends for black pepper? Should I expand cultivation?",
      category: "Market Analysis",
      status: "in-progress",
      createdAt: "2024-01-16",
    },
  ])

  const [isAskingQuestion, setIsAskingQuestion] = useState(false)

  const getAvailabilityColor = (availability: string) => {
    switch (availability) {
      case "available":
        return "bg-green-100 text-green-800"
      case "busy":
        return "bg-yellow-100 text-yellow-800"
      case "offline":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "answered":
        return "bg-green-100 text-green-800"
      case "in-progress":
        return "bg-blue-100 text-blue-800"
      case "pending":
        return "bg-yellow-100 text-yellow-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Expert Advice</h2>
          <p className="text-muted-foreground">Get professional guidance from agricultural experts</p>
        </div>
        <Dialog open={isAskingQuestion} onOpenChange={setIsAskingQuestion}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Ask Expert
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Ask an Expert</DialogTitle>
              <DialogDescription>Submit your farming question to get expert advice</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="expert">Select Expert</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose an expert" />
                  </SelectTrigger>
                  <SelectContent>
                    {experts
                      .filter((e) => e.availability === "available")
                      .map((expert) => (
                        <SelectItem key={expert.id} value={expert.id}>
                          {expert.name} - {expert.specialization.join(", ")}
                        </SelectItem>
                      ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="category">Category</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="plant-diseases">Plant Diseases</SelectItem>
                    <SelectItem value="soil-health">Soil Health</SelectItem>
                    <SelectItem value="crop-management">Crop Management</SelectItem>
                    <SelectItem value="pest-control">Pest Control</SelectItem>
                    <SelectItem value="market-analysis">Market Analysis</SelectItem>
                    <SelectItem value="government-schemes">Government Schemes</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="question">Your Question</Label>
                <Textarea id="question" placeholder="Describe your farming question in detail..." rows={6} />
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsAskingQuestion(false)}>
                Cancel
              </Button>
              <Button onClick={() => setIsAskingQuestion(false)}>Submit Question</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Available Experts</h3>
          {experts.map((expert) => (
            <Card key={expert.id}>
              <CardHeader className="pb-3">
                <div className="flex items-start gap-4">
                  <Avatar className="h-16 w-16">
                    <AvatarImage src={expert.avatar || "/placeholder.svg"} />
                    <AvatarFallback>
                      {expert.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <CardTitle className="text-lg">{expert.name}</CardTitle>
                      <Badge className={getAvailabilityColor(expert.availability)}>{expert.availability}</Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mb-2">{expert.title}</p>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-1">
                        <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        <span>{expert.rating}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <MessageCircle className="h-4 w-4" />
                        <span>{expert.totalConsultations} consultations</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Award className="h-4 w-4" />
                        <span>{expert.experience} years</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div>
                    <p className="text-sm font-medium mb-1">Specialization:</p>
                    <div className="flex flex-wrap gap-1">
                      {expert.specialization.map((spec, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {spec}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm font-medium mb-1">Languages:</p>
                    <p className="text-sm text-muted-foreground">{expert.languages.join(", ")}</p>
                  </div>
                  <p className="text-sm text-muted-foreground">{expert.bio}</p>
                  <Button
                    className="w-full"
                    disabled={expert.availability !== "available"}
                    onClick={() => setIsAskingQuestion(true)}
                  >
                    {expert.availability === "available" ? "Ask Question" : "Currently Unavailable"}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Recent Consultations</h3>
          {consultations.map((consultation) => {
            const expert = experts.find((e) => e.id === consultation.expertId)
            return (
              <Card key={consultation.id}>
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant="secondary">{consultation.category}</Badge>
                        <Badge className={getStatusColor(consultation.status)}>
                          {consultation.status === "answered" && <CheckCircle className="h-3 w-3 mr-1" />}
                          {consultation.status}
                        </Badge>
                      </div>
                      <CardTitle className="text-base">{consultation.question}</CardTitle>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Avatar className="h-6 w-6">
                        <AvatarImage src={expert?.avatar || "/placeholder.svg"} />
                        <AvatarFallback className="text-xs">
                          {expert?.name
                            .split(" ")
                            .map((n) => n[0])
                            .join("")}
                        </AvatarFallback>
                      </Avatar>
                      <span className="text-sm font-medium">{expert?.name}</span>
                      <span className="text-xs text-muted-foreground">
                        {new Date(consultation.createdAt).toLocaleDateString()}
                      </span>
                    </div>

                    {consultation.answer && (
                      <div className="bg-muted p-3 rounded-lg">
                        <p className="text-sm font-medium mb-1">Expert Answer:</p>
                        <p className="text-sm">{consultation.answer}</p>
                        {consultation.answeredAt && (
                          <p className="text-xs text-muted-foreground mt-2">
                            Answered on {new Date(consultation.answeredAt).toLocaleDateString()}
                          </p>
                        )}
                      </div>
                    )}

                    {consultation.status === "in-progress" && (
                      <div className="bg-blue-50 p-3 rounded-lg">
                        <p className="text-sm text-blue-800">
                          Your question is being reviewed by the expert. You'll receive an answer soon.
                        </p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>
    </div>
  )
}
