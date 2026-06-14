<template>
  <div class="metric-feature">
    <div class="header">
      <IcoDrop :size="20" :color="riskColor" />
      <span class="label">{{ t('map.metric_moisture') }}</span>
      <span class="badge" :class="bgClass">{{ t(i18nKey).replace('NÍVEL ', '') }}</span>
    </div>
    <div class="value">{{ moisture.toFixed(1) }}<span class="unit">%</span></div>
    <div class="bar-track">
      <div class="bar-fill" :style="{ width: moisture + '%', background: riskColor }" />
    </div>
    <div class="sub">{{ t('map.trend_rising') }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRiskLevel } from '@/composables/useRiskLevel'
import IcoDrop from '@/components/icons/IcoDrop.vue'

const props = defineProps<{ moisture: number; riskLevel: 'SAFE' | 'ATTENTION' | 'CRITICAL' }>()
const { t } = useI18n()

const riskRef = computed(() => props.riskLevel)
const { color: riskColor, bgClass, i18nKey } = useRiskLevel(riskRef)
</script>

<style scoped>
.metric-feature {
  background: var(--white);
  border-radius: var(--r-md);
  padding: 16px;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.header {
  display: flex;
  align-items: center;
  gap: 6px;
}

.label {
  flex: 1;
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--ink-soft);
  font-weight: 500;
}

.badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 2px 8px;
  border-radius: 20px;
  color: var(--white);
}

.risk-safe { background: var(--green-med); }
.risk-attention { background: var(--yellow); }
.risk-critical { background: var(--red); }

.value {
  font-family: var(--font-head);
  font-size: 48px;
  font-weight: 800;
  line-height: 1;
  color: var(--ink);
}

.unit {
  font-size: 24px;
  font-weight: 600;
  color: var(--ink-soft);
}

.bar-track {
  height: 6px;
  background: var(--line);
  border-radius: 3px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease, background 0.6s ease;
}

.sub {
  font-size: 12px;
  color: var(--ink-faint);
}
</style>
