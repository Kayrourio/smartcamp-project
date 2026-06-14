<template>
  <div class="stat-card">
    <div class="num">{{ num }}</div>
    <div class="tag">{{ tag }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ num: string; tag: string }>()
</script>

<style scoped>
.stat-card {
  background: var(--white);
  border-radius: var(--r-lg);
  padding: 24px 20px;
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
  min-width: 140px;
}

.num {
  font-family: var(--font-head);
  font-size: 28px;
  font-weight: 800;
  color: var(--ink);
  line-height: 1;
}

.tag {
  font-size: 13px;
  color: var(--ink-soft);
  line-height: 1.4;
}
</style>
