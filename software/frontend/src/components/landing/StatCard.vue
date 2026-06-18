<template>
  <div class="stat-card" :class="`accent-${accent}`">
    <div class="accent-bar" />
    <div class="num">{{ num }}</div>
    <div class="tag">{{ tag }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ num: string; tag: string; accent?: 'red' | 'yellow' | 'green' }>()
</script>

<style scoped>
.stat-card {
  background: var(--white);
  border-radius: var(--r-md);
  padding: 20px 18px 18px;
  border: 1px solid var(--line);
  display: flex;
  flex-direction: column;
  gap: 5px;
  position: relative;
  overflow: hidden;
}

.accent-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  border-radius: 0;
}

.accent-red .accent-bar   { background: var(--red); }
.accent-yellow .accent-bar { background: var(--yellow); }
.accent-green .accent-bar  { background: var(--green-med); }

.num {
  font-family: var(--font-head);
  font-size: 26px;
  font-weight: 800;
  color: var(--ink);
  line-height: 1;
  margin-top: 4px;
}

.tag {
  font-size: 12px;
  color: var(--ink-soft);
  line-height: 1.45;
}

@media (max-width: 520px) {
  .stat-card {
    flex-direction: row;
    align-items: center;
    gap: 14px;
    padding: 14px 16px 14px 18px;
  }
  .accent-bar {
    top: 0; left: 0; right: auto; bottom: 0;
    width: 3px;
    height: auto;
    border-radius: 0;
  }
  .num { font-size: 22px; white-space: nowrap; }
}
</style>
