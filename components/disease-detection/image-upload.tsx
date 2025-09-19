"use client"

import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Camera, Upload, X, Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface ImageUploadProps {
  onImageUpload: (file: File) => void
  isAnalyzing: boolean
}

export function ImageUpload({ onImageUpload, isAnalyzing }: ImageUploadProps) {
  const [preview, setPreview] = useState<string | null>(null)

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const file = acceptedFiles[0]
      if (file) {
        const previewUrl = URL.createObjectURL(file)
        setPreview(previewUrl)
        onImageUpload(file)
      }
    },
    [onImageUpload],
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".jpeg", ".jpg", ".png", ".webp"],
    },
    maxFiles: 1,
    disabled: isAnalyzing,
  })

  const clearPreview = () => {
    if (preview) {
      URL.revokeObjectURL(preview)
      setPreview(null)
    }
  }

  return (
    <div className="space-y-4">
      {!preview ? (
        <Card
          {...getRootProps()}
          className={cn(
            "border-2 border-dashed border-muted-foreground/25 hover:border-muted-foreground/50 transition-colors cursor-pointer",
            isDragActive && "border-primary bg-primary/5",
            isAnalyzing && "cursor-not-allowed opacity-50",
          )}
        >
          <div className="flex flex-col items-center justify-center p-8 text-center">
            <input {...getInputProps()} />
            {isAnalyzing ? (
              <Loader2 className="h-12 w-12 text-muted-foreground animate-spin mb-4" />
            ) : (
              <Upload className="h-12 w-12 text-muted-foreground mb-4" />
            )}
            <h3 className="text-lg font-semibold mb-2">
              {isDragActive ? "Drop your image here" : "Upload Plant Image"}
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Drag and drop an image, or click to select from your device
            </p>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" disabled={isAnalyzing}>
                <Camera className="h-4 w-4 mr-2" />
                Take Photo
              </Button>
              <Button variant="outline" size="sm" disabled={isAnalyzing}>
                <Upload className="h-4 w-4 mr-2" />
                Choose File
              </Button>
            </div>
            <p className="text-xs text-muted-foreground mt-2">Supports: JPEG, PNG, WebP (max 10MB)</p>
          </div>
        </Card>
      ) : (
        <Card className="p-4">
          <div className="relative">
            <img
              src={preview || "/placeholder.svg"}
              alt="Uploaded plant"
              className="w-full h-64 object-cover rounded-lg"
            />
            {!isAnalyzing && (
              <Button variant="destructive" size="icon" className="absolute top-2 right-2" onClick={clearPreview}>
                <X className="h-4 w-4" />
              </Button>
            )}
            {isAnalyzing && (
              <div className="absolute inset-0 bg-black/50 rounded-lg flex items-center justify-center">
                <div className="text-center text-white">
                  <Loader2 className="h-8 w-8 animate-spin mx-auto mb-2" />
                  <p className="text-sm">Analyzing...</p>
                </div>
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  )
}
