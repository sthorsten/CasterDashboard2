export default {
  // Target (https://go.nuxtjs.dev/config-target)
  target: "server",

  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: "Caster Dashboard",
    meta: [
      {charset: "utf-8"},
      {name: "viewport", content: "width=device-width, initial-scale=1"},
      {hid: "description", name: "description", content: ""},
    ],
    link: [{rel: "icon", type: "image/x-icon", href: "/assets/favicon.ico"}],
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    {src: "~/plugins/vuex-persist", ssr: false},
    {src: "~/plugins/vuelidate", ssr: true},
    {src: "~/plugins/vue-select", ssr: false},
    {src: "~/plugins/vue-izitoast", ssr: false},
    {src: "~/plugins/vue-apexcharts", ssr: false},
    {src: "~/plugins/vue-clipboard", ssr: false},
    "~/plugins/local-axios",
  ],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  publicRuntimeConfig: {
    baseURL: process.env.BASE_URL || "",
    browserBaseURL: process.env.BROWSER_BASE_URL || "",
    websocketBaseURL: process.env.WEBSOCKET_BASE_URL || "",

    fromEmail: process.env.EMAIL_ADDRESS,
    registrationEnabled: process.env.REGISTRATION_ENABLED,
  },

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: ["@nuxtjs/pwa"],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    "cookie-universal-nuxt",
    "bootstrap-vue/nuxt",
    "@nuxtjs/axios",
    "@nuxtjs/auth-next",
    "nuxt-mail",
    "nuxt-i18n",
    "@nuxtjs/fontawesome",
  ],

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    baseURL: process.env.BASE_URL,
  },

  pwa: {
    manifest: {
      name: "R6 Caster Dashboard v2",
      short_name: "Caster Dashboard",
      background_color: "#121212",
      theme_color: "#363636",
    },
  },

  // Nuxt Auth module config
  auth: {
    redirect: {
      login: "/login",
      callback: "/login",
      home: "/",
    },
    strategies: {
      local: {
        scheme: "refresh",
        token: {
          property: "access",
          maxAge: 60 * 60 * 12, // 12 hours
          type: "Bearer",
        },
        refreshToken: {
          property: "refresh",
          data: "refresh",
          maxAge: 60 * 60 * 24 * 7, // 7 days
        },
        user: {
          property: "user",
          autoFetch: false,
        },
        endpoints: {
          login: {url: "/api/token/", method: "post"},
          refresh: {url: "/api/token/refresh/", method: "post"},
        },
      },
    },
  },

  mail: {
    smtp: {
      host: process.env.EMAIL_HOST,
      port: process.env.EMAIL_PORT,
      secure: process.env.EMAIL_USE_TLS,
      auth: {
        user: process.env.EMAIL_USERNAME,
        pass: process.env.EMAIL_PASSWORD,
      },
    },
  },

  i18n: {
    locales: [
      {
        code: "en",
        file: "en.json",
      },
      {
        code: "de",
        file: "de.json",
      },
    ],
    vueI18n: {
      fallbackLocale: "en",
      silentFallbackWarn: true,
      dateTimeFormats: {
        en: {
          short: {
            year: "numeric",
            month: "short",
            day: "2-digit",
          },
        },
        de: {
          short: {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
          },
        },
      },
    },
    lazy: true,
    langDir: "locales/",
    defaultLocale: "en",
    detectBrowserLanguage: {
      fallbackLocale: "en",
    },
    strategy: "no_prefix",
    vueI18nLoader: true,
  },

  router: {
    middleware: ["auth"],
  },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    extend(config, {isClient}) {
      // Extend only webpack config for client-bundle
      if (isClient) {
        config.devtool = "source-map"
      }
    },
  },
}
