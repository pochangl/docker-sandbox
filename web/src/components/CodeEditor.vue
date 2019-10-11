<template lang="pug">
  div.code-editor
    div.editor-dom(ref="container")
    v-layout.mt-5
      v-spacer
      v-btn(@click="submit" large) Submit
</template>
<script lang="ts">
import ace from 'ace-builds'
import { Component, Vue } from 'vue-property-decorator'

import 'ace-builds/src-noconflict/mode-python'
import 'ace-builds/src-noconflict/theme-vibrant_ink'

@Component
export default class CodeEditor extends Vue {
  container: any
  editor: any

  mounted() {
    const editor = this.editor = ace.edit(this.$refs.container as any)
    editor.setOptions({
      mode: 'ace/mode/python',
      theme: 'ace/theme/vibrant_ink',
      wrap: true,
      useSoftTabs: true,
      tabSize: 4,
    })
  }
  beforeDestroy() {
    this.editor.destroy()
  }
  submit () {
    this.$emit('submit', this.editor.session.getValue())
  }
}
</script>
<style lang="sass" scoped>
  .code-editor
    width: 100%
    height: 100%
    .editor-dom
      font-size: 24px
      line-height: 36px
      width: 100%
      height: calc(100% - 60px)
</style>
