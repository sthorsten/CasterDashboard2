import { defineNuxtConfig } from 'nuxt'

export default defineNuxtConfig({
  css: [
    'vue-toastification/dist/index.css',
    '@/css/main.scss'
  ],

  build: {
    transpile: [
      '@fortawesome/vue-fontawesome',
      '@fortawesome/fontawesome-svg-core',
      '@fortawesome/free-solid-svg-icons',
      '@fortawesome/free-regular-svg-icons',
      '@fortawesome/free-brands-svg-icons',
    ]
  },

  experimental: {
    reactivityTransform: true
  },

  vite: {
    resolve: {

      alias: [
        // @ts-ignore
        {
          find: /^~.+/,
          replacement: (val) => {
            return val.replace(/^~/, "");
          },
        },
      ],
    },
  },

  runtimeConfig: {
    dockerBackendHost: '',
    public: {
      baseURL: ''
    }
  },

  typescript: {
    shim: false
  }
})
