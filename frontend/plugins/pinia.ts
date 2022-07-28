import { defineNuxtPlugin, useCookie } from '#app'
import { createPinia } from 'pinia'
import { createNuxtPersistedState } from 'pinia-plugin-persistedstate'

export default defineNuxtPlugin(nuxtApp => {
  const pinia = createPinia()
  pinia.use(createNuxtPersistedState(useCookie))
  nuxtApp.vueApp.use(pinia)
})