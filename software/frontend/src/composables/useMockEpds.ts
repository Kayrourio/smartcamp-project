import { ref, onMounted, onUnmounted } from 'vue'
import type { EpdOut } from '@/types/sensor'

export function useMockEpds() {
  const epds = ref<EpdOut[]>([])
  const isLoading = ref(true)
  let intervalId: ReturnType<typeof setInterval> | null = null

  async function fetchMock() {
    try {
      const res = await fetch('/api/v1/mock/epds')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      epds.value = await res.json()
    } finally {
      isLoading.value = false
    }
  }

  onMounted(() => {
    fetchMock()
    intervalId = setInterval(fetchMock, 2000)
  })

  onUnmounted(() => {
    if (intervalId !== null) clearInterval(intervalId)
  })

  return { epds, isLoading }
}
