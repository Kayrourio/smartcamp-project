<template>
  <section class="ctx">
    <div class="ctx-dots" aria-hidden="true" />
    <span class="ctx-node n1" aria-hidden="true" />
    <span class="ctx-node n2" aria-hidden="true" />
    <span class="ctx-node n3" aria-hidden="true" />
    <span class="ctx-node n4" aria-hidden="true" />
    <div class="ctx-inner">
      <div class="ctx-header">
        <h2 class="ctx-title">{{ t('landing.context_title') }}</h2>
        <p class="ctx-body">{{ t('landing.context_body') }}</p>
      </div>

      <!-- Problem stats -->
      <div class="ctx-stats">
        <div class="ctx-stat">
          <span class="ctx-stat-num">{{ t('landing.context_stat1_num') }}</span>
          <span class="ctx-stat-label">{{ t('landing.context_stat1_label') }}</span>
        </div>
        <div class="ctx-stat">
          <span class="ctx-stat-num">{{ t('landing.context_stat2_num') }}</span>
          <span class="ctx-stat-label">{{ t('landing.context_stat2_label') }}</span>
        </div>
        <div class="ctx-stat">
          <span class="ctx-stat-num">{{ t('landing.context_stat3_num') }}</span>
          <span class="ctx-stat-label">{{ t('landing.context_stat3_label') }}</span>
        </div>
      </div>

      <blockquote class="ctx-quote">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" class="ctx-quote-icon">
          <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/>
          <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>
        </svg>
        {{ t('landing.context_quote') }}
      </blockquote>

      <!-- Solution contrast row -->
      <div class="ctx-solution">
        <span class="ctx-solution-label">{{ t('landing.eyebrow') }}</span>
        <div class="ctx-solution-stats">
          <div class="ctx-sol-stat">
            <span class="ctx-sol-num">{{ t('landing.stats.cost_num') }}</span>
            <span class="ctx-sol-tag">{{ t('landing.stats.cost_tag') }}</span>
          </div>
          <div class="ctx-sol-divider" />
          <div class="ctx-sol-stat">
            <span class="ctx-sol-num">{{ t('landing.stats.cheaper_num') }}</span>
            <span class="ctx-sol-tag">{{ t('landing.stats.cheaper_tag') }}</span>
          </div>
        </div>
      </div>

      <div class="ctx-news">
        <span class="ctx-news-label">{{ t('landing.context_news_label') }}</span>
        <div class="ctx-news-links">
          <a
            href="https://agenciabrasil.ebc.com.br/geral/noticia/2026-03/sobe-para-72-o-numero-de-mortos-nas-chuvas-em-minas-gerais"
            target="_blank" rel="noopener noreferrer"
            class="ctx-news-link"
          >
            <svg width="10" height="10" viewBox="0 0 12 12" fill="none"><path d="M2 10L10 2M10 2H4M10 2V8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            {{ t('landing.context_news_1') }}
          </a>
          <a
            href="https://www.sgb.gov.br/sala-de-imprensa/-/asset_publisher/ujyx/content/prevencao-de-desastres-servico-geologico-do-brasil-evitou-prejuizos-de-r-800-milhoes-em-2023"
            target="_blank" rel="noopener noreferrer"
            class="ctx-news-link"
          >
            <svg width="10" height="10" viewBox="0 0 12 12" fill="none"><path d="M2 10L10 2M10 2H4M10 2V8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            {{ t('landing.context_news_2') }}
          </a>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<style scoped>
.ctx {
  background: var(--ink);
  padding: 72px 24px;
  position: relative;
  overflow: hidden;
}

/* ── Dot grid ────────────────────────────*/
.ctx-dots {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.07) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
}

/* ── Floating sensor nodes ───────────────*/
.ctx-node {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.ctx-node::before,
.ctx-node::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
}

.ctx-node::before {
  background: var(--green-med);
  opacity: 0.6;
}

.ctx-node::after {
  background: transparent;
  border: 1.5px solid var(--green-med);
  opacity: 0;
  animation: node-ping 3s ease-out infinite;
}

