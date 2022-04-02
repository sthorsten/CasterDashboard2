<template>
  <div class="flex flex-col justify-end min-h-screen min-w-full">
    <div
      class="bg-neutral-300 h-48 w-full flex justify-around border-t-4 border-neutral-500"
    >
      <!-- Map Bans -->
      <div
        v-for="mapBan in mapBans"
        :key="mapBan.id"
        class="mx-2 flex justify-center items-center"
      >
        <div class="flex flex-col justify-center items-center">
          <img
            v-if="getMapByMapBan(mapBan)"
            :src="getMapByMapBan(mapBan).image"
            :class="getMapBorderClasses(mapBan)"
            class="border-4 rounded-lg"
          />
          <img
            v-if="!mapBan.isDecider && getTeamById(mapBan.team)"
            :src="getTeamById(mapBan.team).logoSmall"
            class="w-12 h-12 absolute -mt-5"
          />
          <img
            v-if="mapBan.isDecider && league"
            :src="league.logoSmall"
            class="w-12 h-12 absolute -mt-5"
          />
          <span class="mt-2 font-scout-bold text-3xl uppercase">
            {{ mapBan.mapName }}
          </span>
        </div>
      </div>

      <!-- Placeholder -->
      <template v-if="mapBans">
        <div v-for="i in 9 - mapBans.length" :key="i" class="mx-2 flex">
          <img width="480" height="270" class="invisible" />
        </div>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapBanOverlay',
  auth: false,

  computed: {
    userOverlay() {
      return this.$store.state.overlaySocket.userOverlay
    },

    match() {
      try {
        return this.$store.getters['matchSocket/getMatch'](this.userOverlay.overlayMatch)
      } catch {
        return null
      }
    },
    mapBans() {
      try {
        return this.$store.getters['matchSocket/getMapBansByMatch'](this.userOverlay.overlayMatch)
      } catch {
        return null
      }
    },
    maps() {
      return this.$store.state.coreSocket.maps
    },
    teams() {
      return this.$store.state.mainSocket.teams
    },
    league() {
      return this.$store.getters['mainSocket/getLeague'](this.match.league)
    }
  },

  watch: {
    userOverlay(newVal) {
      if (newVal.overlayMatch) {
        this.$store.dispatch('matchSocket/getMatchMaps', newVal.match)
      }
    }
  },
  methods: {
    getMapByMapBan(mapBan) {
      return this.maps.find((m) => m.id === mapBan.map)
    },
    getTeamById(id) {
      return this.teams.find(t => t.id === id)
    },
    getMapBorderClasses(mapBan) {
      const typeClass = mapBan.type === 'BAN' ? 'brightness-[.4]' : ''
      let borderClass = ''
      if (mapBan.type === 'BAN') {
        borderClass = 'border-red-500'
      } else if (mapBan.type === 'PICK') {
        borderClass = 'border-green-700'
      }
      return `${typeClass} ${borderClass}`
    }
  }

}
</script>

<style scoped>
@import "@/assets/style/tailwind.css";
</style>
