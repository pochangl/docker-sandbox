jest.mock('@/http')

import { client, server } from '@/utils/test/api'
import { Stepper } from '@/utils/test/stepper'
import { Model, ModelList } from '@/models'
import { $nextTick } from '@/utils/test/promise'

beforeEach(() => {
  server.reset()
})

const url: any = '//api/url/'
const body = 'bod'
const baseBusName = '//api/url/'

class DataModel extends Model {
  id = 1
  static viewName = 'url'
  static fields = ['data']
  data: any
}

class DataModelList extends ModelList<DataModel> {
  static Model = DataModel
}

describe('Server', () => {
  const busName = 'get_' + baseBusName

  it('server.busName', () => {
    const name = server.busName('get', { url })
    expect(name).toBe(busName)
  })

  it('buildListUrl', () => {
    const urlObj = server.buildUrl(DataModelList as any)
    expect(urlObj).toEqual(url)
  })

  it('buildDetailUrl', () => {
    const urlObj = server.buildUrl(DataModel as any, 1)
    expect(urlObj).toEqual(`${url}1/`)
  })

  it.skip('id busname', () => {
    /*
    const urlObj = server.buildUrl(DataModelList as any, [1, 2, 3] as any)
    expect(urlObj).toEqual({
      resourceName: url.resourceName,
      namespace: url.namespace,
      ids: [1, 2, 3]
    } as any)
    expect(server.busName('get', { url: urlObj })).toBe('get_ns_rn_1.2.3')
    */
  })

  it.skip('ids busname empty ids', () => {
    /*
    const urlObj = server.buildUrl(DataModelList as any, [] as any)
    expect(urlObj).toEqual({
      resourceName: url.resourceName,
      namespace: url.namespace,
      ids: []
    })
    expect(server.busName('get', { url: urlObj })).toBe('get_ns_rn')
    */
  })

  test('server.request should setup properly', () => {
    let received = false
    server.on('request_' + busName, () => {
      received = true
    })
    expect(received).toBe(false)
    server.request('get', {
      url,
      body: body as any
    })
    expect(server.events).toHaveProperty(busName)
    expect(server.events).toHaveProperty('reject_' + busName)
    expect(received).toBe(true)
  })

  test('check respond object', async () => {
    const promise = server.wait(DataModel, 'get', url.id)
    server.request('get', {
      url,
      body: body as any
    })

    const request = await promise
    expect(request).toMatchObject({
      url,
      body
    })
    expect(request.respond).toBeInstanceOf(Function)
    expect(request.reject).toBeInstanceOf(Function)
  })

  test('wait and respond a request', async () => {
    const promise = server.wait(DataModel, 'get', 1)
    const model = new DataModel()
    const getPromise = model.fetch()
    const request = await promise
    request.respond({
      id: 9
    })
    await getPromise
    expect(model.id).toBe(9)
    expect(server.events).toEqual({})
  })
  test('reject request', async () => {
    const promise = server.wait(DataModel, 'get', 1)
    const model = new DataModel()
    const getPromise = model.fetch()
    const request = await promise
    const err = new Error('rejected')
    request.reject(err)
    await expect(getPromise).rejects.toEqual(err)
    expect(server.events).toEqual({})
  })

  it('should reset', () => {
    server.on('abc', () => {})
    expect(server.events).toHaveProperty('abc')
    server.reset()
    expect(server.events).toEqual({})
  })

  it('hasRequest', () => {
    const model = new DataModel()
    expect(server.hasRequest(DataModel, 'post', 0)).toBe(false)
    model.create()
    expect(server.hasRequest(DataModel, 'post', 0)).toBe(true)
  })
})

