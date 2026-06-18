<template>
  <section class="arch">
    <div class="arch-inner">
      <div class="arch-header">
        <h2 class="arch-title">{{ t('landing.arch_title') }}</h2>
        <p class="arch-sub">{{ t('landing.arch_sub') }}</p>
      </div>

      <!-- Flow: horizontal on desktop, rail on mobile -->
      <div class="arch-flow">
        <div v-for="(node, i) in nodes" :key="node.key" class="arch-flow-item">
          <!-- mobile rail dot -->
          <div class="arch-rail-dot" aria-hidden="true" />

          <div class="arch-node">
            <div class="arch-node-step">{{ String(i + 1).padStart(2, '0') }}</div>
            <div class="arch-node-icon">
              <component :is="node.icon" :size="18" color="var(--green-dark)" />
            </div>
            <div class="arch-node-body">
              <span class="arch-node-name">{{ t('landing.' + node.key) }}</span>
              <span class="arch-node-desc">{{ t('landing.' + node.key + '_desc') }}</span>
            </div>
          </div>

          <!-- desktop arrow -->
          <div v-if="i < nodes.length - 1" class="arch-arrow" aria-hidden="true">
            <svg width="20" height="12" viewBox="0 0 20 12" fill="none">
              <path d="M0 6h16M12 1l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>

      <!-- Protocol chips -->
      <div class="arch-protocol">
        <div class="arch-proto-item">
          <span class="arch-proto-label">ESP-NOW</span>
          <span class="arch-proto-desc">{{ locale === 'pt-BR' ? 'Sensor → Hub · sem roteador' : 'Sensor → Hub · no router needed' }}</span>
        </div>
        <div class="arch-proto-item">
          <span class="arch-proto-label">Serial USB</span>
          <span class="arch-proto-desc">{{ locale === 'pt-BR' ? 'Hub → servidor local' : 'Hub → local server' }}</span>
        </div>
        <div class="arch-proto-item">
          <span class="arch-proto-label">REST / HTTP</span>
          <span class="arch-proto-desc">{{ locale === 'pt-BR' ? 'Bridge → API · a cada 2s' : 'Bridge → API · every 2s' }}</span>
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
  gap: 32px;
}

.arch-header {
  display: flex;
  flex-direction: column;
  gap: 10px;
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

/* ── Flow: desktop horizontal ────────────*/
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

.arch-rail-dot { display: none; }

.arch-node-step { display: none; }

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
  width: 34px;
  height: 34px;
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

/* ── Protocol ────────────────────────────*/
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

/* ── Mobile: vertical rail ───────────────*/
@media (max-width: 600px) {
  .arch { padding: 52px 20px; }

  /* rail container */
  .arch-flow {
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    padding-left: 20px;
    position: relative;
  }

  /* continuous vertical line */
  .arch-flow::before {
    content: '';
    position: absolute;
    left: 28px;
    top: 18px;
    bottom: 18px;
    width: 2px;
    background: linear-gradient(to bottom, var(--green-med), var(--line));
    border-radius: 2px;
  }

  .arch-flow-item {
    flex-direction: row;
    align-items: center;
    gap: 14px;
    padding: 8px 0;
    position: relative;
  }

  /* dot on the rail */
  .arch-rail-dot {
    display: block;
    flex-shrink: 0;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--green-dark);
    border: 2px solid var(--gray-light);
    box-shadow: 0 0 0 2px var(--green-med);
    z-index: 1;
    position: relative;
  }

  /* desktop arrow hidden */
  .arch-arrow { display: none; }

  /* node: full width, step number visible */
  .arch-node {
    flex: 1;
    min-width: unset;
    padding: 12px 14px;
    gap: 12px;
  }

  .arch-node-step {
    display: block;
    font-family: var(--font-head);
    font-size: 10px;
    font-weight: 800;
    color: var(--green-med);
    letter-spacing: 0.08em;
    flex-shrink: 0;
    min-width: 20px;
  }

  .arch-node-name { font-size: 13px; }
  .arch-node-desc { font-size: 11px; }

  /* protocol: 2 cols then 1 */
  .arch-protocol { grid-template-columns: 1fr 1fr; }
  .arch-proto-item:last-child { grid-column: 1 / -1; }
}
</style>
