<template>

    <div>
        <vue-headful :title="$t('overlays.ingame') + ' - Caster Dashboard'"/>

        <div class="main-bg invisible"></div>
        <transition enter-active-class="fadeInDown" leave-active-class="fadeOutUp" @after-enter="animatedLeft = true; animatedRight = true;"
                    @after-leave="reAnimate">
            <div v-if="animated && overlayState && overlayState.ingame_state" class="main" style="animation-delay: 0.5s; animation-duration: 0.5s">

                <div v-if="!animatedLeft" class="container-left" style="background: transparent"></div>
                <transition name="custom-scale-right" enter-active-class="anim_scaleInRight" @after-enter="animateTitle(); animatedScore = true">
                    <div v-if="animatedLeft" class="container-left">
                        <div class="container-title">

                            <transition name="fade" @after-enter="animateTitle">
                                <template v-if="titleAnimated">
                                    <div v-if="matchData.subtitle" id="title-wrapper" class="title-wrapper-sm">
                                        <span class="title-sm">{{ matchData.title }}</span>
                                        <span class="title-sm">{{ matchData.subtitle }}</span>
                                    </div>

                                    <div v-else class="title-wrapper-big">
                                        <span class="title-big">{{ matchData.title }}</span>
                                    </div>
                                </template>

                                <template v-if="mapPickAnimated">
                                    <div v-if="matchMap.type === 3" class="title-wrapper-big">
                                        <span class="title-big">Decider Map</span>
                                    </div>
                                    <div v-if="matchMap.choose_team" class="title-wrapper-big">
                                        <span class="title-big">Map Pick</span>
                                        <img class="logo-team"
                                             :src="chooseTeamLogoURL"
                                             alt="">
                                    </div>
                                </template>
                            </transition>
                        </div>

                        <div class="container-team container-team-left">
                            <img class="logo-team" :src="blueLogoURL" alt="">
                            <span class="team-name-text-left">{{ matchData.team_blue_name }}</span>
                        </div>
                    </div>
                </transition>

                <div class="container-center">
                    <transition name="custom-scale-left" enter-active-class="anim_scaleInLeft">
                        <div v-if="!animatedScore" class="container-score-left" style="background: transparent"></div>
                        <div v-show="animatedScore">
                            <div v-if="matchData.best_of === 1" id="score-left-1" class="container-score-left">
                                <div v-if="matchData.score_blue >= 1" class="score active"></div>
                                <div v-else class="score"></div>
                            </div>
                            <div v-if="matchData.best_of === 2 || matchData.best_of === 3" id="score-left-2" class="container-score-left">
                                <div v-if="matchData.score_blue >= 1" class="score active"></div>
                                <div v-else class="score"></div>
                                <div v-if="matchData.score_blue >= 2" class="score active"></div>
                                <div v-else class="score"></div>
                            </div>
                            <div v-if="matchData.best_of === 5" id="score-left-3" class="container-score-left">
                                <div v-if="matchData.score_blue >= 1" class="score active"></div>
                                <div v-else class="score"></div>
                                <div v-if="matchData.score_blue >= 2" class="score active"></div>
                                <div v-else class="score"></div>
                                <div v-if="matchData.score_blue >= 3" class="score active"></div>
                                <div v-else class="score"></div>
                            </div>
                        </div>
                    </transition>

                    <div class="container-logo">
                        <img class="logo" :src="leagueLogoURL" alt="">
                    </div>

                    <transition name="custom-scale-right" enter-active-class="anim_scaleInRight">
                        <div v-if="!animatedScore" class="container-score-right" style="background: transparent"></div>
                        <div v-show="animatedScore">
                            <div v-if="matchData.best_of === 1" id="score-right-1" class="container-score-right">
                                <div v-if="matchData.score_orange >= 1" class="score active"></div>
                                <div v-else class="score"></div>
                            </div>

                            <div v-if="matchData.best_of === 2 || matchData.best_of === 3" id="score-right-2" class="container-score-right">
                                <div v-if="matchData.score_orange >= 1" class="score active"></div>
                                <div v-else class="score"></div>
                                <div v-if="matchData.score_orange >= 2" class="score active"></div>
                                <div v-else class="score"></div>
                            </div>

                            <div v-if="matchData.best_of === 5" id="score-right-3" class="container-score-right">
                                <div v-if="matchData.score_orange >= 1" class="score active"></div>
                                <div v-else class="score"></div>
                                <div v-if="matchData.score_orange >= 2" class="score active"></div>
                                <div v-else class="score"></div>
                                <div v-if="matchData.score_orange >= 3" class="score active"></div>
                                <div v-else class="score"></div>
                            </div>
                        </div>
                    </transition>
                </div>

                <div v-if="!animatedRight" class="container-right" style="background: transparent"></div>
                <transition name="custom-scale-left" enter-active-class="anim_scaleInLeft" @after-enter="animateSponsor">
                    <div v-if="animatedRight" class="container-right">
                        <div class="container-team">
                            <span class="team-name-text-right">{{ matchData.team_orange_name }}</span>
                            <img class="logo-team" :src="orangeLogoURL" alt="">
                        </div>

                        <div class="container-sponsor">
                            <!--
                            <transition name="fade" mode="out-in" @after-enter="animateSponsor()" @after-leave="animateSponsor()">
                                <img v-if="sponsorAnimated === 0" :src="getCurrentSponsorURL(matchData.sponsors[0])" alt="" class="sponsor">
                                <img v-if="sponsorAnimated === 1" :src="getCurrentSponsorURL(matchData.sponsors[1])" alt="" class="sponsor" style="animation-delay: 1s">
                            </transition>
                            -->

                            <transition name="fade" @after-enter="animateSponsor" mode="out-in">
                                <img v-if="sponsorAnimatedStatus" :src="getCurrentSponsorURL(sponsorAnimated)" alt="" class="sponsor">
                            </transition>
                        </div>
                    </div>
                </transition>

            </div>

        </transition>
    </div>

