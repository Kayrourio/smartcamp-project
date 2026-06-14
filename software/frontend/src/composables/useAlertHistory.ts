import { ref, watch } from 'vue'
import type { Ref } from 'vue'
import type { SensorReading } from '@/types/sensor'

export interface AlertEntry {
  id: number
  risk_level: string
  soil_moisture: number
  timestamp: Date
}

export function useAlertHistory(data: Ref<SensorReading | null>) {
  const alerts = ref<AlertEntry[]>([])
  let idCounter = 0

  watch(data, (newVal, oldVal) => {
    if (!newVal) return
    const changed = !oldVal || newVal.risk_level !== oldVal.risk_level
    if (changed && newVal.risk_level !== 'SAFE') {
      alerts.value.unshift({
        id: ++idCounter,
        risk_level: newVal.risk_level,
        soil_moisture: newVal.soil_moisture,
        timestamp: new Date(),
      })
      if (alerts.value.length > 20) alerts.value.pop()
    }
  })

  return { alerts }
}
