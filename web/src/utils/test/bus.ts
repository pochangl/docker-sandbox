type IEvent = (data?: any) => void

interface IBusEvents {
  [key: string]: IEvent[]
}

export class Bus {
  events: IBusEvents = {}

  on(name: string, func: IEvent) {
    const events = this.events
    events[name] = events[name] || []
    events[name].push(func)
    return () => {
      this.unsubscribe(name, func)
    }
  }

  unsubscribe(name: string, func: IEvent) {
    let list = this.events[name]
    if (list) {
      list = list.filter(f => {
        return f !== func
      })
      if (!list.length) {
        delete this.events[name]
      } else {
        this.events[name] = list
      }
    }
  }

  dispatch(name: string, data?: any) {
    const events = this.events[name] || []
    for (const event of events) {
      event(data)
    }
  }
  unsubscribeAll() {
    this.events = {}
  }

  hasEvent(name: string) {
    return name in this.events
  }
}
