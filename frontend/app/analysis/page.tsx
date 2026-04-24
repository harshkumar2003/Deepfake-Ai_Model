"use client"

import { useState } from "react"
import Header from "@/components/header"
import ProgressIndicator from "@/components/progress-indicator"
import FramePreview from "@/components/frame-preview"
import AnalysisPanel from "@/components/analysis-panel"

export default function AnalysisPage() {
  const [progress, setProgress] = useState(1)

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <h1 className="mb-8 text-3xl font-bold text-foreground">Analysis in Progress</h1>

        <ProgressIndicator currentStep={progress} />

        <div className="mt-8 grid gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <FramePreview />
          </div>
          <div>
            <AnalysisPanel progress={progress} />
          </div>
        </div>
      </main>
    </div>
  )
}
