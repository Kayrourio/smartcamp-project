<template>
  <div ref="mapEl" class="live-map" />
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// leaflet.heat is a side-effect import, no types
// @ts-expect-error — no types for leaflet.heat
import 'leaflet.heat'

const props = withDefaults(
  defineProps<{
    soilMoisture: number
    sensorLat?: number
    sensorLng?: number
    activeLayer?: string
  }>(),
  {
    sensorLat: -20.7546,
    sensorLng: -42.8825,
    activeLayer: 'soil',
  },
)

const mapEl = ref<HTMLDivElement | null>(null)
let mapInstance: L.Map | null = null
let heatLayer: L.Layer & { setLatLngs: (pts: unknown[]) => void; setOptions: (opts: unknown) => void } | null = null
let markerLayer: L.Marker | null = null

function buildMarkerIcon(moisture: number): L.DivIcon {
  return L.divIcon({
    html: `
      <div style="display:flex;flex-direction:column;align-items:center;gap:2px">
        <div style="background:#1F2926;color:#fff;font-size:11px;font-weight:600;padding:2px 7px;border-radius:20px;white-space:nowrap">
          EPD-01 · ${moisture.toFixed(0)}%
        </div>
        <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
          <ellipse cx="18" cy="10" rx="9" ry="6" fill="#6B4528"/>
          <rect x="9" y="10" width="18" height="14" rx="2" fill="#4F6A2E"/>
          <ellipse cx="18" cy="24" rx="9" ry="6" fill="#6E8B43"/>
          <circle cx="18" cy="10" r="3" fill="#FFFFFF" opacity="0.5"/>
        </svg>
      </div>`,
    className: '',
    iconAnchor: [18, 36],
    iconSize: [60, 56],
  })
}

onMounted(() => {
  if (!mapEl.value) return

  mapInstance = L.map(mapEl.value, {
    center: [props.sensorLat, props.sensorLng],
    zoom: 15,
    zoomControl: true,
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(mapInstance)

  // @ts-expect-error — leaflet.heat adds L.heatLayer
  heatLayer = L.heatLayer([[props.sensorLat, props.sensorLng, props.soilMoisture / 100]], {
    radius: 30 + (props.soilMoisture / 100) * 90,
    blur: 25,
    maxZoom: 17,
    gradient: { 0.0: '#52B788', 0.6: '#F39C12', 1.0: '#C0392B' },
  }).addTo(mapInstance)

  markerLayer = L.marker([props.sensorLat, props.sensorLng], {
    icon: buildMarkerIcon(props.soilMoisture),
  })
    .addTo(mapInstance)
    .bindPopup(`<b>EPD-01</b><br>Umidade: ${props.soilMoisture.toFixed(1)}%`)
})

onUnmounted(() => {
  mapInstance?.remove()
  mapInstance = null
})

watch(
  () => props.soilMoisture,
  (val) => {
    if (!heatLayer || !markerLayer) return
    const intensity = val / 100
    const radius = 30 + intensity * 90
    heatLayer.setLatLngs([[props.sensorLat, props.sensorLng, intensity]])
    heatLayer.setOptions({ radius })
    markerLayer.setIcon(buildMarkerIcon(val))
    markerLayer.setPopupContent(`<b>EPD-01</b><br>Umidade: ${val.toFixed(1)}%`)
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
