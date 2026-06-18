<template>
  <div class="sim-view">
    <!-- Header -->
    <header class="sim-header" :style="{ background: headerBg }">
      <RouterLink to="/" class="back-btn">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M10 3L5 8L10 13" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        Voltar
      </RouterLink>

      <div class="header-center">
        <LogoMark />
        <span class="brand">TerraSafe</span>
        <span class="sim-badge">SIMULADOR</span>
      </div>

      <div class="header-risk">
        <span class="risk-chip" :style="{ background: RISK_COLORS[riskLevel] }">
          {{ RISK_LABELS[riskLevel] }}
        </span>
      </div>
    </header>

    <!-- Body: map + controls -->
    <div class="sim-body">
      <!-- Map column -->
      <div class="map-col">
        <LiveMap
          :epds="epds"
          :rain-grid="simulatedRainGrid"
          :selected-uid="null"
          @select-epd="() => {}"
        />

        <!-- Location pill -->
        <div class="location-pill" :class="'location-pill--' + locationStatus">
          <span class="pill-dot" />
          <span v-if="locationStatus === 'pending'">Buscando localização…</span>
          <span v-else-if="locationStatus === 'granted'">Sensor na sua localização atual</span>
          <span v-else>Localização padrão: Viçosa, MG</span>
        </div>
      </div>

      <!-- Controls column -->
      <aside class="controls-col">
        <!-- Sensor card -->
        <div class="sensor-card" :class="'sensor-card--' + riskLevel.toLowerCase()">
          <div class="sensor-card-top">
            <div class="sensor-id">SIM-001</div>
            <div class="risk-badge" :style="{ background: RISK_COLORS[riskLevel] }">
              {{ RISK_LABELS[riskLevel] }}
            </div>
          </div>
          <div class="moisture-big">{{ moisture.toFixed(0) }}<span class="moisture-unit">%</span></div>
          <div class="moisture-label">umidade do solo</div>

          <div v-if="tiltDetected" class="tilt-warning" :class="riskLevel === 'CRITICAL' ? 'tilt-warning--critical' : ''">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            {{ riskLevel === 'CRITICAL' ? 'Deslizamento detectado' : 'Sensor inclinado' }}
          </div>

          <div class="metric-row">
            <div class="metric">
              <span class="metric-icon">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v6m0 0a3 3 0 1 0 3 3"/><path d="M12 8c-3.3 0-6 2.7-6 6 0 2.8 1.9 5.1 4.5 5.8"/><path d="M8 3.5C5.5 4.8 4 7.2 4 10"/></svg>
              </span>
              <span class="metric-val">{{ rainfall.toFixed(0) }} <span class="metric-unit">mm/h</span></span>
            </div>
            <div class="metric">
              <span class="metric-icon">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>
              </span>
              <span class="metric-val">{{ temperature.toFixed(0) }}<span class="metric-unit">°C</span></span>
            </div>
            <div class="metric">
              <span class="metric-icon">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m2 20 20-16"/><path d="M6 20a4 4 0 0 0 4-4"/><path d="M2 16a4 4 0 0 1 4-4"/></svg>
              </span>
              <span class="metric-val">{{ angle.toFixed(0) }}<span class="metric-unit">°</span></span>
            </div>
          </div>
        </div>

        <!-- Presets -->
        <div class="section-label">Cenários</div>
        <div class="presets-grid">
          <button
            v-for="(preset, key) in SIMULATOR_PRESETS"
            :key="key"
            class="preset-btn"
            :class="[
              'preset-btn--' + key,
              activePreset === key ? 'preset-btn--active' : '',
            ]"
            @click="applyPreset(key as PresetKey)"
          >
            <span class="preset-dot" :style="{ background: RISK_COLORS[computePresetRisk(key as PresetKey)] }" />
            <span class="preset-label">{{ preset.label }}</span>
            <span class="preset-desc">{{ preset.description }}</span>
          </button>
        </div>

        <!-- Sliders -->
        <div class="section-label">Ajuste manual</div>
        <div class="sliders">
          <label class="slider-row">
            <span class="slider-name">Umidade do solo</span>
            <span class="slider-val">{{ moisture.toFixed(0) }}%</span>
            <input
              type="range" min="0" max="100" step="1"
              :value="moisture"
              class="slider slider--moisture"
              @input="onSliderInput('moisture', $event)"
            />
          </label>

          <label class="slider-row">
            <span class="slider-name">Chuva</span>
            <span class="slider-val">{{ rainfall.toFixed(0) }} mm/h</span>
            <input
              type="range" min="0" max="100" step="1"
              :value="rainfall"
              class="slider slider--rain"
              @input="onSliderInput('rainfall', $event)"
            />
          </label>

          <label class="slider-row">
            <span class="slider-name">Temperatura</span>
            <span class="slider-val">{{ temperature.toFixed(0) }}°C</span>
            <input
              type="range" min="5" max="45" step="1"
              :value="temperature"
              class="slider slider--temp"
              @input="onSliderInput('temperature', $event)"
            />
          </label>

          <label class="slider-row">
            <span class="slider-name">Inclinação</span>
            <span class="slider-val">{{ angle.toFixed(0) }}°</span>
            <input
              type="range" min="0" max="90" step="1"
              :value="angle"
              class="slider slider--angle"
              @input="onSliderInput('angle', $event)"
            />
          </label>

          <label class="toggle-row">
            <span class="slider-name">Sensor caído / deslizamento</span>
            <button
              class="toggle-btn"
              :class="tiltDetected ? 'toggle-btn--on' : ''"
              @click="toggleTilt"
            >
              <span class="toggle-thumb" />
            </button>
          </label>
        </div>

        <!-- History chart -->
        <div class="chart-section">
          <HumidityChart
            :data="historyData"
            :labels="historyLabels"
          />
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useSimulator, SIMULATOR_PRESETS, type PresetKey } from '@/composables/useSimulator'
import type { RiskLevel, GridPoint } from '@/types/sensor'
import LiveMap from '@/components/map/LiveMap.vue'
import HumidityChart from '@/components/dashboard/HumidityChart.vue'
import LogoMark from '@/components/icons/LogoMark.vue'

