<template lang="pug">
  v-container.pa-0.ma-0
    full-screen(v-model="full")
      iframe(v-if="isFullHTML" ref="iframe" width="100%" height="100%")
      v-layout(v-else column)
        v-layout(justify-end v-if="!full")
          v-icon.clickable.mr-2(@click="full=true") fa-expand
        div.html-tag(v-html="html")
</template>
<script lang="ts">
import { Vue, Component, Prop, Watch } from 'vue-property-decorator'
import FullScreen from '@/components/Scrollable/FullScreen.vue'

@Component({
  components: {
    FullScreen
  }
})
export default class TextHtml extends Vue {
  @Prop({ type: String, required: true })
  value: string

  full: boolean = false

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

  async updateResult () {
    this.full = this.isFullHTML
    await this.$nextTick()

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
.clickable
  cursor: grab
iframe
  border: none
</style>
<style lang="sass">
// django form configuration

.errorlist
  color: red
</style>
