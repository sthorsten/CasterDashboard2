<template>
    <div v-if="!$fetchState.pending">

        <transition appear enter-active-class="animate__animated animate__fadeIn anim_0-5s"
                    leave-active-class="animate__animated animate__slideOutUp">
            <div v-if="animText" class="main-bg"></div>
        </transition>

        <transition appear enter-active-class="animate__animated animate__slideInDown anim_0-5s"
                    leave-active-class="animate__animated animate__slideOutUp">
            <div v-if="animMain" class="main">

                <div class="container-left">

                    <div class="container-title">
                        <!-- Title -->
                        <transition appear
                                    enter-active-class="animate__animated animate__fadeIn anim_0-5s"
                                    leave-active-class="animate__animated animate__fadeOut anim_0-5s">
                            <div v-if="animTitle === 0 && !match.subtitle" class="title-wrapper-big">
                                <span class="title-big">
                                    {{ match.title }}
                                </span>
                            </div>
                            <div v-if="animTitle === 0 && match.subtitle" id="title-wrapper" class="title-wrapper-sm">
                                <span class="title-sm">{{ match.title }}</span>
                                <span class="title-sm">{{ match.subtitle }}</span>
                            </div>
                        </transition>

                        <!-- Map Pick -->
                        <template>
                            <transition appear
                                        enter-active-class="animate__animated animate__fadeIn anim_0-5"
                                        leave-active-class="animate__animated animate__fadeOut anim_0-5s">
                                <div v-if="animTitle === 1 && currentMap && currentMap.type === 3"
                                     class="title-wrapper-big">
                                    <span class="title-big">Decider Map</span>
                                </div>
                            </transition>
                            <transition appear
                                        enter-active-class="animate__animated animate__fadeIn anim_0-5s"
                                        leave-active-class="animate__animated animate__fadeOut anim_0-5s">
                                <div v-if="animTitle === 1 && currentMap && currentMap.choose_team"
                                     class="title-wrapper-big">
                                    <span class="title-big">Map Pick</span>
                                    <img class="logo-team"
                                         :src="getTeamLogoURL(currentMap.choose_team)"
                                         alt="">
                                </div>
                            </transition>
                        </template>
                    </div>

                    <!-- Team Blue -->
                    <transition appear enter-active-class="anim_scaleInRight anim_0-5s">
                        <div v-if="animText" class="container-team-left">
                            <img class="logo-team"
                                 :src="getTeamLogoURL(match.team_blue)"
                                 alt="">
                            <span class="team-name-text-left">{{ match.team_blue_name }}</span>
                        </div>
                    </transition>
                </div>

                <div class="container-center">
                    <!-- Score Blue -->
                    <div v-if="!animScore" class="container-score-left"></div>
                    <transition appear enter-active-class="anim_scaleInLeft anim_0-5s">
                        <div v-if="animScore && match.best_of === 1" class="container-score-left">
                            <div v-if="match.score_blue >= 1" class="score active"></div>
                            <div v-else class="score"></div>
                        </div>
                    </transition>
                    <transition appear enter-active-class="anim_scaleInLeft anim_0-5s">
                        <div v-if="animScore && (match.best_of === 2 || match.best_of === 3)"
                             class="container-score-left">
                            <div v-if="match.score_blue >= 1" class="score active"></div>
                            <div v-else class="score"></div>
                            <div v-if="match.score_blue >= 2" class="score active"></div>
                            <div v-else class="score"></div>
                        </div>
                    </transition>
                    <transition appear enter-active-class="anim_scaleInLeft anim_0-5s">
                        <div v-if="animScore && match.best_of === 5" class="container-score-left">
                            <div v-if="match.score_blue >= 1" class="score active"></div>
                            <div v-else class="score"></div>
                            <div v-if="match.score_blue >= 2" class="score active"></div>
                            <div v-else class="score"></div>
                            <div v-if="match.score_blue >= 3" class="score active"></div>
                            <div v-else class="score"></div>
                        </div>
                    </transition>

                    <!-- League Logo -->
                    <div class="container-logo">
                        <transition appear enter-active-class="animate__animated animate__zoomIn anim_0-5s">
                            <img v-if="animText" class="logo"
                                 :src="getLeagueLogoURL(match.league)" alt="">
                        </transition>
                    </div>

                    <!-- Score Orange -->
                    <div class="container-score-right">
                        <div v-if="!animScore" class="container-score-right"></div>
                        <transition appear enter-active-class="anim_scaleInRight anim_0-5s">
                            <div v-if="animScore && match.best_of === 1" class="container-score-right">
                                <div v-if="match.score_orange >= 1" class="score active"></div>
                                <div v-else class="score"></div>
                            </div>
                        </transition>
                        <transition appear enter-active-class="anim_scaleInRight anim_0-5s">
                            <div v-if="animScore && (match.best_of === 2 || match.best_of === 3)"
                                 class="container-score-right">
                                <div v-if="match.score_orange >= 1" class="score active"></div>
                                <div v-else class="score"></div>
                                <div v-if="match.score_orange >= 2" class="score active"></div>
                                <div v-else class="score"></div>
                            </div>
                        </transition>
                        <transition appear enter-active-class="anim_scaleInRight anim_0-5s">
                            <div v-if="animScore && match.best_of === 5" class="container-score-right">
                                <div v-if="match.score_orange >= 1" class="score active"></div>
                                <div v-else class="score"></div>
                                <div v-if="match.score_orange >= 2" class="score active"></div>
                                <div v-else class="score"></div>
                                <div v-if="match.score_orange >= 3" class="score active"></div>
                                <div v-else class="score"></div>
                            </div>
                        </transition>
                    </div>
                </div>

                <div class="container-right">

                    <transition appear enter-active-class="anim_scaleInLeft anim_0-5s">
                        <div v-if="animText" class="container-team-right">
                            <span class="team-name-text-right">{{ match.team_orange_name }}</span>
                            <img class="logo-team" :src="getTeamLogoURL(match.team_orange)"
                                 alt="">
                        </div>
                    </transition>

                    <div class="container-sponsor">
                        <transition appear
                                    enter-active-class="animate__animated animate__fadeIn anim_0-5s"
                                    leave-active-class="animate__animated animate__fadeOut anim_0-5s">
                            <img v-if="animSponsor !== -1 && activeSponsor !== -1"
                                 :src="getSponsorLogoURL(activeSponsor)" alt=""
                                 class="sponsor">
                        </transition>
                    </div>

                </div>

            </div>
        </transition>

    </div>
