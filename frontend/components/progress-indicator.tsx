const steps = [
  { label: "Uploading", id: 1 },
  { label: "Processing", id: 2 },
  { label: "Model Analysis", id: 3 },
  { label: "Report", id: 4 },
]

interface ProgressIndicatorProps {
  currentStep: number
}

export default function ProgressIndicator({ currentStep }: ProgressIndicatorProps) {
  return (
    <div className="flex items-center justify-between">
      {steps.map((step, idx) => (
        <div key={step.id} className="flex items-center flex-1">
          <div
            className={`flex h-10 w-10 items-center justify-center rounded-full font-semibold transition-colors ${
              step.id <= currentStep ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
            }`}
          >
            {step.id}
          </div>
          <p className="ml-2 text-sm font-medium text-foreground">{step.label}</p>
          {idx < steps.length - 1 && (
            <div className={`mx-4 flex-1 h-1 transition-colors ${step.id < currentStep ? "bg-primary" : "bg-muted"}`} />
          )}
        </div>
      ))}
    </div>
  )
}
