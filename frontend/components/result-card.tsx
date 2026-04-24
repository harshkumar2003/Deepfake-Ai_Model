// interface ResultCardProps {
//   finalScore: number
//   modelScores?: Record<string, number>
// }

// export default function ResultCard({
//   finalScore,
//   modelScores,
// }: ResultCardProps) {
//   const verdict =
//     finalScore < 40
//       ? "Likely Deepfake"
//       : finalScore < 60
//       ? "Uncertain"
//       : "Likely Genuine"

//   return (
//     <div className="card p-6 space-y-6">
//       {/* FINAL SCORE */}
//       <div className="text-center space-y-2">
//         <h2 className="text-xl font-semibold text-gray-800">
//           Final Authenticity Score
//         </h2>

//         {/* 🔥 SCORE FIX */}
//         <div className="text-5xl font-bold text-[#a0573d]">
//           {finalScore.toFixed(2)}%
//         </div>

//         <div className="text-lg text-gray-600">{verdict}</div>
//       </div>

//       {/* MODEL SCORES */}
//       {modelScores && (
//         <>
//           <hr />

//           <div className="space-y-4">
//             <h3 className="text-lg font-semibold text-gray-800">
//               Model-wise Breakdown
//             </h3>

//             {Object.entries(modelScores).map(([model, score]) => (
//               <div key={model} className="space-y-1">
//                 <div className="flex justify-between text-sm font-medium">
//                   <span>{model}</span>
//                   <span>{score.toFixed(2)}%</span>
//                 </div>

//                 <div className="w-full bg-gray-200 rounded-full h-2">
//                   <div
//                     className="h-2 rounded-full bg-[#a0573d]"
//                     style={{ width: `${score}%` }}
//                   />
//                 </div>
//               </div>
//             ))}
//           </div>
//         </>
//       )}

//       {/* EXPLANATION */}
//       <p className="text-sm text-gray-600">
//         This decision is produced by averaging predictions from multiple deepfake
//         detection models. Differences between models indicate uncertainty or
//         complex manipulation patterns.
//       </p>
//     </div>
//   )
// }
// interface ResultCardProps {
//   finalScore?: number        // optional — was crashing when undefined
//   authenticity?: number      // backend sends "authenticity", not "finalScore"
//   modelScores?: Record<string, number>
// }

// export default function ResultCard({
//   finalScore,
//   authenticity,
//   modelScores,
// }: ResultCardProps) {
//   // ── normalise: accept either field name from the backend ──────────────────
//   const score = finalScore ?? authenticity ?? null

//   if (score === null) {
//     return (
//       <div className="card p-6 text-center text-gray-500">
//         No score available.
//       </div>
//     )
//   }

//   const verdict =
//     score < 40 ? "Likely Deepfake" :
//     // score < 60 ? "Uncertain"       :
//                  "Likely Genuine"

//   const verdictColor =
//     score < 40 ? "text-red-600"    :
//     score < 60 ? "text-yellow-600" :
//                  "text-green-600"

//   return (
//     <div className="card p-6 space-y-6">
//       {/* FINAL SCORE */}
//       <div className="text-center space-y-2">
//         <h2 className="text-xl font-semibold text-gray-800">
//           Final Authenticity Score
//         </h2>

//         <div className="text-5xl font-bold text-[#a0573d]">
//           {score.toFixed(2)}%
//         </div>

//         <div className={`text-lg font-medium ${verdictColor}`}>{verdict}</div>
//       </div>

//       {/* MODEL SCORES */}
//       {modelScores && Object.keys(modelScores).length > 0 && (
//         <>
//           <hr />
//           <div className="space-y-4">
//             <h3 className="text-lg font-semibold text-gray-800">
//               Model-wise Breakdown
//             </h3>

//             {Object.entries(modelScores).map(([model, s]) => {
//               const safeScore = typeof s === "number" ? s : 0
//               return (
//                 <div key={model} className="space-y-1">
//                   <div className="flex justify-between text-sm font-medium">
//                     <span>{model}</span>
//                     <span>{safeScore.toFixed(2)}%</span>
//                   </div>
//                   <div className="w-full bg-gray-200 rounded-full h-2">
//                     <div
//                       className="h-2 rounded-full bg-[#a0573d] transition-all"
//                       style={{ width: `${Math.min(100, Math.max(0, safeScore))}%` }}
//                     />
//                   </div>
//                 </div>
//               )
//             })}
//           </div>
//         </>
//       )}

//       <p className="text-sm text-gray-500">
//         This decision is produced by averaging predictions from multiple deepfake
//         detection models. Differences between models indicate uncertainty or
//         complex manipulation patterns.
//       </p>
//     </div>
//   )
// }


