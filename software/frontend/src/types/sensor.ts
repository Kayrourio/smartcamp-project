export type RiskLevel = 'SAFE' | 'ATTENTION' | 'HIGH' | 'CRITICAL'

export interface EpdReading {
  soil_moisture: number
  rainfall: number | null
  temperature: number | null
  angle_x: number | null
  angle_y: number | null
  angle_z: number | null
  tilt_detected: boolean
  risk_level: RiskLevel
  received_at: string
}

export interface EpdOut {
  epd_uid: string
  label: string | null
  lat: number | null
  lng: number | null
  active: boolean
  latest: EpdReading | null
}

export interface GridPoint {
  lat: number
  lng: number
  rainfall_mm: number
}

export interface HistoryPoint {
  soil_moisture: number
  risk_level: RiskLevel
  received_at: string
}

export interface EpdHistory {
  epd_uid: string
  readings: HistoryPoint[]
}
