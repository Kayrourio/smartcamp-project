<template>
  <div class="layer-toggle">
    <button
      v-for="layer in layers"
      :key="layer.key"
      :class="['toggle-btn', { active: modelValue === layer.key }]"
      @click="emit('update:modelValue', layer.key)"
    >
      {{ layer.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

defineProps<{ modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [val: string] }>()

const { t } = useI18n()
const layers = [
  { key: 'soil', label: t('map.layer_soil') },
  { key: 'clouds', label: t('map.layer_clouds') },
]
</script>

<style scoped>
.layer-toggle {
  display: flex;
  gap: 4px;
  background: var(--white);
  border-radius: var(--r-sm);
  padding: 3px;
  box-shadow: var(--shadow-sm);
}

.toggle-btn {
  border: none;
  background: transparent;
  padding: 6px 14px;
  border-radius: 6px;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 500;
  color: var(--ink-soft);
  transition: all 0.2s;
}

.toggle-btn.active {
  background: var(--green-dark);
  color: var(--white);
}
</style>
