<template>
  <section class="hero">
    <div class="topo-bg" />
    <div class="aurora aurora-1" />
    <div class="aurora aurora-2" />
    <div class="hero-inner">
      <div class="hero-top-bar">
        <div class="eyebrow">
          <LogoMark />
          <span>{{ t('landing.eyebrow') }}</span>
        </div>
        <LanguageSwitcher />
      </div>
      <h1 class="tagline">
        <span class="trad">{{ t('landing.tagline_trad') }}</span>
        <span class="punch">{{ t('landing.tagline_punch') }}</span>
      </h1>
      <p class="subtitle">{{ t('landing.subtitle') }}</p>
      <div class="cta-row">
        <RouterLink to="/simulador" class="cta-btn cta-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"/>
            <path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>
            <path d="M4.93 4.93l2.12 2.12M16.95 16.95l2.12 2.12M19.07 4.93l-2.12 2.12M7.05 16.95l-2.12 2.12"/>
          </svg>
          {{ t('landing.sim_btn') }}
        </RouterLink>
        <div class="cta-ghost-row">
          <RouterLink to="/mapa" class="cta-ghost">{{ t('landing.cta') }}</RouterLink>
          <RouterLink to="/mock" class="cta-ghost">{{ t('landing.demo_btn') }}</RouterLink>
        </div>
      </div>
    </div>

    <!-- Wave transition into AwardBanner -->
    <div class="hero-wave" aria-hidden="true">
      <svg viewBox="0 0 1440 72" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M0,32 C240,72 480,8 720,40 C960,72 1200,16 1440,48 L1440,72 L0,72 Z"
          fill="var(--award-bg)"
        />
      </svg>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import LogoMark from '@/components/icons/LogoMark.vue'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
const { t } = useI18n()
</script>

<style scoped>
.hero {
  position: relative;
  background:
    radial-gradient(ellipse at 75% 20%, rgba(120, 170, 70, 0.2) 0%, transparent 52%),
    radial-gradient(ellipse at 5% 85%, rgba(25, 45, 15, 0.45) 0%, transparent 48%),
    var(--green-dark);
  overflow: hidden;
  padding: 44px 24px 88px;
  /* award section uses a slightly darker shade so the wave is visible */
  --award-bg: #3d5222;
}

.topo-bg {
  position: absolute;
  inset: 0;
  background-image: url('/topo.svg');
  background-size: cover;
  opacity: 0.08;
  pointer-events: none;
  animation: topo-drift 40s ease-in-out infinite alternate;
}

/* ── Aurora orbs ─────────────────────────*/
.aurora {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(60px);
  will-change: transform, opacity;
}

.aurora-1 {
  width: 520px;
  height: 320px;
  top: -60px;
  right: -80px;
  background: radial-gradient(ellipse, rgba(120, 190, 70, 0.28) 0%, transparent 70%);
  animation: aurora-float-1 18s ease-in-out infinite;
}

.aurora-2 {
  width: 380px;
  height: 260px;
  bottom: 20px;
  left: -60px;
  background: radial-gradient(ellipse, rgba(60, 120, 40, 0.22) 0%, transparent 70%);
  animation: aurora-float-2 24s ease-in-out infinite;
}

@keyframes topo-drift {
  from { background-position: 0% 0%; }
  to   { background-position: 4% 3%; }
}

@keyframes aurora-float-1 {
  0%   { transform: translate(0, 0) scale(1); opacity: 0.85; }
  33%  { transform: translate(-40px, 30px) scale(1.08); opacity: 1; }
  66%  { transform: translate(20px, -20px) scale(0.94); opacity: 0.75; }
  100% { transform: translate(0, 0) scale(1); opacity: 0.85; }
}

@keyframes aurora-float-2 {
  0%   { transform: translate(0, 0) scale(1); opacity: 0.7; }
  40%  { transform: translate(30px, -40px) scale(1.1); opacity: 0.9; }
  70%  { transform: translate(-20px, 20px) scale(0.92); opacity: 0.65; }
  100% { transform: translate(0, 0) scale(1); opacity: 0.7; }
}

.hero-inner {
  position: relative;
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.eyebrow {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(255,255,255,0.6);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}

.tagline {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin: 4px 0 0;
}

.trad {
  font-family: var(--font-head);
  font-size: 26px;
  font-weight: 500;
  color: rgba(255,255,255,0.45);
  letter-spacing: -0.01em;
}

.punch {
  font-family: var(--font-head);
  font-size: 34px;
  font-weight: 800;
  color: var(--white);
  line-height: 1.12;
  letter-spacing: -0.02em;
}

@media (min-width: 600px) {
  .trad  { font-size: 30px; }
  .punch { font-size: 44px; }
}

.subtitle {
  font-size: 16px;
  color: rgba(255,255,255,0.65);
  line-height: 1.65;
  max-width: 500px;
  margin: 0;
}

/* ── CTAs ────────────────────────────────*/
.cta-row {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
  margin-top: 4px;
}

.cta-primary {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  background: #fff;
  color: var(--green-dark);
  font-family: var(--font-head);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.02em;
  padding: 16px 30px;
  border-radius: var(--r-sm);
  text-decoration: none;
  transition: opacity 0.15s, transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 4px 24px rgba(0,0,0,0.28);
}
.cta-primary:hover {
  opacity: 0.94;
  transform: translateY(-1px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}

.cta-ghost-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.cta-ghost {
  display: inline-flex;
  align-items: center;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.65);
  font-family: var(--font-head);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.02em;
  padding: 10px 18px;
  border-radius: var(--r-sm);
  text-decoration: none;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}
.cta-ghost:hover {
  background: rgba(255,255,255,0.15);
  border-color: rgba(255,255,255,0.35);
  color: rgba(255,255,255,0.95);
}

/* ── Wave ────────────────────────────────*/
.hero-wave {
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  line-height: 0;
  pointer-events: none;
}

.hero-wave svg {
  display: block;
  width: 100%;
  height: 72px;
}

@media (max-width: 420px) {
  .cta-primary { width: 100%; justify-content: center; }
  .cta-ghost-row { width: 100%; }
  .cta-ghost { flex: 1; justify-content: center; }
}
</style>
