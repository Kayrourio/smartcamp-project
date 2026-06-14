<template>
  <div class="chart-wrap">
    <div class="chart-header">
      <span class="chart-title">Umidade do solo</span>
      <span class="chart-window">últimos 30 min</span>
    </div>
    <canvas ref="canvasEl" class="chart-canvas" />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

const props = defineProps<{
  data: number[]
  labels?: string[]
}>()

const canvasEl = ref<HTMLCanvasElement | null>(null)

function draw(readings: number[], labels: string[] = []) {
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
  const LABEL_H = labels.length ? 20 : 0
  const chartH = H - LABEL_H

  ctx.clearRect(0, 0, W, H)
  if (readings.length < 2) return

  const min = 0
  const max = 100
  const pts = readings.map((v, i) => ({
    x: (i / (readings.length - 1)) * W,
    y: chartH - ((v - min) / (max - min)) * chartH,
  }))

  const avg = readings.reduce((a, b) => a + b, 0) / readings.length
  let strokeColor = '#6E8B43'
  if (avg >= 80) strokeColor = '#C0392B'
  else if (avg >= 60) strokeColor = '#F39C12'

  // gradient fill
  const grad = ctx.createLinearGradient(0, 0, 0, chartH)
  grad.addColorStop(0, strokeColor + '55')
  grad.addColorStop(1, strokeColor + '00')

  // draw curve path helper
  function drawCurve() {
    if (!ctx) return
    ctx.beginPath()
    ctx.moveTo(pts[0].x, pts[0].y)
    for (let i = 1; i < pts.length; i++) {
      const cp = { x: (pts[i - 1].x + pts[i].x) / 2, y: (pts[i - 1].y + pts[i].y) / 2 }
      ctx.quadraticCurveTo(pts[i - 1].x, pts[i - 1].y, cp.x, cp.y)
    }
    ctx.quadraticCurveTo(pts[pts.length - 2].x, pts[pts.length - 2].y, pts[pts.length - 1].x, pts[pts.length - 1].y)
  }

  drawCurve()
  ctx.lineTo(W, chartH)
  ctx.lineTo(0, chartH)
  ctx.closePath()
  ctx.fillStyle = grad
  ctx.fill()

  drawCurve()
  ctx.strokeStyle = strokeColor
  ctx.lineWidth = 2
  ctx.stroke()

  // horizontal grid line at 60% and 80%
  ctx.setLineDash([3, 4])
  ctx.lineWidth = 1
  for (const threshold of [60, 80]) {
    const y = chartH - (threshold / max) * chartH
    ctx.strokeStyle = threshold >= 80 ? 'rgba(192,57,43,.2)' : 'rgba(243,156,18,.2)'
    ctx.beginPath()
    ctx.moveTo(0, y)
    ctx.lineTo(W, y)
    ctx.stroke()
  }
  ctx.setLineDash([])

  // time labels — show first, middle, last
  if (labels.length >= 2) {
    ctx.fillStyle = '#999'
    ctx.font = `${10 * Math.min(dpr, 1.5)}px sans-serif`
    const indices = [0, Math.floor((labels.length - 1) / 2), labels.length - 1]
    const aligns: CanvasTextAlign[] = ['left', 'center', 'right']
    indices.forEach((idx, i) => {
      if (!ctx) return
      ctx.textAlign = aligns[i]
      ctx.fillText(labels[idx], pts[idx].x, H - 4)
    })
  }
}

onMounted(() => draw(props.data, props.labels))
watch([() => props.data, () => props.labels], ([d, l]) => draw(d, l ?? []))
</script>

<style scoped>
.chart-wrap {
  background: var(--white);
  border-radius: var(--r-md);
  padding: 12px 14px;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chart-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.chart-title {
  font-family: var(--font-head);
  font-size: 11px;
  font-weight: 700;
  color: var(--ink-soft);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.chart-window {
  font-size: 10px;
  color: var(--ink-faint);
}

.chart-canvas {
  width: 100%;
  height: 90px;
  display: block;
}
</style>
