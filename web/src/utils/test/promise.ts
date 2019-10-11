function halt() {
  return new Promise<void>(resolve => {
    setTimeout(() => {
      resolve()
    })
  })
}

export function $nextTick(): Promise<void> {
  return halt()
}
