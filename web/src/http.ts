import Vue from 'vue'
import { Http } from 'vue-resource/types/vue_resource'
import VueResource from 'vue-resource'

Vue.use(VueResource)
export default (Vue as any).http as Http
