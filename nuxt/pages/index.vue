<template lang="pug">
  v-container(fluid)
    v-list(v-if="problems")
      v-subheader 所有題目
      v-list-item(
        router
        :to="{name: 'problem-id', params: { id: problem.id }}"
        v-for="problem in problems.objects"
        :key="problem.id"
      )
        v-list-item-title {{ problem.title }}
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { ProblemList } from '@/models/problem'

@Component
export default class Home extends Vue {
  problems: ProblemList | null = null

  created () {
    this.fetch().then().catch()
  }

  async fetch () {
    const problems = new ProblemList()
    await problems.fetch()
    this.problems = problems
  }
}
</script>
