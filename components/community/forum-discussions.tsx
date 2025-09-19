"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
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
import { Plus, MessageCircle, ThumbsUp, Clock, Search, Filter } from "lucide-react"

interface Discussion {
  id: string
  title: string
  content: string
  author: {
    name: string
    avatar?: string
    location: string
    expertise: string
  }
  category: string
  tags: string[]
  replies: number
  likes: number
  createdAt: string
  lastActivity: string
  isResolved: boolean
}

export function ForumDiscussions() {
  const [discussions, setDiscussions] = useState<Discussion[]>([
    {
      id: "1",
      title: "Best organic fertilizer for rice cultivation in monsoon season?",
      content:
        "I am looking for recommendations on organic fertilizers that work well for rice during the monsoon season in Kerala. My farm is in Kottayam district.",
      author: {
        name: "Ravi Kumar",
        avatar: "/placeholder.svg?height=40&width=40",
        location: "Kottayam, Kerala",
        expertise: "Rice Farming",
      },
      category: "Fertilizers",
      tags: ["rice", "organic", "monsoon", "fertilizer"],
      replies: 12,
      likes: 8,
      createdAt: "2024-01-15",
      lastActivity: "2024-01-16",
      isResolved: false,
    },
    {
      id: "2",
      title: "Coconut palm disease - leaves turning yellow",
      content:
        "My coconut palms are showing yellowing leaves starting from the bottom. The trees are about 15 years old. Has anyone faced similar issues?",
      author: {
        name: "Priya Nair",
        avatar: "/placeholder.svg?height=40&width=40",
        location: "Thrissur, Kerala",
        expertise: "Coconut Farming",
      },
      category: "Plant Diseases",
      tags: ["coconut", "disease", "yellowing", "palm"],
      replies: 18,
      likes: 15,
      createdAt: "2024-01-14",
      lastActivity: "2024-01-16",
      isResolved: true,
    },
    {
      id: "3",
      title: "Market prices for black pepper - when to sell?",
      content:
        "Current pepper prices seem to be fluctuating. Should I sell now or wait for better prices? What are your experiences with pepper market timing?",
      author: {
        name: "Suresh Menon",
        avatar: "/placeholder.svg?height=40&width=40",
        location: "Wayanad, Kerala",
        expertise: "Spice Farming",
      },
      category: "Market Prices",
      tags: ["pepper", "market", "pricing", "selling"],
      replies: 7,
      likes: 5,
      createdAt: "2024-01-13",
      lastActivity: "2024-01-15",
      isResolved: false,
    },
  ])

  const [isCreatingPost, setIsCreatingPost] = useState(false)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")

  const categories = [
    "All",
    "Plant Diseases",
    "Fertilizers",
    "Market Prices",
    "Weather",
    "Equipment",
    "Government Schemes",
  ]

  const filteredDiscussions = discussions.filter((discussion) => {
    const matchesSearch =
      discussion.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      discussion.content.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory =
      selectedCategory === "all" || discussion.category.toLowerCase() === selectedCategory.toLowerCase()
    return matchesSearch && matchesCategory
  })

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
        <div className="flex flex-col sm:flex-row gap-4 flex-1">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search discussions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <Select value={selectedCategory} onValueChange={setSelectedCategory}>
            <SelectTrigger className="w-full sm:w-48">
              <Filter className="h-4 w-4 mr-2" />
              <SelectValue placeholder="Filter by category" />
            </SelectTrigger>
            <SelectContent>
              {categories.map((category) => (
                <SelectItem key={category} value={category.toLowerCase()}>
                  {category}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <Dialog open={isCreatingPost} onOpenChange={setIsCreatingPost}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              New Discussion
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Start New Discussion</DialogTitle>
              <DialogDescription>Share your question or topic with the farming community</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="title">Title</Label>
                <Input id="title" placeholder="Enter discussion title" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="category">Category</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="plant-diseases">Plant Diseases</SelectItem>
                    <SelectItem value="fertilizers">Fertilizers</SelectItem>
                    <SelectItem value="market-prices">Market Prices</SelectItem>
                    <SelectItem value="weather">Weather</SelectItem>
                    <SelectItem value="equipment">Equipment</SelectItem>
                    <SelectItem value="government-schemes">Government Schemes</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="content">Description</Label>
                <Textarea id="content" placeholder="Describe your question or topic in detail..." rows={6} />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="tags">Tags (comma separated)</Label>
                <Input id="tags" placeholder="e.g., rice, organic, fertilizer" />
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsCreatingPost(false)}>
                Cancel
              </Button>
              <Button onClick={() => setIsCreatingPost(false)}>Post Discussion</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="space-y-4">
        {filteredDiscussions.map((discussion) => (
          <Card key={discussion.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Badge variant="secondary">{discussion.category}</Badge>
                    {discussion.isResolved && (
                      <Badge variant="outline" className="text-green-600 border-green-600">
                        Resolved
                      </Badge>
                    )}
                  </div>
                  <CardTitle className="text-lg hover:text-primary cursor-pointer">{discussion.title}</CardTitle>
                  <CardDescription className="mt-2 line-clamp-2">{discussion.content}</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2 mb-4">
                {discussion.tags.map((tag, index) => (
                  <Badge key={index} variant="outline" className="text-xs">
                    #{tag}
                  </Badge>
                ))}
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={discussion.author.avatar || "/placeholder.svg"} />
                    <AvatarFallback>
                      {discussion.author.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </AvatarFallback>
                  </Avatar>
                  <div className="text-sm">
                    <p className="font-medium">{discussion.author.name}</p>
                    <p className="text-muted-foreground text-xs">
                      {discussion.author.location} • {discussion.author.expertise}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <MessageCircle className="h-4 w-4" />
                    <span>{discussion.replies}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <ThumbsUp className="h-4 w-4" />
                    <span>{discussion.likes}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    <span>{new Date(discussion.lastActivity).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredDiscussions.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <MessageCircle className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No discussions found</h3>
            <p className="text-muted-foreground mb-4">
              {searchTerm || selectedCategory !== "all"
                ? "Try adjusting your search or filter criteria"
                : "Be the first to start a discussion in the community"}
            </p>
            <Button onClick={() => setIsCreatingPost(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Start Discussion
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
