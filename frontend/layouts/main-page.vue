<template>
  <div class="wrapper">
    <adminlte-header />
    <div
      v-if="preloader"
      class="preloader flex-column justify-content-center align-items-center"
    >
      <img src="/static/img/ThorsHero_200.webp" width="100" height="100" />
      <span>Caster Dashboard</span>
    </div>
    <MainNavigation />
    <MainSidebar />
    <div class="content-wrapper">
      <Nuxt />
    </div>
    <MainFooter />
  </div>
</template>

<script>
export default {
  data() {
    return {
      preloader: true
    }
  },
  head() {
    return {
      bodyAttrs: {
        class: 'hold-transition dark-mode sidebar-mini layout-fixed layout-navbar-fixed'
      }
    }
  },
  mounted() {
    this.preloader = false
  }
}
</script>