// interface ResultCardProps {
//   finalScore?: number
//   authenticity?: number
//   modelScores?: Record<string, number>
// }

// export default function ResultCard({
//   finalScore,
//   authenticity,
//   modelScores,
// }: ResultCardProps) {
//   // normalize score
//   const score = finalScore ?? authenticity ?? null

//   if (score === null) {
//     return (
//       <div className="card p-6 text-center text-gray-500">
//         No score available.
//       </div>
//     )
//   }

//   // 🔥 FINAL LOGIC — NO UNCERTAINTY
//   const verdict =
//     score < 40 ? "Likely Deepfake" : "Likely Genuine"

//   const verdictColor =
//     score < 40 ? "text-red-600" : "text-green-600"

//   return (
//     <div className="card p-6 space-y-6">
//       {/* FINAL SCORE */}
//       <div className="text-center space-y-2">
//         <h2 className="text-xl font-semibold text-gray-800">
//           Final Authenticity Score
//         </h2>

//         <div className="text-5xl font-bold text-[#a0573d]">
//           {score.toFixed(2)}%
//         </div>

//         <div className={`text-lg font-medium ${verdictColor}`}>
//           {verdict}
//         </div>
//       </div>

//       {/* MODEL SCORES */}
//       {modelScores && Object.keys(modelScores).length > 0 && (
//         <>
//           <hr />
//           <div className="space-y-4">
//             <h3 className="text-lg font-semibold text-gray-800">
//               Model-wise Breakdown
//             </h3>

//             {Object.entries(modelScores).map(([model, s]) => {
//               const safeScore = typeof s === "number" ? s : 0
//               return (
//                 <div key={model} className="space-y-1">
//                   <div className="flex justify-between text-sm font-medium">
//                     <span>{model}</span>
//                     <span>{safeScore.toFixed(2)}%</span>
//                   </div>

//                   <div className="w-full bg-gray-200 rounded-full h-2">
//                     <div
//                       className="h-2 rounded-full bg-[#a0573d] transition-all"
//                       style={{
//                         width: `${Math.min(100, Math.max(0, safeScore))}%`,
//                       }}
//                     />
//                   </div>
//                 </div>
//               )
//             })}
//           </div>
//         </>
//       )}

//       <p className="text-sm text-gray-500">
//         This decision is produced by averaging predictions from multiple deepfake
//         detection models.
//       </p>
//     </div>
//   )
// }



// interface ResultCardProps {
//   authenticity?: number
//   finalScore?: number
//   modelScores?: Record<string, number>
// }

// export default function ResultCard({
//   authenticity,
//   finalScore,
//   modelScores,
// }: ResultCardProps) {
//   const score = authenticity ?? finalScore ?? null

//   if (score === null) {
//     return (
//       <div className="card p-6 text-center text-gray-500">
//         No score available.
//       </div>
//     )
//   }

//   // ── threshold calibrated from your actual result data ──────────────────────
//   //    Real videos:  60% – 88%  authenticity
//   //    Fake videos:  29% – 58%  authenticity
//   //    Decision boundary: 60%
//   const isReal   = score >= 60
//   const verdict  = isReal ? "Real"  : "Deepfake"
//   const bgColor  = isReal ? "bg-green-50  border-green-200"  : "bg-red-50  border-red-200"
//   const txtColor = isReal ? "text-green-700" : "text-red-700"
//   const barColor = isReal ? "bg-green-500"   : "bg-red-500"
//   const scoreColor = isReal ? "text-green-600" : "text-red-600"

//   return (
//     <div className="card p-6 space-y-6">
//       {/* VERDICT BANNER */}
//       <div className={`rounded-lg border p-4 text-center ${bgColor}`}>
//         <div className={`text-2xl font-semibold ${txtColor}`}>
//           {isReal ? "✓ Real Video" : "✗ Deepfake Detected"}
//         </div>
//       </div>

//       {/* SCORE */}
//       <div className="text-center space-y-1">
//         <div className={`text-5xl font-bold ${scoreColor}`}>
//           {score.toFixed(1)}%
//         </div>
//         <div className="text-sm text-gray-500">
//           Authenticity score — {isReal ? "above" : "below"} 60% threshold
//         </div>
//       </div>

