<template lang="pug">
  v-container(style="height: 90vh" fluid)
    v-layout(row wrap fill-height)
      v-flex.description.flex-grow-0.pa-4
        v-card(flat color="transparent")
          v-card-title.white
            h1.font-weight-bold.display-1 {{ problemModel.title }}

          v-tabs(
            v-model="tab"
            color="grey"
            grow
          )
            v-tab(href="#description") 題目描述
            v-tab(href="#stdout" :disabled="!submission.stdout") 輸出結果
            v-tab(href="#stderr" :disabled="!submission.stderr") 錯誤結果
            v-tab(href="#video" :disabled="!submission.stdout") 視訊
          v-tabs-items.content(v-model="tab")
            v-tab-item(value="description")
              v-card(flat)
                v-card-text {{ problemModel.description }}
            v-tab-item(value="stdout")
              submission-output(:problem="problemModel" :submission="submission")
            v-tab-item(value="stderr")
              v-card(flat)
                v-card-text
                  pre.red--text {{ submission.stderr }}
            v-tab-item(value="video")
              v-card(flat)
                v-card-text
                  youtube(vid="BBwEF6WBUQs" v-if="tab=='video'")
      v-flex.pt-4.pr-4
        code-editor(@submit="submit")
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

// components
import CodeEditor from '@/components/CodeEditor.vue'
import Youtube from '@/components/Youtube.vue'
import SubmissionOutput from '@/components/problem/output/index.vue'

// models
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
    CodeEditor,
    Youtube,
    SubmissionOutput
  }
})
export default class ProblemPage extends Vue {
  get problem () {
    return this.$route.params.problem
  }
  submission: Submission = new Submission()

  @ProblemTransformer('problem')
  problemModel: Problem = new Problem()

  tab: string = 'description'

  async submit(code: string) {
    const submission = new Submission()
    submission.code = code
    submission.problem = this.problemModel.id
    await submission.create()
    this.submission = submission
    this.focusTab()
  }

  focusTab () {
    if (this.submission.stderr) {
      this.tab = 'stderr'
    } else if (this.submission.stdout) {
      this.tab = 'stdout'
    } else {
      this.tab = 'description'
    }
  }
}
</script>
<style lang="sass" scoped>
  .description
    min-width: 500px
  .content
    background-color: transparent
    .v-card
      background-color: transparent
</style>
