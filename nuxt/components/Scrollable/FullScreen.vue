<template lang="pug">
  modal.fullscreen(v-model="full")
    component.fullscreen-content.white(:is="tag" :class="{pad: pad}")
      slot
</template>
<script lang="ts">
import { Vue, Component, Prop, Watch } from 'vue-property-decorator'
import Modal from './Modal.vue'
import Scrollable from './index.vue'

@Component({
  components: {
    Modal,
    Scrollable
  }
})
export default class FullScreen extends Vue {
  @Prop({ type: Boolean, required: true })
  value: boolean

  @Prop({ type: Boolean, default: false })
  pad: boolean

  full: boolean = false

  get tag () {
    return this.value ? 'scrollable' : 'div'
  }

  @Watch('value', { immediate: true })
  onValue (to: boolean) {
    this.full = to
  }

  @Watch('full')
  onFull (to: boolean) {
    this.$emit('input', to)
  }
}
</script>
<style lang="sass" scoped>
  .fullscreen.active
    .fullscreen-content
      position: relative
      left: 40px
      top: 40px
      width: calc(100% - 80px)
      height: calc(100% - 80px)
      &.pad
        padding: 20px
</style>
