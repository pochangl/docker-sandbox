/*
  Data Model that blends well with django_rest_framework
*/
import Vue from 'vue'
import { Http } from 'vue-resource/types/vue_resource'
import VueResource from 'vue-resource'

Vue.use(VueResource)
const http: Http = (Vue as any).http

function getListUrl(name: string): string {
  return '//api/' + name + '/'
}

function getDetailUrl(name: string, id: number): string {
  return '//api/' + name + '/' + id + '/'
}

interface IModelConstructor<T extends Model> {
  new(): T
  fields: string[]
  viewName: string
}

interface IRawModel {
  id: number
  [key: string]: any
}

export abstract class Model {
  // class that handles single data from API
  id: number = 0
  static fields = []
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
    let data: IRawModel = {
      id: this.id
    }
    for (const name of fields) {
      data[name] = (this as any)[name]
    }
    return data
  }

  async fetch() {
    // fetching data from server
    const viewName: string = (this.constructor as any).viewName
    const url = getDetailUrl(viewName, this.id)
    const response = await http.get(url)
    this.construct(response.json())
  }

  async create() {
    // post data to server
    const viewName: string = (this.constructor as any).viewName
    const url = getListUrl(viewName)
    const response = await http.post(url, this.json())
    this.construct(response.json())
  }
}

export abstract class ModelList<T extends Model> {
  // class that handles list of Models
  objects: T[] = []

  async fetch() {
    // fetching data from server
    const Model: IModelConstructor<T> = (this.constructor as any).Model.viewName
    const url: string = getListUrl(Model.viewName)
    const response = await http.get(url)
    this.objects = response.json().map((content: any) => {
      const model = new Model()
      model.construct(content)
      return model
    })
  }
}
