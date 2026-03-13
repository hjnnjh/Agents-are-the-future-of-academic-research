<template>
  <canvas ref="canvasRef" class="character-canvas" />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const canvasRef = ref<HTMLCanvasElement | null>(null)

const CHARS = ['>', '-', 'o', '.', '*', '+', '~', ':', '|', '/', '=', '#', '@', '%', '^', '&']

let animationId = 0
let lastFrameTime = 0
const FPS_INTERVAL = 1000 / 30

interface Cell {
  char: string
  baseChar: string
}

interface Blob {
  x: number
  y: number
  vx: number
  vy: number
  radius: number
  brightness: number
  phase: number
}

let grid: Cell[][] = []
let cols = 0
let rows = 0
let cellSize = 0
let isRunning = false
let canvasCtx: CanvasRenderingContext2D | null = null
let blobs: Blob[] = []
let canvasW = 0
let canvasH = 0

function getCellSize() {
  const w = window.innerWidth
  if (w < 768) return 14
  if (w < 1024) return 12
  return 10
}

function createBlobs(w: number, h: number): Blob[] {
  const count = Math.max(5, Math.floor((w * h) / 80000))
  const result: Blob[] = []
  for (let i = 0; i < count; i++) {
    result.push({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 80,
      vy: (Math.random() - 0.5) * 60,
      radius: 80 + Math.random() * 180,
      brightness: 0.25 + Math.random() * 0.35,
      phase: Math.random() * Math.PI * 2,
    })
  }
  return result
}

function initGrid() {
  const canvas = canvasRef.value
  if (!canvas) return false

  const rect = canvas.getBoundingClientRect()
  if (rect.width === 0 || rect.height === 0) return false

  cellSize = getCellSize()
  const dpr = window.devicePixelRatio || 1

  canvasW = rect.width
  canvasH = rect.height
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr

  canvasCtx = canvas.getContext('2d')
  if (!canvasCtx) return false
  canvasCtx.setTransform(dpr, 0, 0, dpr, 0, 0)

  cols = Math.ceil(rect.width / cellSize) + 1
  rows = Math.ceil(rect.height / cellSize) + 1

  grid = []
  for (let r = 0; r < rows; r++) {
    const row: Cell[] = []
    for (let c = 0; c < cols; c++) {
      const ch = CHARS[Math.floor(Math.random() * CHARS.length)]
      row.push({ char: ch, baseChar: ch })
    }
    grid.push(row)
  }

  blobs = createBlobs(canvasW, canvasH)
  return true
}

function draw(time: number) {
  if (!isRunning) return
  animationId = requestAnimationFrame(draw)

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  const elapsed = time - lastFrameTime
  if (elapsed < FPS_INTERVAL) return
  lastFrameTime = time - (elapsed % FPS_INTERVAL)

  const ctx = canvasCtx
  if (!ctx) return

  const dt = elapsed / 1000
  ctx.clearRect(0, 0, canvasW, canvasH)

  // Update blob positions
  for (const blob of blobs) {
    blob.x += blob.vx * dt
    blob.y += blob.vy * dt

    // Soft bounce off edges
    if (blob.x < -blob.radius) blob.vx = Math.abs(blob.vx)
    if (blob.x > canvasW + blob.radius) blob.vx = -Math.abs(blob.vx)
    if (blob.y < -blob.radius) blob.vy = Math.abs(blob.vy)
    if (blob.y > canvasH + blob.radius) blob.vy = -Math.abs(blob.vy)

    // Gentle drift variation
    blob.vx += (Math.random() - 0.5) * 2 * dt
    blob.vy += (Math.random() - 0.5) * 2 * dt

    // Clamp speed
    const maxSpeed = 80
    blob.vx = Math.max(-maxSpeed, Math.min(maxSpeed, blob.vx))
    blob.vy = Math.max(-maxSpeed, Math.min(maxSpeed, blob.vy))

    // Pulsing brightness
    blob.phase += dt * 0.5
    blob.brightness = 0.25 + Math.sin(blob.phase) * 0.15
  }

  // Randomly swap a few characters for subtle texture change
  const swapCount = Math.ceil(cols * rows * 0.002)
  for (let i = 0; i < swapCount; i++) {
    const rr = Math.floor(Math.random() * rows)
    const cc = Math.floor(Math.random() * cols)
    if (grid[rr]?.[cc]) {
      grid[rr][cc].char = CHARS[Math.floor(Math.random() * CHARS.length)]
    }
  }

  const fontSize = Math.max(7, Math.floor(cellSize * 0.75))
  ctx.font = `${fontSize}px "Fira Code", "JetBrains Mono", monospace`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'

  // Pre-compute blob squared radii
  const blobData = blobs.map(b => ({
    x: b.x,
    y: b.y,
    rSq: b.radius * b.radius,
    brightness: b.brightness,
  }))

  for (let r = 0; r < rows; r++) {
    const py = r * cellSize + cellSize / 2
    for (let c = 0; c < cols; c++) {
      const cell = grid[r]?.[c]
      if (!cell) continue

      const px = c * cellSize + cellSize / 2

      // Accumulate brightness from all blobs (gaussian-like falloff)
      let totalBright = 0
      for (const b of blobData) {
        const dx = px - b.x
        const dy = py - b.y
        const distSq = dx * dx + dy * dy
        if (distSq < b.rSq * 4) {
          // Gaussian: exp(-distSq / (2 * sigma^2)), sigma = radius/2
          const sigma = Math.sqrt(b.rSq) * 0.5
          const falloff = Math.exp(-distSq / (2 * sigma * sigma))
          totalBright += b.brightness * falloff
        }
      }

      // Base dim level + blob illumination
      const baseOpacity = 0.03
      const opacity = Math.min(0.55, baseOpacity + totalBright)

      if (opacity < 0.02) continue // Skip nearly invisible chars

      // Slight color warmth shift for brighter areas
      const warm = Math.min(1, totalBright * 2)
      const red = Math.floor(75 + warm * 40)
      const green = Math.floor(107 + warm * 20)
      const blue = 251

      ctx.fillStyle = `rgba(${red}, ${green}, ${blue}, ${opacity})`
      ctx.fillText(cell.char, px, py)
    }
  }
}

function onResize() {
  initGrid()
}

function start() {
  if (isRunning) return
  const ok = initGrid()
  if (!ok) {
    requestAnimationFrame(() => start())
    return
  }
  isRunning = true
  animationId = requestAnimationFrame(draw)
}

onMounted(() => {
  window.addEventListener('resize', onResize)
  nextTick(() => {
    requestAnimationFrame(() => start())
  })
})

onUnmounted(() => {
  isRunning = false
  cancelAnimationFrame(animationId)
  window.removeEventListener('resize', onResize)
})
</script>

<style scoped>
.character-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
</style>
