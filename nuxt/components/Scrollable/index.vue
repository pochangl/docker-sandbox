<template lang="pug">
  div.scrollable(ref="container")
    slot
</template>
<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import PerfectScrollbar from 'perfect-scrollbar'
import 'perfect-scrollbar/css/perfect-scrollbar.css'

@Component
export default class Scrollable extends Vue {
  ps: PerfectScrollbar

  mounted () {
    this.refresh()
  }
  updated () {
    this.refresh()
  }
  refresh () {
    if (this.ps) {
      this.ps.update()
    } else {
      this.ps = new PerfectScrollbar((this.$refs as any).container)
    }
  }
  beforeDestroy () {
    this.ps.destroy()
  }
}
</script>
<style lang="sass">
  .scrollable
    position: relative
    overflow: hidden
    .ps__rail-y, .ps__rail-x
      z-index: 20
</style>
