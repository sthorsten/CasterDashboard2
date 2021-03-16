<template>
    <div v-if="!$fetchState.pending">

        <transition appear enter-active-class="animate__animated animate__slideInUp"
                    leave-active-class="animate__animated animate__slideOutDown">
            <div v-if="animMain" class="main">
                <DynamicMarquee direction="row" :reverse="true" :speed="{type: 'pps', number: 80}" :repeat-margin="5">
                    <div class="m-text-wrapper">

                        <!-- Manual text -->
                        <template v-if="tickerText.length > 0">
                            <template v-for="text in tickerText">
                                <span class="m-text ml-2 mr-2">//</span>
                                <span class="m-text">{{ text }}</span>
                            </template>
                        </template>

                        <!-- Current match -->
                        <template v-if="match">
                            <span class="m-text ml-2 mr-2">//</span>
                            <span class="m-text">{{ this.$t('navigation.current_match') }}:</span>
                            <span class="m-text">
                                {{ match.team_blue_name }}
                                <img class="m-text-img" :src="getTeamLogoURL(match.team_blue)" alt="">
                                <span v-if="match.score_blue === 0 && match.score_orange === 0"
                                      class="ml-1 mr-1">- vs -</span>
                                <span v-else class="ml-1 mr-1">{{ match.score_blue }} - {{ match.score_orange }}</span>
                                <img class="m-text-img" :src="getTeamLogoURL(match.team_orange)" alt="">
                                {{ match.team_orange_name }}
                            </span>
                        </template>

                        <!-- Finished matches -->
                        <template v-if="finishedMatches.length > 0">
                            <span class="m-text ml-2 mr-2">//</span>
                            <span class="m-text">{{ this.$t('overlays.ticker.recent_matches') }}:</span>

                            <template v-for="(m, index) in finishedMatches">
                                <span class="m-text">
                                    {{ m.team_blue_name }}
                                    <img class="m-text-img" :src="getTeamLogoURL(m.team_blue)" alt="">
                                    <span v-if="m.score_blue === 0 && m.score_orange === 0"
                                          class="ml-1 mr-1">- vs -</span>
                                    <span v-else class="ml-1 mr-1">{{ m.score_blue }} - {{ m.score_orange }}</span>
                                    <img class="m-text-img" :src="getTeamLogoURL(m.team_orange)" alt="">
                                    {{ m.team_orange_name }}
                                </span>
                                <span v-if="index < (finishedMatches.length - 1)" class="m-text ml-2 mr-2">&</span>
                            </template>
                        </template>

                        <!-- Upcoming matches -->
                        <template v-if="upcomingMatches.length > 0">
                            <span class="m-text ml-2 mr-2">//</span>
                            <span class="m-text">{{ this.$t('overlays.ticker.upcoming_matches') }}:</span>

                            <template v-for="(m, index) in upcomingMatches">
                                <span class="m-text">
                                    {{ m.team_blue_name }}
                                    <img class="m-text-img" :src="getTeamLogoURL(m.team_blue)" alt="">
                                    <span v-if="m.score_blue === 0 && m.score_orange === 0"
                                          class="ml-1 mr-1">- vs -</span>
                                    <span v-else class="ml-1 mr-1">{{ m.score_blue }} - {{ m.score_orange }}</span>
                                    <img class="m-text-img" :src="getTeamLogoURL(m.team_orange)" alt="">
                                    {{ m.team_orange_name }}
                                </span>
                                <span v-if="index < (upcomingMatches.length - 1)" class="m-text ml-2 mr-2">&</span>
                            </template>
                        </template>
                    </div>
                </DynamicMarquee>
            </div>

        </transition>
    </div>
</template>

<script>
import {SingleUser} from "~/mixins/axios/SingleUser";
import {OverlayStyle} from "~/mixins/axios/OverlayStyle";
import {MatchSingleWebsocket} from "~/mixins/websocket/MatchSingleWebsocket";
import {OverlayStateWebsocket} from "~/mixins/websocket/OverlayStateWeboscket";
import {OverlayDataWebsocket} from "~/mixins/websocket/OverlayDataWeboscket";
import {MatchGroupWebsocket} from "~/mixins/websocket/MatchGroupWebsocket";
import CustomCard from "~/components/CustomCard";
import DynamicMarquee from 'vue-dynamic-marquee';


export default {
    name: "TickerOverlay",
    layout: "empty",
    auth: false,
    fetchOnServer: false,

    data() {
        return {
            matchGroupData: [],
            animMain: true,
        }
    },

    head() {
        // ToDo: Add custom theme handling
        let style = "default"

        return {
            title: this.$t("overlays.ticker_overlay") + " - Caster Dashboard",
            // Dynamically load theme css
            link: [
                {
                    rel: "stylesheet",
                    href: `/assets/css/overlays/ticker-${style}.css`
                    //href: `/css/overlays/ticker-${style}.css` // dev only
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
        finishedMatches() {
            if (this.matchGroupData.length === 0) return []
            return this.matchGroupData.filter(m => m.state === 4)
        },
        upcomingMatches() {
            if (this.matchGroupData.length === 0) return []
            return this.matchGroupData.filter(m => m.state <= 3)
        },
        tickerText() {
            if (!this.tickerOverlayData || !this.tickerOverlayData.text) return []
            return this.tickerOverlayData.text.split(",")
        }
    },

    watch: {
        matchGroup: {
            deep: true,
            async handler() {
                if (this.matchGroup) {
                    this.animMain = false
                    this.matchGroupData = []
                    for (const matchID of this.matchGroup.matches) {
                        if (matchID !== this.matchID) {
                            await this.$axios.$get(`/api/match/${matchID}/`)
                                .then((data) => {
                                    this.matchGroupData.push(data);
                                })
                        }
                    }
                    if (this.overlayState.ticker_state) this.animMain = true
                }
            }
        },
        overlayState: {
            deep: true,
            handler() {
                this.animMain = !!this.overlayState.ticker_state;
            }
        },
        overlayData: {
            deep: true,
            handler(newState, oldState) {
                if (oldState.current_match == null || newState.current_match === oldState.current_match) return;
                location.reload()
            }
        },
    },

    methods: {
        getTeamLogoURL(id) {
            if (this.$config.baseURL) return `${this.$config.baseURL}/media/teams/${id}_50.webp`
            return `/media/teams/${id}_500.webp`
        }
    },

    async fetch() {
        // Load data
        await this.getSingleUser()
        await this.connectOverlayDataWebsocket()
        await this.getOverlayStyle()

        this.matchID = this.overlayData.current_match
        await this.connectMatchSingleWebsocket()
        await this.connectOverlayStateWebsocket()

        // Get match group and all matches except the current one
        await this.connectMatchGroupWebsocket()
    },

    mixins: [
        SingleUser,
        OverlayDataWebsocket,
        OverlayStyle,
        MatchSingleWebsocket,
        OverlayStateWebsocket,
        MatchGroupWebsocket
    ],

    components: {
        "CustomCard": CustomCard,
        "DynamicMarquee": DynamicMarquee
    }

}
</script>

<style src="animate.css/animate.min.css"></style>
