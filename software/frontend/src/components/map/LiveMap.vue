<template>
  <div ref="mapEl" class="live-map">
    <div class="rain-legend">
      <span class="legend-label">Precipitação</span>
      <div class="legend-scale">
        <div class="legend-bar" />
        <div class="legend-ticks">
          <span>0</span><span>10</span><span>25</span><span>50+ mm/h</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { EpdOut, GridPoint } from '@/types/sensor'

const props = defineProps<{
  epds: EpdOut[]
  rainGrid: GridPoint[]
  selectedUid: string | null
}>()

const emit = defineEmits<{ 'select-epd': [uid: string] }>()

const RISK_COLOR: Record<string, string> = {
  SAFE: '#52B788',
  ATTENTION: '#F39C12',
  CRITICAL: '#C0392B',
}
const MAX_RAIN_MM = 50

const mapEl = ref<HTMLDivElement | null>(null)
let mapInstance: L.Map | null = null
let rainCanvas: HTMLCanvasElement | null = null
let rainCtx: CanvasRenderingContext2D | null = null
const markerMap = new Map<string, L.CircleMarker>()

// ── Weather-radar color scale ───────────────────────────────────────────────
// Mirrors INMET / Windy / Weather.com progression: blue → cyan → green → yellow → orange → red → purple
const COLOR_STOPS: [number, [number, number, number]][] = [
  [0.00, [135, 206, 250]],  // sky-blue   — 0 mm (coverage indicator)
  [0.04, [0,   230, 200]],  // teal       — ~2 mm (drizzle)
  [0.12, [0,   210,  50]],  // green      — ~6 mm (light)
  [0.25, [140, 230,   0]],  // lime       — ~12 mm
  [0.40, [255, 210,   0]],  // yellow     — ~20 mm (moderate)
  [0.60, [255, 130,   0]],  // orange     — ~30 mm (heavy)
  [0.80, [220,  20,  20]],  // red        — ~40 mm (very heavy)
  [1.00, [160,   0, 200]],  // purple     — 50+ mm (extreme)
]

function rainRGB(intensity: number): [number, number, number] {
  for (let i = 1; i < COLOR_STOPS.length; i++) {
    const [t0, c0] = COLOR_STOPS[i - 1]
    const [t1, c1] = COLOR_STOPS[i]
    if (intensity <= t1) {
      const t = (intensity - t0) / (t1 - t0)
      return [
        Math.round(c0[0] + t * (c1[0] - c0[0])),
        Math.round(c0[1] + t * (c1[1] - c0[1])),
        Math.round(c0[2] + t * (c1[2] - c0[2])),
      ]
    }
  }
  return COLOR_STOPS[COLOR_STOPS.length - 1][1]
}

// ── Rain canvas ─────────────────────────────────────────────────────────────

function setupRainCanvas(container: HTMLElement) {
  rainCanvas = document.createElement('canvas')
  Object.assign(rainCanvas.style, {
    position:      'absolute',
    top:           '0',
    left:          '0',
    pointerEvents: 'none',
    zIndex:        '400',
    // CSS blur creates the smooth, cloud-like blending between adjacent grid cells
    filter:        'blur(22px) saturate(1.15)',
    mixBlendMode:  'multiply',
  })
  container.appendChild(rainCanvas)
  rainCtx = rainCanvas.getContext('2d')
}

function drawRain(grid: GridPoint[]) {
  if (!mapInstance || !rainCanvas || !rainCtx) return

  const container = mapInstance.getContainer()
  const w = container.offsetWidth
  const h = container.offsetHeight
  const dpr = window.devicePixelRatio || 1

  rainCanvas.width  = w * dpr
  rainCanvas.height = h * dpr
  rainCanvas.style.width  = w + 'px'
  rainCanvas.style.height = h + 'px'

  const ctx = rainCtx
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, w, h)

  if (!grid.length) return

  // Radius in pixels = map distance between adjacent grid points × scale factor
  // The overlap (>1.0) lets adjacent cells blend seamlessly
  const p0 = mapInstance.latLngToContainerPoint(L.latLng(-20.7546, -42.8825))
  const p1 = mapInstance.latLngToContainerPoint(L.latLng(-20.7546, -42.8325))
  const pxPerStep = Math.abs(p1.x - p0.x)
  const radius = pxPerStep * 1.05

  for (const point of grid) {
    const p = mapInstance.latLngToContainerPoint(L.latLng(point.lat, point.lng))
    const intensity = Math.min(point.rainfall_mm / MAX_RAIN_MM, 1)
    const [r, g, b] = rainRGB(intensity)

    // 0 mm still renders faintly so the grid is always visible on the map
    const centerAlpha = intensity < 0.02 ? 0.22 : 0.18 + intensity * 0.72

    const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius)
    grad.addColorStop(0,    `rgba(${r},${g},${b},${centerAlpha})`)
    grad.addColorStop(0.55, `rgba(${r},${g},${b},${centerAlpha * 0.45})`)
    grad.addColorStop(1,    `rgba(${r},${g},${b},0)`)

    ctx.fillStyle = grad
    ctx.beginPath()
    ctx.arc(p.x, p.y, radius, 0, Math.PI * 2)
    ctx.fill()
  }

  // Keep EPD markers visually on top
  for (const m of markerMap.values()) m.bringToFront()
}

