import { computed } from 'vue'
import type { Ref } from 'vue'

type RiskLevel = 'SAFE' | 'ATTENTION' | 'CRITICAL'

export function useRiskLevel(riskLevel: Ref<RiskLevel | undefined>) {
  const color = computed(() => {
    const map: Record<RiskLevel, string> = {
      SAFE: 'var(--green-med)',
      ATTENTION: 'var(--yellow)',
      CRITICAL: 'var(--red)',
    }
    return map[riskLevel.value ?? 'SAFE']
  })

  const bgClass = computed(() => {
    const map: Record<RiskLevel, string> = {
      SAFE: 'risk-safe',
      ATTENTION: 'risk-attention',
      CRITICAL: 'risk-critical',
    }
    return map[riskLevel.value ?? 'SAFE']
  })

  const i18nKey = computed(() => `risk.${riskLevel.value ?? 'SAFE'}`)

  return { color, bgClass, i18nKey }
}
