import { ref, onMounted, onUnmounted } from 'vue'
import type { GridPoint } from '@/types/sensor'

export function useRainGrid() {
  const grid = ref<GridPoint[]>([])
  let intervalId: ReturnType<typeof setInterval> | null = null

  async function fetchGrid() {
    try {
      const res = await fetch('/api/v1/weather/rain-grid')
      if (!res.ok) return
      const data = await res.json()
      grid.value = data.grid ?? []
    } catch {}
  }

  onMounted(() => {
    fetchGrid()
    // Backend caches for 5 min; poll every 60s to pick up refreshed cache
    intervalId = setInterval(fetchGrid, 60_000)
  })

  onUnmounted(() => {
    if (intervalId !== null) clearInterval(intervalId)
  })

  return { grid }
}
