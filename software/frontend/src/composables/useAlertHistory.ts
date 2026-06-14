import { ref, watch } from 'vue'
import type { Ref } from 'vue'
import type { EpdOut } from '@/types/sensor'

export interface AlertEntry {
  id: number
  epd_uid: string
  risk_level: string
  soil_moisture: number
  tilt_detected: boolean
  is_landslide: boolean
  timestamp: Date
}

export function useAlertHistory(epds: Ref<EpdOut[]>) {
  const alerts = ref<AlertEntry[]>([])
  let idCounter = 0
  const prevRisk = new Map<string, string>()

  watch(
    epds,
    (list) => {
      for (const epd of list) {
        if (!epd.latest) continue
        const prev = prevRisk.get(epd.epd_uid)
        const curr = epd.latest.risk_level
        if (prev !== undefined && prev !== curr && curr !== 'SAFE') {
          const tilt = epd.latest.tilt_detected
          alerts.value.unshift({
            id: ++idCounter,
            epd_uid: epd.epd_uid,
            risk_level: curr,
            soil_moisture: epd.latest.soil_moisture,
            tilt_detected: tilt,
            is_landslide: tilt && curr === 'CRITICAL',
            timestamp: new Date(),
          })
          if (alerts.value.length > 20) alerts.value.pop()
        }
        prevRisk.set(epd.epd_uid, curr)
      }
    },
    { deep: true },
  )

  return { alerts }
}