//       {/* SCORE BAR */}
//       <div className="space-y-1">
//         <div className="relative w-full bg-gray-200 rounded-full h-3">
//           {/* threshold marker */}
//           <div
//             className="absolute top-0 bottom-0 w-0.5 bg-blue-400 z-10"
//             style={{ left: "60%" }}
//           />
//           {/* score fill */}
//           <div
//             className={`h-3 rounded-full ${barColor} transition-all`}
//             style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
//           />
//         </div>
//         <div className="flex justify-between text-xs text-gray-400">
//           <span>0% (Deepfake)</span>
//           <span className="text-blue-400">60%</span>
//           <span>100% (Real)</span>
//         </div>
//       </div>

//       {/* MODEL SCORES */}
//       {modelScores && Object.keys(modelScores).length > 0 && (
//         <>
//           <hr />
//           <div className="space-y-3">
//             <h3 className="text-sm font-semibold text-gray-700">
//               Model breakdown
//             </h3>
//             {Object.entries(modelScores).map(([model, s]) => {
//               const safe = typeof s === "number" ? s : 0
//               // model scores are fake-probability × 100, so invert for display
//               const displayScore = 100 - safe
//               const modelReal = displayScore >= 60
//               return (
//                 <div key={model} className="space-y-1">
//                   <div className="flex justify-between text-sm">
//                     <span className="text-gray-600">{model}</span>
//                     <span className={modelReal ? "text-green-600" : "text-red-600"}>
//                       {displayScore.toFixed(1)}%
//                     </span>
//                   </div>
//                   <div className="w-full bg-gray-200 rounded-full h-2">
//                     <div
//                       className={`h-2 rounded-full transition-all ${modelReal ? "bg-green-400" : "bg-red-400"}`}
//                       style={{ width: `${Math.min(100, Math.max(0, displayScore))}%` }}
//                     />
//                   </div>
//                 </div>
//               )
//             })}
//           </div>
//         </>
//       )}

//       <p className="text-xs text-gray-400">
//         Ensemble of EfficientNet, MobileNet, and ShuffleNet. Scores above 60%
//         indicate a real video; below 60% indicates a deepfake.
//       </p>
//     </div>
//   )
// }

// interface ResultCardProps {
//   authenticity?: number
//   finalScore?: number
//   modelScores?: Record<string, number>
// }

// export default function ResultCard({
//   authenticity,
//   finalScore,
//   modelScores,
// }: ResultCardProps) {
//   const score = authenticity ?? finalScore ?? null

//   if (score === null) {
//     return (
//       <div className="card p-6 text-center text-gray-500">
//         No score available.
//       </div>
//     )
//   }

//   // ── SAME LOGIC ────────────────────────────────────────────────────────────
//   const isReal   = score >= 60
//   const verdict  = isReal ? "Real" : "Deepfake"

//   const bgColor  = isReal ? "bg-green-50 border-green-200" : "bg-red-50 border-red-200"
//   const txtColor = isReal ? "text-green-700" : "text-red-700"
//   const barColor = isReal ? "bg-green-500" : "bg-red-500"
//   const scoreColor = isReal ? "text-green-600" : "text-red-600"

//   return (
//     <div className="card p-6 space-y-6 shadow-lg rounded-2xl border bg-white">

//       {/* 🔥 VERDICT BANNER (Enhanced) */}
//       <div className={`rounded-xl border p-5 text-center ${bgColor}`}>
//         <div className={`text-2xl font-bold tracking-wide ${txtColor}`}>
//           {isReal ? "✓ Real Video" : "✗ Deepfake Detected"}
//         </div>
//         <p className="text-xs mt-1 text-gray-500">
//           AI authenticity decision
//         </p>
//       </div>

//       {/* 🔥 SCORE SECTION (Cleaner + Premium Feel) */}
//       <div className="text-center space-y-2">
//         <div className={`text-6xl font-extrabold ${scoreColor}`}>
//           {score.toFixed(1)}%
//         </div>
//         <div className="text-sm text-gray-500">
//           Authenticity Score
//         </div>
//       </div>

//       {/* 🔥 PROGRESS BAR (Smoother + Highlight Threshold) */}
//       <div className="space-y-2">
//         <div className="relative w-full bg-gray-200 rounded-full h-4 overflow-hidden">

//           {/* Threshold Marker */}
//           <div
//             className="absolute top-0 bottom-0 w-[2px] bg-blue-500 z-10"
//             style={{ left: "60%" }}
//           />

//           {/* Score Fill */}
//           <div
//             className={`h-4 rounded-full transition-all duration-700 ease-in-out ${barColor}`}
//             style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
//           />
//         </div>

//         <div className="flex justify-between text-xs text-gray-400">
//           <span>Fake</span>
//           <span className="text-blue-500 font-medium">60%</span>
//           <span>Real</span>
//         </div>
//       </div>

