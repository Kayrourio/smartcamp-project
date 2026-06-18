import { ref, computed, onMounted, onUnmounted } from 'vue'
import type { EpdOut, EpdReading, RiskLevel, HistoryPoint } from '@/types/sensor'

function computeRisk(moisture: number, tilt: boolean): RiskLevel {
  if (moisture >= 70 || (tilt && moisture >= 25)) return 'CRITICAL'
  if (moisture >= 25) return 'HIGH'
  if (moisture >= 10 || tilt) return 'ATTENTION'
  return 'SAFE'
}

export const SIMULATOR_PRESETS = {
  safe: {
    label: 'Seguro',
    description: 'Solo seco, sem chuva',
    moisture: 5,
    rainfall: 0,
    temperature: 26,
    angle: 0,
    tilt: false,
  },
  attention: {
    label: 'Atenção',
    description: 'Chuva leve, solo úmido',
    moisture: 18,
    rainfall: 10,
    temperature: 22,
    angle: 6,
    tilt: false,
  },
  high: {
    label: 'Alto Risco',
    description: 'Chuva moderada, solo saturado',
    moisture: 45,
    rainfall: 28,
    temperature: 19,
    angle: 14,
    tilt: false,
  },
  critical: {
    label: 'Crítico',
    description: 'Deslizamento em andamento',
    moisture: 85,
    rainfall: 44,
    temperature: 17,
    angle: 38,
    tilt: true,
  },
} as const

export type PresetKey = keyof typeof SIMULATOR_PRESETS

export function useSimulator() {
  const lat = ref<number | null>(null)
  const lng = ref<number | null>(null)
  const locationStatus = ref<'pending' | 'granted' | 'denied'>('pending')

  const moisture = ref(5)
  const rainfall = ref(0)
  const temperature = ref(26)
  const angle = ref(0)
  const tiltDetected = ref(false)
  const activePreset = ref<PresetKey | null>('safe')

  const history = ref<HistoryPoint[]>([])
  let intervalId: ReturnType<typeof setInterval> | null = null

  const riskLevel = computed<RiskLevel>(() => computeRisk(moisture.value, tiltDetected.value))

  const reading = computed<EpdReading>(() => ({
    soil_moisture: moisture.value,
    rainfall: rainfall.value,
    temperature: temperature.value,
    angle_x: angle.value,
    angle_y: 0,
    angle_z: 0,
    tilt_detected: tiltDetected.value,
    risk_level: riskLevel.value,
    received_at: new Date().toISOString(),
  }))

  const epds = computed<EpdOut[]>(() => [
    {
      epd_uid: 'SIM-001',
      label: 'Sensor Simulado',
      lat: lat.value ?? -20.7546,
      lng: lng.value ?? -42.8825,
      active: true,
      latest: reading.value,
    },
  ])

  function applyPreset(key: PresetKey) {
    const p = SIMULATOR_PRESETS[key]
    moisture.value = p.moisture
    rainfall.value = p.rainfall
    temperature.value = p.temperature
    angle.value = p.angle
    tiltDetected.value = p.tilt
    activePreset.value = key
  }

  function onSliderChange() {
    activePreset.value = null
  }

  function pushHistory() {
    const pt: HistoryPoint = {
      soil_moisture: moisture.value,
      risk_level: riskLevel.value,
      received_at: new Date().toISOString(),
    }
    history.value = [...history.value.slice(-59), pt]
  }

  onMounted(() => {
    pushHistory()
    intervalId = setInterval(pushHistory, 2000)

    if (!('geolocation' in navigator)) {
      locationStatus.value = 'denied'
      return
    }

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        lat.value = pos.coords.latitude
        lng.value = pos.coords.longitude
        locationStatus.value = 'granted'
      },
      () => {
        locationStatus.value = 'denied'
      },
      { enableHighAccuracy: true, timeout: 8000 },
    )
  })

  onUnmounted(() => {
    if (intervalId) clearInterval(intervalId)
  })

  return {
    lat,
    lng,
    locationStatus,
    moisture,
    rainfall,
    temperature,
    angle,
    tiltDetected,
    riskLevel,
    reading,
    epds,
    history,
    activePreset,
    applyPreset,
    onSliderChange,
  }
}
