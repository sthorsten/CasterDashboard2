export default {

  ssr: false,

  head: {
    title: 'caster-dashboard-2',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
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
    ]
  },

  css: [
  ],



  plugins: [
    { src: '~/plugins/fontawesome', ssr: false },
    { src: '~/plugins/vue-select', ssr: false },
    { src: '~/plugins/websocket', ssr: false }
  ],

  components: [
    {
      path: '~/components',
      pathPrefix: false
    }
  ],

  buildModules: [
    // '@nuxtjs/eslint-module'
  ],

  modules: [
    'bootstrap-vue/nuxt',
    'vue-toastification/nuxt',
    '@nuxtjs/axios',
    '@nuxtjs/auth-next'
  ],

  publicRuntimeConfig: {
    baseURL: process.env.BASE_URL,
    browserBaseURL: process.env.BROWSER_BASE_URL,
    wsBaseURL: process.env.WS_BASE_URL
  },

  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    baseURL: process.env.BASE_URL,
    browserBaseURL: process.env.BROWSER_BASE_URL
  },

  router: {
    middleware: ['auth'],
    linkActiveClass: 'active'
  },

  toast: {
    position: 'top-center',
    timeout: 3000
  },

  auth: {
    cookie: {
      options: {
        sameSite: 'lax',
        secure: true
      }
    },

    localStorage: false,
    fullPathRedirect: true,

    strategies: {
      local: {
        scheme: 'refresh',
        token: {
          property: 'access',
          maxAge: 1800,
          global: true
        },
        refreshToken: {
          property: 'refresh',
          data: 'refresh',
          maxAge: 60 * 60 * 24
        },
        user: {
          property: false,
          autoFetch: true
        },
        endpoints: {
          login: { url: '/api/v2/token/', method: 'post' },
          refresh: { url: '/api/v2/token/refresh/', method: 'post' },
          user: { url: '/api/v2/user/me/', method: 'get' },
          logout: false
        },
        redirect: {
          login: '/login',
          logout: '/logout',
          home: '/dashboard/home'
        }
      }
    }
  },

  build: {
    loaders: {
      scss: {
        sassOptions: {
          quietDeps: true
        }
      }
    }
  }
}
