import { defineStore } from "pinia";
import { io, Socket } from 'socket.io-client'
import { useRuntimeConfig } from "#app";
import { useAuthStore } from "./auth";
import { Match } from "~~/types/match/Match";

export const useMatchDataStore = defineStore('matchData', {
  state: () => {
    return {
      socketIO: null as Socket,
      socketError: false,
      matches: [] as Match[],
    }
  },

  actions: {
    connect() {
      const authStore = useAuthStore()
      if (!authStore.loggedIn) return

      this.socketIO = io(useRuntimeConfig().public.baseURL + "/match", {
        auth: {
          token: authStore.token
        }
      });
      this.socketIO.on("connect", this.getInitialData);
      this.socketIO.on("connect_error", () => {
        this.socketError = true
      });
    },
    getInitialData() {
      this.socketIO.emit("match:list", {}, (response: Match[]) => {
        this.matches = response;
      })
    }
  }

})