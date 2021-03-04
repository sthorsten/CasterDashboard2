<template>
    <div v-if="!$fetchState.pending">

        <!-- Background -->
        <transition appear enter-active-class="animate__animated animate__fadeIn"
                    leave-active-class="animate__animated animate__fadeOut">
            <div v-if="animMain" class="main-bg"></div>
        </transition>

        <!-- Main container -->
        <transition appear enter-active-class="animate__animated animate__fadeIn"
                    leave-active-class="animate__animated animate__fadeOut">
            <div v-if="animMain" class="main">

                <!-- Team Blue -->
                <div class="container-left">
                    <transition appear enter-active-class="animate__animated animate__fadeIn">
                        <img v-if="animLogos" :src="getTeamLogoURL(match.team_blue)"
                             class="logo-team" alt="">
                    </transition>
                    <transition appear enter-active-class="anim_scaleInRight">
                        <span v-if="animText" class="team-name-text-right">{{ match.team_blue_name }}</span>
                    </transition>
                </div>

                <!-- Score -->
                <div class="container-center">
                    <transition appear enter-active-class="animate__animated animate__zoomIn anim_0-5s">
                        <span v-if="animText && match.score_blue === 0 && match.score_orange === 0" class="center-text">
                            - vs -
                        </span>
                        <span v-if="animText && (match.score_blue !== 0 || match.score_orange !== 0)"
                              class="center-text">
                            {{ match.score_blue }} - {{ match.score_orange }}
                        </span>
                    </transition>
                </div>

                <!-- Team Orange -->
                <div class="container-right">
                    <transition appear enter-active-class="anim_scaleInLeft">
                        <span v-if="animText" class="team-name-text-right">{{ match.team_orange_name }}</span>
                    </transition>
                    <transition appear enter-active-class="animate__animated animate__fadeIn">
                        <img v-if="animLogos" :src="getTeamLogoURL(match.team_orange)"
                             class="logo-team" alt="">
                    </transition>
                </div>

            </div>
        </transition>

    </div>
</template>

<script>

import {CurrentUserMatch} from "~/mixins/axios/CurrentUserMatch";
import {MatchSingleWebsocket} from "~/mixins/websocket/MatchSingleWebsocket";
import {OverlayStateWebsocket} from "~/mixins/websocket/OverlayStateWeboscket";
import {OverlayStyle} from "~/mixins/axios/OverlayStyle";

export default {
    name: "StartOverlay",
    layout: "empty",
    auth: false,
    fetchOnServer: false,

    data() {
        return {
            matchID: null,
            animMain: false,
            animText: false,
            animLogos: false,
        }
    },

    head() {
        let styleCSS = ""
        if (this.overlayStyle && this.overlayStyle.start_style){
            styleCSS = this.overlayStyle.start_style
        } else {
            styleCSS = "default"
        }

        return {
            title: this.$t("overlays.start") + " - Caster Dashboard",
            // Dynamically load theme css
            link: [
                {
                    rel: "stylesheet",
                    href: `/assets/css/overlays/start-${styleCSS}.css`
                    //href: `/css/overlays/start-${styleCSS}.css` // dev only
                }
            ]
        }
    },

    computed: {
        username() {
            return this.$route.params.username
        },
        userID() {
            return this.currentUser.id
        }
    },

    watch: {
        overlayState: {
            deep: true,
            handler() {
                if (this.overlayState.start_state) {
                    this.animMain = true
                } else {
                    this.animMain = false
                    this.animText = false
                    this.animLogos = false
                }
            }
        },

        animMain: {
            deep: true,
            handler() {
                if (this.animMain) {
                    setTimeout(() => this.animLogos = true, 1000)
                    setTimeout(() => this.animText = true, 1000)
                }
            }
        }
    },

    methods: {
        getTeamLogoURL(id){
            if (this.$config.baseURL) return `${this.$config.baseURL}/media/teams/${id}_500.webp`
            return `/media/teams/${id}_500.webp`
        }
    },

    async fetch() {
        // Load data
        await this.getCurrentUserMatch()
        await this.getOverlayStyle()

        this.matchID = this.currentUserMatch.id
        await this.connectMatchSingleWebsocket()
        await this.connectOverlayStateWebsocket()

        // Start Animation
        if (this.overlayState.start_state) this.animMain = true
    },

    mixins: [
        CurrentUserMatch,
        OverlayStyle,
        MatchSingleWebsocket,
        OverlayStateWebsocket
    ],
}
</script>

<style src="animate.css/animate.min.css"></style>
