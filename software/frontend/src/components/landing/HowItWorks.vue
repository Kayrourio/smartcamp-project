<template>
  <section class="how">
    <div class="how-inner">
      <div class="how-header">
        <h2 class="title">{{ t('landing.how_title') }}</h2>
        <p class="sub">{{ t('landing.how_sub') }}</p>
      </div>
      <div class="steps">
        <div v-for="(step, i) in steps" :key="i" class="step">
          <div class="step-left">
            <div class="step-icon">
              <component :is="icons[i]" :size="24" :color="'var(--green-dark)'" />
            </div>
            <div v-if="i < steps.length - 1" class="step-connector" />
          </div>
          <div class="step-body">
            <span class="step-n">{{ step.n }}</span>
            <h3 class="step-title">{{ step.title }}</h3>
            <p class="step-desc">{{ step.desc }}</p>
          </div>
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

const { t, tm } = useI18n()
const steps = tm('landing.steps') as { n: string; title: string; desc: string }[]
const icons = [IcoSensor, IcoMesh, IcoMapAlert]
</script>

<style scoped>
.how {
  background: var(--white);
  padding: 72px 24px;
  border-bottom: 1px solid var(--line);
}

.how-inner {
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.how-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.title {
  font-family: var(--font-head);
  font-size: 28px;
  font-weight: 800;
  color: var(--ink);
  margin: 0;
  letter-spacing: -0.01em;
}

.sub {
  font-size: 15px;
  color: var(--ink-soft);
  margin: 0;
  line-height: 1.6;
}

/* ── Steps ───────────────────────────────*/
.steps {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.step {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.step-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.step-icon {
  width: 52px;
  height: 52px;
  background: var(--gray-light);
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

.step-connector {
  width: 2px;
  flex: 1;
  min-height: 24px;
  background: var(--line);
  margin: 6px 0;
}

.step-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-bottom: 32px;
  padding-top: 10px;
}

.step:last-child .step-body {
  padding-bottom: 0;
}

.step-n {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--green-med);
}

.step-title {
  font-family: var(--font-head);
  font-size: 18px;
  font-weight: 700;
  color: var(--ink);
  margin: 0;
  letter-spacing: -0.01em;
}

.step-desc {
  font-size: 14px;
  color: var(--ink-soft);
  line-height: 1.65;
  margin: 0;
  max-width: 480px;
}

@media (max-width: 480px) {
  .how { padding: 52px 20px; }
  .step-icon { width: 44px; height: 44px; }
  .step-title { font-size: 16px; }
}
</style>
