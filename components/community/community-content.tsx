"use client"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ForumDiscussions } from "./forum-discussions"
import { ExpertAdvice } from "./expert-advice"
import { KnowledgeSharing } from "./knowledge-sharing"
import { LocalEvents } from "./local-events"
import { FarmerProfiles } from "./farmer-profiles"

export function CommunityContent() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Community Platform</h1>
        <p className="text-muted-foreground">Connect with fellow farmers, share knowledge, and get expert advice</p>
      </div>

      <Tabs defaultValue="discussions" className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="discussions">Discussions</TabsTrigger>
          <TabsTrigger value="experts">Expert Advice</TabsTrigger>
          <TabsTrigger value="knowledge">Knowledge Hub</TabsTrigger>
          <TabsTrigger value="events">Local Events</TabsTrigger>
          <TabsTrigger value="farmers">Farmers</TabsTrigger>
        </TabsList>

        <TabsContent value="discussions" className="space-y-4">
          <ForumDiscussions />
        </TabsContent>

        <TabsContent value="experts" className="space-y-4">
          <ExpertAdvice />
        </TabsContent>

        <TabsContent value="knowledge" className="space-y-4">
          <KnowledgeSharing />
        </TabsContent>

        <TabsContent value="events" className="space-y-4">
          <LocalEvents />
        </TabsContent>

        <TabsContent value="farmers" className="space-y-4">
          <FarmerProfiles />
        </TabsContent>
      </Tabs>
    </div>
  )
}
