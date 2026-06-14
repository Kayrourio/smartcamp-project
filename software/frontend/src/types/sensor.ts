export interface SensorReading {
  sensor_id: string
  location: string
  soil_moisture: number
  rainfall: number | null
  temperature: number | null
  lux: number | null
  risk_level: 'SAFE' | 'ATTENTION' | 'CRITICAL'
  timestamp: string
  online: boolean
}

export interface HistoryPoint {
  soil_moisture: number
  timestamp: string
}

export interface SensorHistory {
  sensor_id: string
  readings: HistoryPoint[]
}
