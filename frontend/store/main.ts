import { defineStore } from 'pinia'


export const useMainStore = defineStore('main', {
  state: () => {
    return {
      currentPageTitle: "Home",
      currentPageIcon: "fa-solid fa-house-chimney"
    }
  }
})