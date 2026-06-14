<template>
  <div class="alert-list">
    <h3 class="list-title">{{ t('map.alerts_title') }}</h3>
    <div v-if="alerts.length === 0" class="empty">Nenhum alerta ainda.</div>
    <ul v-else class="list">
      <li v-for="alert in alerts" :key="alert.id" class="alert-item" :class="`level-${alert.risk_level.toLowerCase()}`">
        <IcoWarn :size="14" :color="riskColor(alert.risk_level)" />
        <div class="alert-body">
          <span class="alert-level">{{ t(`risk.${alert.risk_level}`) }}</span>
          <span class="alert-detail">{{ alert.soil_moisture.toFixed(1) }}% umidade · {{ formatTime(alert.timestamp) }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import IcoWarn from '@/components/icons/IcoWarn.vue'
import type { AlertEntry } from '@/composables/useAlertHistory'

defineProps<{ alerts: AlertEntry[] }>()
const { t } = useI18n()

function riskColor(level: string): string {
  if (level === 'CRITICAL') return 'var(--red)'
  if (level === 'ATTENTION') return 'var(--yellow)'
  return 'var(--green-med)'
}

function formatTime(d: Date): string {
  return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}
</script>

<style scoped>
.alert-list {
  background: var(--white);
  border-radius: var(--r-md);
  padding: 16px;
  box-shadow: var(--shadow-sm);
}

.list-title {
  font-family: var(--font-head);
  font-size: 14px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 12px;
}

.empty {
  font-size: 13px;
  color: var(--ink-faint);
}

.list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.alert-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 10px;
  border-radius: var(--r-sm);
  background: var(--gray-light);
}

.level-critical { border-left: 3px solid var(--red); }
.level-attention { border-left: 3px solid var(--yellow); }

.alert-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.alert-level {
  font-size: 11px;
  font-weight: 700;
  color: var(--ink);
  letter-spacing: 0.04em;
}

.alert-detail {
  font-size: 11px;
  color: var(--ink-faint);
}
</style>
