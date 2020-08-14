<template lang="pug">
  div.modal-base.pa-0.ma-0(:class="{active: value}")
    v-icon.grey--text.white.clickable(v-if="value" @click="$emit('input', false)" fab) fa-times-circle
    div.mask.black(v-if="value" @click="$emit('input', false)" fab)
    slot
</template>
<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component
export default class Modal extends Vue {
  @Prop({ type: Boolean, required: true })
  value: boolean
}
</script>

<style lang="sass" scoped>
  .modal-base.active
    z-index: 1000
    position: fixed
    width: 100%
    height: 100%
    left: 0
    top: 0
    .mask
      position: absolute
      top: 0
      left: 0
      opacity: 0.3
      width: 100%
      height: 100%
    .v-icon
      z-index: 1001
      position: absolute
      right: 30px
      top: 30px
      border-radius: 20px
      &.clickable
        cursor: grab

</style>
