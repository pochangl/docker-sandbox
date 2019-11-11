<template lang="pug">
  component(:is="tag" :value="submission.stdout")
</template>
<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { Problem, Submission } from '@/models/problem'
import TextPlain from './TextPlain.vue'
import TextHtml from './TextHtml.vue'

@Component({
  components: {
    TextPlain,
    TextHtml
  }
})
export default class Output extends Vue {
  @Prop({ type: Submission, required: true })
  submission: Submission

  @Prop({ type: Problem, required: true })
  problem: Problem

  get tag() {
    return this.problem.output_type.replace('/', '-')
  }
}
</script>
