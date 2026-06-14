<template>
  <section class="hero">
    <div class="topo-bg" />
    <div class="hero-inner">
      <div class="eyebrow">
        <LogoMark />
        <span>{{ t('landing.eyebrow') }}</span>
      </div>
      <h1 class="tagline">
        <span class="trad">{{ t('landing.tagline_trad') }}</span>
        <span class="punch">{{ t('landing.tagline_punch') }}</span>
      </h1>
      <p class="subtitle">{{ t('landing.subtitle') }}</p>
      <div class="cta-row">
        <RouterLink to="/mapa" class="cta-btn">{{ t('landing.cta') }}</RouterLink>
        <RouterLink to="/mock" class="demo-btn">Ver demonstração com 100 sensores</RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import LogoMark from '@/components/icons/LogoMark.vue'
const { t } = useI18n()
</script>

<style scoped>
.hero {
  position: relative;
  background: var(--green-dark);
  overflow: hidden;
  padding: 80px 24px 64px;
}

.topo-bg {
  position: absolute;
  inset: 0;
  background-image: url('/topo.svg');
  background-size: cover;
  opacity: 0.08;
  pointer-events: none;
}

.hero-inner {
  position: relative;
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.eyebrow {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(255,255,255,0.75);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.tagline {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.trad {
  font-family: var(--font-head);
  font-size: 28px;
  font-weight: 600;
  color: rgba(255,255,255,0.6);
}

.punch {
  font-family: var(--font-head);
  font-size: 32px;
  font-weight: 800;
  color: var(--white);
  line-height: 1.15;
}

@media (min-width: 600px) {
  .trad { font-size: 32px; }
  .punch { font-size: 40px; }
}

.subtitle {
  font-size: 16px;
  color: rgba(255,255,255,0.75);
  line-height: 1.6;
  max-width: 520px;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  align-self: flex-start;
  background: var(--white);
  color: var(--green-dark);
  font-family: var(--font-head);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 14px 28px;
  border-radius: var(--r-sm);
  transition: opacity 0.2s;
}

.cta-btn:hover { opacity: 0.9; }

.cta-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}

.demo-btn {
  display: inline-flex;
  align-items: center;
  align-self: flex-start;
  background: rgba(255,255,255,0.15);
  border: 1.5px solid rgba(255,255,255,0.4);
  color: var(--white);
  font-family: var(--font-head);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.04em;
  padding: 13px 22px;
  border-radius: var(--r-sm);
  transition: background 0.2s;
}
.demo-btn:hover { background: rgba(255,255,255,0.25); }
</style>
