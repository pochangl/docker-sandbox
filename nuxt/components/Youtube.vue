<template lang="pug">
  iframe(
    v-if="vid"
    v-bind="sizes"
    sandbox="allow-scripts allow-same-origin allow-presentation"
    class="item item-body full-image state"
    :src="'https://youtube.com/embed/' + vid"
    frameborder="0"
    allowfullscreen
  )
</template>
<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component
export default class Youtube extends Vue {
  @Prop({ type: String, required: true })
  vid: string

  @Prop({ type: Number, default: 400 })
  width: number

  @Prop({ type: Number, default: 0 })
  height: number

  @Prop({ type: Boolean, default: false })
  resizable: boolean

  get sizes () {
    if (this.resizable) {
      return {}
    } else {
      return {
        width: this.width,
        height: this.height || Math.ceil(this.width * 3 / 4)
      }
    }
  }
}
</script>
