<template>
  <div v-if="!$fetchState.pending">
    <transition
      appear
      enter-active-class="animate__animated animate__slideInUp anim_0-5s"
      leave-active-class="animate__animated animate__slideOutDown anim_0-5s"
    >
      <div v-if="animMain" class="main">
        <div
          v-for="(map, index) in matchMaps"
          :key="map.id"
          :class="mapContainerClass(map)"
        >
          <transition
            appear
            enter-active-class="animate__animated animate__fadeIn anim_0-5s"
          >
            <div v-if="animMap >= index" class="img-container">
              <img
                class="map"
                :src="require('~/assets/img/maps/' + map.map_name + '.webp')"
                alt=""
              />
              <img
                v-if="map.type !== 3 && map.type !== 4"
                class="team"
                :src="getTeamLogoURL(map.choose_team)"
                alt=""
              />
              <img
                v-else
                class="team"
                :src="getLeagueLogoURL(match.league)"
                alt=""
              />
            </div>
          </transition>
          <transition
            appear
            enter-active-class="animate__animated animate__slideInUp anim_0-5s"
          >
            <span v-if="animMap >= index" class="map-description">{{
              map.map_name
            }}</span>
          </transition>
        </div>

        <div v-for="i in 7 - matchMaps.length" :key="i" class="map-container">
          "
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
  import {SingleUser} from "~/mixins/axios/SingleUser"
  import {MatchSingleWebsocket} from "~/mixins/websocket/MatchSingleWebsocket"
  import {MatchMapAllWebsocket} from "~/mixins/websocket/MatchMapAllWebsocket"
  import {OverlayStateWebsocket} from "~/mixins/websocket/OverlayStateWeboscket"
  import {OverlayDataWebsocket} from "~/mixins/websocket/OverlayDataWeboscket"

  export default {
    name: "MapsOverlay",
    layout: "empty",
    auth: false,
    fetchOnServer: false,

    data() {
      return {
        animMain: false,
        animMap: -1,
      }
    },

    head() {
      // ToDo: Add custom theme handling
      let style = "default"

      return {
        title: this.$t("overlays.maps") + " - Caster Dashboard",
        // Dynamically load theme css
        link: [
          {
            rel: "stylesheet",
            href: `/css/overlays/maps-${style}.css`,
          },
        ],
      }
    },

    computed: {
      username() {
        return this.$route.params.username
      },
      userID() {
        return this.currentUser.id
      },
    },

    watch: {
      matchMaps: {
        deep: true,
        handler() {
          if (this.matchMaps.length > 0 && this.animMain) {
            this.animMap = this.matchMaps.length
          }
        },
      },

      overlayState: {
        deep: true,
        handler() {
          if (this.overlayState.maps_state) {
            this.animMain = true
          } else {
            this.animMain = false
            this.animMap = -1
          }
        },
      },

      overlayData: {
        deep: true,
        handler(newState, oldState) {
          if (
            oldState.current_match == null ||
            newState.current_match === oldState.current_match
          )
            return
          location.reload()
        },
      },

      animMain: {
        deep: true,
        handler() {
          if (!this.matchMaps || !this.animMain) return
          for (let i = 0; i < this.matchMaps.length; i++) {
            setTimeout(() => this.animMap++, (i + 1) * 500)
          }
        },
      },
    },

    methods: {
      mapContainerClass(map) {
        if (map.type === 1 || map.type === 4) {
          return "map-container ban"
        } else if (map.type === 2 || map.type === 3) {
          return "map-container pick"
        }
        return "map-container"
      },

      getTeamLogoURL(id) {
        if (this.$config.baseURL)
          return `${this.$config.baseURL}/media/teams/${id}_500.webp`
        return `/media/teams/${id}_500.webp`
      },

      getLeagueLogoURL(id) {
        if (this.$config.baseURL)
          return `${this.$config.baseURL}/media/leagues/${id}_500.webp`
        return `/media/leagues/${id}_500.webp`
      },
    },

    async fetch() {
      // Load data
      await this.getSingleUser()
      await this.connectOverlayDataWebsocket()

      this.matchID = this.overlayData.current_match

      await Promise.all([
        this.connectMatchSingleWebsocket(),
        this.connectMatchMapAllWebsocket(),
        this.connectOverlayStateWebsocket(),
      ])

      // Start Animation
      if (this.overlayState.maps_state) this.animMain = true
    },

    mixins: [
      SingleUser,
      MatchSingleWebsocket,
      MatchMapAllWebsocket,
      OverlayStateWebsocket,
      OverlayDataWebsocket,
    ],
  }
</script>

<style src="animate.css/animate.min.css"></style>
