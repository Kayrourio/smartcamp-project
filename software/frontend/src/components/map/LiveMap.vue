<template>
  <div ref="mapEl" class="live-map" />
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
// leaflet.heat has no type declarations — side-effect import only
import 'leaflet.heat'
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
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let rainHeatLayer: any = null
const markerMap = new Map<string, L.CircleMarker>()

function buildCircleMarker(epd: EpdOut): L.CircleMarker {
  const lat = epd.lat ?? -20.7546
  const lng = epd.lng ?? -42.8825
  const risk = epd.latest?.risk_level ?? 'SAFE'
  const moisture = epd.latest?.soil_moisture ?? 0
  const isSelected = epd.epd_uid === props.selectedUid

  const marker = L.circleMarker([lat, lng], {
    radius: isSelected ? 13 : 9,
    fillColor: RISK_COLOR[risk] ?? '#52B788',
    color: '#fff',
    weight: isSelected ? 3 : 2,
    opacity: 1,
    fillOpacity: 0.92,
  })

  marker.bindTooltip(
    `<b>${epd.epd_uid}</b>${epd.label ? `<br><span style="color:#888">${epd.label}</span>` : ''}<br>Umidade: ${moisture.toFixed(1)}%`,
    { sticky: true },
  )

  marker.on('click', () => emit('select-epd', epd.epd_uid))
  return marker
}

function updateMarkers(epds: EpdOut[]) {
  if (!mapInstance) return

  const currentUids = new Set(epds.map((e) => e.epd_uid))

  for (const [uid, m] of markerMap) {
    if (!currentUids.has(uid)) {
      m.remove()
      markerMap.delete(uid)
    }
  }

  for (const epd of epds) {
    if (epd.lat == null || epd.lng == null) continue
    const existing = markerMap.get(epd.epd_uid)
    if (existing) {
      existing.remove()
      markerMap.delete(epd.epd_uid)
    }
    const m = buildCircleMarker(epd)
    m.addTo(mapInstance)
    markerMap.set(epd.epd_uid, m)
  }
}

function updateRainGrid(grid: GridPoint[]) {
  if (!rainHeatLayer) return
  const pts = grid.map((p) => [p.lat, p.lng, Math.min(p.rainfall_mm / MAX_RAIN_MM, 1.0)])
  rainHeatLayer.setLatLngs(pts)
}

onMounted(() => {
  if (!mapEl.value) return

  mapInstance = L.map(mapEl.value, {
    center: [-20.7546, -42.8825],
    zoom: 14,
    zoomControl: true,
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(mapInstance)

  // Rain heatmap — always below markers, starts empty until first fetch
  // @ts-expect-error
  rainHeatLayer = L.heatLayer([], {
    radius: 55,
    blur: 35,
    maxZoom: 17,
    gradient: { 0.0: '#aed6f1', 0.4: '#2980b9', 0.8: '#1a5276', 1.0: '#0d2137' },
  }).addTo(mapInstance)

  updateMarkers(props.epds)
  updateRainGrid(props.rainGrid)
})

onUnmounted(() => {
  mapInstance?.remove()
  mapInstance = null
})

// Redraw markers on any EPD data change or selection change
watch([() => props.epds, () => props.selectedUid], () => updateMarkers(props.epds), { deep: true })

// Update rain heatmap when grid data changes
watch(() => props.rainGrid, updateRainGrid, { deep: true })

// Pan map to the newly selected EPD
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
}
</style>
