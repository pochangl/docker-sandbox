<template lang="pug" functional>
  v-toolbar.flex-grow-0
    v-toolbar-items
      v-btn(
        exact-active-class="hide"
        exact
        text
        router
        :to="{name: 'home'}"
      ) Home
    v-spacer
    v-toolbar-items
      v-btn(
        router
        href="https://github.com/pochangl/docker-sandbox"
        target="_blank"
        text
      )
        i.fab.fa-github.fa-2x
</template>
<style lang="sass" scoped>
.hide
  display: none
</style>
