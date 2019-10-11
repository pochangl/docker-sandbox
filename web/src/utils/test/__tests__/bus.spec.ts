import { Bus } from '../bus'

describe('Bus', () => {
  it('should subscribe', () => {
    const bus = new Bus()
    function func() {}

    expect(bus.events).toEqual({})

    bus.on('ev', func)

    expect(bus.events['ev']).toEqual([func])
  })

  it('should unsubscribe', () => {
    const bus = new Bus()
    function func() {}

    bus.on('ev', func)

    expect(bus.events).toEqual({
      ev: [func]
    })
    bus.unsubscribe('ev', func)
    expect(bus.events).toEqual({})
  })

  it('should unsubscribe with unsubscriber', () => {
    const bus = new Bus()
    function func() {}
    const unsub = bus.on('ev', func)
    expect(bus.events).toEqual({
      ev: [func]
    })
    unsub()
    expect(bus.events).toEqual({})
  })

  it('should skip unsubscription', () => {
    const bus = new Bus()
    function func1() {}
    function func2() {}
    bus.on('ev', func1)
    expect(bus.events).toEqual({
      ev: [func1]
    })
    bus.unsubscribe('ev', func2)
    expect(bus.events).toEqual({
      ev: [func1]
    })
  })

  it('should skip unsubscription event if event is empty', () => {
    const bus = new Bus()
    function func1() {}
    expect(bus.events).toEqual({})
    bus.unsubscribe('', func1)
    expect(bus.events).toEqual({})
  })

  it('should dispatch data', () => {
    let data = undefined
    function func1(d: any) {
      data = d
    }
    const bus = new Bus()
    bus.on('e', func1)
    expect(data).toBeUndefined()
    bus.dispatch('e', 3)
    expect(data).toBe(3)
  })

  it('should handle different subscriber', () => {
    const data = {
      one: 0,
      two: 0
    }
    const bus = new Bus()

    function func1() {
      data.one += 1
    }
    function func2() {
      data.two += 2
    }

    bus.on('e', func1)
    bus.on('e', func2)
    bus.dispatch('e')

    expect(data).toEqual({
      one: 1,
      two: 2
    })

    bus.unsubscribe('e', func1)
    bus.dispatch('e')
    expect(data).toEqual({
      one: 1,
      two: 4
    })

    bus.on('e', func1)
    bus.unsubscribe('e', func2)
    bus.dispatch('e')
    expect(data).toEqual({
      one: 2,
      two: 4
    })
  })
  it('can still dispatch on empty bus without failure', () => {
    const bus = new Bus()
    bus.dispatch('e')
  })
  it('should reset', () => {
    const bus = new Bus()
    let data = 0
    function func(value: number) {
      data = value
    }
    bus.on('e', func)
    expect(bus.events).toEqual({
      e: [func]
    })
    bus.dispatch('e', 1)
    expect(data).toBe(1)
    bus.unsubscribeAll()
    bus.dispatch('e', 9)
    expect(data).toBe(1)
  })

  it('has event', () => {
    const bus = new Bus()
    function func() {}
    expect(bus.hasEvent('e')).toBe(false)
    bus.on('e', func)
    expect(bus.hasEvent('e')).toBe(true)
    bus.unsubscribe('e', func)
    expect(bus.hasEvent('e')).toBe(false)
  })
})
