"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { motion } from "framer-motion"

interface UploadCardProps {
  icon: React.ReactNode
  title: string
  description: string
  type: "file" | "url"
}

export default function UploadCard({ icon, title, description, type }: UploadCardProps) {
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
  }

  return (
    <motion.div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      whileHover={{ y: -4, boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)" }}
      transition={{ type: "spring", stiffness: 400, damping: 10 }}
      className={`rounded-2xl border-2 border-dashed p-12 text-center cursor-pointer transition-all ${
        isDragging
          ? "border-primary bg-primary/10 scale-105 glow-border"
          : "border-border bg-card hover:border-primary/50"
      }`}
    >
      <motion.div
        className="mb-4 flex justify-center text-primary"
        animate={isDragging ? { scale: 1.2 } : { scale: 1 }}
        transition={{ duration: 0.2 }}
      >
        {icon}
      </motion.div>
      <h3 className="mb-2 font-semibold text-foreground text-lg">{title}</h3>
      <p className="mb-6 text-sm text-muted-foreground">{description}</p>
      <Button variant="default" size="lg" className="rounded-full px-6 h-10">
        {type === "file" ? "Choose File" : "Enter URL"}
      </Button>
    </motion.div>
  )
}
