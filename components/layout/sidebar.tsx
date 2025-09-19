"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Home,
  Camera,
  Sprout,
  CloudRain,
  BarChart3,
  Users,
  MessageCircle,
  Menu,
  Leaf,
  TrendingUp,
  FileText,
  HelpCircle,
} from "lucide-react"

const navigation = [
  { name: "Dashboard", href: "/", icon: Home },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Disease Detection", href: "/disease-detection", icon: Camera },
  { name: "Crop Recommendations", href: "/crop-recommendations", icon: Sprout },
  { name: "Weather Analytics", href: "/weather", icon: CloudRain },
  { name: "Farm Management", href: "/farm-management", icon: TrendingUp },
  { name: "Community", href: "/community", icon: Users },
  { name: "AI Assistant", href: "/chat", icon: MessageCircle },
  { name: "Reports", href: "/reports", icon: FileText },
  { name: "Support", href: "/help", icon: HelpCircle },
]

interface SidebarProps {
  className?: string
}

export function Sidebar({ className }: SidebarProps) {
  const pathname = usePathname()

  return (
    <div className={cn("professional-sidebar pb-12 min-h-screen w-64", className)}>
      <div className="space-y-4 py-4">
        <div className="px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-sidebar-primary">
              <Leaf className="h-6 w-6 text-sidebar-primary-foreground" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-sidebar-foreground">AgroGlobal</h2>
              <p className="text-xs text-sidebar-foreground/70">NAVIGATION</p>
            </div>
          </div>
        </div>

        <div className="px-3">
          <ScrollArea className="h-[calc(100vh-12rem)]">
            <div className="space-y-1">
              {navigation.map((item) => (
                <Link key={item.name} href={item.href}>
                  <Button
                    variant="ghost"
                    className={cn(
                      "w-full justify-start gap-3 h-11 px-4 text-sidebar-foreground/80 hover:text-sidebar-foreground hover:bg-sidebar-foreground/10",
                      pathname === item.href &&
                        "bg-sidebar-primary text-sidebar-primary-foreground hover:bg-sidebar-primary hover:text-sidebar-primary-foreground",
                    )}
                  >
                    <item.icon className="h-5 w-5" />
                    {item.name}
                  </Button>
                </Link>
              ))}
            </div>
          </ScrollArea>
        </div>

        <div className="absolute bottom-4 left-3 right-3">
          <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-sidebar-foreground/5">
            <Avatar className="h-8 w-8">
              <AvatarImage src="/placeholder.svg?height=32&width=32" />
              <AvatarFallback className="bg-sidebar-primary text-sidebar-primary-foreground text-sm">AW</AvatarFallback>
            </Avatar>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-sidebar-foreground truncate">Alex Williamson</p>
              <p className="text-xs text-sidebar-foreground/70 truncate">Radio-1974</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export function MobileSidebar() {
  const [open, setOpen] = useState(false)

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="h-5 w-5" />
          <span className="sr-only">Toggle navigation menu</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-64 p-0 professional-sidebar">
        <Sidebar />
      </SheetContent>
    </Sheet>
  )
}
