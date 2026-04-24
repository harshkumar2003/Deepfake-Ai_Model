// "use client"

// import { useState } from "react"
// import UploadArea from "@/components/upload-area"
// import ProgressIndicator from "@/components/progress-indicator"
// import ResultCard from "@/components/result-card"

// export default function AnalyzePage() {
//   const [step, setStep] = useState(1)
//   const [loading, setLoading] = useState(false)
//   const [result, setResult] = useState<any>(null)

//   const handleUpload = async (file: File) => {
//     setLoading(true)
//     setResult(null)
//     setStep(1)

//     const formData = new FormData()
//     formData.append("video", file)

//     try {
//       setStep(2)

//       const res = await fetch("http://localhost:8000/upload", {
//         method: "POST",
//         body: formData,
//       })

//       setStep(3)

//       if (!res.ok) {
//         throw new Error("Backend error")
//       }

//       const data = await res.json()
//       console.log("Backend response:", data)

//       setResult(data)
//       setStep(4)
//     } catch (err) {
//       console.error("Upload failed:", err)
//       alert("Video upload or analysis failed")
//     } finally {
//       setLoading(false)
//     }
//   }

//   return (
//     <div className="max-w-5xl mx-auto px-6 py-12 space-y-10">
//       <UploadArea onUpload={handleUpload} />

//       {loading && <ProgressIndicator currentStep={step} />}

//       {result && (
//         <ResultCard
//   finalScore={result.final_score}
//   modelScores={result.model_scores}
// />

//       )}
//     </div>
//   )
// }


"use client"

import { useState } from "react"
import UploadArea from "@/components/upload-area"
import ProgressIndicator from "@/components/progress-indicator"
import ResultCard from "@/components/result-card"

interface ApiResponse {
  prediction:    string
  authenticity:  number
  ensemble_prob: number
  frames_used:   number
  model_scores:  Record<string, number>
  error?:        string
}

export default function AnalyzePage() {
  const [step, setStep]       = useState(0)           // 0 = idle
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState<ApiResponse | null>(null)
  const [error, setError]     = useState<string | null>(null)

  const handleUpload = async (file: File) => {
    setLoading(true)
    setResult(null)
    setError(null)
    setStep(1)                                         // step 1 — uploading

    const formData = new FormData()
    formData.append("video", file)

    try {
      setStep(2)                                       // step 2 — analysing

      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      })

      const data: ApiResponse = await res.json()
      console.log("Backend response:", data)

      if (!res.ok || data.error) {
        throw new Error(data.error ?? `Server error ${res.status}`)
      }

      setStep(3)                                       // step 3 — done
      setResult(data)
    } catch (err: any) {
      console.error("Upload failed:", err)
      setError(err.message ?? "Video upload or analysis failed.")
      setStep(0)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-10">
      <UploadArea onUpload={handleUpload} />

      {loading && <ProgressIndicator currentStep={step} />}

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      {result && (
        <ResultCard
          authenticity={result.authenticity}
          modelScores={result.model_scores}
        />
      )}
    </div>
  )
}