const {
  locationStatus,
  moisture, rainfall, temperature, angle, tiltDetected,
  riskLevel, epds, history,
  activePreset, applyPreset, onSliderChange,
} = useSimulator()

const RISK_COLORS: Record<RiskLevel, string> = {
  SAFE:      '#52B788',
  ATTENTION: '#F1C40F',
  HIGH:      '#E67E22',
  CRITICAL:  '#C0392B',
}

const RISK_LABELS: Record<RiskLevel, string> = {
  SAFE:      'Seguro',
  ATTENTION: 'Atenção',
  HIGH:      'Alto Risco',
  CRITICAL:  'Crítico',
}

function computePresetRisk(key: PresetKey): RiskLevel {
  const p = SIMULATOR_PRESETS[key]
  const m = p.moisture
  const t = p.tilt
  if (m >= 70 || (t && m >= 25)) return 'CRITICAL'
  if (m >= 25) return 'HIGH'
  if (m >= 10 || t) return 'ATTENTION'
  return 'SAFE'
}

const headerBg = computed(() => RISK_COLORS[riskLevel.value] ?? '#2d6a4f')

// Build a simulated rain grid centered on the sensor
const simulatedRainGrid = computed<GridPoint[]>(() => {
  const sensorLat = epds.value[0]?.lat ?? -20.7546
  const sensorLng = epds.value[0]?.lng ?? -42.8825
  const step = 0.05
  const grid: GridPoint[] = []
  for (let dlat = -1; dlat <= 1; dlat++) {
    for (let dlng = -1; dlng <= 1; dlng++) {
      const dist = Math.sqrt(dlat * dlat + dlng * dlng)
      const mm = rainfall.value * Math.max(0, 1 - dist * 0.4)
      grid.push({
        lat: sensorLat + dlat * step,
        lng: sensorLng + dlng * step,
        rainfall_mm: mm,
      })
    }
  }
  return grid
})

