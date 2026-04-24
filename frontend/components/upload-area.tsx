"use client"

import type React from "react"
import { useState } from "react"
import { Upload } from "lucide-react"

interface UploadAreaProps {
  onUpload?: (file: File) => void
}

export default function UploadArea({ onUpload }: UploadAreaProps) {
  const [isDragging, setIsDragging] = useState(false)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) {
      onUpload?.(files[0])
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files
    if (files && files.length > 0) {
      onUpload?.(files[0])
    }
  }

  return (
    <label
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`card p-8 md:p-12 text-center cursor-pointer transition-smooth block border-2 ${
        isDragging ? "border-[#a0573d] bg-[#f5ede9]" : "border-[#e8ddd4] hover:border-[#c9a872]"
      } ${isDragging ? "glow" : ""}`}
    >
      <div className="flex flex-col items-center gap-4">
        <div className="w-16 h-16 rounded-full bg-[#f5ede9] flex items-center justify-center">
          <Upload className="w-8 h-8 text-[#a0573d]" />
        </div>
        <div>
          <h3 className="text-xl font-semibold text-[#2a2a2a] mb-2">Drop your video here</h3>
          <p className="text-[#8a8580]">or click to browse your files</p>
        </div>
        <p className="text-sm text-[#8a8580] mt-4">Supported formats: MP4, WebM, MOV • Max size: 500MB</p>
      </div>
      {/* Hidden file input */}
      <input type="file" accept="video/*" onChange={handleInputChange} className="hidden" />
    </label>
  )
}
