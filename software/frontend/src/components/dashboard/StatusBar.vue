<template>
  <div class="status-bar" :class="bgClass">
    <IcoWarn :size="18" color="white" />
    <span>{{ t(i18nKey) }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRiskLevel } from '@/composables/useRiskLevel'
import IcoWarn from '@/components/icons/IcoWarn.vue'

const props = defineProps<{ riskLevel: 'SAFE' | 'ATTENTION' | 'CRITICAL' }>()
const { t } = useI18n()

const riskRef = computed(() => props.riskLevel)
const { bgClass, i18nKey } = useRiskLevel(riskRef)
</script>

<style scoped>
.status-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: var(--r-sm);
  color: var(--white);
  font-family: var(--font-head);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  transition: background 0.8s ease;
}

.risk-safe { background: var(--green-med); }
.risk-attention { background: var(--yellow); }
.risk-critical { background: var(--red); }
</style>
