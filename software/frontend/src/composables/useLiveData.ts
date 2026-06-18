import { ref, onMounted, onUnmounted } from 'vue'

// Legacy composable,superseded by useEpdList for the multi-EPD architecture.
// Kept for reference only; not used in the current UI.
export function useLiveData() {
  const data = ref<Record<string, unknown> | null>(null)
  const isLoading = ref(true)
  const error = ref<string | null>(null)
  const lastUpdated = ref<Date | null>(null)

  let intervalId: ReturnType<typeof setInterval> | null = null

  async function fetchLatest() {
    try {
      const res = await fetch('/api/v1/sensor/latest')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      data.value = await res.json()
      error.value = null
      lastUpdated.value = new Date()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Erro de conexão'
    } finally {
      isLoading.value = false
    }
  }

  onMounted(() => {
    fetchLatest()
    intervalId = setInterval(fetchLatest, 2000)
  })

  onUnmounted(() => {
    if (intervalId !== null) clearInterval(intervalId)
  })

  return { data, isLoading, error, lastUpdated }
}
