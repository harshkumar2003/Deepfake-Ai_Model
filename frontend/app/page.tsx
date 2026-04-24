"use client"

import Link from "next/link"
import Header from "@/components/header"
import UploadArea from "@/components/upload-area"
import { Lock, Shield, Zap, CheckCircle2, ArrowRight } from "lucide-react"

export default function Home() {
  return (
    <div className="min-h-screen bg-[#faf7f3]">
      <Header />

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="py-16 md:py-24">
          <div className="text-center mb-12 animate-slide-up">
            <h1 className="mb-6 text-[#2a2a2a]">
              Verify Reality.
              <br />
              Protect Trust.
            </h1>
            <p className="text-xl text-[#5a5555] mb-8 max-w-2xl mx-auto leading-relaxed">
              Upload a video and let our system help you uncover what's real.
            </p>
          </div>

          {/* Upload Area */}
          <div className="mb-12 max-w-2xl mx-auto">
            <UploadArea />
          </div>

          {/* Privacy Badge */}
          <div className="flex items-center justify-center gap-2 text-[#5a5555] bg-[#f5ede9] rounded-full px-4 py-2 w-fit mx-auto">
            <Lock className="w-4 h-4" />
            <span className="text-sm">Your video stays private. Nothing is stored.</span>
          </div>
        </div>

        {/* How It Works */}
        <div className="py-16 md:py-24">
          <h2 className="text-center text-[#2a2a2a] mb-12">How It Works</h2>

          <div className="grid md:grid-cols-4 gap-6 mb-8">
            {[
              { step: "1", title: "Reading your video…", desc: "We extract and process every frame" },
              { step: "2", title: "Examining faces…", desc: "Deep analysis of facial patterns" },
              { step: "3", title: "Checking inconsistencies…", desc: "Detection of AI-generated artifacts" },
              { step: "4", title: "Your Verdict", desc: "Comprehensive deepfake report" },
            ].map((item, idx) => (
              <div key={idx} className="card p-6 text-center group hover:shadow-lg transition-smooth">
                <div className="w-12 h-12 rounded-full bg-[#f5ede9] text-[#a0573d] font-bold mx-auto mb-4 flex items-center justify-center group-hover:bg-[#a0573d] group-hover:text-white transition-smooth">
                  {item.step}
                </div>
                <h3 className="font-semibold text-[#2a2a2a] mb-2">{item.title}</h3>
                <p className="text-sm text-[#8a8580]">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="py-16 md:py-24">
          <h2 className="text-center text-[#2a2a2a] mb-12">Why Choose DeepfakeID</h2>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                icon: Shield,
                title: "Advanced Detection",
                desc: "Using cutting-edge AI models to identify deepfakes with 94% accuracy",
              },
              {
                icon: Zap,
                title: "Fast Processing",
                desc: "Get results in seconds, not hours. Real-time analysis you can trust",
              },
              {
                icon: CheckCircle2,
                title: "Transparent",
                desc: "Understand why we flagged something. No black boxes here",
              },
            ].map((feature, idx) => {
              const Icon = feature.icon
              return (
                <div key={idx} className="card p-8 text-center group hover:shadow-lg transition-smooth">
                  <Icon className="w-8 h-8 text-[#a0573d] mx-auto mb-4 group-hover:scale-110 transition-smooth" />
                  <h3 className="font-semibold text-[#2a2a2a] mb-2">{feature.title}</h3>
                  <p className="text-sm text-[#8a8580]">{feature.desc}</p>
                </div>
              )
            })}
          </div>
        </div>

        {/* CTA */}
        <div className="py-16 md:py-24 pb-24">
          <div className="card p-12 text-center bg-gradient-to-br from-[#f5ede9] to-[#efe8e0]">
            <h2 className="text-[#2a2a2a] mb-4">Ready to verify?</h2>
            <p className="text-[#5a5555] mb-8">Start analyzing videos now to detect deepfakes with confidence</p>
            <Link href="/analyze" className="btn btn-primary btn-lg">
              Get Started
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t mt-12" style={{ borderColor: "#e8ddd4", backgroundColor: "white" }}>
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h4 className="font-semibold text-[#2a2a2a] mb-4">DeepfakeID</h4>
              <p className="text-sm text-[#8a8580]">Verify reality, protect trust.</p>
            </div>
            <div>
              <h4 className="font-semibold text-[#2a2a2a] mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="/analyze" className="text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                    Analyze
                  </Link>
                </li>
                <li>
                  <Link href="/research" className="text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                    Research
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-[#2a2a2a] mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="/about" className="text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                    About
                  </Link>
                </li>
                <li>
                  <a href="#" className="text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                    Privacy
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-[#2a2a2a] mb-4">Connect</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#" className="text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                    Twitter
                  </a>
                </li>
                <li>
                  <a href="#" className="text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                    GitHub
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t pt-8 text-center text-sm text-[#8a8580]" style={{ borderColor: "#e8ddd4" }}>
            <p>&copy; 2025 DeepfakeID. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
