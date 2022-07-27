import { defineStore } from 'pinia'


export const useMainStore = defineStore('main', {
  state: () => {
    return {
      sidebarCollapse: false
    }
  },

  actions: {
    collapseSidebar() {
      this.sidebarCollapse = !this.sidebarCollapse
    }
  }
})