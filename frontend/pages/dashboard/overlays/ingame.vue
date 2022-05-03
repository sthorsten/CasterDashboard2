<template>
  <div
    v-if="match"
    class="min-h-screen min-w-full flex justify-center items-start"
  >
    <!-- Overlay container -->
    <div
      id="overlay-container"
      class="min-w-full h-[50px] flex justify-center items-center"
    >
      <!-- Left container -->
      <div class="h-full grow flex bg__team-blue">
        <div class="w-56">
          <p
            class="font-scout-bold uppercase text-2xl leading-none ml-2 text__primary"
          >
            {{ match.title }}
            <br />
            {{ match.subTitle }}
          </p>
        </div>
        <div class="grow flex justify-end items-center">
          <p class="font-scout-bold uppercase text-4xl text__primary">
            {{ match.teamBlueName }}
          </p>
          <img
            :src="getTeamLogo(match.teamBlue)"
            height="35"
            width="35"
            class="mx-3"
          />
        </div>
      </div>

      <!-- Center container -->
      <div class="w-44 h-full bg__center flex">
        <div class="w-12">
          <div class="flex flex-col justify-center items-center h-full">
            <div
              v-if="match.bestOf >= 1"
              class="w-9 h-2 my-0.5 shadow"
              :class="
                match.scoreBlue >= 1 ? 'bg__score-active' : 'bg__score-inactive'
              "
            ></div>
            <div
              v-if="match.bestOf >= 2"
              class="w-9 h-2 my-0.5"
              :class="
                match.scoreBlue >= 2 ? 'bg__score-active' : 'bg__score-inactive'
              "
            ></div>
            <div
              v-if="match.bestOf === 5"
              class="w-9 h-2 my-0.5"
              :class="
                match.scoreBlue >= 3 ? 'bg__score-active' : 'bg__score-inactive'
              "
            ></div>
          </div>
        </div>

        <div class="grow flex justify-center items-center">
          <img :src="leagueLogo" width="35" height="35" />
        </div>

        <div class="w-12">
          <div class="flex flex-col justify-center items-center h-full">
            <div
              v-if="match.bestOf >= 1"
              class="w-9 h-2 my-0.5 1"
              :class="
                match.scoreOrange >= 1
                  ? 'bg__score-active'
                  : 'bg__score-inactive'
              "
            ></div>
            <div
              v-if="match.bestOf >= 2"
              class="w-9 h-2 my-0.5"
              :class="
                match.scoreOrange >= 2
                  ? 'bg__score-active'
                  : 'bg__score-inactive'
              "
            ></div>
            <div
              v-if="match.bestOf === 5"
              class="w-9 h-2 my-0.5"
              :class="
                match.scoreOrange >= 3
                  ? 'bg__score-active'
                  : 'bg__score-inactive'
              "
            ></div>
          </div>
        </div>
      </div>

      <!-- Right container -->
      <div class="h-full grow flex justify-end bg__team-orange">
        <div class="grow flex justify-start items-center">
          <img
            :src="getTeamLogo(match.teamOrange)"
            height="35"
            width="35"
            class="mx-3"
          />
          <p class="font-scout-bold uppercase text-4xl text__primary">
            {{ match.teamOrangeName }}
          </p>
        </div>
        <div class="w-56 flex justify-end items-center">
          <div
            class="absolute"
            v-for="(sponsor, index) in sponsors"
            :key="sponsor.id"
          >
            <transition name="fade" appear>
              <img
                v-if="index === sponsorVisibleIndex"
                class="mr-2 h-[35px]"
                :src="sponsor.logo"
              />
            </transition>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "InGameOverlay",
  auth: false,

  head() {
    return {
      title: "InGame Overlay"
    }
  },

  data() {
    return {
      sponsorVisibleIndex: -1,
      sponsorVisibleInterval: null
    }
  },

  mounted() {
    this.animateSponsor()
    this.sponsorVisibleInterval = setInterval(this.animateSponsor, 10000)
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
    matchMaps() {
      if (this.match) {
        return this.$store.getters['matchSocket/getMatchMapsByMatch'](this.match.id)
      }
    },
    leagueLogo() {
      return this.$store.getters['mainSocket/getLeagueLogo'](this.match.league)
    },
    sponsors() {
      return this.$store.getters['mainSocket/getSponsorsByLeague'](this.match.league)
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
    },
    animateSponsor() {
      // if (!this.sponsors) return
      // if (this.sponsors.length <= 1) return


      if (this.sponsorVisibleIndex === -1) {
        this.sponsorVisibleIndex = 0
      }
      else if ((this.sponsorVisibleIndex + 1) === this.sponsors.length) {
        this.sponsorVisibleIndex = 0
      } else {
        this.sponsorVisibleIndex++
      }
    }
  }

}
</script>

<style scoped>
@import "@/assets/style/tailwind.css";

@layer components {
  .bg__team-blue {
    background: linear-gradient(
      90deg,
      rgba(96, 165, 250, 0.5) 0%,
      rgba(96, 165, 250, 1) 100%
    );
  }
  .bg__team-orange {
    background: linear-gradient(
      90deg,
      rgba(251, 146, 60, 1) 0%,
      rgba(251, 146, 60, 0.5) 100%
    );
  }
  .bg__center {
    @apply bg-gray-900;
  }

  .text__primary {
    @apply text-gray-800;
  }

  .bg__score-inactive {
    @apply bg-gray-500;
  }
  .bg__score-active {
    @apply bg-yellow-300;
  }
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-to,
.fade-leave {
  opacity: 1;
}
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s ease;
}
</style>
