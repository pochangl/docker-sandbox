<template lang="pug">
  div(id="app")
    v-app
      navbar
      router-view
</template>
<script lang="ts">
import Navbar from '@/components/Navbar.vue'
export default {
  components: {
    Navbar
  }
}
</script>
