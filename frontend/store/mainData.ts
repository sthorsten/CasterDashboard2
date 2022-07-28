import { defineStore } from "pinia";
import { io, Socket } from 'socket.io-client'
import { useRuntimeConfig } from "#app";
import { useAuthStore } from "./auth";
import { Team } from "~~/types/main/Team";
import { League } from "~~/types/main/League";

export const useMainDataStore = defineStore('mainData', {
  state: () => {
    return {
      socketIO: null as Socket,
      socketError: false,
      leagues: [] as League[],
      teams: [] as Team[],
    }
  },

  actions: {
    connect() {
      const authStore = useAuthStore()
      if (!authStore.loggedIn) return

      this.socketIO = io(useRuntimeConfig().public.baseURL + "/main", {
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
      this.socketIO.emit("team:list", {}, (response: Team[]) => {
        this.teams = response;
      })
      this.socketIO.emit("league:list", {}, (response: League[]) => {
        this.leagues = response;
      })
    }
  },

  getters: {
    getTeamLogoById(state) {
      return (teamId: number) => {
        const team = state.teams.find((team) => team.id === teamId)
        return team.logo
      }
    },
    getLeagueLogoById(state) {
      return (leagueId: number) => {
        const league = state.leagues.find((league) => league.id === leagueId)
        return league.logo
      }
    }
  }

})