"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Send, Bot, User, Languages, Loader2 } from "lucide-react"
import { apiClient, ChatbotResponse } from "@/lib/api-client"
import { useToast } from "@/hooks/use-toast"

interface Message {
  id: string
  content: string
  isUser: boolean
  timestamp: Date
  language?: string
  intent?: string
}

export function ChatContent() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [selectedLanguage, setSelectedLanguage] = useState("en")
  const [supportedLanguages, setSupportedLanguages] = useState<Record<string, string>>({})
  const [userId] = useState("user_" + Date.now()) // Simple user ID for demo
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  // Load supported languages on component mount
  useEffect(() => {
    loadSupportedLanguages()
  }, [])

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const loadSupportedLanguages = async () => {
    try {
      const response = await apiClient.getSupportedLanguages()
      if (response.success && response.data) {
        setSupportedLanguages(response.data.languages)
      }
    } catch (error) {
      console.error("Failed to load supported languages:", error)
    }
  }

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      isUser: true,
      timestamp: new Date(),
      language: selectedLanguage,
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage("")
    setIsLoading(true)

    try {
      const response = await apiClient.chatWithBot({
        message: inputMessage,
        language: selectedLanguage,
        user_id: userId,
      })

      if (response.success && response.data) {
        const botResponse: Message = {
          id: (Date.now() + 1).toString(),
          content: response.data.response,
          isUser: false,
          timestamp: new Date(),
          language: response.data.language,
          intent: response.data.intent,
        }
        setMessages(prev => [...prev, botResponse])
      } else {
        throw new Error(response.error || "Failed to get response")
      }
    } catch (error) {
      console.error("Chat error:", error)
      toast({
        title: "Chat Error",
        description: error instanceof Error ? error.message : "Failed to send message",
        variant: "destructive",
      })

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "I'm sorry, I encountered an error. Please try again.",
        isUser: false,
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const quickQuestions = [
    "What crops are best for Kerala?",
    "How to improve soil health?",
    "What are common plant diseases?",
    "When should I plant rice?",
    "How to control pests naturally?",
  ]

  const handleQuickQuestion = (question: string) => {
    setInputMessage(question)
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-balance">AI Farming Assistant</h1>
        <p className="text-muted-foreground text-pretty">
          Get instant answers to your farming questions in multiple languages. Ask about crops, diseases, weather, and more.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-4">
        {/* Chat Interface */}
        <Card className="lg:col-span-3">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <Bot className="h-5 w-5" />
                Chat Assistant
              </CardTitle>
              <div className="flex items-center gap-2">
                <Languages className="h-4 w-4" />
                <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(supportedLanguages).map(([code, name]) => (
                      <SelectItem key={code} value={code}>
                        {name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <CardDescription>
              Ask me anything about farming, crops, diseases, or agricultural practices
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Messages */}
            <ScrollArea className="h-96 w-full">
              <div className="space-y-4 pr-4">
                {messages.length === 0 ? (
                  <div className="text-center text-muted-foreground py-8">
                    <Bot className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>Start a conversation by typing a message or selecting a quick question below.</p>
                  </div>
                ) : (
                  messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex gap-3 ${message.isUser ? "justify-end" : "justify-start"}`}
                    >
                      <div className={`flex gap-3 max-w-[80%] ${message.isUser ? "flex-row-reverse" : "flex-row"}`}>
                        <div className={`flex h-8 w-8 items-center justify-center rounded-full ${
                          message.isUser ? "bg-primary text-primary-foreground" : "bg-muted"
                        }`}>
                          {message.isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                        </div>
                        <div className={`rounded-lg px-4 py-2 ${
                          message.isUser 
                            ? "bg-primary text-primary-foreground" 
                            : "bg-muted"
                        }`}>
                          <p className="text-sm">{message.content}</p>
                          <div className="flex items-center gap-2 mt-1">
                            <span className="text-xs opacity-70">
                              {message.timestamp.toLocaleTimeString()}
                            </span>
                            {message.intent && (
                              <Badge variant="secondary" className="text-xs">
                                {message.intent}
                              </Badge>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                )}
                {isLoading && (
                  <div className="flex gap-3 justify-start">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-muted">
                      <Bot className="h-4 w-4" />
                    </div>
                    <div className="rounded-lg px-4 py-2 bg-muted">
                      <div className="flex items-center gap-2">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span className="text-sm">Thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </ScrollArea>

            {/* Input */}
            <div className="flex gap-2">
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about farming, crops, diseases..."
                disabled={isLoading}
                className="flex-1"
              />
              <Button 
                onClick={sendMessage} 
                disabled={!inputMessage.trim() || isLoading}
                size="icon"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Quick Questions */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Quick Questions</CardTitle>
            <CardDescription>Click to ask common farming questions</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {quickQuestions.map((question, index) => (
              <Button
                key={index}
                variant="outline"
                className="w-full justify-start text-left h-auto p-3"
                onClick={() => handleQuickQuestion(question)}
                disabled={isLoading}
              >
                <span className="text-sm">{question}</span>
              </Button>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Features Info */}
      <Card>
        <CardHeader>
          <CardTitle>What I Can Help With</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <div className="space-y-2">
              <h4 className="font-semibold">Crop Advice</h4>
              <p className="text-sm text-muted-foreground">
                Best crops for your soil, planting times, and care tips
              </p>
            </div>
            <div className="space-y-2">
              <h4 className="font-semibold">Disease Detection</h4>
              <p className="text-sm text-muted-foreground">
                Identify plant diseases and get treatment recommendations
              </p>
            </div>
            <div className="space-y-2">
              <h4 className="font-semibold">Weather Guidance</h4>
              <p className="text-sm text-muted-foreground">
                Weather-based farming advice and irrigation tips
              </p>
            </div>
            <div className="space-y-2">
              <h4 className="font-semibold">Soil Health</h4>
              <p className="text-sm text-muted-foreground">
                Soil improvement techniques and nutrient management
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}