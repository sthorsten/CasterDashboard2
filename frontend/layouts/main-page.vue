<template>
  <div class="wrapper">
    <div v-if="preloader" class="preloader flex-column justify-content-center align-items-center">
      <img src="img/ThorsHero_200.webp" width="100" height="100">
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
  data () {
    return {
      preloader: true
    }
  },
  head () {
    return {
      script: [
        {
          src: 'https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js',
          integrity: 'sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj',
          crossorigin: 'anonymous'
        },
        {
          src: 'https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js',
          integrity: 'sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjsOMm/tB9LTS58ONXgqbR9W8oWht/amnpF',
          crossorigin: 'anonymous',
          defer: true
        },
        { src: 'https://cdn.jsdelivr.net/npm/admin-lte@3.1/dist/js/adminlte.min.js', defer: true }
      ],
      link: [
        { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/admin-lte@3.1/dist/css/adminlte.min.css' }
      ],
      bodyAttrs: {
        class: 'hold-transition dark-mode sidebar-mini layout-fixed layout-navbar-fixed'
      }
    }
  },
  mounted () {
    this.preloader = false
  }
}
</script>
