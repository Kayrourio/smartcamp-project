<template>
  <div class="lang-switcher" role="group" aria-label="Idioma / Language">
    <button
      class="lang-opt"
      :class="{ 'lang-opt--active': locale === 'pt-BR' }"
      @click="locale = 'pt-BR'"
    >
      <span class="lang-flag">BR</span>
      <span class="lang-label">PT</span>
    </button>
    <span class="lang-sep" />
    <button
      class="lang-opt"
      :class="{ 'lang-opt--active': locale === 'en-US' }"
      @click="locale = 'en-US'"
    >
      <span class="lang-flag">US</span>
      <span class="lang-label">EN</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { locale } = useI18n()
</script>

<style scoped>
.lang-switcher {
  display: flex;
  align-items: center;
  gap: 0;
  background: rgba(0,0,0,0.20);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.lang-opt {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 11px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: rgba(255,255,255,0.55);
  transition: color 0.15s, background 0.15s;
  font-family: var(--font-head, sans-serif);
}

.lang-opt:hover {
  color: rgba(255,255,255,0.85);
  background: rgba(255,255,255,0.08);
}

.lang-opt--active {
  background: rgba(255,255,255,0.18);
  color: #fff;
}

.lang-flag {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.04em;
  background: rgba(255,255,255,0.2);
  padding: 1px 4px;
  border-radius: 3px;
  color: inherit;
}

.lang-opt--active .lang-flag {
  background: rgba(255,255,255,0.35);
}

.lang-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
}

.lang-sep {
  width: 1px;
  height: 20px;
  background: rgba(255,255,255,0.2);
  flex-shrink: 0;
}
</style>
