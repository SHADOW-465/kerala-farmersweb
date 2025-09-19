"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Plus, Calendar, MapPin, Users, Filter } from "lucide-react"

interface Event {
  id: string
  title: string
  description: string
  type: "workshop" | "seminar" | "field-visit" | "training" | "exhibition"
  date: string
  time: string
  location: string
  organizer: string
  maxParticipants?: number
  currentParticipants: number
  isRegistered: boolean
  isFree: boolean
  fee?: number
  tags: string[]
}

export function LocalEvents() {
  const [events, setEvents] = useState<Event[]>([
    {
      id: "1",
      title: "Organic Farming Workshop",
      description: "Learn the fundamentals of organic farming practices, composting, and natural pest control methods.",
      type: "workshop",
      date: "2024-02-15",
      time: "09:00 AM",
      location: "Kerala Agricultural University, Thrissur",
      organizer: "Kerala Agricultural University",
      maxParticipants: 50,
      currentParticipants: 32,
      isRegistered: false,
      isFree: true,
      tags: ["organic", "farming", "composting", "pest-control"],
    },
    {
      id: "2",
      title: "Rice Cultivation Techniques Seminar",
      description: "Expert discussion on modern rice cultivation techniques and water management strategies.",
      type: "seminar",
      date: "2024-02-20",
      time: "02:00 PM",
      location: "District Collectorate, Kottayam",
      organizer: "Department of Agriculture",
      maxParticipants: 100,
      currentParticipants: 67,
      isRegistered: true,
      isFree: false,
      fee: 200,
      tags: ["rice", "cultivation", "water-management", "techniques"],
    },
    {
      id: "3",
      title: "Spice Processing Unit Visit",
      description: "Field visit to a modern spice processing facility to understand value addition processes.",
      type: "field-visit",
      date: "2024-02-25",
      time: "10:00 AM",
      location: "Kumily, Idukki",
      organizer: "Spice Board of India",
      maxParticipants: 25,
      currentParticipants: 18,
      isRegistered: false,
      isFree: true,
      tags: ["spices", "processing", "value-addition", "field-visit"],
    },
    {
      id: "4",
      title: "Digital Agriculture Training",
      description: "Training on using digital tools and mobile apps for modern farm management.",
      type: "training",
      date: "2024-03-05",
      time: "11:00 AM",
      location: "Krishi Vigyan Kendra, Ernakulam",
      organizer: "ICAR",
      maxParticipants: 40,
      currentParticipants: 15,
      isRegistered: false,
      isFree: true,
      tags: ["digital", "technology", "apps", "farm-management"],
    },
  ])

  const [isCreatingEvent, setIsCreatingEvent] = useState(false)
  const [selectedType, setSelectedType] = useState("all")

  const eventTypes = ["All", "Workshop", "Seminar", "Field Visit", "Training", "Exhibition"]

  const getTypeColor = (type: string) => {
    switch (type) {
      case "workshop":
        return "bg-blue-100 text-blue-800"
      case "seminar":
        return "bg-green-100 text-green-800"
      case "field-visit":
        return "bg-purple-100 text-purple-800"
      case "training":
        return "bg-orange-100 text-orange-800"
      case "exhibition":
        return "bg-pink-100 text-pink-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const filteredEvents = events.filter((event) => {
    const matchesType = selectedType === "all" || event.type === selectedType.toLowerCase().replace(" ", "-")
    return matchesType
  })

  const upcomingEvents = filteredEvents.filter((event) => new Date(event.date) >= new Date())
  const pastEvents = filteredEvents.filter((event) => new Date(event.date) < new Date())

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
        <div className="flex items-center gap-4">
          <Select value={selectedType} onValueChange={setSelectedType}>
            <SelectTrigger className="w-48">
              <Filter className="h-4 w-4 mr-2" />
              <SelectValue placeholder="Filter by type" />
            </SelectTrigger>
            <SelectContent>
              {eventTypes.map((type) => (
                <SelectItem key={type} value={type.toLowerCase().replace(" ", "-")}>
                  {type}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <Dialog open={isCreatingEvent} onOpenChange={setIsCreatingEvent}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Create Event
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Create New Event</DialogTitle>
              <DialogDescription>Organize a farming event for the community</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="eventTitle">Event Title</Label>
                <Input id="eventTitle" placeholder="Enter event title" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="eventType">Event Type</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="workshop">Workshop</SelectItem>
                      <SelectItem value="seminar">Seminar</SelectItem>
                      <SelectItem value="field-visit">Field Visit</SelectItem>
                      <SelectItem value="training">Training</SelectItem>
                      <SelectItem value="exhibition">Exhibition</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="maxParticipants">Max Participants</Label>
                  <Input id="maxParticipants" type="number" placeholder="50" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="eventDate">Date</Label>
                  <Input id="eventDate" type="date" />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="eventTime">Time</Label>
                  <Input id="eventTime" type="time" />
                </div>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="location">Location</Label>
                <Input id="location" placeholder="Enter event location" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="organizer">Organizer</Label>
                <Input id="organizer" placeholder="Enter organizer name" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="description">Description</Label>
                <Textarea id="description" placeholder="Describe the event details..." rows={4} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="isFree">Registration</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select option" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="free">Free</SelectItem>
                      <SelectItem value="paid">Paid</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="fee">Fee (if paid)</Label>
                  <Input id="fee" type="number" placeholder="0" />
                </div>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="tags">Tags (comma separated)</Label>
                <Input id="tags" placeholder="e.g., organic, farming, workshop" />
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsCreatingEvent(false)}>
                Cancel
              </Button>
              <Button onClick={() => setIsCreatingEvent(false)}>Create Event</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold mb-4">Upcoming Events</h3>
          <div className="grid gap-4 md:grid-cols-2">
            {upcomingEvents.map((event) => (
              <Card key={event.id} className="hover:shadow-md transition-shadow">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge className={getTypeColor(event.type)}>{event.type.replace("-", " ")}</Badge>
                        {event.isFree ? (
                          <Badge variant="outline" className="text-green-600 border-green-600">
                            Free
                          </Badge>
                        ) : (
                          <Badge variant="outline">₹{event.fee}</Badge>
                        )}
                        {event.isRegistered && (
                          <Badge variant="outline" className="text-blue-600 border-blue-600">
                            Registered
                          </Badge>
                        )}
                      </div>
                      <CardTitle className="text-lg">{event.title}</CardTitle>
                      <CardDescription className="mt-2 line-clamp-2">{event.description}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="grid gap-2 text-sm">
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <span>
                          {new Date(event.date).toLocaleDateString()} at {event.time}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <MapPin className="h-4 w-4 text-muted-foreground" />
                        <span className="line-clamp-1">{event.location}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Users className="h-4 w-4 text-muted-foreground" />
                        <span>
                          {event.currentParticipants}
                          {event.maxParticipants && `/${event.maxParticipants}`} participants
                        </span>
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-1">
                      {event.tags.map((tag, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          #{tag}
                        </Badge>
                      ))}
                    </div>

                    <div className="pt-2 border-t">
                      <p className="text-sm text-muted-foreground mb-2">Organized by: {event.organizer}</p>
                      <Button
                        className="w-full"
                        variant={event.isRegistered ? "outline" : "default"}
                        disabled={event.maxParticipants && event.currentParticipants >= event.maxParticipants}
                      >
                        {event.isRegistered
                          ? "Registered"
                          : event.maxParticipants && event.currentParticipants >= event.maxParticipants
                            ? "Event Full"
                            : "Register Now"}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {pastEvents.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Past Events</h3>
            <div className="grid gap-4 md:grid-cols-2">
              {pastEvents.map((event) => (
                <Card key={event.id} className="opacity-75">
                  <CardHeader className="pb-3">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <Badge className={getTypeColor(event.type)} variant="outline">
                            {event.type.replace("-", " ")}
                          </Badge>
                          <Badge variant="outline" className="text-gray-600">
                            Completed
                          </Badge>
                        </div>
                        <CardTitle className="text-lg">{event.title}</CardTitle>
                        <CardDescription className="mt-2 line-clamp-2">{event.description}</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2 text-sm text-muted-foreground">
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4" />
                        <span>{new Date(event.date).toLocaleDateString()}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <MapPin className="h-4 w-4" />
                        <span>{event.location}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Users className="h-4 w-4" />
                        <span>{event.currentParticipants} participants attended</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>

      {upcomingEvents.length === 0 && pastEvents.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <Calendar className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No events found</h3>
            <p className="text-muted-foreground mb-4">
              {selectedType !== "all"
                ? "No events found for the selected type"
                : "Be the first to organize an event for the farming community"}
            </p>
            <Button onClick={() => setIsCreatingEvent(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create Event
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
