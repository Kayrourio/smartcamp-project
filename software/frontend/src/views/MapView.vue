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
        <div class="map-controls">
          <LayerToggle v-model="activeLayer" />
        </div>
        <LiveMap
          v-if="data"
          :soil-moisture="data.soil_moisture"
          :active-layer="activeLayer"
        />
        <div v-else class="map-placeholder">Carregando mapa...</div>
      </div>

      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sensor-info">
          <span class="sensor-id">EPD-01</span>
          <span class="sensor-loc">{{ t('map.sensor_location') }}</span>
          <span class="sensor-status" :class="{ online: data?.online }">
            ● {{ data?.online ? t('map.online') : 'offline' }}
          </span>
        </div>

        <StatusBar v-if="data" :risk-level="data.risk_level" />

        <MetricFeature
          v-if="data"
          :moisture="data.soil_moisture"
          :risk-level="data.risk_level"
        />

        <div class="chips">
          <MetricChip
            :label="t('map.metric_rainfall')"
            :value="data?.rainfall ?? null"
            unit=" mm"
            :sub="t('map.rainfall_sub')"
          >
            <template #icon>
              <IcoRain :size="20" color="var(--blue)" />
            </template>
          </MetricChip>

          <MetricChip
            :label="t('map.metric_temp')"
            :value="data?.temperature ?? null"
            unit="°C"
            :sub="t('map.temp_sub')"
          >
            <template #icon>
              <IcoTemp :size="20" color="var(--brown)" />
            </template>
          </MetricChip>

          <MetricChip
            :label="t('map.metric_lux')"
            :value="data?.lux ?? null"
            unit=" lx"
          >
            <template #icon>
              <IcoSun :size="20" color="var(--yellow)" />
            </template>
          </MetricChip>
        </div>

        <HumidityChart :data="chartData" />

        <AlertList :alerts="alerts" />
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLiveData } from '@/composables/useLiveData'
import { useAlertHistory } from '@/composables/useAlertHistory'
import LiveMap from '@/components/map/LiveMap.vue'
import LayerToggle from '@/components/map/LayerToggle.vue'
import LiveBadge from '@/components/dashboard/LiveBadge.vue'
import StatusBar from '@/components/dashboard/StatusBar.vue'
import MetricFeature from '@/components/dashboard/MetricFeature.vue'
import MetricChip from '@/components/dashboard/MetricChip.vue'
import HumidityChart from '@/components/dashboard/HumidityChart.vue'
import AlertList from '@/components/dashboard/AlertList.vue'
import LogoMark from '@/components/icons/LogoMark.vue'
import IcoRain from '@/components/icons/IcoRain.vue'
import IcoTemp from '@/components/icons/IcoTemp.vue'
import IcoSun from '@/components/icons/IcoSun.vue'

const { t } = useI18n()
const activeLayer = ref('soil')
const { data } = useLiveData()
const { alerts } = useAlertHistory(data)

const chartData = ref<number[]>([])
const MAX_CHART_POINTS = 30

watch(data, (v) => {
  if (!v) return
  chartData.value.push(v.soil_moisture)
  if (chartData.value.length > MAX_CHART_POINTS) chartData.value.shift()
})

const headerBg = computed(() => {
  if (!data.value) return 'var(--green-dark)'
  return { SAFE: 'var(--green-dark)', ATTENTION: 'var(--yellow)', CRITICAL: 'var(--red)' }[data.value.risk_level] ?? 'var(--green-dark)'
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

.map-controls {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 1000;
}

.map-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ink-faint);
  font-size: 14px;
  background: var(--gray-light);
}

.sidebar {
  width: 340px;
  flex-shrink: 0;
  overflow-y: auto;
  background: var(--gray-light);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-left: 1px solid var(--line);
}

.sensor-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 12px 0 4px;
}

.sensor-id {
  font-family: var(--font-head);
  font-size: 18px;
  font-weight: 800;
  color: var(--ink);
}

.sensor-loc {
  font-size: 13px;
  color: var(--ink-soft);
}

.sensor-status {
  font-size: 12px;
  font-weight: 600;
  color: var(--ink-faint);
}

.sensor-status.online { color: var(--green-med); }

.chips {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Mobile: stack vertically */
@media (max-width: 700px) {
  .layout { flex-direction: column; }
  .map-container { min-height: 50dvh; }
  .sidebar {
    width: 100%;
    border-left: none;
    border-top: 1px solid var(--line);
    overflow-y: auto;
    max-height: 50dvh;
  }
}
</style>
