import { defineNuxtConfig } from 'nuxt'

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  css: [
    'admin-lte/dist/css/adminlte.css',
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

  runtimeConfig: {
    dockerBackendHost: '',
    public: {
      baseURL: ''
    }
  }
})