// ── EPD markers ─────────────────────────────────────────────────────────────

function buildCircleMarker(epd: EpdOut): L.CircleMarker {
  const lat = epd.lat ?? -20.7546
  const lng = epd.lng ?? -42.8825
  const risk = epd.latest?.risk_level ?? 'SAFE'
  const moisture = epd.latest?.soil_moisture ?? 0
  const isSelected = epd.epd_uid === props.selectedUid

  const marker = L.circleMarker([lat, lng], {
    radius:      isSelected ? 14 : 10,
    fillColor:   RISK_COLOR[risk] ?? '#52B788',
    color:       '#fff',
    weight:      isSelected ? 3 : 2,
    opacity:     1,
    fillOpacity: 0.95,
    // Use a higher z-index pane so markers stay above rain canvas
    pane: 'markerPane',
  })

  const tooltipHtml = `
    <div style="font-family:sans-serif;font-size:12px;line-height:1.5">
      <b style="font-size:13px">${epd.epd_uid}</b>
      ${epd.label ? `<br><span style="color:#888">${epd.label}</span>` : ''}
      <br>🌱 Umidade: <b>${moisture.toFixed(1)}%</b>
    </div>`
  marker.bindTooltip(tooltipHtml, { sticky: true, offset: [0, -8] })
  marker.on('click', () => emit('select-epd', epd.epd_uid))
  return marker
}

function updateMarkers(epds: EpdOut[]) {
  if (!mapInstance) return

  const currentUids = new Set(epds.map((e) => e.epd_uid))
  for (const [uid, m] of markerMap) {
    if (!currentUids.has(uid)) { m.remove(); markerMap.delete(uid) }
  }

  for (const epd of epds) {
    if (epd.lat == null || epd.lng == null) continue
    const existing = markerMap.get(epd.epd_uid)
    if (existing) { existing.remove(); markerMap.delete(epd.epd_uid) }
    markerMap.set(epd.epd_uid, buildCircleMarker(epd).addTo(mapInstance))
  }
}

// ── Lifecycle ────────────────────────────────────────────────────────────────

onMounted(() => {
  if (!mapEl.value) return

  mapInstance = L.map(mapEl.value, {
    center: [-20.7546, -42.8825],
    zoom: 14,
    zoomControl: false,
  })

  // Custom zoom position
  L.control.zoom({ position: 'bottomright' }).addTo(mapInstance)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(mapInstance)

  setupRainCanvas(mapEl.value)

  // Redraw rain canvas on every map movement so it stays aligned
  mapInstance.on('move zoom moveend zoomend', () => drawRain(props.rainGrid))

  updateMarkers(props.epds)
  drawRain(props.rainGrid)
})

onUnmounted(() => {
  mapInstance?.remove()
  mapInstance = null
})

watch([() => props.epds, () => props.selectedUid], () => updateMarkers(props.epds), { deep: true })

watch(() => props.rainGrid, (grid) => drawRain(grid), { deep: true })

watch(
  () => props.selectedUid,
  (uid) => {
    if (!uid || !mapInstance) return
    const epd = props.epds.find((e) => e.epd_uid === uid)
    if (epd?.lat != null && epd.lng != null) {
      mapInstance.panTo([epd.lat, epd.lng], { animate: true, duration: 0.5 })
    }
  },
)
</script>

<style scoped>
.live-map {
  width: 100%;
  height: 100%;
  min-height: 300px;
  position: relative;
}

/* ── Rain legend ────────────────────────────────── */
.rain-legend {
  position: absolute;
  bottom: 40px;
  left: 12px;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(8px);
  border-radius: 10px;
  padding: 8px 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,.12);
  display: flex;
  flex-direction: column;
  gap: 4px;
  pointer-events: none;
}

.legend-label {
  font-size: 10px;
  font-weight: 700;
  color: #555;
  letter-spacing: .06em;
  text-transform: uppercase;
}

.legend-scale {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.legend-bar {
  width: 140px;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(
    to right,
    rgba(135,206,250,.6),
    rgba(0,230,200,.75),
    rgba(0,210,50,.8),
    rgba(255,210,0,.85),
    rgba(255,130,0,.9),
    rgba(220,20,20,.95),
    rgba(160,0,200,1)
  );
}

.legend-ticks {
  display: flex;
  justify-content: space-between;
  font-size: 9px;
  color: #777;
  width: 140px;
}
</style>
