"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Loader2, TestTube, MapPin, Thermometer, CloudRain } from "lucide-react"
import type { SoilData } from "./crop-recommendation-content"

const soilAnalysisSchema = z.object({
  ph: z.number().min(3).max(10),
  nitrogen: z.number().min(0).max(100),
  phosphorus: z.number().min(0).max(100),
  potassium: z.number().min(0).max(100),
  organicMatter: z.number().min(0).max(20),
  soilType: z.string().min(1, "Please select soil type"),
  rainfall: z.number().min(0).max(5000),
  temperature: z.number().min(15).max(45),
  season: z.string().min(1, "Please select season"),
  location: z.string().min(1, "Please enter location"),
})

interface SoilAnalysisFormProps {
  onSubmit: (data: SoilData) => void
  isAnalyzing: boolean
}

export function SoilAnalysisForm({ onSubmit, isAnalyzing }: SoilAnalysisFormProps) {
  const [step, setStep] = useState(1)
  const totalSteps = 3

  const form = useForm<SoilData>({
    resolver: zodResolver(soilAnalysisSchema),
    defaultValues: {
      ph: 6.5,
      nitrogen: 50,
      phosphorus: 30,
      potassium: 40,
      organicMatter: 3,
      soilType: "",
      rainfall: 2500,
      temperature: 28,
      season: "",
      location: "",
    },
  })

  const handleSubmit = (data: SoilData) => {
    onSubmit(data)
  }

  const nextStep = () => {
    if (step < totalSteps) setStep(step + 1)
  }

  const prevStep = () => {
    if (step > 1) setStep(step - 1)
  }

  const getStepTitle = (stepNumber: number) => {
    switch (stepNumber) {
      case 1:
        return "Soil Composition"
      case 2:
        return "Environmental Conditions"
      case 3:
        return "Location & Season"
      default:
        return "Analysis"
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TestTube className="h-5 w-5" />
          Soil & Environmental Analysis
        </CardTitle>
        <CardDescription>
          Provide your soil test results and environmental conditions for personalized crop recommendations
        </CardDescription>
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span>
              Step {step} of {totalSteps}: {getStepTitle(step)}
            </span>
            <span>{Math.round((step / totalSteps) * 100)}% Complete</span>
          </div>
          <Progress value={(step / totalSteps) * 100} className="h-2" />
        </div>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
            {step === 1 && (
              <div className="space-y-6">
                <Alert>
                  <TestTube className="h-4 w-4" />
                  <AlertDescription>
                    Enter your soil test results. If you don't have recent soil test data, we recommend getting your
                    soil tested at a local agricultural extension office.
                  </AlertDescription>
                </Alert>

                <div className="grid gap-4 md:grid-cols-2">
                  <FormField
                    control={form.control}
                    name="ph"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>pH Level</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            step="0.1"
                            min="3"
                            max="10"
                            {...field}
                            onChange={(e) => field.onChange(Number.parseFloat(e.target.value))}
                          />
                        </FormControl>
                        <FormDescription>Soil acidity/alkalinity (3.0 - 10.0)</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="soilType"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Soil Type</FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select soil type" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="clay">Clay</SelectItem>
                            <SelectItem value="sandy">Sandy</SelectItem>
                            <SelectItem value="loamy">Loamy</SelectItem>
                            <SelectItem value="silt">Silt</SelectItem>
                            <SelectItem value="laterite">Laterite</SelectItem>
                            <SelectItem value="alluvial">Alluvial</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div className="grid gap-4 md:grid-cols-3">
                  <FormField
                    control={form.control}
                    name="nitrogen"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Nitrogen (N)</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min="0"
                            max="100"
                            {...field}
                            onChange={(e) => field.onChange(Number.parseFloat(e.target.value))}
                          />
                        </FormControl>
                        <FormDescription>mg/kg</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="phosphorus"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Phosphorus (P)</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min="0"
                            max="100"
                            {...field}
                            onChange={(e) => field.onChange(Number.parseFloat(e.target.value))}
                          />
                        </FormControl>
                        <FormDescription>mg/kg</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="potassium"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Potassium (K)</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min="0"
                            max="100"
                            {...field}
                            onChange={(e) => field.onChange(Number.parseFloat(e.target.value))}
                          />
                        </FormControl>
                        <FormDescription>mg/kg</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <FormField
                  control={form.control}
                  name="organicMatter"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Organic Matter Content</FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          step="0.1"
                          min="0"
                          max="20"
                          {...field}
                          onChange={(e) => field.onChange(Number.parseFloat(e.target.value))}
                        />
                      </FormControl>
                      <FormDescription>Percentage (0-20%)</FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            )}

            {step === 2 && (
              <div className="space-y-6">
                <Alert>
                  <Thermometer className="h-4 w-4" />
                  <AlertDescription>
                    Environmental conditions greatly influence crop selection. Provide average values for your area.
                  </AlertDescription>
                </Alert>

                <div className="grid gap-4 md:grid-cols-2">
                  <FormField
                    control={form.control}
                    name="rainfall"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="flex items-center gap-2">
                          <CloudRain className="h-4 w-4" />
                          Annual Rainfall
                        </FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min="0"
                            max="5000"
                            {...field}
                            onChange={(e) => field.onChange(Number.parseFloat(e.target.value))}
                          />
                        </FormControl>
                        <FormDescription>Millimeters per year</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="temperature"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="flex items-center gap-2">
                          <Thermometer className="h-4 w-4" />
                          Average Temperature
                        </FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min="15"
                            max="45"
                            {...field}
                            onChange={(e) => field.onChange(Number.parseFloat(e.target.value))}
                          />
                        </FormControl>
                        <FormDescription>Degrees Celsius</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div className="p-4 bg-muted rounded-lg">
                  <h4 className="font-medium mb-2">Kerala Climate Reference</h4>
                  <div className="text-sm text-muted-foreground space-y-1">
                    <p>• Coastal areas: 2000-3000mm rainfall, 25-32°C temperature</p>
                    <p>• Midland areas: 2500-3500mm rainfall, 23-30°C temperature</p>
                    <p>• Highland areas: 3000-5000mm rainfall, 15-25°C temperature</p>
                  </div>
                </div>
              </div>
            )}

            {step === 3 && (
              <div className="space-y-6">
                <Alert>
                  <MapPin className="h-4 w-4" />
                  <AlertDescription>
                    Location and seasonal information help us provide region-specific recommendations.
                  </AlertDescription>
                </Alert>

                <div className="grid gap-4 md:grid-cols-2">
                  <FormField
                    control={form.control}
                    name="location"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="flex items-center gap-2">
                          <MapPin className="h-4 w-4" />
                          Location
                        </FormLabel>
                        <FormControl>
                          <Input placeholder="e.g., Kochi, Thiruvananthapuram" {...field} />
                        </FormControl>
                        <FormDescription>District or city in Kerala</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="season"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Current Season</FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select season" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="pre-monsoon">Pre-Monsoon (March-May)</SelectItem>
                            <SelectItem value="monsoon">Monsoon (June-September)</SelectItem>
                            <SelectItem value="post-monsoon">Post-Monsoon (October-December)</SelectItem>
                            <SelectItem value="winter">Winter (January-February)</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div className="p-4 bg-primary/5 rounded-lg border border-primary/20">
                  <h4 className="font-medium mb-2 text-primary">Ready for Analysis</h4>
                  <p className="text-sm text-muted-foreground">
                    Our AI will analyze your soil and environmental data to recommend the most suitable crops for your
                    farm, considering market trends and profitability.
                  </p>
                </div>
              </div>
            )}

            <div className="flex justify-between">
              <Button type="button" variant="outline" onClick={prevStep} disabled={step === 1 || isAnalyzing}>
                Previous
              </Button>
              {step < totalSteps ? (
                <Button type="button" onClick={nextStep}>
                  Next Step
                </Button>
              ) : (
                <Button type="submit" disabled={isAnalyzing}>
                  {isAnalyzing ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    "Get Recommendations"
                  )}
                </Button>
              )}
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  )
}