//       {/* 🔥 MODEL BREAKDOWN (More Structured) */}
//       {modelScores && Object.keys(modelScores).length > 0 && (
//         <>
//           <hr />
//           <div className="space-y-4">
//             <h3 className="text-sm font-semibold text-gray-700">
//               Model-wise Analysis
//             </h3>

//             {Object.entries(modelScores).map(([model, s]) => {
//               const safe = typeof s === "number" ? s : 0
//               const displayScore = 100 - safe
//               const modelReal = displayScore >= 60

//               return (
//                 <div key={model} className="space-y-1">
//                   <div className="flex justify-between text-sm">
//                     <span className="text-gray-600">{model}</span>
//                     <span className={modelReal ? "text-green-600 font-medium" : "text-red-600 font-medium"}>
//                       {displayScore.toFixed(1)}%
//                     </span>
//                   </div>

//                   <div className="w-full bg-gray-200 rounded-full h-2">
//                     <div
//                       className={`h-2 rounded-full transition-all duration-500 ${
//                         modelReal ? "bg-green-400" : "bg-red-400"
//                       }`}
//                       style={{
//                         width: `${Math.min(100, Math.max(0, displayScore))}%`,
//                       }}
//                     />
//                   </div>
//                 </div>
//               )
//             })}
//           </div>
//         </>
//       )}

//       {/* 🔥 FOOTNOTE (Sharper tone) */}
//       <p className="text-xs text-gray-400 text-center leading-relaxed">
//         Ensemble decision from EfficientNet, MobileNet, and ShuffleNet.  
//         Scores above <span className="text-blue-500 font-medium">60%</span> indicate authenticity,
//         while lower values suggest manipulation.
//       </p>
//     </div>
//   )
// }



interface ResultCardProps {
  authenticity?: number
  finalScore?: number
  modelScores?: Record<string, number>
}

export default function ResultCard({
  authenticity,
  finalScore,
  modelScores,
}: ResultCardProps) {
  const score = authenticity ?? finalScore ?? null

  if (score === null) {
    return (
      <div className="p-6 text-center text-[#8a7f78] border rounded-xl bg-white shadow">
        No score available.
      </div>
    )
  }

  const isReal = score >= 60

  return (
    <div className="p-6 space-y-6 bg-white border border-[#e7d6cd] rounded-xl shadow-sm">

      {/* 🔹 VERDICT */}
      <div className="text-center p-4 rounded-lg bg-[#f5f1ed] border border-[#e7d6cd]">
        <div className="text-xl font-semibold text-[#3a2f2a]">
          {isReal ? "✓ Real Video" : "✗ Deepfake Detected"}
        </div>
      </div>

      {/* 🔹 SCORE */}
      <div className="text-center">
        <div className="text-5xl font-bold text-[#a0573d]">
          {score.toFixed(1)}%
        </div>
        <p className="text-sm text-[#8a7f78] mt-1">
          Authenticity Score
        </p>
      </div>

      {/* 🔹 PROGRESS BAR */}
      <div>
        <div className="relative w-full h-3 bg-[#e7d6cd] rounded-full overflow-hidden">

          {/* threshold line */}
          <div
            className="absolute top-0 bottom-0 w-[2px] bg-[#a0573d]"
            style={{ left: "60%" }}
          />

          {/* score fill */}
          <div
            className="h-3 bg-[#a0573d]"
            style={{
              width: `${Math.min(100, Math.max(0, score))}%`,
            }}
          />
        </div>

        <div className="flex justify-between text-xs text-[#8a7f78] mt-1">
          <span>Fake</span>
          <span className="text-[#a0573d]">60%</span>
          <span>Real</span>
        </div>
      </div>

      {/* 🔹 MODEL SCORES */}
      {modelScores && Object.keys(modelScores).length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-[#3a2f2a]">
            Model Breakdown
          </h3>

          {Object.entries(modelScores).map(([model, s]) => {
            const safe = typeof s === "number" ? s : 0
            const displayScore = 100 - safe

            return (
              <div key={model}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-[#6b5e57]">{model}</span>
                  <span className="text-[#a0573d]">
                    {displayScore.toFixed(1)}%
                  </span>
                </div>

                <div className="w-full h-2 bg-[#e7d6cd] rounded-full">
                  <div
                    className="h-2 rounded-full bg-[#a0573d]"
                    style={{
                      width: `${Math.min(
                        100,
                        Math.max(0, displayScore)
                      )}%`,
                    }}
                  />
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* 🔹 FOOTNOTE */}
      <p className="text-xs text-[#8a7f78] text-center">
        Scores above 60% indicate authenticity. Below 60% suggests manipulation.
      </p>
    </div>
  )
}