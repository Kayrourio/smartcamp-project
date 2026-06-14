import { ref, onMounted, onUnmounted } from 'vue'
import type { EpdOut } from '@/types/sensor'

export function useEpdList() {
  const epds = ref<EpdOut[]>([])
  const isLoading = ref(true)
  const error = ref<string | null>(null)
  let intervalId: ReturnType<typeof setInterval> | null = null

  async function fetchEpds() {
    try {
      const res = await fetch('/api/v1/epd/')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      epds.value = await res.json()
      error.value = null
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Erro de conexão'
    } finally {
      isLoading.value = false
    }
  }

  onMounted(() => {
    fetchEpds()
    intervalId = setInterval(fetchEpds, 2000)
  })

  onUnmounted(() => {
    if (intervalId !== null) clearInterval(intervalId)
  })

  return { epds, isLoading, error }
}
