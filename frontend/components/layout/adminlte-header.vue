<script>
export default {
  head() {
    return {
      script: [
        {
          hid: 'jquery',
          src: 'https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js',
          integrity: 'sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj',
          crossorigin: 'anonymous'
        },
        {
          hid: 'bootstrap',
          src: 'https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js',
          integrity: 'sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjsOMm/tB9LTS58ONXgqbR9W8oWht/amnpF',
          crossorigin: 'anonymous'
        },
        {
          hid: 'adminlte',
          src: 'https://cdn.jsdelivr.net/npm/admin-lte@3.1/dist/js/adminlte.min.js'
        }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/admin-lte@3.1/dist/css/adminlte.min.css' }
      ],
    }
  }
}
</script>