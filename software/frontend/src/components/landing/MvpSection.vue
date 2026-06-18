<template>
  <section class="mvp">
    <div class="mvp-inner">
      <h2 class="mvp-title">{{ t('landing.mvp_title') }}</h2>
      <p class="mvp-sub">{{ t('landing.mvp_sub') }}</p>

      <!-- Sensor hardware -->
      <div class="mvp-sensor-card">
        <div class="mvp-sensor-visual">
          <div class="sensor-cylinder">
            <div class="sensor-top-section">
              <IcoSensor :size="22" color="var(--green-med)" />
              <span class="sensor-zone-label">{{ locale === 'pt-BR' ? '~20 cm exposto' : '~20 cm exposed' }}</span>
            </div>
            <div class="sensor-divider">
              <span class="sensor-soil-line">{{ locale === 'pt-BR' ? 'Nível do solo' : 'Soil level' }}</span>
            </div>
            <div class="sensor-bottom-section">
              <IcoDrop :size="18" color="var(--blue)" />
              <span class="sensor-zone-label">{{ locale === 'pt-BR' ? '~80 cm enterrado' : '~80 cm buried' }}</span>
            </div>
          </div>
        </div>
        <div class="mvp-sensor-info">
          <div class="mvp-sensor-header">
            <h3 class="mvp-sensor-title">{{ t('landing.mvp_sensor_title') }}</h3>
            <span class="mvp-sensor-cost">R$ 60–80 / {{ locale === 'pt-BR' ? 'unidade' : 'unit' }}</span>
          </div>
          <p class="mvp-sensor-desc">{{ t('landing.mvp_sensor_desc') }}</p>
          <div class="mvp-components">
            <div class="mvp-components-label">{{ t('landing.mvp_components_label') }}</div>
            <div v-for="c in components" :key="c.part" class="mvp-component-row">
              <span class="mvp-component-part">{{ c.part }}</span>
              <span class="mvp-component-role">{{ c.role }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Scalability -->
      <div class="mvp-scale">
        <h3 class="mvp-scale-title">{{ t('landing.mvp_scale_title') }}</h3>
        <div class="mvp-scale-steps">
          <div v-for="(_phase, i) in scalePhases" :key="i" class="mvp-phase">
            <div class="mvp-phase-num">{{ String(i).padStart(2, '0') }}</div>
            <div class="mvp-phase-body">
              <span class="mvp-phase-label">{{ t('landing.mvp_scale_' + i + '_label') }}</span>
              <span class="mvp-phase-desc">{{ t('landing.mvp_scale_' + i + '_desc') }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import IcoSensor from '@/components/icons/IcoSensor.vue'
import IcoDrop from '@/components/icons/IcoDrop.vue'

const { t, locale, tm } = useI18n()
const components = tm('mvp_components') as { part: string; role: string }[]
const scalePhases = [0, 1, 2, 3]
</script>

<style scoped>
.mvp {
  background: var(--gray-light);
  padding: 64px 24px;
}

.mvp-inner {
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.mvp-title {
  font-family: var(--font-head);
  font-size: 28px;
  font-weight: 800;
  color: var(--ink);
  margin: 0;
}

.mvp-sub {
  font-size: 15px;
  color: var(--ink-soft);
  margin: -24px 0 0;
}

/* ── Sensor card ──────────────────────── */
.mvp-sensor-card {
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow-md);
  overflow: hidden;
  display: flex;
  gap: 0;
}

.mvp-sensor-visual {
  background: var(--gray-light);
  border-right: 1px solid var(--line);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28px 24px;
  flex-shrink: 0;
  min-width: 130px;
}

.sensor-cylinder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
  width: 72px;
  border: 2px solid var(--green-dark);
  border-radius: 12px;
  overflow: hidden;
}

.sensor-top-section {
  background: rgba(79,106,46,0.08);
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: 100%;
}

.sensor-bottom-section {
  background: rgba(46,90,116,0.08);
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: 100%;
}

.sensor-zone-label {
  font-size: 8px;
  font-weight: 600;
  color: var(--ink-faint);
  text-align: center;
  line-height: 1.3;
}

.sensor-divider {
  background: #a0784a;
  width: 100%;
  padding: 4px 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sensor-soil-line {
  font-size: 8px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.04em;
}

.mvp-sensor-info {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.mvp-sensor-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.mvp-sensor-title {
  font-family: var(--font-head);
  font-size: 15px;
  font-weight: 700;
  color: var(--ink);
  margin: 0;
}

.mvp-sensor-cost {
  font-family: var(--font-head);
  font-size: 13px;
  font-weight: 700;
  color: var(--green-dark);
  white-space: nowrap;
}

.mvp-sensor-desc {
  font-size: 13px;
  color: var(--ink-soft);
  line-height: 1.55;
  margin: 0;
}

.mvp-components {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.mvp-components-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin-bottom: 2px;
}

.mvp-component-row {
  display: flex;
  gap: 8px;
  align-items: baseline;
}

.mvp-component-part {
  font-family: var(--font-head);
  font-size: 11px;
  font-weight: 700;
  color: var(--ink);
  min-width: 120px;
  flex-shrink: 0;
}

.mvp-component-role {
  font-size: 11px;
  color: var(--ink-soft);
  line-height: 1.4;
}

/* ── Scale phases ─────────────────────── */
.mvp-scale-title {
  font-family: var(--font-head);
  font-size: 18px;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 16px;
}

.mvp-scale-steps {
  display: flex;
  flex-direction: column;
  gap: 0;
  border: 1px solid var(--line);
  border-radius: 12px;
  overflow: hidden;
  background: var(--white);
}

.mvp-phase {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--line);
}
.mvp-phase:last-child { border-bottom: none; }

.mvp-phase-num {
  font-family: var(--font-head);
  font-size: 24px;
  font-weight: 800;
  color: var(--line);
  line-height: 1;
  min-width: 36px;
  flex-shrink: 0;
}

.mvp-phase-body {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding-top: 2px;
}

.mvp-phase-label {
  font-family: var(--font-head);
  font-size: 14px;
  font-weight: 700;
  color: var(--ink);
}

.mvp-phase-desc {
  font-size: 13px;
  color: var(--ink-soft);
  line-height: 1.5;
}

@media (max-width: 560px) {
  .mvp-sensor-card { flex-direction: column; }
  .mvp-sensor-visual { display: none; }
  .mvp-sensor-info { padding: 20px 18px; }
  .mvp-sensor-header { flex-direction: column; gap: 4px; }
  .mvp-component-part { min-width: 90px; }

  .mvp-scale-steps { border-radius: 10px; }
  .mvp-phase { gap: 12px; padding: 14px 16px; }
  .mvp-phase-num { font-size: 18px; min-width: 28px; }
}
</style>
