import Link from "next/link"

export default function Footer() {
  return (
    <footer className="border-t mt-16 transition-smooth" style={{ borderColor: "#e8ddd4", backgroundColor: "white" }}>
      <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-8 md:grid-cols-4 mb-8">
          {/* Brand */}
          <div>
            <h3 className="text-lg font-bold text-[#a0573d] mb-4">DeepfakeID</h3>
            <p className="text-sm text-[#8a8580]">AI-powered deepfake detection technology for the modern web.</p>
          </div>

          {/* Product */}
          <div>
            <h4 className="font-semibold text-[#2a2a2a] mb-4">Product</h4>
            <nav className="space-y-2">
              <Link href="/" className="block text-sm text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                Home
              </Link>
              <Link href="/analyze" className="block text-sm text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                Analyze
              </Link>
              <Link href="/research" className="block text-sm text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                Research
              </Link>
            </nav>
          </div>

          {/* Company */}
          <div>
            <h4 className="font-semibold text-[#2a2a2a] mb-4">Company</h4>
            <nav className="space-y-2">
              <Link href="/about" className="block text-sm text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                About
              </Link>
              <a href="#" className="block text-sm text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                Blog
              </a>
              <a href="#" className="block text-sm text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                Contact
              </a>
            </nav>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-semibold text-[#2a2a2a] mb-4">Legal</h4>
            <nav className="space-y-2">
              <a href="#" className="block text-sm text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                Privacy
              </a>
              <a href="#" className="block text-sm text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                Terms
              </a>
              <a href="#" className="block text-sm text-[#8a8580] hover:text-[#a0573d] transition-smooth">
                Security
              </a>
            </nav>
          </div>
        </div>

        <div className="my-8 border-t transition-smooth" style={{ borderColor: "#e8ddd4" }} />

        <div className="flex flex-col md:flex-row items-center justify-between text-sm text-[#8a8580] gap-4">
          <p>&copy; 2025 DeepfakeID. All rights reserved.</p>
          <div className="flex gap-6">
            <a href="#" className="hover:text-[#a0573d] transition-smooth">
              Twitter
            </a>
            <a href="#" className="hover:text-[#a0573d] transition-smooth">
              GitHub
            </a>
            <a href="#" className="hover:text-[#a0573d] transition-smooth">
              LinkedIn
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
