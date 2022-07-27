import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  persist: true,

  state: () => {
    return {
      loggedIn: false,
      token: null,
      user: null
    }
  },

  actions: {
    async login(username: string, password: string) {
      try {
        const response: any = await $fetch("/api/v2/token/", {
          method: "POST",

          body: {
            username: username,
            password: password
          }
        })
        this.token = response.token;
        this.user = response.user;
        this.loggedIn = true;
      }
      catch (e) {
        console.error("Login failed: " + e)
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      this.loggedIn = false;
    }
  }

})