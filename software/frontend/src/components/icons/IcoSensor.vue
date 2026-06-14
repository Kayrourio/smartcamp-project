<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="9" y="2" width="6" height="12" rx="3" :stroke="color" stroke-width="1.5" />
    <line x1="12" y1="14" x2="12" y2="22" :stroke="color" stroke-width="1.5" stroke-linecap="round" />
    <line x1="8" y1="22" x2="16" y2="22" :stroke="color" stroke-width="1.5" stroke-linecap="round" />
    <circle cx="12" cy="8" r="1.5" :fill="color" />
  </svg>
</template>
<script setup lang="ts">
withDefaults(defineProps<{ size?: number; color?: string }>(), {
  size: 24,
  color: 'currentColor',
})
</script>
