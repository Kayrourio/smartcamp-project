<template>
  <section class="arch">
    <div class="arch-inner">
      <div class="arch-header">
        <h2 class="arch-title">{{ t('landing.arch_title') }}</h2>
        <p class="arch-sub">{{ t('landing.arch_sub') }}</p>
      </div>

      <!-- Flow vertical on mobile, horizontal on desktop -->
      <div class="arch-flow">
        <div v-for="(node, i) in nodes" :key="node.key" class="arch-flow-item">
          <div class="arch-node">
            <div class="arch-node-icon">
              <component :is="node.icon" :size="20" color="var(--green-dark)" />
            </div>
            <div class="arch-node-body">
              <span class="arch-node-name">{{ t('landing.' + node.key) }}</span>
              <span class="arch-node-desc">{{ t('landing.' + node.key + '_desc') }}</span>
            </div>
          </div>
          <div v-if="i < nodes.length - 1" class="arch-arrow">
            <svg class="arrow-h" width="20" height="12" viewBox="0 0 20 12" fill="none">
              <path d="M0 6h16M12 1l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg class="arrow-v" width="12" height="20" viewBox="0 0 12 20" fill="none">
              <path d="M6 0v16M1 12l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>

      <!-- Protocol badges -->
      <div class="arch-protocol">
        <div class="arch-proto-item">
          <span class="arch-proto-label">ESP-NOW</span>
          <span class="arch-proto-desc">{{ locale === 'pt-BR' ? 'Sensor → Hub (sem roteador)' : 'Sensor → Hub (no router needed)' }}</span>
        </div>
        <div class="arch-proto-item">
          <span class="arch-proto-label">Serial USB</span>
          <span class="arch-proto-desc">{{ locale === 'pt-BR' ? 'Hub → servidor local' : 'Hub → local server' }}</span>
        </div>
        <div class="arch-proto-item">
          <span class="arch-proto-label">REST / HTTP</span>
          <span class="arch-proto-desc">{{ locale === 'pt-BR' ? 'Bridge → API · atualiza a cada 2s' : 'Bridge → API · updates every 2s' }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import IcoSensor from '@/components/icons/IcoSensor.vue'
import IcoMesh from '@/components/icons/IcoMesh.vue'
import IcoMapAlert from '@/components/icons/IcoMapAlert.vue'

const { t, locale } = useI18n()

const nodes = [
  { key: 'arch_flow_epd',      icon: IcoSensor },
  { key: 'arch_flow_cpd',      icon: IcoMesh },
  { key: 'arch_flow_bridge',   icon: IcoSensor },
  { key: 'arch_flow_backend',  icon: IcoMesh },
  { key: 'arch_flow_frontend', icon: IcoMapAlert },
]
</script>

<style scoped>
.arch {
  background: var(--gray-light);
  padding: 72px 24px;
}

.arch-inner {
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.arch-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.arch-title {
  font-family: var(--font-head);
  font-size: 28px;
  font-weight: 800;
  color: var(--ink);
  margin: 0;
  letter-spacing: -0.01em;
}

.arch-sub {
  font-size: 15px;
  color: var(--ink-soft);
  margin: 0;
  line-height: 1.6;
}

/* ── Flow ─────────────────────────────── */
.arch-flow {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
}

.arch-flow-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.arch-node {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--white);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 10px 14px;
  min-width: 110px;
  box-shadow: var(--shadow-sm);
}

.arch-node-icon {
  width: 36px;
  height: 36px;
  background: var(--gray-light);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.arch-node-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.arch-node-name {
  font-family: var(--font-head);
  font-size: 12px;
  font-weight: 700;
  color: var(--ink);
}

.arch-node-desc {
  font-size: 10px;
  color: var(--ink-faint);
  line-height: 1.3;
}

.arch-arrow {
  color: var(--ink-faint);
  flex-shrink: 0;
}
.arrow-v { display: none; }

/* ── Protocol row ─────────────────────── */
.arch-protocol {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.arch-proto-item {
  background: var(--white);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.arch-proto-label {
  font-family: var(--font-head);
  font-size: 11px;
  font-weight: 800;
  color: var(--green-dark);
  letter-spacing: 0.06em;
}

.arch-proto-desc {
  font-size: 11px;
  color: var(--ink-soft);
  line-height: 1.4;
}

@media (max-width: 600px) {
  .arch-flow { flex-direction: column; align-items: flex-start; }
  .arch-flow-item { flex-direction: column; align-items: flex-start; }
  .arch-arrow { padding-left: 23px; }
  .arrow-h { display: none; }
  .arrow-v { display: block; }
  .arch-protocol { grid-template-columns: 1fr; }
}
</style>
