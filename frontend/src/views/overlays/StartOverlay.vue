<template>

    <div>
        <vue-headful :title="$t('overlays.start') + ' - Caster Dashboard'"/>

        <div class="main-bg"></div>
        <transition name="fade" @after-enter="centerTextAnimated = true; leftAnimated = true; rightAnimated = true" @after-leave="reAnimate">
            <div v-if="animated" class="main" style="animation-delay: 0.5s; animation-duration: 0.5s">


                <div class="container-left" style="background: transparent">
                    <transition name="custom-scale-right" enter-active-class="anim_scaleInRight">
                        <div v-if="leftAnimated" class="container-left">
                            <template v-if="matchData">
                                <img class="logo-team" :src="blueLogoURL" alt="-">
                                <span class="team-name-text-left">{{ matchData.team_blue_name }}</span>
                            </template>
                            <template v-else>
                                <span class="team-name-text-left">Team Blue</span>
                            </template>
                        </div>
                    </transition>
                </div>

                <div class="container-center">
                    <transition name="zoom">
                        <span v-if="centerTextAnimated" class="center-text" style="animation-duration: 0.5s">{{ centerText }}</span>
                    </transition>
                </div>

                <div class="container-right" style="background: transparent">
                    <transition name="custom-scale-left" enter-active-class="anim_scaleInLeft">
                        <div v-if="leftAnimated" class="container-right">
                            <template v-if="matchData">
                                <span class="team-name-text-right">{{ matchData.team_orange_name }}</span>
                                <img class="logo-team" :src="orangeLogoURL" alt="-">
                            </template>
                            <template v-else>
                                <span class="team-name-text-right">Team Orange</span>
                            </template>
                        </div>
                    </transition>
                </div>

            </div>
        </transition>
    </div>

</template>

<script>
require('vue2-animate/dist/vue2-animate.min.css')

export default {
    name: "StartOverlay",
    data() {
        return {
            matchDataWebSocket: null,
            overlayStatusWebSocket: null,

            matchData: null,

            animated: false,
            centerTextAnimated: false,
            leftAnimated: false,
            rightAnimated: false
        }
    },
    computed: {
        centerText() {
            if (this.matchData) {
                if (this.matchData.score_blue === 0 && this.matchData.score_orange === 0) return "- vs -"
                return this.matchData.score_blue + " - " + this.matchData.score_orange
            }
            return "- vs -"
        },
        blueLogoURL() {
            return `${this.$store.state.backendURL}/media/teams/${this.matchData.team_blue}_500.webp`
        },
        orangeLogoURL() {
            return `${this.$store.state.backendURL}/media/teams/${this.matchData.team_orange}_500.webp`
        }
    },
    watch: {
        matchData: function (newState, oldState) {
            if (oldState != null){
                if (oldState.id === newState.id && oldState.score_blue === newState.score_blue && oldState.score_orange === newState.score_orange)
                    return
            }
            this.animated = !oldState;
        }
    },
    methods: {
        reAnimate() {
            if (this.matchData) {
                this.animated = true
                this.centerTextAnimated = false
                this.leftAnimated = false
                this.rightAnimated = false
            }
        },
        connectMatchDataWebsocket() {
            let user = this.$route.path.split('/')[2]
            this.matchDataWebSocket = new WebSocket(`${this.$store.getters.websocketURL}/ws/match_data/${user}/`)
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
    },
    created() {
        this.connectMatchDataWebsocket()
    },
    components: {}
}
</script>

<style scoped lang="scss">
@import "~@/assets/scss/overlays/start.scss";
</style>