</template>

<script>

import {SingleUser} from "~/mixins/axios/SingleUser";
import {OverlayStyle} from "~/mixins/axios/OverlayStyle";
import {MatchSingleWebsocket} from "~/mixins/websocket/MatchSingleWebsocket";
import {MatchMapAllWebsocket} from "~/mixins/websocket/MatchMapAllWebsocket";
import {OverlayStateWebsocket} from "~/mixins/websocket/OverlayStateWeboscket";
import {OverlayDataWebsocket} from "~/mixins/websocket/OverlayDataWeboscket";

export default {
    name: "InGameOverlay",
    layout: "empty",
    auth: false,
    fetchOnServer: false,

    data() {
        return {
            animMain: false,
            animText: false,
            animScore: false,

            animTitle: -1,
            animSponsor: -1,
            activeSponsor: -1,

            animTitleTimeout1: null,
            animTitleTimeout2: null,
            animSponsorTimeout1: null,
            animSponsorTimeout2: null
        }
    },

    head() {
        let styleCSS = ""
        if (this.overlayStyle && this.overlayStyle.ingame_style) {
            styleCSS = this.overlayStyle.ingame_style
        } else {
            styleCSS = "default"
        }

        return {
            title: this.$t("overlays.ingame") + " - Caster Dashboard",
            // Dynamically load theme css
            link: [
                {
                    rel: "stylesheet",
                    href: `/assets/css/overlays/ingame-${styleCSS}.css`
                    //href: `/css/overlays/ingame-${styleCSS}.css` // dev only
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
        },
        currentMap() {
            if (this.matchMaps == null) return null
            let matchMaps = this.matchMaps.filter(m => m.status === 2)
            if (matchMaps == null || matchMaps.length === 0) return null
            return matchMaps[0]
        },
    },

    watch: {
        currentMap: {
            deep: true,
            handler(newState, oldState) {
                if (oldState == null) {
                    // (Re)Start Title animation
                    this.animTitle = -1
                    setTimeout(() => this.animTitle = 0, 600)
                }
            }
        },

        overlayState: {
            deep: true,
            handler() {
                if (this.overlayState.ingame_state) {
                    this.animMain = true
                } else {
                    this.animMain = false
                    this.animText = false
                    this.animScore = false
                    this.animTitle = -1
                    this.animSponsor = -1

                    clearTimeout(this.animTitleTimeout1)
                    clearTimeout(this.animTitleTimeout2)
                    clearTimeout(this.animSponsorTimeout1)
                    clearTimeout(this.animSponsorTimeout2)
                }
            }
        },

        overlayData: {
            deep: true,
            handler(newState, oldState) {
                if (oldState.current_match == null || newState.current_match === oldState.current_match) return;
                location.reload()
            }
        },

        animMain: {
            deep: true,
            handler() {
                if (this.animMain) {
                    setTimeout(() => this.animText = true, 500)
                    setTimeout(() => this.animScore = true, 1000)
                    setTimeout(() => this.animTitle = 0, 1000)
                    setTimeout(() => this.animSponsor = 0, 1000)
                }
            }
        },

        animTitle: {
            deep: true,
            handler() {
                if (this.match.best_of !== 1 && this.currentMap) {
                    if (this.animTitle === 0) {
                        // Title => Map
                        this.animTitleTimeout1 = setTimeout(() => this.animTitle = -1, 9400)
                        this.animTitleTimeout2 = setTimeout(() => this.animTitle = 1, 10000)
                    } else if (this.animTitle === 1) {
                        // Map => Title
                        this.animTitleTimeout1 = setTimeout(() => this.animTitle = -1, 9400)
                        this.animTitleTimeout2 = setTimeout(() => this.animTitle = 0, 10000)
                    }
                } else {
                    if (this.match.best_of !== 1 && this.currentMap && this.animTitle !== 0) {
                        clearTimeout(this.animTitleTimeout1)
                        clearTimeout(this.animTitleTimeout2)
                        this.animTitle = -1
                        setTimeout(() => this.animTitle = 0, 600)
                    }
                }
            }
        },

        animSponsor: {
            deep: true,
            handler() {
                if (this.activeSponsor !== -1 && this.animSponsor !== -1 && this.match.sponsors.length > 1) {
                    if (this.animSponsor >= (this.match.sponsors.length - 1)) {
                        this.animSponsorTimeout1 = setTimeout(() => this.animSponsor = -1, 9400)
                        this.animSponsorTimeout2 = setTimeout(() => {
                            this.activeSponsor = this.match.sponsors[0]
                            this.animSponsor = 0
                        }, 10000)
                    } else {
                        let next = this.animSponsor + 1
                        this.animSponsorTimeout1 = setTimeout(() => this.animSponsor = -1, 9400)
                        this.animSponsorTimeout2 = setTimeout(() => {
                            this.activeSponsor = this.match.sponsors[next]
                            this.animSponsor = next
                        }, 10000)
                    }
                }
            }
        }
    },

    methods: {
        getTeamLogoURL(id) {
            if (this.$config.baseURL) return `${this.$config.baseURL}/media/teams/${id}_500.webp`
            return `/media/teams/${id}_500.webp`
        },
        getLeagueLogoURL(id) {
            if (this.$config.baseURL) return `${this.$config.baseURL}/media/leagues/${id}_500.webp`
            return `/media/leagues/${id}_500.webp`
        },
        getSponsorLogoURL(id) {
            if (this.$config.baseURL) return `${this.$config.baseURL}/media/sponsors/${id}_100.webp`
            return `/media/sponsors/${id}_100.webp`
        }
    },

    async fetch() {
        // Load data
        await this.getSingleUser()

        await Promise.all([
            this.connectOverlayDataWebsocket(),
            this.getOverlayStyle()
        ])

        this.matchID = this.overlayData.current_match

        await Promise.all([
            this.connectMatchSingleWebsocket(),
            this.connectMatchMapAllWebsocket(),
            this.connectOverlayStateWebsocket()
        ])

        // Set first sponsor (if present)
        if (this.match && this.match.sponsors && this.match.sponsors.length > 0) {
            this.activeSponsor = this.match.sponsors[0]
        }

        // Start Animation
        if (this.overlayState.ingame_state) this.animMain = true
    },

    mixins: [
        SingleUser,
        OverlayStyle,
        MatchSingleWebsocket,
        MatchMapAllWebsocket,
        OverlayStateWebsocket,
        OverlayDataWebsocket
    ],

}
</script>

<style src="animate.css/animate.min.css"></style>
