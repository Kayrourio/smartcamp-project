<template>
  <div class="map-view">
    <!-- Header -->
    <header class="map-header" :style="{ background: headerBg }">
      <RouterLink to="/" class="back-btn">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M10 3L5 8L10 13" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        {{ t('map.back') }}
      </RouterLink>
      <div class="header-center">
        <LogoMark />
        <span class="brand">TerraSafe</span>
      </div>
      <LiveBadge />
    </header>

    <!-- Layout -->
    <div class="layout">
      <!-- Map -->
      <div class="map-container">
        <LiveMap
          :epds="epds"
          :rain-grid="rainGrid"
          :selected-uid="selectedUid"
          @select-epd="selectEpd"
        />
        <div v-if="isLoading && epds.length === 0" class="map-overlay">
          Carregando sensores...
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="section-title">{{ t('map.sensors_title') }} ({{ epds.length }})</div>

        <div v-if="epds.length === 0 && !isLoading" class="empty-state">
          Nenhum sensor cadastrado.
        </div>

        <div
          v-for="epd in epds"
          :key="epd.epd_uid"
          class="epd-card"
          :class="{
            selected: epd.epd_uid === selectedUid,
            'border-critical': epd.latest?.risk_level === 'CRITICAL' && epd.epd_uid === selectedUid,
            'border-attention': epd.latest?.risk_level === 'ATTENTION' && epd.epd_uid === selectedUid,
          }"
          @click="selectEpd(epd.epd_uid)"
        >
          <!-- Card header -->
          <div class="epd-row">
            <div class="epd-id-block">
              <span class="epd-uid">{{ epd.epd_uid }}</span>
              <span v-if="epd.label" class="epd-label">{{ epd.label }}</span>
            </div>
            <div
              class="risk-dot"
              :title="epd.latest?.risk_level ?? 'SEM LEITURA'"
              :style="{ background: riskColor(epd.latest?.risk_level) }"
            />
          </div>

          <!-- Moisture + risk badge -->
          <div v-if="epd.latest" class="epd-metrics-row">
            <span class="epd-moisture">
              {{ epd.latest.soil_moisture.toFixed(0) }}<span class="pct">%</span>
            </span>
            <span class="risk-badge" :style="{ background: riskColor(epd.latest.risk_level) }">
              {{ riskLabel(epd.latest.risk_level) }}
            </span>
          </div>
          <div v-else class="epd-offline">Sem leitura</div>

          <!-- Metrics: always visible when there's a reading -->
          <div v-if="epd.latest" class="chips">
            <MetricChip
              :label="t('map.metric_rainfall')"
              :value="epd.latest.rainfall"
              unit=" mm"
              :sub="t('map.rainfall_sub')"
            >
              <template #icon><IcoRain :size="18" color="var(--blue)" /></template>
            </MetricChip>
            <MetricChip
              :label="t('map.metric_temp')"
              :value="epd.latest.temperature"
              unit="°C"
              :sub="t('map.temp_sub')"
            >
              <template #icon><IcoTemp :size="18" color="var(--brown)" /></template>
            </MetricChip>
            <MetricChip
              :label="t('map.metric_lux')"
              :value="epd.latest.lux"
              unit=" lx"
            >
              <template #icon><IcoSun :size="18" color="var(--yellow)" /></template>
            </MetricChip>
          </div>

          <!-- History chart: only for the selected EPD -->
          <template v-if="epd.epd_uid === selectedUid">
            <HumidityChart v-if="chartData.length > 0" :data="chartData" />
            <div v-else class="chart-empty">Aguardando histórico...</div>
          </template>
        </div>

        <AlertList :alerts="alerts" />
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useEpdList } from '@/composables/useEpdList'
import { useRainGrid } from '@/composables/useRainGrid'
import { useAlertHistory } from '@/composables/useAlertHistory'
import { useEpdHistory } from '@/composables/useEpdHistory'
import type { RiskLevel } from '@/types/sensor'
import LiveMap from '@/components/map/LiveMap.vue'
import LiveBadge from '@/components/dashboard/LiveBadge.vue'
import MetricChip from '@/components/dashboard/MetricChip.vue'
import HumidityChart from '@/components/dashboard/HumidityChart.vue'
import AlertList from '@/components/dashboard/AlertList.vue'
import LogoMark from '@/components/icons/LogoMark.vue'
import IcoRain from '@/components/icons/IcoRain.vue'
import IcoTemp from '@/components/icons/IcoTemp.vue'
import IcoSun from '@/components/icons/IcoSun.vue'

const { t } = useI18n()

