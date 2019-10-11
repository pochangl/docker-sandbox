import { Bus } from './bus'

export function getListUrl(name: string): string {
  return 'http://localhost/api/' + name + '/'
}

export function getDetailUrl(name: string, id: number): string {
  return 'http://localhost/api/' + name + '/' + id + '/'
}

interface IServerRequest {
  respond(data: any): void
  reject(err: Error): void
}

interface IServer {
  dispatch(busname: string, obj: IServerRequest): void
}

interface IOptions {
  url: string
  body?: object
}

interface IModel {
  id: number
}
interface IDataModel {
  viewName: string
  Model?: {
    viewName: string
  }
}

class Server extends Bus implements IServer {
  busName(method: string, opt: { url: string }): string {
    return method + '_' + opt.url
  }
  request(method: string, options: IOptions) {
    // intercept http request
    const opt = Object.assign({}, options)
    const busName: string = this.busName(method, opt)

    return new Promise((resolve, reject) => {
      // send request signal
      this.dispatch('request_' + busName, {
        respond: (data: object) => {
          this.dispatch(busName, data)
        },
        reject: (err: Error) => {
          this.dispatch('reject_' + busName, err)
        },
        body: options.body,
        url: options.url
      })

      // listen to response
      const res = this.on(busName, data => {
        unsub()
        resolve({
          json: () => data
        })
      })

      // listen to failure
      const rej = this.on('reject_' + busName, err => {
        unsub()
        reject(err)
      })

      // unload all listener
      function unsub() {
        res()
        rej()
      }
    })
  }
  reset() {
    this.unsubscribeAll()
  }
  buildUrl(DM: IDataModel, id?: number): string {
    const DataModel: IDataModel = DM
    if (DataModel.Model) {
      return getListUrl(DataModel.Model.viewName)
    } else if (id) {
      return getDetailUrl(DataModel.viewName, id)
    } else {
      return getListUrl(DataModel.viewName)
    }
  }
  wait(DataModel: IDataModel, method: string, id?: number): Promise<any> {
    const name = this.busName(method, {
      url: this.buildUrl(DataModel, id)
    })

    return new Promise<any>((resolve, _) => {
      const unsub = this.on('request_' + name, data => {
        resolve(data)
        unsub()
      })
    })
  }
  send(DataModel: IDataModel, method: string, id: number, data: any) {
    const busName = this.busName(method, {
      url: this.buildUrl(DataModel, id)
    })
    this.dispatch(busName, {
      body: data
    })
  }
  hasRequest(DataModel: IDataModel, method: string, id: number) {
    const busName = this.busName(method, {
      url: this.buildUrl(DataModel, id)
    })
    return super.hasEvent(busName)
  }
}

class Client extends Bus {
  server: Server

  constructor(server: Server) {
    super()
    this.server = server
  }

  get(url: string) {
    return this.server.request('get', {
      url
    })
  }
  post(url: string, body: object) {
    return this.server.request('post', {
      url,
      body
    })
  }
  put(url: string, body: object) {
    return this.server.request('put', {
      url,
      body
    })
  }
  delete(url: string, body: object) {
    return this.server.request('delete', {
      url
    })
  }
  patch(url: string, body: object) {
    return this.server.request('patch', {
      url,
      body
    })
  }
  run(func: () => any): Request {
    return new Request(this, func)
  }
}

class Request {
  func: () => any
  waitFunc: () => Promise<any> = async () => {}
  client: Client
  beforeFunc: () => void = () => { }

  constructor(client: Client, func: () => any) {
    this.func = func
    this.client = client
  }
  wait(DataModel: IDataModel, method: string, id?: number) {
    this.waitFunc = () => {
      return this.client.server.wait(DataModel, method, id)
    }
    return this
  }
  before(func: () => void) {
    this.beforeFunc = func
    return this
  }
  async reject() {
    const requestPromise = this.waitFunc()
    const runPromise = this.func()
    const request = await requestPromise
    request.reject()
    return new Promise((resolve) => {
      runPromise.then(resolve).catch(resolve)
    })
  }
  async respond(data: any) {
    const requestPromise = this.waitFunc()
    const runPromise = this.func()
    const request = await requestPromise

    this.beforeFunc()

    if (typeof data === 'function') {
      data(request)
    } else {
      request.respond(data)
    }
    return runPromise
  }
}

export const server = new Server()
const http = new Client(server)

export default function () {
  return http
}

export const client = http
