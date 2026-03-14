<template>
  <canvas ref="canvasRef" class="character-canvas" />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const canvasRef = ref<HTMLCanvasElement | null>(null)

const CHARS = ['o', '>', '_']

let animationId = 0
let lastFrameTime = 0
const FPS_INTERVAL = 1000 / 30

let cols = 0
let rows = 0
let cellW = 0
let cellH = 0
let isRunning = false
let canvasCtx: CanvasRenderingContext2D | null = null
let canvasW = 0
let canvasH = 0
let baseScrollOffset = 0
let mouseX = -9999
let mouseY = -9999

// Per-row scroll speed multipliers for staggered motion
let rowSpeedFactors: number[] = []

// Brightness map — each cell has a brightness value that decays over time
let brightnessMap: Float32Array = new Float32Array(0)

// Pre-generated character rows with consecutive runs
let charRows: string[][] = []

function getCellSize() {
  const w = window.innerWidth
  if (w < 768) return { w: 10, h: 13 }
  if (w < 1024) return { w: 9, h: 12 }
  return { w: 8, h: 11 }
}

function generateRow(length: number): string[] {
  const row: string[] = []
  let i = 0
  while (i < length) {
    const char = CHARS[Math.floor(Math.random() * CHARS.length)]
    const runLen = 3 + Math.floor(Math.random() * 6) // 3-8 consecutive
    for (let j = 0; j < runLen && i < length; j++, i++) {
      row.push(char)
    }
  }
  return row
}

function initGrid() {
  const canvas = canvasRef.value
  if (!canvas) return false

  const rect = canvas.getBoundingClientRect()
  if (rect.width === 0 || rect.height === 0) return false

  const size = getCellSize()
  cellW = size.w
  cellH = size.h
  const dpr = window.devicePixelRatio || 1

  canvasW = rect.width
  canvasH = rect.height
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr

  canvasCtx = canvas.getContext('2d')
  if (!canvasCtx) return false
  canvasCtx.setTransform(dpr, 0, 0, dpr, 0, 0)

  cols = Math.ceil(canvasW / cellW) + 2
  rows = Math.ceil(canvasH / cellH) + 1

  // Initialize brightness map (all dark)
  brightnessMap = new Float32Array(rows * cols)

  // Generate per-row staggered speed factors (0.5x — 1.5x base speed)
  rowSpeedFactors = []
  for (let r = 0; r < rows; r++) {
    rowSpeedFactors.push(0.5 + Math.random())
  }

  // Generate wide rows for seamless scrolling (3x screen width)
  charRows = []
  const totalCols = cols * 3
  for (let r = 0; r < rows; r++) {
    charRows.push(generateRow(totalCols))
  }

  baseScrollOffset = 0
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

  // Advance base scroll (slow drift)
  baseScrollOffset += 12 * dt

  // Get canvas position in viewport for mouse mapping
  const canvas = canvasRef.value
  if (!canvas) return
  const canvasRect = canvas.getBoundingClientRect()

  // Mouse position relative to canvas
  const mx = mouseX - canvasRect.left
  const my = mouseY - canvasRect.top

  // --- Update brightness map ---
  const brushRadius = 120
  const brushRadiusSq = brushRadius * brushRadius
  const decayRate = 1.8

  // Decay all cells
  for (let i = 0; i < brightnessMap.length; i++) {
    if (brightnessMap[i] > 0) {
      brightnessMap[i] = Math.max(0, brightnessMap[i] - decayRate * dt)
    }
  }

  // Paint brightness around current mouse position
  if (mx > -brushRadius && mx < canvasW + brushRadius && my > -brushRadius && my < canvasH + brushRadius) {
    const rStart = Math.max(0, Math.floor((my - brushRadius) / cellH))
    const rEnd = Math.min(rows, Math.ceil((my + brushRadius) / cellH))
    const cStart = Math.max(0, Math.floor((mx - brushRadius) / cellW))
    const cEnd = Math.min(cols, Math.ceil((mx + brushRadius) / cellW))

    for (let r = rStart; r < rEnd; r++) {
      const py = r * cellH + cellH / 2
      for (let c = cStart; c < cEnd; c++) {
        const px = c * cellW + cellW / 2
        const dx = px - mx
        const dy = py - my
        const distSq = dx * dx + dy * dy

        if (distSq < brushRadiusSq) {
          const dist = Math.sqrt(distSq)
          const t = 1 - dist / brushRadius
          const paintStrength = t * t
          const idx = r * cols + c
          brightnessMap[idx] = Math.min(1, Math.max(brightnessMap[idx], paintStrength))
        }
      }
    }
  }

  ctx.clearRect(0, 0, canvasW, canvasH)

  // Detect dark mode
  const isDark = document.documentElement.classList.contains('dark')

  const fontSize = Math.max(9, Math.floor(cellH * 0.85))
  ctx.font = `${fontSize}px "Source Code Pro", "Fira Code", "JetBrains Mono", monospace`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'

  // Wave time
  const waveTime = time * 0.001

  // Wrap width for seamless scrolling
  const rowLen = charRows[0]?.length || 1
  const wrapCols = Math.floor(rowLen / 3)
  const wrapWidth = wrapCols * cellW

  for (let r = 0; r < rows; r++) {
    const py = r * cellH + cellH / 2
    const row = charRows[r]
    if (!row) continue

    // Per-row staggered scroll offset
    const rowScroll = baseScrollOffset * (rowSpeedFactors[r] || 1)
    const wrappedScroll = wrapWidth > 0 ? rowScroll % wrapWidth : 0
    const colOffset = Math.floor(wrappedScroll / cellW)
    const subPixelOffset = wrappedScroll % cellW

    for (let c = 0; c < cols; c++) {
      const idx = r * cols + c
      const brightness = brightnessMap[idx]

      if (brightness < 0.01) continue

      const px = c * cellW + cellW / 2 - subPixelOffset

      if (px < -cellW || px > canvasW + cellW) continue

      // Wave modulation
      const wave = Math.sin(px * 0.02 + waveTime * 1.5) * 0.3
            + Math.sin(py * 0.015 + waveTime * 0.8) * 0.2
      const waveOffset = wave * cellH * 0.35

      const waveBoost = 0.5 + wave * 0.25
      const opacity = brightness * waveBoost * 0.7

      if (opacity < 0.01) continue

      const charIdx = ((c + colOffset) % row.length + row.length) % row.length
      const char = row[charIdx]

      if (isDark) {
        ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`
      } else {
        ctx.fillStyle = `rgba(0, 0, 0, ${opacity})`
      }

      ctx.fillText(char, px, py + waveOffset)
    }
  }
}

function onMouseMove(e: MouseEvent) {
  mouseX = e.clientX
  mouseY = e.clientY
}

function onMouseLeave() {
  mouseX = -9999
  mouseY = -9999
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
  window.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseleave', onMouseLeave)
  nextTick(() => {
    requestAnimationFrame(() => start())
  })
})

onUnmounted(() => {
  isRunning = false
  cancelAnimationFrame(animationId)
  window.removeEventListener('resize', onResize)
  window.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseleave', onMouseLeave)
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
