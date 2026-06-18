<template>
  <section class="award">
    <div class="topo-bg" />
    <div class="award-lines" aria-hidden="true" />
    <div class="award-inner">
      <div class="award-body">
        <div class="award-pill">{{ t('landing.award_pill') }}</div>
        <h2 class="award-title">{{ t('landing.award_title') }}</h2>
        <p class="award-event">{{ t('landing.award_event') }}</p>
        <p class="award-desc">{{ t('landing.award_desc') }}</p>
        <div class="award-meta">
          <div class="meta-item">
            <span class="meta-label">{{ t('landing.award_prize_label') }}</span>
            <span class="meta-val">{{ t('landing.award_prize') }}</span>
          </div>
          <div class="meta-divider" />
          <div class="meta-item">
            <span class="meta-label">{{ t('landing.award_organizers_label') }}</span>
            <span class="meta-val small">{{ t('landing.award_organizers') }}</span>
          </div>
        </div>
        <a
          href="https://centev.ufv.br/solucoes-para-desafios-urbanos-marcam-o-bootcamp-cidades-inteligentes-do-tecnoparq-ufv/"
          target="_blank"
          rel="noopener noreferrer"
          class="article-link"
        >
          {{ t('landing.award_article_link') }}
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M2 10L10 2M10 2H4M10 2V8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
      </div>

      <div class="award-badge-wrap">
        <div class="badge-glow" />
        <div class="badge-ring">
          <span class="badge-trophy">🏆</span>
          <span class="badge-num">1º</span>
          <span class="badge-place">{{ locale === 'pt-BR' ? 'Lugar' : 'Place' }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t, locale } = useI18n()
</script>

<style scoped>
.award {
  background:
    radial-gradient(ellipse at 85% 50%, rgba(130, 180, 70, 0.15) 0%, transparent 55%),
    radial-gradient(ellipse at 10% 90%, rgba(20, 38, 10, 0.5) 0%, transparent 50%),
    #3d5222;
  padding: 52px 24px 64px;
  position: relative;
  overflow: hidden;
}

.topo-bg {
  position: absolute;
  inset: 0;
  background-image: url('/topo.svg');
  background-size: cover;
  opacity: 0.07;
  pointer-events: none;
}

.award-lines {
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(
      -55deg,
      rgba(255,255,255,0.03) 0px,
      rgba(255,255,255,0.03) 1px,
      transparent 1px,
      transparent 40px
    );
  pointer-events: none;
}

.award-inner {
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  gap: 32px;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.award-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.award-pill {
  display: inline-flex;
  align-items: center;
  background: rgba(212, 175, 55, 0.18);
  border: 1px solid rgba(212, 175, 55, 0.45);
  color: rgba(212, 175, 55, 0.95);
  font-family: var(--font-head);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.12em;
  padding: 4px 12px;
  border-radius: 20px;
  align-self: flex-start;
  text-transform: uppercase;
}

.award-title {
  font-family: var(--font-head);
  font-size: 26px;
  font-weight: 800;
  color: #fff;
  line-height: 1.2;
  margin: 0;
}

@media (min-width: 600px) {
  .award-title { font-size: 30px; }
}

.award-event {
  font-size: 13px;
  font-weight: 500;
  color: rgba(255,255,255,0.5);
  margin: 0;
}

.award-desc {
  font-size: 14px;
  color: rgba(255,255,255,0.72);
  line-height: 1.7;
  margin: 0;
  max-width: 460px;
}

.award-meta {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 2px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.meta-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.35);
}

.meta-val {
  font-family: var(--font-head);
  font-size: 20px;
  font-weight: 800;
  color: #fff;
}

.meta-val.small {
  font-size: 12px;
  font-weight: 600;
  color: rgba(255,255,255,0.65);
  line-height: 1.4;
}

.meta-divider {
  width: 1px;
  height: 40px;
  background: rgba(255,255,255,0.12);
  flex-shrink: 0;
}

.article-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.45);
  text-decoration: none;
  transition: color 0.2s;
  align-self: flex-start;
  margin-top: 2px;
}
.article-link:hover { color: rgba(255,255,255,0.85); }

/* ── Badge ─────────────────────────────── */
.award-badge-wrap {
  position: relative;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
}

.badge-glow {
  position: absolute;
  inset: -30px;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.45) 0%, rgba(212, 175, 55, 0.1) 45%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 1;    transform: scale(1); }
  50%       { opacity: 0.6; transform: scale(0.88); }
}

.badge-ring {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid rgba(212, 175, 55, 0.6);
  background: rgba(212, 175, 55, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0;
  box-shadow: 0 0 0 1px rgba(212, 175, 55, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.badge-trophy {
  font-size: 26px;
  line-height: 1;
  filter: drop-shadow(0 0 6px rgba(212, 175, 55, 0.7));
}

.badge-num {
  font-family: var(--font-head);
  font-size: 22px;
  font-weight: 900;
  color: #fff;
  line-height: 1;
  margin-top: 2px;
}

.badge-place {
  font-family: var(--font-head);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(212, 175, 55, 0.8);
}

@media (max-width: 480px) {
  .award-inner {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
  .award-badge-wrap {
    order: -1;
    align-self: center;
    margin-top: 0;
  }
  .award-body {
    width: 100%;
    align-items: center;
    text-align: center;
  }
  .award-pill { align-self: center; }
  .award-meta { justify-content: center; }
  .article-link { align-self: center; }
}
</style>
