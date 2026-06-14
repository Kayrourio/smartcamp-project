import { ref, watch, onUnmounted } from 'vue'
import type { Ref } from 'vue'
import type { HistoryPoint } from '@/types/sensor'

export function useEpdHistory(selectedUid: Ref<string | null>) {
  const history = ref<HistoryPoint[]>([])
  let intervalId: ReturnType<typeof setInterval> | null = null

  async function fetchHistory(uid: string) {
    try {
      const res = await fetch(`/api/v1/epd/${encodeURIComponent(uid)}/history?minutes=30`)
      if (!res.ok) return
      const data = await res.json()
      history.value = data.readings ?? []
    } catch {}
  }

  watch(
    selectedUid,
    (uid) => {
      if (intervalId !== null) {
        clearInterval(intervalId)
        intervalId = null
      }
      if (!uid) {
        history.value = []
        return
      }
      fetchHistory(uid)
      intervalId = setInterval(() => fetchHistory(uid), 10_000)
    },
    { immediate: true },
  )

  onUnmounted(() => {
    if (intervalId !== null) clearInterval(intervalId)
  })

  return { history }
}