</template>

<script>
import axios from "axios"

require('vue2-animate/dist/vue2-animate.min.css')

export default {
    name: "InGameOverlay",
    data() {
        return {
            items: [{id: 1, text: "1"}, {id: 2, text: "2"}, {id: 3, text: "3"}],
            matchDataWebSocket: null,
            matchMapWebSocket: null,
            overlayStateWebSocket: null,

            matchData: null,
            matchMap: null,
            overlayState: null,

            titleAnimated: false,
            mapPickAnimated: false,

            sponsorAnimated: null,
            sponsorAnimatedStatus: false,
            sponsorAnimatedIndex: 0,

            userID: null,
            animated: false,
            animatedLeft: false,
            animatedRight: false,
            animatedScore: false,
            centerTextAnimated: false,
        }
    },
    computed: {
        user() {
            return this.$route.path.split('/')[2]
        },
        chooseTeamLogoURL() {
            if (this.matchMap)
                return `${this.$store.state.backendURL}/media/teams/${this.matchMap.choose_team}_50.webp`
            return ""
        },
        leagueLogoURL() {
            return `${this.$store.state.backendURL}/media/leagues/${this.matchData.league}_50.webp`
        },
        blueLogoURL() {
            return `${this.$store.state.backendURL}/media/teams/${this.matchData.team_blue}_500.webp`
        },
        orangeLogoURL() {
            return `${this.$store.state.backendURL}/media/teams/${this.matchData.team_orange}_500.webp`
        },
    },
    watch: {
        matchData: function (newState, oldState) {
            if (oldState != null) {
                if (oldState.id === newState.id && oldState.score_blue === newState.score_blue && oldState.score_orange === newState.score_orange)
                    return

                if (oldState.id !== newState.id) {
                    this.matchMap = null
                    this.matchMapWebSocket.send(JSON.stringify({"command": "get_match_map"}))
                }

                this.reAnimate()
            } else {
                this.animated = true;
            }
        },
        matchMap: function () {
            this.animateTitle()
        }
    },
    methods: {
        reAnimate() {
            if (this.matchData) {
                this.animated = false
                this.titleAnimated = false
                this.mapPickAnimated = false

                this.sponsorAnimated = null
                this.sponsorAnimatedStatus = false
                this.sponsorAnimatedIndex = 0

                this.animatedLeft = false
                this.animatedRight = false
                this.animatedScore = false
                setTimeout(() => {
                    this.animated = true
                }, 1000)
            }
        },
        animateTitle() {
            if (!this.titleAnimated && !this.mapPickAnimated) {
                this.titleAnimated = true
                return;
            }
            if (this.matchMap && (this.matchMap.choose_team || this.matchMap.type === 3)) {
                setTimeout(() => {
                    if (this.titleAnimated) {
                        this.titleAnimated = false
                        setTimeout(() => {
                            this.mapPickAnimated = true;
                        }, 1000)

                    } else {
                        this.mapPickAnimated = false
                        setTimeout(() => {
                            this.titleAnimated = true;
                        }, 1000)
                    }
                }, 5000)
            }
        },
        animateSponsor() {
            if (this.sponsorAnimated === null) {
                if (this.matchData.sponsors === null || this.matchData.sponsors.length === 0) return
                this.sponsorAnimated = this.matchData.sponsors[0];
                this.sponsorAnimatedStatus = true;
                return
            }

            if (this.matchData.sponsors.length === 1) return;

            setTimeout(() => {
                this.sponsorAnimatedStatus = false;

                this.sponsorAnimatedIndex += 1;
                if (this.sponsorAnimatedIndex >= (this.matchData.sponsors.length)) {
                    this.sponsorAnimatedIndex = 0;
                }

                this.sponsorAnimated = this.matchData.sponsors[this.sponsorAnimatedIndex];

            }, 5000)

            setTimeout(() => {
                this.sponsorAnimatedStatus = true;
            }, 6000)
        },
        getCurrentSponsorURL(id) {
            return `${this.$store.state.backendURL}/media/sponsors/${id}_100.webp`
        },
        loadStyle() {
            // Get user id
            axios.get(`${this.$store.state.backendURL}/api/user/?username=${this.user}`, this.$store.getters.authHeader
            ).then((response) => {
                this.userID = response.data[0].id

                // Get user style
                axios.get(`${this.$store.state.backendURL}/api/overlay/style/?user=${this.userID}`, this.$store.getters.authHeader
                ).then((response) => {
                    console.log(response.data[0])
                    import(`@/assets/scss/overlays/ingame-${response.data[0].ingame_style}.scss`);
                })
            }).catch((error) => {
                console.log(error)
            })
        },
        connectMatchMapWebsocket() {
            this.matchMapWebSocket = new WebSocket(`${this.$store.getters.websocketURL}/ws/match_map/${this.user}/`)
            this.matchMapWebSocket.onopen = function () {
                console.log("MatchMap websocket connected.")
                this.send(JSON.stringify({"command": "get_match_map"}))
            }
            this.matchMapWebSocket.onmessage = (e) => {
                console.log(e)
                this.matchMap = JSON.parse(e.data)
            }
            this.matchMapWebSocket.onclose = () => {
                console.warn("Lost websocket connection. Trying to reconnect (5s.)")
                setTimeout(this.connectMatchDataWebsocket, 5000)
            }
        },
        connectMatchDataWebsocket() {
            this.matchDataWebSocket = new WebSocket(`${this.$store.getters.websocketURL}/ws/match_data/${this.user}/`)
            this.matchDataWebSocket.onopen = function () {
                console.log("MatchData websocket connected.")
                this.send(JSON.stringify({"command": "get_match_data"}))
            }
            this.matchDataWebSocket.onmessage = (e) => {
                console.log(e)
                this.matchData = JSON.parse(e.data)
            }
            this.matchDataWebSocket.onclose = () => {
                console.warn("Lost websocket connection. Trying to reconnect (5s.)")
                setTimeout(this.connectMatchDataWebsocket, 5000)
            }
        },
        connectOverlayStateWebsocket() {
            this.overlayStateWebSocket = new WebSocket(`${this.$store.getters.websocketURL}/ws/overlay_state/${this.user}/`)
            this.overlayStateWebSocket.onopen = function () {
                console.log("OverlayState websocket connected.")
                this.send(JSON.stringify({"command": "get_overlay_state"}))
            }
            this.overlayStateWebSocket.onmessage = (e) => {
                console.log(e)
                this.overlayState = JSON.parse(e.data)
            }
            this.overlayStateWebSocket.onclose = () => {
                console.warn("Lost websocket connection. Trying to reconnect (5s.)")
                setTimeout(this.connectOverlayStateWebsocket, 5000)
            }
        },
    },
    created() {
        this.loadStyle()
        this.connectMatchDataWebsocket()
        this.connectMatchMapWebsocket()
        this.connectOverlayStateWebsocket()
    },
    components: {}
}
</script>

<style scoped lang="scss">
* {
    line-height: 1 !important;
}

</style>