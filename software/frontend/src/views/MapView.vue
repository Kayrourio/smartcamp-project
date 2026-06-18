<template>
  <div class="map-view">
    <OfflineModal />
    <!-- Header -->
    <header
      class="map-header"
      :style="{ background: headerBg, color: headerTextColor }"
    >
      <RouterLink to="/" class="back-btn" :style="{ color: headerTextColor }">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M10 3L5 8L10 13" :stroke="headerTextColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        {{ t('map.back') }}
      </RouterLink>
      <div class="header-center">
        <LogoMark />
        <span class="brand" :style="{ color: headerTextColor }">TerraSafe</span>
      </div>
      <LiveBadge />
    </header>

    <!-- Mobile tab bar -->
    <div class="mobile-tabs">
      <button
        class="tab-btn"
        :class="{ active: mobileTab === 'map' }"
        @click="mobileTab = 'map'"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/>
        </svg>
        Mapa
      </button>
      <button
        class="tab-btn"
        :class="{ active: mobileTab === 'list' }"
        @click="mobileTab = 'list'"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/>
          <circle cx="3" cy="6" r="1" fill="currentColor"/><circle cx="3" cy="12" r="1" fill="currentColor"/><circle cx="3" cy="18" r="1" fill="currentColor"/>
        </svg>
        Sensores ({{ epds.length }})
      </button>
    </div>

    <!-- Layout -->
    <div class="layout" :class="{ 'mobile-show-map': mobileTab === 'map', 'mobile-show-list': mobileTab === 'list' }">
      <!-- Map -->
      <div class="map-container">
        <LiveMap
          ref="liveMapRef"
          :epds="epds"
          :rain-grid="rainGrid"
          :selected-uid="selectedUid"
          @select-epd="selectEpdFromMap"
        />
        <div v-if="isLoading && epds.length === 0" class="map-overlay">
          Carregando sensores...
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="sidebar">
        <!-- Alert banner (sticky at top) -->
        <AlertList v-if="alerts.length > 0" :alerts="alerts" />

        <!-- Risk distribution heat map legend -->
        <div v-if="riskRows.length" class="risk-dist">
          <div class="section-title">Distribuição de Risco</div>
          <div class="risk-bars">
            <div v-for="item in riskRows" :key="item.key" class="risk-bar-row">
              <span class="risk-bar-dot" :style="{ background: item.color }" />
              <span class="risk-bar-label">{{ item.label }}</span>
              <div class="risk-bar-track">
                <div class="risk-bar-fill" :style="{ width: item.pct + '%', background: item.color }" />
              </div>
              <span class="risk-bar-pct">{{ item.pct }}%</span>
            </div>
          </div>
        </div>

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
            'border-high': epd.latest?.risk_level === 'HIGH' && epd.epd_uid === selectedUid,
            'border-attention': epd.latest?.risk_level === 'ATTENTION' && epd.epd_uid === selectedUid,
            'no-coords': epd.lat == null || epd.lng == null,
          }"
          @click="selectEpd(epd.epd_uid)"
        >
          <!-- Card header -->
          <div class="epd-row">
            <div class="epd-id-block">
              <span class="epd-uid">{{ epd.epd_uid }}</span>
              <span v-if="epd.label" class="epd-label">{{ epd.label }}</span>
            </div>
            <div class="epd-header-right">
              <!-- No-coordinates warning -->
              <span
                v-if="epd.lat == null || epd.lng == null"
                class="no-coords-badge"
                title="Sensor sem localização cadastrada,não aparece no mapa"
              >
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <line x1="12" y1="7" x2="12" y2="12"/><circle cx="12" cy="16" r=".5" fill="currentColor"/>
                </svg>
                Sem GPS
              </span>
              <div
                class="risk-dot"
                :title="epd.latest?.risk_level ?? 'SEM LEITURA'"
                :style="{ background: riskColor(epd.latest?.risk_level) }"
              />
            </div>
          </div>

          <!-- Moisture + risk badge + timestamp -->
          <div v-if="epd.latest" class="epd-metrics-row">
            <span class="epd-moisture">
              {{ epd.latest.soil_moisture.toFixed(0) }}<span class="pct">%</span>
            </span>
            <div class="epd-meta">
              <span class="risk-badge" :style="{ background: riskColor(epd.latest.risk_level) }">
                {{ riskLabel(epd.latest.risk_level) }}
              </span>
              <span class="last-seen">{{ relativeTime(epd.latest.received_at) }}</span>
            </div>
          </div>
          <div v-else class="epd-offline">Sem leitura</div>

          <!-- Tilt / landslide alert -->
          <div v-if="epd.latest?.tilt_detected" class="tilt-alert" :class="epd.latest.risk_level === 'CRITICAL' ? 'tilt-alert--critical' : 'tilt-alert--warning'">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/><circle cx="12" cy="17" r=".5" fill="currentColor"/>
            </svg>
            <span v-if="epd.latest.risk_level === 'CRITICAL'">Alerta de desabamento!</span>
            <span v-else>Sensor inclinado/caído</span>
          </div>

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
              v-if="epd.latest.angle_x !== null"
              label="Inclinação X"
              :value="epd.latest.angle_x"
              unit="°"
            >
              <template #icon>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--ink-soft)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
                </svg>
              </template>
            </MetricChip>
          </div>

          <!-- History chart: only for the selected EPD -->
          <template v-if="epd.epd_uid === selectedUid">
            <HumidityChart
              v-if="chartData.length > 0"
              :data="chartData"
              :labels="chartLabels"
            />
            <div v-else class="chart-empty">Aguardando histórico...</div>
          </template>
        </div>

        <!-- Alert list at bottom only when no alerts (so it shows a "no alerts" state) -->
        <AlertList v-if="alerts.length === 0" :alerts="alerts" />
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
import type { RiskLevel, EpdOut } from '@/types/sensor'
import LiveMap from '@/components/map/LiveMap.vue'
import LiveBadge from '@/components/dashboard/LiveBadge.vue'
import MetricChip from '@/components/dashboard/MetricChip.vue'
import HumidityChart from '@/components/dashboard/HumidityChart.vue'
import AlertList from '@/components/dashboard/AlertList.vue'
import LogoMark from '@/components/icons/LogoMark.vue'
import OfflineModal from '@/components/OfflineModal.vue'
import IcoRain from '@/components/icons/IcoRain.vue'
import IcoTemp from '@/components/icons/IcoTemp.vue'

