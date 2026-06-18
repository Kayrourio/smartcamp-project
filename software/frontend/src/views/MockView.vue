<template>
  <div class="mock-view">
    <OfflineModal />
    <!-- Header -->
    <header class="mock-header" :style="{ background: headerBg }">
      <RouterLink to="/" class="back-btn">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M10 3L5 8L10 13" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        Voltar
      </RouterLink>

      <div class="header-center">
        <LogoMark />
        <span class="brand">TerraSafe</span>
        <span class="demo-badge">DEMO</span>
      </div>

      <div class="header-stats">
        <span class="stat critical">{{ counts.CRITICAL }} críticos</span>
        <span class="stat high">{{ counts.HIGH }} altos</span>
        <span class="stat attention">{{ counts.ATTENTION }} atenção</span>
      </div>
    </header>

    <!-- Map -->
    <div class="map-wrap">
      <LiveMap
        :epds="epds"
        :rain-grid="[]"
        :selected-uid="null"
        @select-epd="() => {}"
      />

      <!-- Demo overlay -->
      <div class="demo-overlay">
        <div class="demo-pill">
          <span class="pulse-dot" />
          <span>100 sensores simulados · Viçosa, MG · atualiza a cada 2s</span>
        </div>
      </div>

      <!-- Risk legend -->
      <div class="risk-legend">
        <div class="legend-title">Distribuição de risco</div>
        <div v-for="row in riskRows" :key="row.key" class="legend-row">
          <span class="legend-dot" :style="{ background: row.color }" />
          <span class="legend-label">{{ row.label }}</span>
          <div class="legend-track">
            <div class="legend-fill" :style="{ width: row.pct + '%', background: row.color }" />
          </div>
          <span class="legend-pct">{{ row.pct }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useMockEpds } from '@/composables/useMockEpds'
import type { EpdOut } from '@/types/sensor'
import LiveMap from '@/components/map/LiveMap.vue'
import LogoMark from '@/components/icons/LogoMark.vue'
import OfflineModal from '@/components/OfflineModal.vue'

const { epds } = useMockEpds()

const RISK_COLORS: Record<string, string> = {
  SAFE:      '#52B788',
  ATTENTION: '#F1C40F',
  HIGH:      '#E67E22',
  CRITICAL:  '#C0392B',
}

const RISK_ROW_META = [
  { key: 'CRITICAL'  as const, label: 'Crítico', color: '#C0392B' },
  { key: 'HIGH'      as const, label: 'Alto',    color: '#E67E22' },
  { key: 'ATTENTION' as const, label: 'Atenção', color: '#F1C40F' },
  { key: 'SAFE'      as const, label: 'Seguro',  color: '#52B788' },
]

const counts = computed(() => {
  const c = { CRITICAL: 0, HIGH: 0, ATTENTION: 0, SAFE: 0 }
  for (const epd of epds.value) {
    const r = epd.latest?.risk_level
    if (r && r in c) c[r as keyof typeof c]++
  }
  return c
})

const riskRows = computed(() => {
  const total = epds.value.filter((e: EpdOut) => e.latest).length
  if (!total) return []
  return RISK_ROW_META.map((m) => ({
    ...m,
    pct: Math.round(counts.value[m.key] / total * 100),
  }))
})

const headerBg = computed(() => {
  const levels = epds.value.map((e) => e.latest?.risk_level)
  if (levels.includes('CRITICAL')) return RISK_COLORS.CRITICAL
  if (levels.includes('HIGH')) return RISK_COLORS.HIGH
  if (levels.includes('ATTENTION')) return RISK_COLORS.ATTENTION
  return '#2d6a4f'
})
</script>

<style scoped>
.mock-view {
  display: flex;
  flex-direction: column;
  height: 100dvh;
  overflow: hidden;
}

.mock-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  transition: background 0.8s ease;
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
  transition: opacity 0.2s;
  text-decoration: none;
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

.demo-badge {
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

.header-stats {
  display: flex;
  gap: 8px;
  align-items: center;
}

.stat {
  font-size: 12px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 20px;
  background: rgba(0,0,0,0.25);
  color: #fff;
  white-space: nowrap;
}
.stat.critical { background: rgba(192,57,43,0.5); }
.stat.high     { background: rgba(230,126,34,0.5); }
.stat.attention { background: rgba(241,196,15,0.35); color: #ffd; }

/* ── Map area ─────────────────────────────── */
.map-wrap {
  flex: 1;
  position: relative;
  overflow: hidden;
}

/* ── Demo pill ────────────────────────────── */
.demo-overlay {
  position: absolute;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  pointer-events: none;
}

.demo-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 7px 16px;
  font-size: 12px;
  font-weight: 600;
  color: #333;
  box-shadow: 0 2px 14px rgba(0,0,0,0.15);
  white-space: nowrap;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #C0392B;
  animation: pulse-dot 1.4s ease-in-out infinite;
  flex-shrink: 0;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.7); }
}

/* ── Risk legend panel ────────────────────── */
.risk-legend {
  position: absolute;
  bottom: 80px;
  right: 12px;
  z-index: 1000;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 10px 14px 12px;
  box-shadow: 0 2px 14px rgba(0,0,0,0.13);
  min-width: 170px;
  display: flex;
  flex-direction: column;
  gap: 7px;
  pointer-events: none;
}

.legend-title {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: #666;
  margin-bottom: 2px;
}

.legend-row {
  display: flex;
  align-items: center;
  gap: 7px;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-label {
  font-size: 11px;
  font-weight: 600;
  color: #555;
  width: 44px;
  flex-shrink: 0;
}

.legend-track {
  flex: 1;
  height: 5px;
  background: #eee;
  border-radius: 3px;
  overflow: hidden;
}

.legend-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease;
  min-width: 2px;
}

.legend-pct {
  font-size: 11px;
  font-weight: 700;
  color: #333;
  width: 26px;
  text-align: right;
  flex-shrink: 0;
}

@media (max-width: 600px) {
  .header-stats { display: none; }
  .demo-pill { font-size: 11px; padding: 6px 12px; }
  .risk-legend { bottom: 68px; right: 8px; }
}
</style>