const { epds, isLoading } = useEpdList()
const { grid: rainGrid } = useRainGrid()
const { alerts } = useAlertHistory(epds)

const selectedUid = ref<string | null>(null)
const { history } = useEpdHistory(selectedUid)

// Auto-select first EPD on first load
watch(
  epds,
  (list) => {
    if (!selectedUid.value && list.length > 0) {
      selectedUid.value = list[0].epd_uid
    }
  },
  { immediate: true },
)

function selectEpd(uid: string) {
  selectedUid.value = uid
}

const RISK_COLORS: Record<string, string> = {
  SAFE: '#52B788',
  ATTENTION: '#F39C12',
  CRITICAL: '#C0392B',
}
const RISK_LABELS: Record<string, string> = {
  SAFE: 'Seguro',
  ATTENTION: 'Atenção',
  CRITICAL: 'Crítico',
}

function riskColor(level?: RiskLevel | null): string {
  return RISK_COLORS[level ?? 'SAFE'] ?? '#52B788'
}

function riskLabel(level: RiskLevel): string {
  return RISK_LABELS[level] ?? level
}

// Chart: moisture history of selected EPD
const chartData = computed(() => history.value.map((r) => r.soil_moisture))

// Header color = worst risk level across all EPDs
const headerBg = computed(() => {
  const levels = epds.value.map((e) => e.latest?.risk_level)
  if (levels.includes('CRITICAL')) return 'var(--red)'
  if (levels.includes('ATTENTION')) return 'var(--yellow)'
  return 'var(--green-dark)'
})
</script>

<style scoped>
.map-view {
  display: flex;
  flex-direction: column;
  height: 100dvh;
  overflow: hidden;
}

.map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  transition: background 0.8s ease;
  flex-shrink: 0;
  gap: 12px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--white);
  font-size: 13px;
  font-weight: 600;
  opacity: 0.85;
  transition: opacity 0.2s;
}
.back-btn:hover { opacity: 1; }

.header-center {
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand {
  font-family: var(--font-head);
  font-size: 18px;
  font-weight: 800;
  color: var(--white);
}

.layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.map-container {
  flex: 1;
  position: relative;
  min-width: 0;
}

.map-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(245, 245, 240, 0.8);
  color: var(--ink-faint);
  font-size: 14px;
  pointer-events: none;
  z-index: 500;
}

/* ── Sidebar ─────────────────────────────────── */
.sidebar {
  width: 320px;
  flex-shrink: 0;
  overflow-y: auto;
  background: var(--gray-light);
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-left: 1px solid var(--line);
}

.section-title {
  font-family: var(--font-head);
  font-size: 11px;
  font-weight: 700;
  color: var(--ink-faint);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 2px;
}

.empty-state {
  font-size: 13px;
  color: var(--ink-faint);
  text-align: center;
  padding: 24px 0;
}

/* ── EPD card ─────────────────────────────────── */
.epd-card {
  background: var(--white);
  border-radius: var(--r-md);
  padding: 12px 14px;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.18s, box-shadow 0.18s;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.epd-card:hover { border-color: var(--line); }
.epd-card.selected { border-color: var(--green-med); box-shadow: var(--shadow-md); }
.epd-card.selected.border-critical { border-color: var(--red); }
.epd-card.selected.border-attention { border-color: var(--yellow); }

.epd-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.epd-id-block {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.epd-uid {
  font-family: var(--font-head);
  font-size: 14px;
  font-weight: 800;
  color: var(--ink);
}

.epd-label {
  font-size: 11px;
  color: var(--ink-faint);
}

.risk-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 3px;
  flex-shrink: 0;
  transition: background 0.4s;
}

.epd-metrics-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.epd-moisture {
  font-family: var(--font-head);
  font-size: 30px;
  font-weight: 800;
  color: var(--ink);
  line-height: 1;
}

.pct {
  font-size: 15px;
  font-weight: 600;
  color: var(--ink-soft);
}

.risk-badge {
  font-family: var(--font-head);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--white);
  padding: 3px 9px;
  border-radius: 20px;
  text-transform: uppercase;
}

.epd-offline {
  font-size: 12px;
  color: var(--ink-faint);
}

/* ── Expanded detail ──────────────────────────── */
.chips {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chart-empty {
  font-size: 12px;
  color: var(--ink-faint);
  text-align: center;
  padding: 8px 0;
}

/* ── Mobile ───────────────────────────────────── */
@media (max-width: 700px) {
  .layout { flex-direction: column; }
  .map-container { min-height: 45dvh; }
  .sidebar {
    width: 100%;
    border-left: none;
    border-top: 1px solid var(--line);
    max-height: 55dvh;
  }
}
</style>