const { t } = useI18n()

const { epds, isLoading } = useEpdList()
const { grid: rainGrid } = useRainGrid()
const { alerts } = useAlertHistory(epds)

const selectedUid = ref<string | null>(null)
const { history } = useEpdHistory(selectedUid)
const liveMapRef = ref<InstanceType<typeof LiveMap> | null>(null)
const mobileTab = ref<'map' | 'list'>('map')

// Auto-select first EPD on first load,no fly, just highlights the card
watch(
  epds,
  (list) => {
    if (!selectedUid.value && list.length > 0) {
      selectedUid.value = list[0].epd_uid
    }
  },
  { immediate: true },
)

// User clicked a card in the sidebar,select + fly
function selectEpd(uid: string) {
  selectedUid.value = uid
  liveMapRef.value?.flyToEpd(uid)
  mobileTab.value = 'map'
}

// User clicked a marker on the map,select only (already centered)
function selectEpdFromMap(uid: string) {
  selectedUid.value = uid
}

const RISK_COLORS: Record<string, string> = {
  SAFE: '#52B788',
  ATTENTION: '#F1C40F',
  HIGH: '#E67E22',
  CRITICAL: '#C0392B',
}
const RISK_LABELS: Record<string, string> = {
  SAFE: 'Seguro',
  ATTENTION: 'Atenção',
  HIGH: 'Alto',
  CRITICAL: 'Crítico',
}

function riskColor(level?: RiskLevel | null): string {
  return RISK_COLORS[level ?? 'SAFE'] ?? '#52B788'
}

function riskLabel(level: RiskLevel): string {
  return RISK_LABELS[level] ?? level
}

function relativeTime(dateStr: string): string {
  const diff = Math.floor((Date.now() - new Date(dateStr).getTime()) / 60_000)
  if (diff < 1) return 'agora'
  if (diff === 1) return 'há 1 min'
  if (diff < 60) return `há ${diff} min`
  const h = Math.floor(diff / 60)
  return h === 1 ? 'há 1h' : `há ${h}h`
}

// Risk distribution: rows ready for the template (% per risk level)
const RISK_ROW_META = [
  { key: 'SAFE'      as const, label: 'Seguro',  color: '#52B788' },
  { key: 'ATTENTION' as const, label: 'Atenção', color: '#F1C40F' },
  { key: 'HIGH'      as const, label: 'Alto',    color: '#E67E22' },
  { key: 'CRITICAL'  as const, label: 'Crítico', color: '#C0392B' },
]
const riskRows = computed(() => {
  const active = epds.value.filter((e: EpdOut) => e.latest)
  const total = active.length
  if (!total) return []
  const counts = { SAFE: 0, ATTENTION: 0, HIGH: 0, CRITICAL: 0 }
  for (const epd of active) counts[epd.latest!.risk_level]++
  return RISK_ROW_META.map((m) => ({
    ...m,
    pct: Math.round(counts[m.key] / total * 100),
  }))
})

