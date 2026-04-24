import { Card } from "@/components/ui/card"
import { Activity } from "lucide-react"

interface AnalysisPanelProps {
  progress: number
}

export default function AnalysisPanel({ progress }: AnalysisPanelProps) {
  const operations = [
    { name: "Extracting frames...", completed: progress > 1 },
    { name: "Running CNN...", completed: progress > 2 },
    { name: "Checking audio inconsistencies...", completed: progress > 3 },
    { name: "Generating report...", completed: progress > 4 },
  ]

  return (
    <div className="space-y-4">
      <Card className="p-4">
        <h3 className="mb-4 font-semibold text-foreground">Facial Landmarks</h3>
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Eyes</span>
            <span className="font-medium text-foreground">Detected</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Mouth</span>
            <span className="font-medium text-foreground">Detected</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Face Contour</span>
            <span className="font-medium text-foreground">Detected</span>
          </div>
        </div>
      </Card>

      <Card className="p-4">
        <h3 className="mb-4 font-semibold text-foreground">Operations Log</h3>
        <div className="space-y-3 max-h-64 overflow-y-auto">
          {operations.map((op, idx) => (
            <div key={idx} className="flex items-start gap-2 text-sm">
              <Activity
                className={`h-4 w-4 mt-0.5 flex-shrink-0 ${op.completed ? "text-primary" : "text-muted-foreground"}`}
              />
              <span className={op.completed ? "text-foreground" : "text-muted-foreground"}>{op.name}</span>
            </div>
          ))}
        </div>
      </Card>

      <div className="p-4 bg-muted rounded-lg">
        <label className="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" className="rounded" defaultChecked />
          <span className="text-sm font-medium text-foreground">Heatmap Overlay</span>
        </label>
      </div>
    </div>
  )
}