const historyData = computed(() => history.value.map((h) => h.soil_moisture))

const historyLabels = computed(() => {
  const items = history.value
  if (!items.length) return []
  return items.map((h) => {
    const d = new Date(h.received_at)
    return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`
  })
})

function onSliderInput(field: 'moisture' | 'rainfall' | 'temperature' | 'angle', event: Event) {
  const val = Number((event.target as HTMLInputElement).value)
  if (field === 'moisture') moisture.value = val
  else if (field === 'rainfall') rainfall.value = val
  else if (field === 'temperature') temperature.value = val
  else if (field === 'angle') angle.value = val
  onSliderChange()
}

function toggleTilt() {
  tiltDetected.value = !tiltDetected.value
  onSliderChange()
}
</script>

<style scoped>
.sim-view {
  display: flex;
  flex-direction: column;
  height: 100dvh;
  overflow: hidden;
  background: var(--bg, #f5f5f0);
}

/* ── Header ─────────────────────────────────────── */
.sim-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  transition: background 0.6s ease;
  flex-shrink: 0;
  gap: 12px;
  color: #fff;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  transition: opacity 0.2s;
  white-space: nowrap;
}
.back-btn:hover { opacity: 1; color: #fff; }

.header-center {
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand {
  font-family: var(--font-head);
  font-size: 18px;
  font-weight: 800;
  color: #fff;
}

.sim-badge {
  font-family: var(--font-head);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.1em;
  background: rgba(255,255,255,0.25);
  border: 1px solid rgba(255,255,255,0.5);
  color: #fff;
  padding: 2px 8px;
  border-radius: 20px;
}

.header-risk {
  display: flex;
  align-items: center;
}

.risk-chip {
  font-size: 12px;
  font-weight: 700;
  padding: 3px 12px;
  border-radius: 20px;
  color: #fff;
  background: rgba(0,0,0,0.25);
  transition: background 0.4s ease;
}

/* ── Body ───────────────────────────────────────── */
.sim-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* ── Map column ─────────────────────────────────── */
.map-col {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.location-pill {
  position: absolute;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 7px;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 600;
  color: #333;
  box-shadow: 0 2px 14px rgba(0,0,0,0.13);
  white-space: nowrap;
  pointer-events: none;
}

.pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.location-pill--pending .pill-dot  { background: #F1C40F; animation: pill-pulse 1.2s ease-in-out infinite; }
.location-pill--granted .pill-dot  { background: #2980B9; }
.location-pill--denied  .pill-dot  { background: #888; }

@keyframes pill-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
}

/* ── Controls column ────────────────────────────── */
.controls-col {
  width: 300px;
  flex-shrink: 0;
  background: #f5f5f0;
  border-left: 1px solid rgba(0,0,0,0.08);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
}

/* ── Sensor card ────────────────────────────────── */
.sensor-card {
  background: #fff;
  border-radius: 12px;
  padding: 14px 16px 12px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.08);
  border: 2px solid transparent;
  transition: border-color 0.4s ease;
}

.sensor-card--safe      { border-color: #52B788; }
.sensor-card--attention { border-color: #F1C40F; }
.sensor-card--high      { border-color: #E67E22; }
.sensor-card--critical  { border-color: #C0392B; animation: card-pulse 1.2s ease-in-out infinite; }

@keyframes card-pulse {
  0%, 100% { box-shadow: 0 1px 6px rgba(0,0,0,0.08); }
  50%       { box-shadow: 0 2px 18px rgba(192,57,43,0.35); }
}

.sensor-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.sensor-id {
  font-family: var(--font-head);
  font-size: 12px;
  font-weight: 700;
  color: #666;
  letter-spacing: 0.06em;
}

.risk-badge {
  font-size: 11px;
  font-weight: 700;
  color: #fff;
  padding: 2px 10px;
  border-radius: 20px;
  transition: background 0.4s ease;
}

.moisture-big {
  font-family: var(--font-head);
  font-size: 48px;
  font-weight: 800;
  color: #1a1a1a;
  line-height: 1;
}

.moisture-unit {
  font-size: 20px;
  font-weight: 600;
  color: #888;
  margin-left: 2px;
}

.moisture-label {
  font-size: 11px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-top: 2px;
  margin-bottom: 10px;
}

.tilt-warning {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 700;
  color: #E67E22;
  background: rgba(230,126,34,0.1);
  border-radius: 8px;
  padding: 6px 10px;
  margin-bottom: 10px;
}

.tilt-warning--critical {
  color: #C0392B;
  background: rgba(192,57,43,0.1);
}

.metric-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.metric {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #f5f5f0;
  border-radius: 8px;
  padding: 4px 8px;
}

.metric-icon { font-size: 12px; }

.metric-val {
  font-size: 12px;
  font-weight: 700;
  color: #333;
}

.metric-unit {
  font-weight: 400;
  color: #888;
  font-size: 10px;
}

/* ── Presets ────────────────────────────────────── */
.section-label {
  font-family: var(--font-head);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #888;
  padding: 8px 2px 2px;
}

.presets-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.preset-btn {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  background: #fff;
  border: 1.5px solid rgba(0,0,0,0.08);
  border-radius: 10px;
  padding: 9px 10px;
  cursor: pointer;
  transition: border-color 0.15s, box-shadow 0.15s, background 0.15s;
  text-align: left;
}

.preset-btn:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  background: #f8f8f8;
}

.preset-btn--active {
  border-color: #2d6a4f;
  box-shadow: 0 2px 10px rgba(45,106,79,0.2);
  background: rgba(45,106,79,0.04);
}

.preset-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-bottom: 3px;
}

.preset-label {
  font-size: 12px;
  font-weight: 700;
  color: #222;
}

.preset-desc {
  font-size: 10px;
  color: #888;
  line-height: 1.3;
}

/* ── Sliders ────────────────────────────────────── */
.sliders {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #fff;
  border-radius: 12px;
  padding: 14px 14px 12px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
}

.slider-row, .toggle-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
  cursor: pointer;
}

.toggle-row {
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.slider-name {
  font-size: 11px;
  font-weight: 600;
  color: #555;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.slider-val {
  font-size: 11px;
  font-weight: 700;
  color: #222;
  margin-left: auto;
}

.slider-row {
  flex-direction: row;
  align-items: center;
  gap: 8px;
}

.slider-row .slider-name { flex: 1; min-width: 0; }
.slider-row .slider-val  { white-space: nowrap; min-width: 52px; text-align: right; }

.slider {
  flex: 1;
  -webkit-appearance: none;
  appearance: none;
  height: 5px;
  border-radius: 3px;
  background: #e0e0e0;
  outline: none;
  cursor: pointer;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #2d6a4f;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
  transition: box-shadow 0.15s;
}
.slider::-webkit-slider-thumb:hover { box-shadow: 0 2px 8px rgba(45,106,79,0.4); }

/* Toggle */
.toggle-btn {
  width: 42px;
  height: 24px;
  border-radius: 12px;
  background: #ddd;
  border: none;
  cursor: pointer;
  position: relative;
  transition: background 0.25s ease;
  flex-shrink: 0;
}

.toggle-btn--on {
  background: #C0392B;
}

.toggle-thumb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
  transition: left 0.25s ease;
}

.toggle-btn--on .toggle-thumb {
  left: 21px;
}

/* ── Chart ──────────────────────────────────────── */
.chart-section {
  margin-top: 4px;
}

/* ── Responsive (mobile) ─────────────────────────── */
@media (max-width: 700px) {
  .sim-body {
    flex-direction: column;
  }

  .map-col {
    height: 45dvh;
  }

  .controls-col {
    width: 100%;
    border-left: none;
    border-top: 1px solid rgba(0,0,0,0.08);
    flex: 1;
  }

  .presets-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
