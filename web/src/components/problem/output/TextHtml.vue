<template lang="pug">
  v-container.pa-0.ma-0
    iframe(v-if="isFullHTML" ref="iframe") {{ html }}
    div(v-else v-html="html")
</template>
<script lang="ts">
import { Vue, Component, Prop, Watch } from 'vue-property-decorator'

@Component
export default class TextHtml extends Vue {
  @Prop({ type: String, required: true })
  value: string

  get isFullHTML() {
    return this.html.search('<html') >= 0
  }

  get html() {
    return this.value
  }

  @Watch('value', { immediate: true })
  async onValue () {
    await this.$nextTick()
    this.updateResult()
  }

  updateResult () {
    if (this.isFullHTML) {
      const iframe: { contentWindow: Window } = this.$refs.iframe as any
      iframe.contentWindow.document.open()
      iframe.contentWindow.document.write(this.html)
      iframe.contentWindow.document.close()
    }
  }
}
</script>
<style lang="sass" scoped>
iframe
  border: none
  width: 100%
  height 100%
</style>
