<template lang="pug">
  v-container(style="height: 90vh" fluid)
    v-layout(row wrap)
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
            v-tab(href="#settings") 設定
          v-tabs-items.content(v-model="tab")
            v-tab-item(value="description")
              v-card(flat)
                v-card-text
                  pre {{ problemModel.description }}
            v-tab-item(value="stdout")
              submission-output(:problem="problemModel" :submission="submission")
            v-tab-item(value="stderr")
              v-card(flat)
                v-card-text
                  pre.red--text {{ submission.stderr }}
            v-tab-item(value="settings")
              v-card(flat)
                v-card-text
                  v-btn(:href="'/admin/problem/problem/' + problemModel.id + '/change/'" target="_blank")
                    v-icon fa-edit
                    | 編輯
      v-flex.pt-4.pr-4.editor
        code-editor(@submit="submit" :initial="problemModel.initial_code" :key="problemModel.id")
    v-snackbar(
      v-model="notification"
      :timeout="10000"
    ) submission {{ submission.stdout ? 'success' : 'failed'}}
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
    return this.$route.params.id
  }
  submission: Submission = new Submission()

  @ProblemTransformer('problem')
  problemModel: Problem = new Problem()

  tab: string = 'description'
  notification: string = ''

  async submit(code: string) {
    Submission.contextmanager<Submission>(async socket => {
      socket.send('run', socket.json())
      const [submission, notification] = await Promise.all([socket.onResult(), socket.onNotification()])
      this.submission = submission
      this.notification = notification

      this.focusTab()
    }, {
      code,
      problem: this.problemModel.id
    })
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
    max-width: 500px
  .content
    background-color: transparent
    pre
      word-wrap: break-word
      white-space: pre-wrap
    .v-card
      background-color: transparent
  .editor
    height: 80vh
</style>
