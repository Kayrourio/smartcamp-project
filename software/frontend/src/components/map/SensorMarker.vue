<template>
  <!-- Rendered into Leaflet DivIcon — no template root needed -->
  <div class="sensor-marker">
    <div class="marker-label">{{ sensorId }} · {{ moisture }}%</div>
    <div class="marker-pin">
      <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="18" cy="10" rx="9" ry="6" fill="#6B4528" />
        <rect x="9" y="10" width="18" height="14" rx="2" fill="#4F6A2E" />
        <ellipse cx="18" cy="24" rx="9" ry="6" fill="#6E8B43" />
        <circle cx="18" cy="10" r="3" fill="#FFFFFF" opacity="0.5" />
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ sensorId: string; moisture: number }>()
</script>

<style scoped>
.sensor-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.marker-label {
  background: var(--ink);
  color: var(--white);
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 20px;
  white-space: nowrap;
}

.marker-pin {
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}
</style>
