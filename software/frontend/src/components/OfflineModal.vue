<template>
  <Teleport to="body">
    <div v-if="visible" class="modal-backdrop" @click.self="dismiss">
      <div class="modal" role="dialog" aria-modal="true">
        <div class="modal-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>
        <h2 class="modal-title">{{ t('landing.offline_title') }}</h2>
        <p class="modal-body">{{ t('landing.offline_body') }}</p>
        <div class="modal-actions">
          <RouterLink to="/simulador" class="modal-cta">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"/>
              <path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>
            </svg>
            {{ t('landing.offline_cta') }}
          </RouterLink>
          <button class="modal-dismiss" @click="dismiss">
            {{ t('landing.offline_dismiss') }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const visible = ref(true)

function dismiss() {
  visible.value = false
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(4px);
  z-index: 9000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.modal {
  background: #fff;
  border-radius: 16px;
  padding: 32px 28px 28px;
  max-width: 440px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,0.25);
  display: flex;
  flex-direction: column;
  gap: 12px;
  animation: modal-in 0.22s ease;
}

@keyframes modal-in {
  from { opacity: 0; transform: translateY(12px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

.modal-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: #f5f0ea;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8a6a3a;
  align-self: flex-start;
  margin-bottom: 4px;
}

.modal-title {
  font-family: var(--font-head);
  font-size: 20px;
  font-weight: 800;
  color: var(--ink);
  margin: 0;
}

.modal-body {
  font-size: 14px;
  color: var(--ink-soft);
  line-height: 1.65;
  margin: 0;
}

.modal-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}

.modal-cta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: var(--green-dark);
  color: #fff;
  font-family: var(--font-head);
  font-size: 14px;
  font-weight: 700;
  padding: 14px 20px;
  border-radius: 10px;
  text-decoration: none;
  transition: opacity 0.15s;
}
.modal-cta:hover { opacity: 0.88; }

.modal-dismiss {
  background: none;
  border: none;
  color: var(--ink-faint);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: color 0.15s;
  text-align: center;
}
.modal-dismiss:hover { color: var(--ink-soft); }
</style>