.n1 { width: 6px; height: 6px; top: 18%;  left: 12%;  animation: node-drift 20s ease-in-out infinite; }
.n2 { width: 5px; height: 5px; top: 55%;  left: 88%;  animation: node-drift 26s ease-in-out infinite reverse; }
.n3 { width: 7px; height: 7px; top: 78%;  left: 22%;  animation: node-drift 22s ease-in-out infinite 4s; }
.n4 { width: 4px; height: 4px; top: 35%;  left: 75%;  animation: node-drift 18s ease-in-out infinite 2s; }

.n2::after { animation-delay: 1s; }
.n3::after { animation-delay: 0.5s; }
.n4::after { animation-delay: 1.8s; }

@keyframes node-drift {
  0%   { transform: translate(0, 0); }
  25%  { transform: translate(8px, -12px); }
  50%  { transform: translate(-6px, 10px); }
  75%  { transform: translate(12px, 4px); }
  100% { transform: translate(0, 0); }
}

@keyframes node-ping {
  0%   { transform: scale(1);    opacity: 0.6; }
  70%  { transform: scale(3.5);  opacity: 0; }
  100% { transform: scale(3.5);  opacity: 0; }
}

.ctx-inner {
  position: relative;
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.ctx-header {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ctx-title {
  font-family: var(--font-head);
  font-size: 30px;
  font-weight: 800;
  color: #fff;
  margin: 0;
  letter-spacing: -0.01em;
  line-height: 1.15;
}

@media (min-width: 600px) {
  .ctx-title { font-size: 36px; }
}

.ctx-body {
  font-size: 15px;
  color: rgba(255,255,255,0.6);
  line-height: 1.75;
  margin: 0;
  max-width: 560px;
}

/* ── Problem stats grid ──────────────────*/
.ctx-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2px;
  background: rgba(255,255,255,0.08);
  border-radius: 14px;
  overflow: hidden;
}

.ctx-stat {
  background: rgba(255,255,255,0.04);
  padding: 22px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: background 0.2s;
}
.ctx-stat:hover { background: rgba(255,255,255,0.07); }

.ctx-stat-num {
  font-family: var(--font-head);
  font-size: 28px;
  font-weight: 800;
  color: #fff;
  line-height: 1;
  letter-spacing: -0.02em;
}

.ctx-stat-label {
  font-size: 11px;
  color: rgba(255,255,255,0.45);
  line-height: 1.4;
}

/* ── Quote ───────────────────────────────*/
.ctx-quote {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  border-left: 3px solid var(--green-med);
  padding: 2px 0 2px 22px;
  margin: 0;
  font-family: var(--font-head);
  font-size: 16px;
  font-style: italic;
  font-weight: 600;
  color: rgba(255,255,255,0.82);
  line-height: 1.55;
}

.ctx-quote-icon {
  color: var(--green-med);
  flex-shrink: 0;
  margin-top: 3px;
  opacity: 0.8;
}

/* ── Solution contrast ───────────────────*/
.ctx-solution {
  border: 1px solid rgba(110, 139, 67, 0.35);
  border-radius: 14px;
  padding: 20px 24px;
  background: rgba(110, 139, 67, 0.08);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.ctx-solution-label {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--green-med);
}

.ctx-solution-stats {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.ctx-sol-stat {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.ctx-sol-num {
  font-family: var(--font-head);
  font-size: 28px;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
  line-height: 1;
}

.ctx-sol-tag {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
}

.ctx-sol-divider {
  width: 1px;
  height: 40px;
  background: rgba(255,255,255,0.12);
  flex-shrink: 0;
}

/* ── News links ──────────────────────────*/
.ctx-news {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ctx-news-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.28);
}

.ctx-news-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 20px;
}

.ctx-news-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: rgba(255,255,255,0.4);
  text-decoration: none;
  transition: color 0.15s;
}
.ctx-news-link:hover { color: rgba(255,255,255,0.75); }

@media (max-width: 480px) {
  .ctx { padding: 52px 20px; }
  .ctx-title { font-size: 26px; }
  .ctx-stats { grid-template-columns: 1fr; }
  .ctx-stat-num { font-size: 22px; }
  .ctx-solution { padding: 16px 18px; }
  .ctx-sol-num { font-size: 22px; }
}
</style>
