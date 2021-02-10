<template>
    <div v-if="!$fetchState.pending">

        <div class="main-bg"></div>

        <transition appear enter-active-class="animate__animated animate__fadeIn"
                    leave-active-class="animate__animated animate__fadeOut">
            <div v-if="animMain" class="main">

                <div class="container-left">
                    <transition appear enter-active-class="animate__animated animate__fadeIn">
                        <img v-if="animLogos" :src="`${$config.baseURL}/media/teams/${match.team_blue}_500.webp`"
                             class="logo-team" alt="">
                    </transition>
                    <transition appear enter-active-class="anim_scaleInRight">
                        <span v-if="animText" class="team-name-text-right">{{ match.team_blue_name }}</span>
                    </transition>
                </div>

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

                <div class="container-right">
                    <transition appear enter-active-class="anim_scaleInLeft">
                        <span v-if="animText" class="team-name-text-right">{{ match.team_orange_name }}</span>
                    </transition>
                    <transition appear enter-active-class="animate__animated animate__fadeIn">
                        <img v-if="animLogos" :src="`${$config.baseURL}/media/teams/${match.team_orange}_500.webp`"
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
        let style = "default"

        return {
            title: this.$t("overlays.start") + " - Caster Dashboard",
            link: [
                {
                    rel: "stylesheet",
                    href: `/css/overlays/start-${style}.css`
                }
            ]
        }
    },

    computed: {
        username() {
            return this.$route.params.username
        },
        userID(){
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

    mounted() {
    },

    async fetch() {
        await this.getCurrentUserMatch()
        this.matchID = this.currentUserMatch.id
        await this.connectMatchSingleWebsocket()
        await this.connectOverlayStateWebsocket()

        // Start Animation
        if (this.overlayState.start_state) this.animMain = true
    },

    mixins: [
        CurrentUserMatch,
        MatchSingleWebsocket,
        OverlayStateWebsocket
    ],

    components: {}

}
</script>

<style src="animate.css/animate.min.css"></style>
