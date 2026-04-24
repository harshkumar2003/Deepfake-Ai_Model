"use client"

import { useState } from "react"
import Header from "@/components/header"
import { Download, DownloadCloud, ArrowLeft } from "lucide-react"
import Link from "next/link"

export default function ResultPage() {
  const [activeTab, setActiveTab] = useState("overview")
  const confidence = 92

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "visual", label: "Visual Issues" },
    { id: "audio", label: "Audio Analysis" },
    { id: "details", label: "Technical Details" },
  ]

  return (
    <div className="min-h-screen bg-[#faf7f3]">
      <Header />

      <main className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Back Button */}
        <Link
          href="/analyze"
          className="flex items-center gap-2 text-[#a0573d] hover:text-[#8a4a31] transition-smooth mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Analyze
        </Link>

        {/* Result Header */}
        <div className="card p-8 mb-8 text-center animate-fade-in">
          <h1 className="text-[#2a2a2a] mb-4">Our Analysis Suggests</h1>
          <div className="inline-block">
            <p className="text-2xl font-bold text-[#c85a54] mb-2">DEEPFAKE DETECTED</p>
          </div>
        </div>

        {/* Confidence Meter */}
        <div className="card p-12 mb-8 animate-fade-in">
          <div className="text-center mb-8">
            <p className="text-[#8a8580] text-sm font-medium mb-4">CONFIDENCE SCORE</p>
          </div>

          {/* Custom Circular Confidence Meter */}
          <div className="flex justify-center mb-8">
            <div className="relative w-48 h-48">
              <svg className="w-full h-full" viewBox="0 0 200 200">
                {/* Gray background circle */}
                <circle cx="100" cy="100" r="90" fill="none" stroke="#e8ddd4" strokeWidth="12" />

                {/* Red confidence arc */}
                <circle
                  cx="100"
                  cy="100"
                  r="90"
                  fill="none"
                  stroke="#c85a54"
                  strokeWidth="12"
                  strokeDasharray={`${(confidence / 100) * (2 * Math.PI * 90)} ${2 * Math.PI * 90}`}
                  strokeDashoffset={`${(Math.PI * 90) / -1}`}
                  strokeLinecap="round"
                  className="transition-all duration-1000"
                />
              </svg>

              {/* Center content */}
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-5xl font-bold text-[#c85a54]">{confidence}%</span>
                <span className="text-sm text-[#8a8580] mt-1">Likely Deepfake</span>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4 text-center">
            <div className="p-4 bg-[#f5ede9] rounded-lg">
              <p className="text-sm text-[#8a8580] mb-1">Face Manipulation</p>
              <p className="text-2xl font-bold text-[#a0573d]">94%</p>
            </div>
            <div className="p-4 bg-[#f5ede9] rounded-lg">
              <p className="text-sm text-[#8a8580] mb-1">Audio Mismatch</p>
              <p className="text-2xl font-bold text-[#c9a872]">78%</p>
            </div>
            <div className="p-4 bg-[#f5ede9] rounded-lg">
              <p className="text-sm text-[#8a8580] mb-1">Artifact Detection</p>
              <p className="text-2xl font-bold text-[#a0573d]">88%</p>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="card mb-8 overflow-hidden animate-fade-in">
          <div className="flex border-b border-[#e8ddd4]">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 px-6 py-4 font-medium text-center transition-smooth border-b-2 ${
                  activeTab === tab.id
                    ? "border-[#a0573d] text-[#a0573d]"
                    : "border-transparent text-[#8a8580] hover:text-[#5a5555]"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="p-8">
            {activeTab === "overview" && (
              <div className="space-y-4">
                <h3 className="font-semibold text-[#2a2a2a]">Key Findings</h3>
                <ul className="space-y-2 text-[#5a5555]">
                  <li className="flex gap-3">
                    <span className="text-[#c85a54] font-bold">•</span>
                    <span>Facial features show unnatural transitions and warping patterns</span>
                  </li>
                  <li className="flex gap-3">
                    <span className="text-[#c85a54] font-bold">•</span>
                    <span>Audio waveform analysis reveals synchronization issues</span>
                  </li>
                  <li className="flex gap-3">
                    <span className="text-[#c85a54] font-bold">•</span>
                    <span>Frame-by-frame analysis detected AI-generated artifacts</span>
                  </li>
                </ul>
              </div>
            )}

            {activeTab === "visual" && (
              <div className="space-y-4">
                <h3 className="font-semibold text-[#2a2a2a]">Visual Analysis</h3>
                <p className="text-[#5a5555] mb-4">Detected the following visual inconsistencies:</p>
                <div className="space-y-3">
                  <div className="p-4 bg-[#f5ede9] rounded-lg">
                    <p className="font-medium text-[#2a2a2a]">Eye Region</p>
                    <p className="text-sm text-[#8a8580]">Unnatural blinking patterns and pupil distortion</p>
                  </div>
                  <div className="p-4 bg-[#f5ede9] rounded-lg">
                    <p className="font-medium text-[#2a2a2a]">Facial Boundaries</p>
                    <p className="text-sm text-[#8a8580]">Soft edges indicating neural network upsampling</p>
                  </div>
                  <div className="p-4 bg-[#f5ede9] rounded-lg">
                    <p className="font-medium text-[#2a2a2a]">Skin Texture</p>
                    <p className="text-sm text-[#8a8580]">Lack of natural pores and minor skin imperfections</p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "audio" && (
              <div className="space-y-4">
                <h3 className="font-semibold text-[#2a2a2a]">Audio Analysis</h3>
                <p className="text-[#5a5555] mb-4">Audio-visual synchronization issues detected:</p>
                <div className="space-y-3">
                  <div className="p-4 bg-[#f5ede9] rounded-lg">
                    <p className="font-medium text-[#2a2a2a]">Lip Sync</p>
                    <p className="text-sm text-[#8a8580]">Off-sync by ~120ms in frames 45-78</p>
                  </div>
                  <div className="p-4 bg-[#f5ede9] rounded-lg">
                    <p className="font-medium text-[#2a2a2a]">Voice Characteristics</p>
                    <p className="text-sm text-[#8a8580]">Possible voice synthesis detected using spectral analysis</p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "details" && (
              <div className="space-y-4">
                <h3 className="font-semibold text-[#2a2a2a]">Technical Details</h3>
                <div className="bg-[#f5ede9] rounded-lg p-4 font-mono text-xs text-[#5a5555] space-y-2">
                  <p>Analysis Duration: 2.3s</p>
                  <p>Frames Processed: 138</p>
                  <p>Model Version: v2.4.1</p>
                  <p>Detection Algorithm: FaceForensics++ CNN</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4 justify-center pb-12 animate-fade-in flex-wrap">
          <button className="btn btn-primary btn-lg">
            <Download className="w-4 h-4" />
            Download Full Report
          </button>
          <button className="btn btn-outline btn-lg">
            <DownloadCloud className="w-4 h-4" />
            Export Analysis
          </button>
        </div>
      </main>
    </div>
  )
}
