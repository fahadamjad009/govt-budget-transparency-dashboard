import { useEffect, useRef, useState } from 'react'

// Reveals an element once it scrolls into view, then stays revealed.
// Used for the folio sections and the audit-stamp signature element.
export function useReveal(threshold = 0.25) {
  const ref = useRef(null)
  const [revealed, setRevealed] = useState(false)

  useEffect(() => {
    const node = ref.current
    if (!node) return
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setRevealed(true)
            observer.disconnect()
          }
        })
      },
      { threshold }
    )
    observer.observe(node)
    return () => observer.disconnect()
  }, [threshold])

  return [ref, revealed]
}

// Counts a number up from 0 once `start` is true. Used for ledger figures.
export function useCountUp(target, start, durationMs = 1400) {
  const [value, setValue] = useState(0)
  useEffect(() => {
    if (!start) return
    let raf
    const startTime = performance.now()
    const tick = (now) => {
      const progress = Math.min((now - startTime) / durationMs, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setValue(target * eased)
      if (progress < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [start, target, durationMs])
  return value
}