describe('Client Request', () => {
  it('should handles get', async () => {
    const promise = server.wait(DataModel, 'get', 1)
    const model = new DataModel()
    model.data = 'd'
    model.fetch()
    const request = await promise
    expect(request).toMatchObject({
      url: `${url}1/`
    })
  })

  it.skip('should handles put', async () => {
    /*
    const promise = server.wait(DataModel, 'put')
    const model = new DataModel()
    model.data = 'd'
    model.update()
    const request = await promise
    expect(request).toMatchObject({
      url,
      body: {
        data: 'd'
      }
    })
    */
  })

  it('should handles post', async () => {
    const promise = server.wait(DataModel, 'post')
    const model = new DataModel()
    model.data = 'd'
    model.create()
    const request = await promise
    expect(request).toMatchObject({
      url,
      body: {
        data: 'd'
      }
    })
  })

  it.skip('should handles delete', async () => {
    /*
    const promise = server.wait(DataModel, 'delete')
    const model = new DataModel()
    model.data = 'd'
    model.delete()
    const request = await promise
    expect(request).toMatchObject({
      url,
      body: undefined
    })
    */
  })

  it.skip('should handles patch', async () => {
    /*
    const promise = server.wait(DataModel, 'patch')
    client.patch(url, 'd')

    const request = await promise
    expect(request).toMatchObject({
      url,
      body: 'd'
    })
    */
  })

  it.skip('should handles head', async () => {
    /*
    const promise = server.wait(DataModel, 'head')
    client.head(url)

    const request = await promise
    expect(request).toMatchObject({
      url,
      body: undefined
    })
    */
  })

  test('client.run wait and respond request', async () => {
    const model = new DataModel()

    await client
      .run(() => {
        model.fetch()
      })
      .wait(DataModel, 'get', 1)
      .before(() => {
        expect(model.id).not.toBe(9)
      })
      .respond({
        id: 9
      })
    expect(model.id).toBe(9)
    expect(server.events).toEqual({})
  })

  test('async client.run wait and respond request', async () => {
    const model = new DataModel()
    const stepper = new Stepper()

    await client
      .run(async () => {
        stepper.step(1)
        await model.fetch()
        stepper.step(3)
      })
      .wait(DataModel, 'get', 1)
      .before(() => {
        stepper.step(2)
        expect(model.id).not.toBe(9)
      })
      .respond({
        id: 9
      })
    expect(model.id).toBe(9)
    expect(server.events).toEqual({})
  })

  test('client.run and fail request', async () => {
    const model = new DataModel()
    let reach = false
    let executed = false

    await client
    .run(async () => {
      executed = true
      await model.fetch()
      reach = true
    })
    .wait(DataModel, 'get', 1)
    .reject()

    expect(executed).toBe(true)
    expect(reach).toBe(false)
  })

  test('client.run wait and respond request with func', async () => {
    const model = new DataModel()
    await client
      .run(() => {
        model.fetch()
      })
      .wait(DataModel, 'get', 1)
      .respond((request: any) => {
        request.respond({
          id: 9
        })
      })
    expect(model.id).toBe(9)
    expect(server.events).toEqual({})
  })

  test('async client.run should reaches end of execution', async () => {
    const model = new DataModel()
    let reached = false

    await client.run(async () => {
        await model.fetch()
        for (const _ in [1, 2, 3, 4, 5]) {
          await $nextTick()
        }
        reached = true
      })
      .wait(DataModel, 'get', 1)
      .respond({})
    expect(reached).toBe(true)
  })

  test.skip('client.run wait for ModelList with pks', async () => {
    /*
    const models = new DataModelList()

    await client
      .run(() => {
        models.fetch([1, 2, 3] as any)
      })
      .wait(DataModelList as any, 'get', [1, 2, 3])
      .respond(
        [1, 2, 3].map(id => ({
          id
        }))
      )

    expect(models).toMatchObject({
      objects: [1, 2, 3].map(id => ({
        id
      }))
    })
    */
  })

  test.skip('client.run wait for ModelList without pks', async () => {
    /*
    const models = new DataModelList()
    await client
      .run(() => {
        models.fetch()
      })
      .wait(DataModelList, 'get')
      .respond(
        [1, 2, 3].map(id => ({
          id
        })))
    expect(models).toMatchObject({
      objects: [1, 2, 3].map(id => ({
        id
      }))
    })
    */
  })
})
