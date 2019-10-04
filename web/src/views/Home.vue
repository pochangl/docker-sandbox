<template lang="pug">
  div(class="home")
    p This is a Home page
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Home extends Vue {}
</script>
