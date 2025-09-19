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
import { Plus, BookOpen, ThumbsUp, Eye, Download, Search, Filter, FileText, Video, ImageIcon } from "lucide-react"

interface KnowledgeItem {
  id: string
  title: string
  description: string
  type: "article" | "video" | "guide" | "case-study"
  category: string
  author: {
    name: string
    avatar?: string
    location: string
  }
  tags: string[]
  views: number
  likes: number
  downloads?: number
  createdAt: string
  content?: string
  difficulty: "beginner" | "intermediate" | "advanced"
}

export function KnowledgeSharing() {
  const [knowledgeItems, setKnowledgeItems] = useState<KnowledgeItem[]>([
    {
      id: "1",
      title: "Complete Guide to Organic Rice Farming in Kerala",
      description:
        "A comprehensive guide covering all aspects of organic rice cultivation, from seed selection to harvest.",
      type: "guide",
      category: "Rice Farming",
      author: {
        name: "Krishnan Nair",
        avatar: "/placeholder.svg?height=40&width=40",
        location: "Alappuzha, Kerala",
      },
      tags: ["rice", "organic", "cultivation", "kerala"],
      views: 1250,
      likes: 89,
      downloads: 156,
      createdAt: "2024-01-10",
      difficulty: "intermediate",
    },
    {
      id: "2",
      title: "Coconut Palm Disease Management - Video Tutorial",
      description: "Learn to identify and treat common coconut palm diseases with this detailed video guide.",
      type: "video",
      category: "Plant Diseases",
      author: {
        name: "Dr. Suma Krishnan",
        avatar: "/placeholder.svg?height=40&width=40",
        location: "Thrissur, Kerala",
      },
      tags: ["coconut", "disease", "treatment", "video"],
      views: 2100,
      likes: 145,
      createdAt: "2024-01-08",
      difficulty: "beginner",
    },
    {
      id: "3",
      title: "Successful Pepper Farming: A Case Study",
      description: "How I increased my pepper yield by 40% using integrated farming methods.",
      type: "case-study",
      category: "Spice Farming",
      author: {
        name: "Ravi Menon",
        avatar: "/placeholder.svg?height=40&width=40",
        location: "Wayanad, Kerala",
      },
      tags: ["pepper", "yield", "integrated-farming", "success"],
      views: 890,
      likes: 67,
      createdAt: "2024-01-05",
      difficulty: "advanced",
    },
    {
      id: "4",
      title: "Soil Testing and Nutrient Management",
      description: "Understanding soil health and managing nutrients for optimal crop growth.",
      type: "article",
      category: "Soil Health",
      author: {
        name: "Priya Varma",
        avatar: "/placeholder.svg?height=40&width=40",
        location: "Kottayam, Kerala",
      },
      tags: ["soil", "nutrients", "testing", "health"],
      views: 1450,
      likes: 102,
      downloads: 89,
      createdAt: "2024-01-03",
      difficulty: "intermediate",
    },
  ])

  const [isSharing, setIsSharing] = useState(false)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")
  const [selectedType, setSelectedType] = useState("all")

  const categories = ["All", "Rice Farming", "Plant Diseases", "Spice Farming", "Soil Health", "Market Analysis"]
  const types = ["All", "Article", "Video", "Guide", "Case Study"]

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "article":
        return <FileText className="h-4 w-4" />
      case "video":
        return <Video className="h-4 w-4" />
      case "guide":
        return <BookOpen className="h-4 w-4" />
      case "case-study":
        return <ImageIcon className="h-4 w-4" />
      default:
        return <FileText className="h-4 w-4" />
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "beginner":
        return "bg-green-100 text-green-800"
      case "intermediate":
        return "bg-yellow-100 text-yellow-800"
      case "advanced":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const filteredItems = knowledgeItems.filter((item) => {
    const matchesSearch =
      item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === "all" || item.category.toLowerCase() === selectedCategory.toLowerCase()
    const matchesType = selectedType === "all" || item.type === selectedType.toLowerCase()
    return matchesSearch && matchesCategory && matchesType
  })

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
        <div className="flex flex-col sm:flex-row gap-4 flex-1">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search knowledge base..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <div className="flex gap-2">
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-48">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((category) => (
                  <SelectItem key={category} value={category.toLowerCase()}>
                    {category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={selectedType} onValueChange={setSelectedType}>
              <SelectTrigger className="w-32">
                <SelectValue placeholder="Type" />
              </SelectTrigger>
              <SelectContent>
                {types.map((type) => (
                  <SelectItem key={type} value={type.toLowerCase()}>
                    {type}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <Dialog open={isSharing} onOpenChange={setIsSharing}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Share Knowledge
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Share Your Knowledge</DialogTitle>
              <DialogDescription>Contribute to the farming community by sharing your experience</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="title">Title</Label>
                <Input id="title" placeholder="Enter title for your content" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="type">Content Type</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="article">Article</SelectItem>
                      <SelectItem value="video">Video</SelectItem>
                      <SelectItem value="guide">Guide</SelectItem>
                      <SelectItem value="case-study">Case Study</SelectItem>
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
                      <SelectItem value="rice-farming">Rice Farming</SelectItem>
                      <SelectItem value="plant-diseases">Plant Diseases</SelectItem>
                      <SelectItem value="spice-farming">Spice Farming</SelectItem>
                      <SelectItem value="soil-health">Soil Health</SelectItem>
                      <SelectItem value="market-analysis">Market Analysis</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="difficulty">Difficulty Level</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select difficulty" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="beginner">Beginner</SelectItem>
                    <SelectItem value="intermediate">Intermediate</SelectItem>
                    <SelectItem value="advanced">Advanced</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="description">Description</Label>
                <Textarea id="description" placeholder="Brief description of your content..." rows={3} />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="content">Content</Label>
                <Textarea id="content" placeholder="Share your knowledge, experience, or guide..." rows={8} />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="tags">Tags (comma separated)</Label>
                <Input id="tags" placeholder="e.g., rice, organic, cultivation" />
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsSharing(false)}>
                Cancel
              </Button>
              <Button onClick={() => setIsSharing(false)}>Share Knowledge</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredItems.map((item) => (
          <Card key={item.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2 mb-2">
                  {getTypeIcon(item.type)}
                  <Badge variant="secondary">{item.category}</Badge>
                  <Badge className={getDifficultyColor(item.difficulty)} variant="outline">
                    {item.difficulty}
                  </Badge>
                </div>
              </div>
              <CardTitle className="text-lg hover:text-primary cursor-pointer line-clamp-2">{item.title}</CardTitle>
              <CardDescription className="line-clamp-3">{item.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-1 mb-4">
                {item.tags.map((tag, index) => (
                  <Badge key={index} variant="outline" className="text-xs">
                    #{tag}
                  </Badge>
                ))}
              </div>

              <div className="flex items-center gap-3 mb-4">
                <Avatar className="h-6 w-6">
                  <AvatarImage src={item.author.avatar || "/placeholder.svg"} />
                  <AvatarFallback className="text-xs">
                    {item.author.name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </AvatarFallback>
                </Avatar>
                <div className="text-xs">
                  <p className="font-medium">{item.author.name}</p>
                  <p className="text-muted-foreground">{item.author.location}</p>
                </div>
              </div>

              <div className="flex items-center justify-between text-sm text-muted-foreground mb-4">
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1">
                    <Eye className="h-4 w-4" />
                    <span>{item.views}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <ThumbsUp className="h-4 w-4" />
                    <span>{item.likes}</span>
                  </div>
                  {item.downloads && (
                    <div className="flex items-center gap-1">
                      <Download className="h-4 w-4" />
                      <span>{item.downloads}</span>
                    </div>
                  )}
                </div>
                <span className="text-xs">{new Date(item.createdAt).toLocaleDateString()}</span>
              </div>

              <Button className="w-full bg-transparent" variant="outline">
                {item.type === "video" ? "Watch Video" : "Read More"}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredItems.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <BookOpen className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No content found</h3>
            <p className="text-muted-foreground mb-4">
              {searchTerm || selectedCategory !== "all" || selectedType !== "all"
                ? "Try adjusting your search or filter criteria"
                : "Be the first to share knowledge with the community"}
            </p>
            <Button onClick={() => setIsSharing(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Share Knowledge
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
