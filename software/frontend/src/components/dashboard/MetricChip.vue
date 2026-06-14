<template>
  <div class="metric-chip">
    <slot name="icon" />
    <div class="info">
      <span class="label">{{ label }}</span>
      <span class="value">{{ value !== null ? value.toFixed(1) + unit : '—' }}</span>
      <span v-if="sub" class="sub">{{ sub }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  value: number | null
  unit: string
  sub?: string
}>()
</script>

<style scoped>
.metric-chip {
  background: var(--white);
  border-radius: var(--r-md);
  padding: 14px;
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  gap: 12px;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.label {
  font-size: 12px;
  color: var(--ink-faint);
  font-weight: 500;
}

.value {
  font-family: var(--font-head);
  font-size: 22px;
  font-weight: 700;
  color: var(--ink);
  line-height: 1;
}

.sub {
  font-size: 11px;
  color: var(--ink-faint);
}
</style>
