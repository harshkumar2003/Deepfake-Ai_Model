"use client"

import { Card } from "@/components/ui/card"

interface ResultTabsProps {
  selectedTab: string
  setSelectedTab: (tab: string) => void
}

export default function ResultTabs({ selectedTab, setSelectedTab }: ResultTabsProps) {
  const tabs = [
    { id: "visual", label: "Visual Inconsistencies" },
    { id: "audio", label: "Audio Inconsistencies" },
    { id: "metadata", label: "Metadata Details" },
  ]

  const tabContent = {
    visual: [
      { issue: "Unnatural eye blinks", severity: "High" },
      { issue: "Skin tone discontinuities", severity: "Medium" },
      { issue: "Hair edge artifacts", severity: "High" },
    ],
    audio: [
      { issue: "Audio-lip sync mismatch", severity: "High" },
      { issue: "Frequency anomalies", severity: "Medium" },
    ],
    metadata: [
      { field: "Codec", value: "H.264" },
      { field: "Creation Date", value: "Unknown" },
      { field: "Compression Quality", value: "87%" },
    ],
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-2 border-b border-border">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setSelectedTab(tab.id)}
            className={`px-4 py-2 text-sm font-medium transition-colors ${
              selectedTab === tab.id
                ? "border-b-2 border-primary text-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <Card className="p-6">
        <div className="space-y-4">
          {selectedTab === "metadata"
            ? (tabContent.metadata as Array<{ field: string; value: string }>).map((item, idx) => (
                <div
                  key={idx}
                  className="flex justify-between items-center py-2 border-b border-border last:border-b-0"
                >
                  <span className="text-muted-foreground">{item.field}</span>
                  <span className="font-medium text-foreground">{item.value}</span>
                </div>
              ))
            : (tabContent[selectedTab as keyof typeof tabContent] as Array<{ issue: string; severity: string }>).map(
                (item, idx) => (
                  <div key={idx} className="flex items-center justify-between py-3 px-4 rounded-lg bg-muted">
                    <span className="text-foreground">{item.issue}</span>
                    <span
                      className={`text-xs font-semibold px-2 py-1 rounded ${
                        item.severity === "High" ? "bg-accent/20 text-accent" : "bg-primary/20 text-primary"
                      }`}
                    >
                      {item.severity}
                    </span>
                  </div>
                ),
              )}
        </div>
      </Card>
    </div>
  )
}
