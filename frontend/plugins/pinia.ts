import { defineNuxtPlugin, useCookie } from '#app'
import { createPinia } from 'pinia'
import { createNuxtPersistedState } from 'pinia-plugin-persistedstate'

const pinia = createPinia()
pinia.use(createNuxtPersistedState(useCookie))

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(pinia)
})