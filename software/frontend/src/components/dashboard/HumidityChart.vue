<template>
  <div class="chart-wrap">
    <canvas ref="canvasEl" class="chart-canvas" />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

const props = defineProps<{ data: number[] }>()

const canvasEl = ref<HTMLCanvasElement | null>(null)

function draw(readings: number[]) {
  const canvas = canvasEl.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const dpr = window.devicePixelRatio || 1
  const rect = canvas.getBoundingClientRect()
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr
  ctx.scale(dpr, dpr)

  const W = rect.width
  const H = rect.height
  ctx.clearRect(0, 0, W, H)

  if (readings.length < 2) return

  const min = 0
  const max = 100
  const pts = readings.map((v, i) => ({
    x: (i / (readings.length - 1)) * W,
    y: H - ((v - min) / (max - min)) * H,
  }))

  const avg = readings.reduce((a, b) => a + b, 0) / readings.length
  let strokeColor = '#6E8B43'
  if (avg >= 80) strokeColor = '#C0392B'
  else if (avg >= 60) strokeColor = '#F39C12'

  // gradient fill
  const grad = ctx.createLinearGradient(0, 0, 0, H)
  grad.addColorStop(0, strokeColor + '55')
  grad.addColorStop(1, strokeColor + '00')

  ctx.beginPath()
  ctx.moveTo(pts[0].x, pts[0].y)
  for (let i = 1; i < pts.length; i++) {
    const cp = { x: (pts[i - 1].x + pts[i].x) / 2, y: (pts[i - 1].y + pts[i].y) / 2 }
    ctx.quadraticCurveTo(pts[i - 1].x, pts[i - 1].y, cp.x, cp.y)
  }
  ctx.quadraticCurveTo(pts[pts.length - 2].x, pts[pts.length - 2].y, pts[pts.length - 1].x, pts[pts.length - 1].y)

  // fill
  ctx.lineTo(W, H)
  ctx.lineTo(0, H)
  ctx.closePath()
  ctx.fillStyle = grad
  ctx.fill()

  // stroke
  ctx.beginPath()
  ctx.moveTo(pts[0].x, pts[0].y)
  for (let i = 1; i < pts.length; i++) {
    const cp = { x: (pts[i - 1].x + pts[i].x) / 2, y: (pts[i - 1].y + pts[i].y) / 2 }
    ctx.quadraticCurveTo(pts[i - 1].x, pts[i - 1].y, cp.x, cp.y)
  }
  ctx.quadraticCurveTo(pts[pts.length - 2].x, pts[pts.length - 2].y, pts[pts.length - 1].x, pts[pts.length - 1].y)
  ctx.strokeStyle = strokeColor
  ctx.lineWidth = 2
  ctx.stroke()
}

onMounted(() => draw(props.data))
watch(() => props.data, (v) => draw(v))
</script>

<style scoped>
.chart-wrap {
  background: var(--white);
  border-radius: var(--r-md);
  padding: 16px;
  box-shadow: var(--shadow-sm);
}

.chart-canvas {
  width: 100%;
  height: 80px;
  display: block;
}
</style>
