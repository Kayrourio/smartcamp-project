<template>
  <div ref="mapEl" class="live-map">
    <!-- Locate-me button -->
    <button
      class="locate-btn"
      :class="{ 'locate-btn--active': userPos !== null }"
      :title="userPos ? 'Ir para minha localização' : 'Buscando localização…'"
      @click="flyToUser"
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="3"/>
        <path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>
        <path d="M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2z" stroke-opacity=".25"/>
      </svg>
    </button>

    <!-- Rain legend -->
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
  ATTENTION: '#F1C40F',
  HIGH: '#E67E22',
  CRITICAL: '#C0392B',
}
// Concentric gradient stops per risk level (center → edge), like a weather radar heat map
const RISK_GRADIENT: Record<string, { stop: number; r: number; g: number; b: number; a: number }[]> = {
  CRITICAL: [
    { stop: 0.00, r: 192, g:  57, b:  43, a: 0.90 },  // red
    { stop: 0.30, r: 230, g: 126, b:  34, a: 0.60 },  // orange
    { stop: 0.55, r: 241, g: 196, b:  15, a: 0.35 },  // yellow
    { stop: 0.78, r:  82, g: 183, b: 136, a: 0.15 },  // green
    { stop: 1.00, r:  82, g: 183, b: 136, a: 0.00 },
  ],
  HIGH: [
    { stop: 0.00, r: 230, g: 126, b:  34, a: 0.85 },  // orange
    { stop: 0.40, r: 241, g: 196, b:  15, a: 0.45 },  // yellow
    { stop: 0.72, r:  82, g: 183, b: 136, a: 0.18 },  // green
    { stop: 1.00, r:  82, g: 183, b: 136, a: 0.00 },
  ],
  ATTENTION: [
    { stop: 0.00, r: 241, g: 196, b:  15, a: 0.80 },  // yellow
    { stop: 0.55, r:  82, g: 183, b: 136, a: 0.25 },  // green
    { stop: 1.00, r:  82, g: 183, b: 136, a: 0.00 },
  ],
  SAFE: [
    { stop: 0.00, r:  82, g: 183, b: 136, a: 0.70 },  // green
    { stop: 1.00, r:  82, g: 183, b: 136, a: 0.00 },
  ],
}
const MAX_RAIN_MM = 50

const mapEl = ref<HTMLDivElement | null>(null)
let mapInstance: L.Map | null = null
let heatCanvas: HTMLCanvasElement | null = null
let heatCtx: CanvasRenderingContext2D | null = null
let rainCanvas: HTMLCanvasElement | null = null
let rainCtx: CanvasRenderingContext2D | null = null
const markerMap = new Map<string, L.Marker>()
let userMarker: L.CircleMarker | null = null
let watchId: number | null = null
const userPos = ref<[number, number] | null>(null)

// ── Weather-radar color scale ───────────────────────────────────────────────
// Mirrors INMET / Windy / Weather.com progression: blue → cyan → green → yellow → orange → red → purple
const COLOR_STOPS: [number, [number, number, number]][] = [
  [0.00, [135, 206, 250]],  // sky-blue  ,0 mm (coverage indicator)
  [0.04, [0,   230, 200]],  // teal      ,~2 mm (drizzle)
  [0.12, [0,   210,  50]],  // green     ,~6 mm (light)
  [0.25, [140, 230,   0]],  // lime      ,~12 mm
  [0.40, [255, 210,   0]],  // yellow    ,~20 mm (moderate)
  [0.60, [255, 130,   0]],  // orange    ,~30 mm (heavy)
  [0.80, [220,  20,  20]],  // red       ,~40 mm (very heavy)
  [1.00, [160,   0, 200]],  // purple    ,50+ mm (extreme)
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

// ── Soil-moisture heat map ──────────────────────────────────────────────────

function setupHeatCanvas(map: L.Map) {
  heatCanvas = document.createElement('canvas')
  Object.assign(heatCanvas.style, {
    position:      'absolute',
    top:           '0',
    left:          '0',
    pointerEvents: 'none',
    zIndex:        '299',
    filter:        'blur(20px) saturate(1.4)',
  })
  const mapPane = map.getPanes().mapPane
  map.getContainer().insertBefore(heatCanvas, mapPane)
  heatCtx = heatCanvas.getContext('2d')
}

function drawHeat(epds: EpdOut[]) {
  if (!mapInstance || !heatCanvas || !heatCtx) return

  const container = mapInstance.getContainer()
  const w = container.offsetWidth
  const h = container.offsetHeight
  const dpr = window.devicePixelRatio || 1

  heatCanvas.width  = w * dpr
  heatCanvas.height = h * dpr
  heatCanvas.style.width  = w + 'px'
  heatCanvas.style.height = h + 'px'

  const ctx = heatCtx
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, w, h)

  const valid = epds.filter((e) => e.lat != null && e.lng != null && e.latest)
  if (!valid.length) return

  // Convert 50 m to pixels at the current zoom/latitude of the first valid sensor
  const refLat = valid[0].lat!
  const refLng = valid[0].lng!
  const refPx = mapInstance.latLngToContainerPoint(L.latLng(refLat, refLng))
  const offPx = mapInstance.latLngToContainerPoint(L.latLng(refLat + 50 / 111_320, refLng))
  const radius = Math.max(Math.abs(offPx.y - refPx.y), 8) // at least 8 px so it's always visible

  for (const epd of valid) {
    const p = mapInstance.latLngToContainerPoint(L.latLng(epd.lat!, epd.lng!))
    const stops = RISK_GRADIENT[epd.latest!.risk_level] ?? RISK_GRADIENT.SAFE

    const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius)
    for (const s of stops) {
      grad.addColorStop(s.stop, `rgba(${s.r},${s.g},${s.b},${s.a})`)
    }

    ctx.fillStyle = grad
    ctx.beginPath()
    ctx.arc(p.x, p.y, radius, 0, Math.PI * 2)
    ctx.fill()
  }
}

