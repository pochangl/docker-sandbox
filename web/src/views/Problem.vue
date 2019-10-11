<template lang="pug">
  v-container(style="height: 90vh" fluid)
    v-layout(row wrap fill-height)
      v-flex(xs2)
        p {{ problemModel.title }}
        p {{ problemModel.description }}
      v-flex(xs10)
        code-editor(@submit="submit")
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import CodeEditor from '@/components/CodeEditor.vue'
import { Submission, Problem } from '@/models/problem'
import { DataTransformer } from '@/utils/component'

const ProblemTransformer = DataTransformer(async (id: number) => {
  const problem = new Problem()
  problem.id = id
  await problem.fetch()
  return problem
})

@Component({
  components: {
    CodeEditor
  }
})
export default class ProblemPage extends Vue {
  get problem () {
    return this.$route.params.problem
  }

  @ProblemTransformer('problem')
  problemModel: Problem = new Problem()

  async submit(code: string) {
    const submission = new Submission()
    submission.code = code
    submission.problem = this.problemModel.id
    await submission.create()
  }
}
</script>
