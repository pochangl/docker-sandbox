/*
  Data Model that blends well with django_rest_framework
*/
import http from '@/http'
import { WebSocketSubject } from 'rxjs/observable/dom/WebSocketSubject'
import { webSocket } from 'rxjs/observable/dom/webSocket'

export function getListUrl(name: string): string {
  return `${window.location.origin}/api/${name}/`
}

export function getDetailUrl(name: string, id: number): string {
  return `${window.location.origin}/api/${name}/${id}/`
}

interface IModelConstructor<T extends Model> {
  new(): T
  fields: string[]
  viewName: string
  getListUrl (): string
  getDetailUrl(id: number): string
}

interface IRawModel {
  id: number
  [key: string]: any
}

abstract class BaseModel {
  id: number = 0
  // class that handles single data from API
  static fields: string[] = []
  static viewName = ''

  construct(obj: IRawModel) {
    // construct data model from raw data
    const fields = (this.constructor as any).fields
    this.id = obj.id
    for (const name of fields) {
      (this as any)[name] = obj[name]
    }
  }

  json(): IRawModel {
    // convert model to json that can be passed to api
    const fields = (this.constructor as any).fields
    const data: IRawModel = {
      id: this.id
    }
    for (const name of fields) {
      data[name] = (this as any)[name]
    }
    return data
  }
}

export abstract class Model extends BaseModel {
  async fetch() {
    // fetching data from server
    const viewName: string = (this.constructor as any).viewName
    const url = getDetailUrl((this.constructor as IModelConstructor<Model>).viewName, this.id)
    const response = await http.get(url)
    this.construct(await response.json())
  }

  async create() {
    // post data to server
    const viewName: string = (this.constructor as any).viewName
    const url = getListUrl((this.constructor as IModelConstructor<Model>).viewName)
    const response = await http.post(url, this.json())
    this.construct(await response.json())
  }
}

export abstract class ModelList<T extends Model> {
  // class that handles list of Models
  objects: T[] = []

  async fetch() {
    // fetching data from server
    const Model: IModelConstructor<T> = (this.constructor as any).Model
    const url: string = getListUrl(Model.viewName)
    const response = await http.get(url)
    this.objects = (await response.json()).map((content: any) => {
      const model = new Model()
      model.construct(content)
      return model
    })
  }
}

interface IWebsocketPacket<V> {
  type: string
  value: V
}

const isProduction = window.location.protocol.slice(0, 5) === 'https'
const wsProtocol = isProduction ? 'wss' : 'ws'

export abstract class WebSocketModel<V = any> extends BaseModel {
  subject: WebSocketSubject<string>

  connect() {
    // post data to server
    const viewName: string = (this.constructor as any).viewName
    const url = `${wsProtocol}://${window.location.host}/ws/${viewName}/`
    const subject = this.subject = webSocket<string>(url)
  }

  disconnect() {
    this.subject.complete()
  }

  receive(name: string): Promise<V> {
    return new Promise((resolve) => {
      const subscription = this.subject.subscribe((response: any) => {
        let data: IWebsocketPacket<V>
        if (typeof response === 'string') {
          data = JSON.parse(response)
        } else {
          data = response
        }
        if (data.type === name) {
          subscription.unsubscribe()
          resolve(data.value)
        }
      })
    })
  }

  static async contextmanager<WSM extends WebSocketModel> (func: (wsm: WSM) => Promise<any>, data: any) {
    const wsm: WSM = new (this as any)()
    if (data) {
      wsm.construct(data)
      wsm.connect()
    }

    func(wsm).finally(() => {
      wsm.disconnect()
    })
    return wsm
  }

  send(name: string, value: V) {
    this.subject.next(JSON.stringify({
      type: name,
      value
    }))
  }
}
