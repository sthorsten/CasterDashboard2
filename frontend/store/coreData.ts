import { defineStore } from "pinia";
import { io, Socket } from 'socket.io-client'
import { Map } from "~~/types/core/Map";

export const useCoreDataStore = defineStore('coreData', {
  state: () => {
    return {
      socketIO: null as Socket,
      maps: [] as Map[],
    }
  },

  actions: {
    connect() {
      this.socketIO = io("http://localhost:8000/core");
      this.socketIO.on("connect", this.getInitialData);
      this.socketIO.on("map:update", this.handleMapUpdate);
    },
    getInitialData() {
      console.log("getInitialData");
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