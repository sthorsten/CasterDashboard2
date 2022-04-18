<template>
  <div
    v-if="match"
    class="min-h-screen min-w-full flex justify-center items-center"
  >
    <div
      v-if="mode === 'full'"
      class="w-[1400px] h-24 flex justify-center items-center bg-gradient-to-r from-blue-400 via-gray-400 to-orange-400"
    >
      <div class="flex justify-end items-center">
        <p class="mr-3 font-scout-bold uppercase text-black text-5xl">
          {{ match.teamBlueName }}
        </p>
        <img :src="getTeamLogo(match.teamBlue)" class="h-16 w-16" />
      </div>

      <p class="mx-4 font-scout-bold text-black text-5xl">
        <template v-if="match.scoreBlue === 0 && match.scoreOrange === 0">
          - VS -
        </template>
        <template v-else>
          {{ match.scoreBlue }} - {{ match.scoreOrange }}
        </template>
      </p>

      <div class="flex justify-start items-center">
        <img :src="getTeamLogo(match.teamOrange)" class="h-16 w-16" />
        <p class="ml-3 font-scout-bold uppercase text-black text-5xl">
          {{ match.teamOrangeName }}
        </p>
      </div>
    </div>

    <!-- Normal mode / logos only -->
    <div v-else class="w-60 h-24 flex justify-center items-center">
      <img :src="getTeamLogo(match.teamBlue)" class="h-16 w-16" />
      <p class="mx-3 font-scout-bold text-black text-5xl">
        <template v-if="match.scoreBlue === 0 && match.scoreOrange === 0">
          - VS -
        </template>
        <template v-else>
          {{ match.scoreBlue }} - {{ match.scoreOrange }}
        </template>
      </p>
      <img :src="getTeamLogo(match.teamOrange)" class="h-16 w-16" />
    </div>
  </div>
</template>

<script>
export default {
  name: "StartOverlay",
  auth: false,

  head() {
    return {
      title: "Start Overlay"
    }
  },

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
    mode() {
      if (this.$route.query.mode && this.$route.query.mode === 'full') return 'full'
      return 'logos'
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
    getTeamLogo(id) {
      const team = this.$store.getters['mainSocket/getTeam'](id)
      return team.logo
    }
  }

}
</script>

<style scoped>
@import "@/assets/style/tailwind.css";
</style>
