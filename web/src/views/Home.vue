<template lang="pug">
  v-container(style="height: 90vh")
    code-editor
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import CodeEditor from '@/components/CodeEditor.vue'

@Component({
  components: {
    CodeEditor
  }
})
export default class Home extends Vue {}
</script>
