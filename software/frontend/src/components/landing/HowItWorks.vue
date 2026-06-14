<template>
  <section class="how">
    <div class="how-inner">
      <h2 class="title">{{ t('landing.how_title') }}</h2>
      <p class="sub">{{ t('landing.how_sub') }}</p>
      <div class="steps">
        <div v-for="(step, i) in steps" :key="i" class="step">
          <div class="step-icon">
            <component :is="icons[i]" :size="28" :color="'var(--green-dark)'" />
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
  background: var(--gray-light);
  padding: 64px 24px;
}

.how-inner {
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.title {
  font-family: var(--font-head);
  font-size: 28px;
  font-weight: 800;
  color: var(--ink);
}

.sub {
  font-size: 15px;
  color: var(--ink-soft);
  margin-top: -28px;
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.step {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.step-icon {
  width: 52px;
  height: 52px;
  background: var(--white);
  border-radius: var(--r-md);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
  flex-shrink: 0;
}

.step-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.step-n {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--green-med);
}

.step-title {
  font-family: var(--font-head);
  font-size: 18px;
  font-weight: 700;
  color: var(--ink);
}

.step-desc {
  font-size: 14px;
  color: var(--ink-soft);
  line-height: 1.6;
}
</style>
