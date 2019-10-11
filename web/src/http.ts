import Vue from 'vue'
import { Http, HttpInterceptor } from 'vue-resource/types/vue_resource'
import VueResource from 'vue-resource'

Vue.use(VueResource)
const http = (Vue as any).http as Http
export default http

function getCookie (cookieKey: string) {
  const cookieName = `${cookieKey}=`
  const cookieArray = document.cookie.split(';').map(w => w.trim())

  for (const cookie of cookieArray) {
    if (cookie.indexOf(cookieName) === 0) {
      return cookie.substring(cookieName.length, cookie.length);
    }
  }
}

function setCSRF (request: any) {
  request.headers.set('X-CSRFToken', getCookie('csrftoken'))
}
http.interceptors.push(setCSRF as any)
