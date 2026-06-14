<template>
  <main>
    <HeroSection />
    <section class="stats">
      <div class="stats-inner">
        <StatCard :num="t('landing.stats.deaths_num')" :tag="t('landing.stats.deaths_tag')" />
        <StatCard :num="t('landing.stats.cost_num')" :tag="t('landing.stats.cost_tag')" />
        <StatCard :num="t('landing.stats.cheaper_num')" :tag="t('landing.stats.cheaper_tag')" />
      </div>
    </section>
    <HowItWorks />
  </main>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import HeroSection from '@/components/landing/HeroSection.vue'
import StatCard from '@/components/landing/StatCard.vue'
import HowItWorks from '@/components/landing/HowItWorks.vue'
const { t } = useI18n()
</script>

<style scoped>
.stats {
  background: var(--white);
  padding: 32px 24px;
  border-bottom: 1px solid var(--line);
}

.stats-inner {
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
</style>
