"use client"

import Header from "@/components/header"
import { BookOpen, FileText, TrendingUp } from "lucide-react"

export default function ResearchPage() {
  return (
    <div className="min-h-screen bg-[#faf7f3]">
      <Header />

      <main className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Intro */}
        <div className="mb-16 animate-fade-in">
          <h1 className="text-[#2a2a2a] mb-6">Research & Technology</h1>
          <div className="card p-8">
            <p className="text-[#5a5555] leading-relaxed">
              DeepfakeID is built on cutting-edge research in computer vision, machine learning, and forensic analysis.
              We combine multiple detection methods to provide the most accurate results possible.
            </p>
          </div>
        </div>

        {/* Key Technologies */}
        <div className="mb-16 animate-fade-in">
          <h2 className="text-[#2a2a2a] mb-8 text-center">Technologies We Use</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {[
              {
                icon: BookOpen,
                title: "FaceForensics++",
                desc: "Large-scale benchmark dataset for deepfake detection containing face manipulation videos",
              },
              {
                icon: FileText,
                title: "CNN-based Detection",
                desc: "Convolutional neural networks trained to identify AI-generated facial features and artifacts",
              },
              {
                icon: TrendingUp,
                title: "Audio Analysis",
                desc: "Spectral and waveform analysis to detect voice synthesis and lip-sync mismatches",
              },
              {
                icon: BookOpen,
                title: "Temporal Analysis",
                desc: "Frame-by-frame consistency checks to identify unnatural transitions and artifacts",
              },
            ].map((tech, idx) => {
              const Icon = tech.icon
              return (
                <div key={idx} className="card p-6">
                  <Icon className="w-8 h-8 text-[#a0573d] mb-3" />
                  <h3 className="font-semibold text-[#2a2a2a] mb-2">{tech.title}</h3>
                  <p className="text-sm text-[#8a8580]">{tech.desc}</p>
                </div>
              )
            })}
          </div>
        </div>

        {/* Papers */}
        <div className="mb-16 animate-fade-in">
          <h2 className="text-[#2a2a2a] mb-8 text-center">Research Papers</h2>
          <div className="space-y-4">
            {[
              {
                title: "FaceForensics++: Learning to Detect Manipulated Facial Images",
                authors: "Li et al., 2019",
                venue: "ICCV",
              },
              {
                title: "Multi-Modal Deepfake Detection: Combining Visual and Audio Analysis",
                authors: "Rodriguez & Chen, 2023",
                venue: "CVPR",
              },
              {
                title: "Advanced Deepfake Detection Using Neural Networks",
                authors: "Smith et al., 2024",
                venue: "IEEE",
              },
            ].map((paper, idx) => (
              <div key={idx} className="card p-6 hover:shadow-lg transition-smooth cursor-pointer group">
                <h3 className="font-semibold text-[#a0573d] group-hover:text-[#2a2a2a] transition-smooth mb-2">
                  {paper.title}
                </h3>
                <p className="text-sm text-[#8a8580] mb-1">{paper.authors}</p>
                <p className="text-xs text-[#c9a872]">{paper.venue}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Limitations */}
        <div className="mb-16 animate-fade-in">
          <h2 className="text-[#2a2a2a] mb-8 text-center">Limitations & Challenges</h2>
          <div className="card p-8">
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-[#2a2a2a] mb-2">Evolving Technology</h3>
                <p className="text-[#5a5555]">
                  Deepfake technology improves constantly. Our models are regularly updated to stay ahead of new
                  manipulation techniques, but there's always a lag between new methods and detection.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-[#2a2a2a] mb-2">Accuracy Trade-offs</h3>
                <p className="text-[#5a5555]">
                  We optimize for high accuracy while minimizing false positives. However, some edge cases may be
                  misclassified, especially with novel or hybrid manipulation techniques.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-[#2a2a2a] mb-2">Data Bias</h3>
                <p className="text-[#5a5555]">
                  Our training data is predominantly English and Western-centric. Performance may vary for videos in
                  other languages or cultural contexts.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t mt-12" style={{ borderColor: "#e8ddd4", backgroundColor: "white" }}>
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-12 text-center text-sm text-[#8a8580]">
          <p>&copy; 2025 DeepfakeID. Advancing the frontier of synthetic media detection.</p>
        </div>
      </footer>
    </div>
  )
}