// Chart: moisture history + time labels of selected EPD
const chartData = computed(() => history.value.map((r) => r.soil_moisture))
const chartLabels = computed(() =>
  history.value.map((r) => {
    const d = new Date(r.received_at)
    return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
  }),
)

// Header background = worst risk level across all EPDs
const headerBg = computed(() => {
  const levels = epds.value.map((e) => e.latest?.risk_level)
  if (levels.includes('CRITICAL')) return 'var(--red)'
  if (levels.includes('HIGH')) return '#E67E22'
  if (levels.includes('ATTENTION')) return 'var(--yellow)'
  return 'var(--green-dark)'
})

// Yellow background needs dark text for contrast (WCAG AA)
const headerTextColor = computed(() => {
  const levels = epds.value.map((e) => e.latest?.risk_level)
  if (!levels.includes('CRITICAL') && !levels.includes('HIGH') && levels.includes('ATTENTION')) {
    return '#1a1a0f'
  }
  return '#ffffff'
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
  transition: background 0.8s ease, color 0.4s ease;
  flex-shrink: 0;
  gap: 12px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
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
  transition: color 0.4s ease;
}

/* ── Mobile tab bar ───────────────────────────────── */
.mobile-tabs {
  display: none;
  flex-shrink: 0;
  background: var(--white);
  border-bottom: 1px solid var(--line);
}

.tab-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 0;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink-faint);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: color 0.15s, border-color 0.15s;
}
.tab-btn.active {
  color: var(--green-dark);
  border-bottom-color: var(--green-dark);
}

/* ── Layout ───────────────────────────────────────── */
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

/* ── Sidebar ─────────────────────────────────────── */
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

/* ── EPD card ─────────────────────────────────────── */
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
.epd-card.selected.border-high { border-color: #E67E22; }
.epd-card.selected.border-attention { border-color: var(--yellow); }
.epd-card.no-coords { opacity: 0.85; }

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

.epd-header-right {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 2px;
}

.no-coords-badge {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 10px;
  font-weight: 600;
  color: #a05000;
  background: #fff3e0;
  border: 1px solid #ffe0b2;
  border-radius: 20px;
  padding: 2px 7px 2px 5px;
  white-space: nowrap;
}

.risk-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
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

.epd-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
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

.last-seen {
  font-size: 10px;
  color: var(--ink-faint);
  padding-left: 2px;
}

.epd-offline {
  font-size: 12px;
  color: var(--ink-faint);
}

/* ── Expanded detail ──────────────────────────────── */
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

/* ── Mobile ───────────────────────────────────────── */
@media (max-width: 700px) {
  .mobile-tabs { display: flex; }

  .layout {
    flex-direction: column;
    position: relative;
  }

  .map-container {
    position: absolute;
    inset: 0;
    transition: opacity 0.2s, pointer-events 0s;
  }

  .sidebar {
    position: absolute;
    inset: 0;
    width: 100%;
    border-left: none;
    border-top: none;
    max-height: none;
    transition: opacity 0.2s, pointer-events 0s;
  }

  /* Show/hide via tabs */
  .mobile-show-map .map-container { opacity: 1; pointer-events: auto; z-index: 1; }
  .mobile-show-map .sidebar       { opacity: 0; pointer-events: none;  z-index: 0; }

  .mobile-show-list .map-container { opacity: 0; pointer-events: none;  z-index: 0; }
  .mobile-show-list .sidebar       { opacity: 1; pointer-events: auto;  z-index: 1; }
}
</style>

<style scoped>
/* ── Tilt / landslide alert ────────────────────────── */
.tilt-alert {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 8px;
  letter-spacing: 0.02em;
}
.tilt-alert--warning {
  background: #fff3e0;
  color: #a05000;
  border: 1px solid #ffe0b2;
}
.tilt-alert--critical {
  background: #fdecea;
  color: #b71c1c;
  border: 1px solid #f5c6cb;
  animation: pulse-alert 1.4s ease-in-out infinite;
}
@keyframes pulse-alert {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.65; }
}

/* ── Risk distribution panel ───────────────────────── */
.risk-dist {
  background: var(--white);
  border-radius: var(--r-md);
  padding: 10px 14px 12px;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.risk-bars {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.risk-bar-row {
  display: flex;
  align-items: center;
  gap: 7px;
}

.risk-bar-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.risk-bar-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--ink-soft);
  width: 46px;
  flex-shrink: 0;
}

.risk-bar-track {
  flex: 1;
  height: 6px;
  background: var(--line);
  border-radius: 3px;
  overflow: hidden;
}

.risk-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
  min-width: 2px;
}

.risk-bar-pct {
  font-size: 11px;
  font-weight: 700;
  color: var(--ink);
  width: 28px;
  text-align: right;
  flex-shrink: 0;
}
</style>
