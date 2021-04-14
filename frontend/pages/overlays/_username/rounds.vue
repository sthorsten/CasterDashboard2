<template>
    <div v-if="!$fetchState.pending">

        <div class="layout-container">

            <transition appear enter-active-class="animate__animated animate__slideInUp anim_0-5s"
                        leave-active-class="animate__animated animate__slideOutDown anim_0-5s">
                <div v-if="animMain" class="main">

                    <table class="rounds-table">
                        <tbody>
                        <!-- Team Blue Row -->
                        <tr>
                            <th>
                                <img class="logo" :src="getTeamLogoURL(match.team_blue)" alt="">
                            </th>

                            <td v-for="(round, index) in rounds" :key="index">
                                <transition appear enter-active-class="animate__animated animate__fadeIn anim_0-5s">
                                    <template v-if="animRounds >= index && round.win_team === match.team_blue">
                                        <img class="win-icon" :src="getWinIconURL(round.win_type)">
                                    </template>
                                </transition>
                            </td>
                        </tr>

                        <!-- Team Orange Row -->
                        <tr>
                            <th>
                                <img class="logo" :src="getTeamLogoURL(match.team_orange)" alt="">
                            </th>

                            <td v-for="(round, index) in rounds" :key="index">
                                <transition appear enter-active-class="animate__animated animate__fadeIn anim_0-5s">
                                    <template v-if="animRounds >= index && round.win_team === match.team_orange">
                                        <img class="win-icon" :src="getWinIconURL(round.win_type)">
                                    </template>
                                </transition>
                            </td>
                        </tr>

                        </tbody>
                    </table>

                    <div class="title-container">
                        <span id="title" class="title">Round Breakdown</span>
                    </div>

                </div>
            </transition>
        </div>

    </div>
</template>

<script>

import {SingleUser} from "~/mixins/axios/SingleUser";
import {OverlayStyle} from "~/mixins/axios/OverlayStyle";
import {MatchSingleWebsocket} from "~/mixins/websocket/MatchSingleWebsocket";
import {OverlayStateWebsocket} from "~/mixins/websocket/OverlayStateWeboscket";
import {OverlayDataWebsocket} from "~/mixins/websocket/OverlayDataWeboscket";
import {MatchMapAllWebsocket} from "~/mixins/websocket/MatchMapAllWebsocket";
import {RoundWebsocket} from "~/mixins/websocket/RoundWebsocket";

export default {
    name: "RoundsOverlay",
    layout: "empty",
    auth: false,
    fetchOnServer: false,

    data() {
        return {
            matchID: null,
            animMain: false,
            animRounds: -1
        }
    },

    head() {
        let styleCSS = ""
        if (this.overlayStyle && this.overlayStyle.rounds_style) {
            styleCSS = this.overlayStyle.rounds_style
        } else {
            styleCSS = "default"
        }

        return {
            title: this.$t("overlays.rounds") + " - Caster Dashboard",
            // Dynamically load theme css
            link: [
                {
                    rel: "stylesheet",
                    href: `/css/overlays/rounds-${styleCSS}.css`
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
        mapID() {
            if (this.currentMap == null) return null
            return this.currentMap.map
        }
    },

    watch: {
        rounds: {
            deep: true,
            handler() {
                if (this.rounds.length > 0 && this.animMain) {
                    this.animRounds = this.rounds.length
                }
            }
        },

        overlayState: {
            deep: true,
            handler() {
                if (this.overlayState.rounds_state) {
                    this.animMain = true
                } else {
                    this.animMain = false
                    this.animRounds = -1
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
                if (!this.rounds || !this.animMain) return
                for (let i = 0; i < this.rounds.length; i++) {
                    setTimeout(() => this.animRounds++, (i + 1) * 500)
                }
            }
        }
    },

    methods: {
        getTeamLogoURL(id) {
            if (this.$config.baseURL) return `${this.$config.baseURL}/media/teams/${id}_500.webp`
            return `/media/teams/${id}_500.webp`
        },
        getWinIconURL(type) {
            return require(`~/assets/img/winicons/${type}.png`)
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
            this.connectMatchMapAllWebsocket()
        ])
        await Promise.all([
            this.connectRoundWebsocket(),
            this.connectOverlayStateWebsocket()
        ])

        // Start Animation
        if (this.overlayState.rounds_state) this.animMain = true
    },

    mixins: [
        SingleUser,
        OverlayDataWebsocket,
        OverlayStyle,
        MatchSingleWebsocket,
        MatchMapAllWebsocket,
        RoundWebsocket,
        OverlayStateWebsocket
    ],
}
</script>

<style src="animate.css/animate.min.css"></style>
