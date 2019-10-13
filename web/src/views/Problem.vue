<template lang="pug">
  v-container(style="height: 90vh" fluid)
    v-layout(row wrap fill-height)
      v-flex.flex-grow-0.pa-4
        p {{ problemModel.title }}
        p {{ problemModel.description }}
        template(v-if="submission")
          pre.green--text {{ submission.stdout }}
          pre.red--text(v-if="submission.stderr") {{ submission.stderr }}
      v-flex
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
  submission: Submission | null = null

  @ProblemTransformer('problem')
  problemModel: Problem = new Problem()

  async submit(code: string) {
    const submission = new Submission()
    submission.code = code
    submission.problem = this.problemModel.id
    await submission.create()
    this.submission = submission
  }
}
</script>
