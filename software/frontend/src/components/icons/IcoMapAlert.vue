<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" :stroke="color" stroke-width="1.5" />
    <line x1="12" y1="7" x2="12" y2="11" :stroke="color" stroke-width="1.5" stroke-linecap="round" />
    <circle cx="12" cy="13.5" r="0.75" :fill="color" />
  </svg>
</template>
<script setup lang="ts">
withDefaults(defineProps<{ size?: number; color?: string }>(), {
  size: 24,
  color: 'currentColor',
})
</script>
