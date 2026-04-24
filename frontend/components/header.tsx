"use client"

import Link from "next/link"
import { useState } from "react"
import { Menu, X } from "lucide-react"

export default function Header() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <header
      className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b transition-smooth"
      style={{ borderColor: "#e8ddd4" }}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#a0573d] to-[#8a4a31] flex items-center justify-center group-hover:shadow-md transition-smooth">
              <span className="text-white font-bold text-lg">D</span>
            </div>
            <span className="font-bold text-xl text-[#2a2a2a]">DeepfakeID</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <Link href="/" className="text-[#5a5555] hover:text-[#a0573d] transition-smooth text-sm font-medium">
              Home
            </Link>
            <Link href="/analyze" className="text-[#5a5555] hover:text-[#a0573d] transition-smooth text-sm font-medium">
              Analyze
            </Link>
            <Link
              href="/research"
              className="text-[#5a5555] hover:text-[#a0573d] transition-smooth text-sm font-medium"
            >
              Research
            </Link>
            <Link href="/about" className="text-[#5a5555] hover:text-[#a0573d] transition-smooth text-sm font-medium">
              About
            </Link>
            <Link href="/analyze" className="btn btn-primary btn-md">
              Get Started
            </Link>
          </nav>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 hover:bg-[#f5ede9] rounded-lg transition-smooth"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X className="w-6 h-6 text-[#2a2a2a]" /> : <Menu className="w-6 h-6 text-[#2a2a2a]" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden pb-4 border-t animate-slide-up" style={{ borderColor: "#e8ddd4" }}>
            <nav className="flex flex-col gap-3 pt-4">
              <Link href="/" className="px-4 py-2 hover:bg-[#f5ede9] rounded-lg transition-smooth text-[#5a5555]">
                Home
              </Link>
              <Link
                href="/analyze"
                className="px-4 py-2 hover:bg-[#f5ede9] rounded-lg transition-smooth text-[#5a5555]"
              >
                Analyze
              </Link>
              <Link
                href="/research"
                className="px-4 py-2 hover:bg-[#f5ede9] rounded-lg transition-smooth text-[#5a5555]"
              >
                Research
              </Link>
              <Link href="/about" className="px-4 py-2 hover:bg-[#f5ede9] rounded-lg transition-smooth text-[#5a5555]">
                About
              </Link>
              <Link href="/analyze" className="btn btn-primary btn-md mx-4">
                Get Started
              </Link>
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}
