"use client"

import Header from "@/components/header"
import { Heart, Users, Zap } from "lucide-react"

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-[#faf7f3]">
      <Header />

      <main className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-12">
        {/* About Section */}
        <div className="mb-16 animate-fade-in">
          <h1 className="text-[#2a2a2a] mb-6">About DeepfakeID</h1>
          <div className="card p-8">
            <p className="text-[#5a5555] mb-4 leading-relaxed">
              DeepfakeID is a cutting-edge platform dedicated to identifying synthetic media and deepfakes. Built with
              care for truth and transparency, we provide tools to help detect AI-generated or manipulated video
              content.
            </p>
            <p className="text-[#5a5555] leading-relaxed">
              Our mission is to empower users, journalists, and researchers with reliable deepfake detection technology
              that's both accurate and understandable—not hidden behind black boxes.
            </p>
          </div>
        </div>

        {/* Values */}
        <div className="mb-16 animate-fade-in">
          <h2 className="text-[#2a2a2a] mb-8 text-center">Our Values</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="card p-8 text-center">
              <Heart className="w-8 h-8 text-[#c85a54] mx-auto mb-4" />
              <h3 className="font-semibold text-[#2a2a2a] mb-2">Truth</h3>
              <p className="text-sm text-[#8a8580]">
                We believe accurate information is fundamental to a healthy society
              </p>
            </div>
            <div className="card p-8 text-center">
              <Users className="w-8 h-8 text-[#a0573d] mx-auto mb-4" />
              <h3 className="font-semibold text-[#2a2a2a] mb-2">Transparency</h3>
              <p className="text-sm text-[#8a8580]">We explain our findings clearly so you understand our analysis</p>
            </div>
            <div className="card p-8 text-center">
              <Zap className="w-8 h-8 text-[#c9a872] mx-auto mb-4" />
              <h3 className="font-semibold text-[#2a2a2a] mb-2">Innovation</h3>
              <p className="text-sm text-[#8a8580]">
                We stay ahead of deepfake technology with continuous improvements
              </p>
            </div>
          </div>
        </div>

        {/* Ethical Concerns */}
        <div className="mb-16 animate-fade-in">
          <h2 className="text-[#2a2a2a] mb-8 text-center">Ethical Concerns</h2>
          <div className="card p-8">
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-[#2a2a2a] mb-2">Privacy & Security</h3>
                <p className="text-[#5a5555]">
                  Your uploaded videos are processed securely and never stored on our servers. All analysis happens in
                  real-time with no data retention.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-[#2a2a2a] mb-2">Responsible AI</h3>
                <p className="text-[#5a5555]">
                  We recognize the power of our technology and use it only to help identify deepfakes, never to create
                  them. Our research contributes to the broader understanding of synthetic media.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-[#2a2a2a] mb-2">Accuracy & Limitations</h3>
                <p className="text-[#5a5555]">
                  No detection system is 100% accurate. We provide confidence scores and detailed explanations so you
                  can make informed decisions.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Team */}
        <div className="mb-16 animate-fade-in">
          <h2 className="text-[#2a2a2a] mb-8 text-center">Meet the Team</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {[
              { name: "Harsh Kumar", 
                // role: "Founder & CEO", bio: "ML researcher passionate about digital integrity" 
                },
              {
                name: "Ishan Singh",
                // role: "Head of Research",
                // bio: "Computer vision expert with 10+ years experience",
              },
              // { name: "Elena Rodriguez", role: "Head of Ethics", bio: "Policy expert focused on AI responsibility" },
            ].map((member, idx) => (
              <div key={idx} className="card p-6 text-center">
                <div className="w-16 h-16 rounded-full bg-[#f5ede9] mx-auto mb-4 flex items-center justify-center">
                  <span className="text-2xl font-bold text-[#a0573d]">{member.name[0]}</span>
                </div>
                <h3 className="font-semibold text-[#2a2a2a] mb-1">{member.name}</h3>
                <p className="text-sm text-[#a0573d] font-medium mb-2">{member.role}</p>
                <p className="text-sm text-[#8a8580]">{member.bio}</p>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t mt-12" style={{ borderColor: "#e8ddd4", backgroundColor: "white" }}>
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-12 text-center text-sm text-[#8a8580]">
          <p>&copy; 2025 DeepfakeID. All rights reserved. Built with care for truth.</p>
        </div>
      </footer>
    </div>
  )
}
