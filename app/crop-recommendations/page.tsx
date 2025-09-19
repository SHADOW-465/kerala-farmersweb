import { Header } from "@/components/layout/header"
import { Sidebar } from "@/components/layout/sidebar"
import { CropRecommendationContent } from "@/components/crop-recommendations/crop-recommendation-content"

export default function CropRecommendationPage() {
  return (
    <div className="flex min-h-screen">
      <aside className="hidden md:block w-64 border-r bg-sidebar">
        <Sidebar />
      </aside>
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 p-6">
          <CropRecommendationContent />
        </main>
      </div>
    </div>
  )
}
