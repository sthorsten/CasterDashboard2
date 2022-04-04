<template>
  <footer class="main-footer">
    Created by Thorsten "ThorsHero Schmitt" -
    <a href="https://www.thorshero.de" target="_blank">Website</a>
    <div class="float-right d-none d-sm-inline-block">
      <b>Version</b> {{ version }}
    </div>
  </footer>
</template>

<script>
export default {
  async mounted() {
    if (this.$store.state.version === '0.0.0') {
      try {
        const data = await this.$axios.$get('/api/v2/version/')
        this.$store.commit('setVersion', data.version)
      } catch (e) {
        console.error(e)
      }
    }
  },

  computed: {
    version() {
      return this.$store.state.version
    }
  }
}
</script>
