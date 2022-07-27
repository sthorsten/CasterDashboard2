import { defineStore } from "pinia";
import { io, Socket } from 'socket.io-client'
import { Map } from "~~/types/core/Map";
import { useRuntimeConfig } from "#app";
import { useAuthStore } from "./auth";
import { useToast } from "vue-toastification";

export const useCoreDataStore = defineStore('coreData', {
  state: () => {
    return {
      socketIO: null as Socket,
      socketError: false,
      maps: [] as Map[],
    }
  },

  actions: {
    connect() {
      const authStore = useAuthStore()
      if (!authStore.loggedIn) return

      this.socketIO = io(useRuntimeConfig().public.baseURL + "/core", {
        auth: {
          token: authStore.token
        }
      });
      this.socketIO.on("connect", this.getInitialData);
      this.socketIO.on("connect_error", () => {
        this.socketError = true
      });
      this.socketIO.on("map:update", this.handleMapUpdate);
    },
    getInitialData() {
      this.socketIO.emit("map:list", {}, (response: Map[]) => {
        this.maps = response;
      })
    },
    handleMapUpdate(data) {
      let oldMap = this.maps.find(map => map.id === data.id);
      if (oldMap) Object.assign(oldMap, data);
      else this.maps.push(data);
    }
  }

})