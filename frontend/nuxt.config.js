export default {
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
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  css: [
  ],

  plugins: [
    { src: '~/plugins/websocket', ssr: false }
  ],

  components: [
    {
      path: '~/components',
      pathPrefix: false
    }
  ],

  buildModules: [
    '@nuxtjs/eslint-module',
    '@nuxtjs/fontawesome'
  ],

  modules: [
    'bootstrap-vue/nuxt',
    '@nuxtjs/axios',
    '@nuxtjs/auth-next'
  ],

  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    baseURL: 'https://dev.thorshero.de',
    browserBaseURL: 'https://dev.thorshero.de'
  },

  router: {
    middleware: ['auth']
  },

  fontawesome: {
    component: 'Fa',
    suffix: true,
    icons: {
      solid: [
        'faHome',
        'faBars',
        'faUserCircle',
        'faChevronCircleRight'
      ],
      brands: [
        'faGithub'
      ]
    }
  },

  auth: {
    strategies: {
      local: {
        scheme: 'refresh',
        token: {
          property: 'access',
          maxAge: 1800,
          global: true
          // type: 'Bearer'
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
        localStorage: false,
        fullPathRedirect: true,
        redirect: {
          login: '/login',
          logout: '/login',
          callback: false,
          home: '/'
        }
        // autoLogout: false
      }
    }
  },

  build: {
  }
}