// ── Rain canvas ─────────────────────────────────────────────────────────────

function setupRainCanvas(map: L.Map) {
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
  // Insert BEFORE the Leaflet map pane so its markers (z-index 600 inside the pane)
  // remain on top even though canvas and pane share z-index 400 (DOM order breaks the tie)
  const mapPane = map.getPanes().mapPane
  map.getContainer().insertBefore(rainCanvas, mapPane)
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
  for (const m of markerMap.values()) m.setZIndexOffset(1000)
}

// ── EPD markers ─────────────────────────────────────────────────────────────

function buildPinIcon(color: string, isSelected: boolean, isTilted = false, isLandslide = false): L.DivIcon {
  const size = isSelected ? 44 : 36
  const ring = isSelected ? `<circle cx="22" cy="22" r="21" fill="${color}" opacity="0.18"/>` : ''
  const strokeW = isSelected ? 3 : 2.5
  // When sensor is tilted/fallen, rotate the inner body 90° around the icon center so it appears lying on its side
  const sensorTransform = isTilted ? 'rotate(90, 22, 22) translate(10, 6)' : 'translate(10, 6)'
  const badgeColor = isLandslide ? '#C0392B' : '#E67E22'
  const tiltBadge = isTilted
    ? `<circle cx="33" cy="11" r="7" fill="${badgeColor}" stroke="white" stroke-width="1.5"/>
       <text x="33" y="15" text-anchor="middle" font-size="9" font-weight="bold" fill="white">!</text>`
    : ''
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 44 44">
    ${ring}
    <circle cx="22" cy="22" r="18" fill="white" stroke="${color}" stroke-width="${strokeW}"/>
    <g transform="${sensorTransform}">
      <rect x="9" y="2" width="6" height="12" rx="3" stroke="${color}" stroke-width="1.8" fill="none"/>
      <line x1="12" y1="14" x2="12" y2="22" stroke="${color}" stroke-width="1.8" stroke-linecap="round"/>
      <line x1="8" y1="22" x2="16" y2="22" stroke="${color}" stroke-width="1.8" stroke-linecap="round"/>
      <circle cx="12" cy="8" r="2" fill="${color}"/>
    </g>
    ${tiltBadge}
  </svg>`
  const wrapClass = [
    'epd-pin-wrap',
    isSelected ? 'epd-pin-wrap--selected' : '',
    isLandslide ? 'epd-pin-wrap--landslide' : '',
  ].filter(Boolean).join(' ')
  return L.divIcon({
    html: `<div class="${wrapClass}">${svg}</div>`,
    className: '',
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    tooltipAnchor: [0, -(size / 2 + 4)],
    popupAnchor: [0, -(size / 2 + 4)],
  })
}

function buildMarker(epd: EpdOut): L.Marker {
  const lat = epd.lat!
  const lng = epd.lng!
  const risk = epd.latest?.risk_level ?? 'SAFE'
  const moisture = epd.latest?.soil_moisture ?? 0
  const tiltDetected = epd.latest?.tilt_detected ?? false
  const angleX = epd.latest?.angle_x ?? null
  const isSelected = epd.epd_uid === props.selectedUid
  const isLandslide = tiltDetected && risk === 'CRITICAL'

  const marker = L.marker([lat, lng], {
    icon: buildPinIcon(RISK_COLOR[risk] ?? '#52B788', isSelected, tiltDetected, isLandslide),
    pane: 'markerPane',
    zIndexOffset: isSelected ? 1000 : 0,
  })

  const angleRow = angleX !== null
    ? `<br>📐 X: <b>${angleX.toFixed(1)}°</b>`
    : ''
  const statusRow = isLandslide
    ? `<br><span style="color:#C0392B;font-weight:700">🚨 DESLIZAMENTO DETECTADO</span>`
    : tiltDetected
      ? `<br><span style="color:#E67E22;font-weight:700">⚠️ Sensor caído</span>`
      : ''

  const tooltipHtml = `
    <div style="font-family:sans-serif;font-size:12px;line-height:1.7">
      <b style="font-size:13px">${epd.epd_uid}</b>
      ${epd.label ? `<br><span style="color:#888">${epd.label}</span>` : ''}
      <br>🌱 Umidade: <b>${moisture.toFixed(1)}%</b>
      ${angleRow}
      ${statusRow}
    </div>`
  marker.bindTooltip(tooltipHtml, { sticky: true, offset: [0, 4] })
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
    const m = buildMarker(epd).addTo(mapInstance)
    if (epd.epd_uid === props.selectedUid) {
      setTimeout(() => m.openTooltip(), 120)
    }
    markerMap.set(epd.epd_uid, m)
  }
}

// ── Public API ───────────────────────────────────────────────────────────────

function flyToEpd(uid: string) {
  if (!mapInstance) return
  const epd = props.epds.find((e) => e.epd_uid === uid)
  if (epd?.lat != null && epd.lng != null) {
    mapInstance.flyTo([epd.lat, epd.lng], 18, { animate: true, duration: 0.8 })
  }
}

defineExpose({ flyToEpd })

// ── User location ────────────────────────────────────────────────────────────

function placeUserMarker(lat: number, lng: number, firstFix: boolean) {
  if (!mapInstance) return
  userPos.value = [lat, lng]

  if (!userMarker) {
    userMarker = L.circleMarker([lat, lng], {
      radius:      8,
      fillColor:   '#2980B9',
      color:       '#fff',
      weight:      2.5,
      opacity:     1,
      fillOpacity: 1,
      pane:        'markerPane',
    })
    userMarker.bindTooltip('Você está aqui', { permanent: false, offset: [0, -8] })
    userMarker.addTo(mapInstance)
  } else {
    userMarker.setLatLng([lat, lng])
  }

  if (firstFix) flyToUser()
}

function flyToUser() {
  if (!mapInstance || !userPos.value) return
  mapInstance.flyTo(userPos.value, mapInstance.options.maxZoom ?? 19, { animate: true, duration: 1 })
}

function startGeolocation() {
  if (!('geolocation' in navigator)) return
  let firstFix = true
  watchId = navigator.geolocation.watchPosition(
    ({ coords }) => {
      placeUserMarker(coords.latitude, coords.longitude, firstFix)
      firstFix = false
    },
    () => { /* permission denied or unavailable,silent fail */ },
    { enableHighAccuracy: true, maximumAge: 10_000 },
  )
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

  setupHeatCanvas(mapInstance)
  setupRainCanvas(mapInstance)

  // Redraw both canvases on every map movement so they stay aligned
  mapInstance.on('move zoom moveend zoomend', () => {
    drawHeat(props.epds)
    drawRain(props.rainGrid)
  })

  updateMarkers(props.epds)
  drawHeat(props.epds)
  drawRain(props.rainGrid)
  startGeolocation()
})

onUnmounted(() => {
  if (watchId !== null) navigator.geolocation.clearWatch(watchId)
  mapInstance?.remove()
  mapInstance = null
})

watch([() => props.epds, () => props.selectedUid], () => {
  updateMarkers(props.epds)
  drawHeat(props.epds)
}, { deep: true })

watch(() => props.rainGrid, (grid) => drawRain(grid), { deep: true })

</script>

<style scoped>
.live-map {
  width: 100%;
  height: 100%;
  min-height: 300px;
  position: relative;
}

/* ── Locate-me button ───────────────────────────── */
.locate-btn {
  position: absolute;
  bottom: 100px;
  right: 12px;
  z-index: 1000;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 10px rgba(0,0,0,.18);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  transition: background 0.15s, color 0.15s, box-shadow 0.15s;
}
.locate-btn:hover {
  background: #fff;
  box-shadow: 0 3px 14px rgba(0,0,0,.22);
  color: #2980B9;
}
.locate-btn--active { color: #2980B9; }
.locate-btn--active:hover { color: #1a5f87; }

/* ── Rain legend ────────────────────────────────── */
.rain-legend {
  position: absolute;
  bottom: 68px;
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

<style>
/* Pin hover,DivIcon lives outside Vue scope, must be non-scoped */
.epd-pin-wrap {
  cursor: pointer;
  transform-origin: bottom center;
  transition: transform 0.15s ease, filter 0.15s ease;
  display: inline-block;
}
.epd-pin-wrap:hover {
  transform: scale(1.18) translateY(-2px);
  filter: drop-shadow(0 4px 8px rgba(0,0,0,.35));
}
.epd-pin-wrap--selected {
  filter: drop-shadow(0 3px 6px rgba(0,0,0,.3));
}
.epd-pin-wrap--selected:hover {
  transform: scale(1.1) translateY(-2px);
}
.epd-pin-wrap--landslide {
  animation: epd-landslide-pulse 1.1s ease-in-out infinite;
}
@keyframes epd-landslide-pulse {
  0%, 100% { filter: drop-shadow(0 3px 6px rgba(192, 57, 43, 0.4)); }
  50%       { filter: drop-shadow(0 4px 14px rgba(192, 57, 43, 0.95)) brightness(1.1); }
}
</style>
