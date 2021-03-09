<template>
    <div v-if="!$fetchState.pending">

        <div v-if="animMain" class="main">

            <transition appear enter-active-class="animate__animated animate__fadeIn anim_0-5s">
                <div v-if="(animOps >= 1 && getBanOrder(1) === 2) || (animOps >= 0 && getBanOrder(1) === 1)"
                     id="op1" class="opban-container">
                    <img class="opban-image" :src="getOperatorImgURL(this.match.team_blue, 'ATK')" alt="">
                </div>
            </transition>

            <transition appear enter-active-class="animate__animated animate__fadeIn anim_0-5s">
                <div v-if="(animOps >= 2 && getBanOrder(2) === 3) || (animOps >= 3 && getBanOrder(2) === 4)"
                     id="op2" class="opban-container">
                    <img class="opban-image" :src="getOperatorImgURL(this.match.team_blue, 'DEF')" alt="">
                </div>
            </transition>

            <transition appear enter-active-class="animate__animated animate__fadeIn anim_0-5s">
                <div v-if="(animOps >= 3 && getBanOrder(3) === 4) || (animOps >= 2 && getBanOrder(3) === 3)"
                     id="op3" class="opban-container">
                    <img class="opban-image" :src="getOperatorImgURL(this.match.team_orange, 'DEF')" alt="">
                </div>
            </transition>

            <transition appear enter-active-class="animate__animated animate__fadeIn anim_0-5s">
                <div v-if="(animOps >= 0 && getBanOrder(4) === 1) || (animOps >= 1 && getBanOrder(4) === 2)"
                     id="op4" class="opban-container">
                    <img class="opban-image" :src="getOperatorImgURL(this.match.team_orange, 'ATK')" alt="">
                </div>
            </transition>

        </div>

    </div>
</template>

<script>
import {SingleUser} from "~/mixins/axios/SingleUser";
import {OverlayStyle} from "~/mixins/axios/OverlayStyle";
import {OverlayStateWebsocket} from "~/mixins/websocket/OverlayStateWeboscket";
import {MatchMapAllWebsocket} from "~/mixins/websocket/MatchMapAllWebsocket";
import {MatchSingleWebsocket} from "~/mixins/websocket/MatchSingleWebsocket";
import {OperatorBansWebsocket} from "~/mixins/websocket/OperatorBansWebsocket";
import {OverlayDataWebsocket} from "~/mixins/websocket/OverlayDataWeboscket";

export default {
    name: "OperatorBansOverlay",
    layout: "empty",
    auth: false,
    fetchOnServer: false,

    data() {
        return {
            animMain: false,
            animOps: -1
        }
    },

    head() {
        // ToDo: Add custom theme handling
        let style = "default"

        return {
            title: this.$t("overlays.opbans") + " - Caster Dashboard",
            // Dynamically load theme css
            link: [
                {
                    rel: "stylesheet",
                    href: `/assets/css/overlays/opbans-${style}.css`
                    //href: `/css/overlays/opbans-${style}.css` // dev only
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
            return this.matchMaps.filter(m => m.status === 2)[0]
        },
        mapID() {
            if (this.currentMap == null) return null
            return this.currentMap.map
        },
    },

    watch: {
        bannedOperators: {
            deep: true,
            handler() {
                if (this.bannedOperators.length > 0 && this.animMain) {
                    this.animOps = this.bannedOperators.length - 1
                }
            }
        },
        overlayState: {
            deep: true,
            handler() {
                if (this.overlayState.opbans_state) {
                    this.animMain = true
                } else {
                    this.animMain = false
                    this.animOps = -1
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
                if (!this.bannedOperators || !this.animMain) return
                for (let i = 0; i < this.bannedOperators.length; i++) {
                    setTimeout(() => this.animOps++, (i + 1) * 500)
                }
            }
        }
    },

    methods: {
        getTeamLogoURL(id) {
            if (this.$config.baseURL) return `${this.$config.baseURL}/media/teams/${id}_500.webp`
            return `/media/teams/${id}_500.webp`
        },
        getOperatorImgURL(team, side) {
            if (!this.bannedOperators.length > 0) return 0
            let operator = this.bannedOperators.filter(o => o.operator_side === side && o.team === team)[0]
            if (operator) return require(`@/assets/img/operators/${operator.operator}.svg`)
            return 0
        },
        getBanOrder(overlayOrder) {
            if (this.currentMap.atk_team === this.match.team_blue) {
                switch (overlayOrder) {
                    case 1:
                        return 2
                    case 2:
                        return 3
                    case 3:
                        return 4
                    case 4:
                        return 1
                }
            } else {
                switch (overlayOrder) {
                    case 1:
                        return 1
                    case 2:
                        return 4
                    case 3:
                        return 3
                    case 4:
                        return 2
                }
            }
        }
    },

    async fetch() {
        // Load data
        await this.getSingleUser()
        await this.getOverlayStyle()
        await this.connectOverlayDataWebsocket()

        this.matchID = this.overlayData.current_match
        await this.connectMatchSingleWebsocket()
        await this.connectMatchMapAllWebsocket()
        await this.connectOperatorBansWebsocket()
        await this.connectOverlayStateWebsocket()

        // Start Animation
        if (this.overlayState.opbans_state) this.animMain = true
    },

    mixins: [
        SingleUser,
        OverlayStyle,
        MatchSingleWebsocket,
        MatchMapAllWebsocket,
        OverlayStateWebsocket,
        OverlayDataWebsocket,
        OperatorBansWebsocket,
    ],

}
</script>

<style src="animate.css/animate.min.css"></style>
