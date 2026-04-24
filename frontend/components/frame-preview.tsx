import { Card } from "@/components/ui/card"
import { Play } from "lucide-react"

export default function FramePreview() {
  return (
    <Card className="overflow-hidden">
      <div className="relative aspect-video bg-muted">
        <div className="absolute inset-0 flex items-center justify-center bg-black/20">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/20 backdrop-blur-sm">
            <Play className="h-6 w-6 text-primary fill-primary" />
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-2 bg-muted">
          <div className="h-full w-1/3 bg-accent" />
        </div>
      </div>
      <div className="p-4">
        <p className="text-xs text-muted-foreground">Frame 1234 / 5000</p>
      </div>
    </Card>
  )
}
