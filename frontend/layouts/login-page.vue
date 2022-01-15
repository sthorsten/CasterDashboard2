<template>
  <div class="login-box">
    <div class="login-logo">
      <a href="/"><b>Caster Dashboard</b></a>
    </div>

    <div class="card">
      <div class="card-body login-card-body">
        <Nuxt />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  head () {
    return {
      script: [
        {
          hid: 'jquery',
          src: 'https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js',
          integrity: 'sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj',
          crossorigin: 'anonymous',
          defer: true
        },
        {
          hid: 'bootstrap',
          src: 'https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js',
          integrity: 'sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjsOMm/tB9LTS58ONXgqbR9W8oWht/amnpF',
          crossorigin: 'anonymous',
          defer: true
        },
        {
          hid: 'adminlte',
          src: 'https://cdn.jsdelivr.net/npm/admin-lte@3.1/dist/js/adminlte.min.js',
          defer: true
        }
      ],
      link: [
        { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/admin-lte@3.1/dist/css/adminlte.min.css' }
      ],
      bodyAttrs: {
        class: 'hold-transition dark-mode login-page'
      }
    }
  }
}
</script>
