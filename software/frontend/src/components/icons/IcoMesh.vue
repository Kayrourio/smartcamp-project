<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="4" cy="12" r="2" :stroke="color" stroke-width="1.5" />
    <circle cx="12" cy="4" r="2" :stroke="color" stroke-width="1.5" />
    <circle cx="20" cy="12" r="2" :stroke="color" stroke-width="1.5" />
    <circle cx="12" cy="20" r="2" :stroke="color" stroke-width="1.5" />
    <circle cx="12" cy="12" r="2" :stroke="color" stroke-width="1.5" />
    <line x1="6" y1="12" x2="10" y2="12" :stroke="color" stroke-width="1.5" />
    <line x1="14" y1="12" x2="18" y2="12" :stroke="color" stroke-width="1.5" />
    <line x1="12" y1="6" x2="12" y2="10" :stroke="color" stroke-width="1.5" />
    <line x1="12" y1="14" x2="12" y2="18" :stroke="color" stroke-width="1.5" />
  </svg>
</template>
<script setup lang="ts">
withDefaults(defineProps<{ size?: number; color?: string }>(), {
  size: 24,
  color: 'currentColor',
})
</script>
