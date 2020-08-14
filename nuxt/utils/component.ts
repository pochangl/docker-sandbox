import { createDecorator } from 'vue-class-component'

export function DataTransformer(transformer: (to: any) => any) {

  return function DataTransformerDecorator(path: string) {
    return createDecorator((options, key) => {
      options.watch = options.watch || {}
      const watch = options.watch as any

      if (typeof watch[path] === 'object' && !Array.isArray(watch[path])) {
        watch[path] = [watch[path]]
      } else if (typeof watch[path] === 'undefined') {
        watch[path] = []
      }
      watch[path].push({
        immediate: true,
        async handler(to: any) {
          const promise = transformer(to)
          if (promise instanceof Promise) {
            this[key] = await transformer(to)
          } else {
            this[key] = transformer(to)
          }
        }
      })
    })
  }
}
