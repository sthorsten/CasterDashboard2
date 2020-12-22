<template>
    <div>
        <vue-headful :title="$t('overlays.maps') + ' - Caster Dashboard'"/>

        <transition name="fade" @after-enter="animateMap1 = true">
            <div class="main" style="bottom: 0; overflow: hidden;" v-show="animated" v-if="match != null && matchMaps != null">

                <div v-if="matchMaps && matchMaps.length >= 1" :class="mapContainerClass(matchMaps[0].type)">
                    <transition name="zoom" @after-enter="animateMap2 = true">
                        <div v-show="matchMaps[0] && animateMap1" class="img-container">
                            <img class="map" :src="mapImgURL(matchMaps[0].map)" alt="">
                            <img class="team" :src="teamLogoURL(matchMaps[0].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="matchMaps[0] && animateMap1" class="map-description">{{ matchMaps[0].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="matchMaps && matchMaps.length >= 2" :class="mapContainerClass(matchMaps[1].type)">
                    <transition name="zoom" @after-enter="animateMap3 = true">
                        <div v-show="matchMaps[1] && animateMap2" class="img-container">
                            <img class="map" :src="mapImgURL(matchMaps[1].map)" alt="">
                            <img class="team" :src="teamLogoURL(matchMaps[1].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="matchMaps[1] && animateMap2" class="map-description">{{ matchMaps[1].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="matchMaps && matchMaps.length >= 3" :class="mapContainerClass(matchMaps[2].type)">
                    <transition name="zoom" @after-enter="animateMap4 = true">
                        <div v-show="matchMaps[2] && animateMap3" class="img-container">
                            <img class="map" :src="mapImgURL(matchMaps[2].map)" alt="">
                            <img class="team" :src="teamLogoURL(matchMaps[2].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="matchMaps[2] && animateMap3" class="map-description">{{ matchMaps[2].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="matchMaps && matchMaps.length >= 4" :class="mapContainerClass(matchMaps[3].type)">
                    <transition name="zoom" @after-enter="animateMap5 = true">
                        <div v-show="matchMaps[3] && animateMap4" class="img-container">
                            <img class="map" :src="mapImgURL(matchMaps[3].map)" alt="">
                            <img class="team" :src="teamLogoURL(matchMaps[3].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="matchMaps[3] && animateMap4" class="map-description">{{ matchMaps[3].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="matchMaps && matchMaps.length >= 5" :class="mapContainerClass(matchMaps[4].type)">
                    <transition name="zoom" @after-enter="animateMap6 = true">
                        <div v-show="matchMaps[4] && animateMap5" class="img-container">
                            <img class="map" :src="mapImgURL(matchMaps[4].map)" alt="">
                            <img class="team" :src="teamLogoURL(matchMaps[4].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="matchMaps[4] && animateMap5" class="map-description">{{ matchMaps[4].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="matchMaps && matchMaps.length >= 6" :class="mapContainerClass(matchMaps[5].type)">
                    <transition name="zoom" @after-enter="animateMap7 = true">
                        <div v-show="matchMaps[5] && animateMap6" class="img-container">
                            <img class="map" :src="mapImgURL(matchMaps[5].map)" alt="">
                            <img class="team" :src="teamLogoURL(matchMaps[5].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="matchMaps[5] && animateMap6" class="map-description">{{ matchMaps[5].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="matchMaps && matchMaps.length >= 7" :class="mapContainerClass(matchMaps[6].type)">
                    <transition name="zoom">
                        <div v-show="matchMaps[6] && animateMap7" class="img-container">
                            <img class="map" :src="mapImgURL(matchMaps[6].map)" alt="">
                            <img class="team" :src="leagueLogoURL" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="matchMaps[6] && animateMap7" class="map-description">{{ matchMaps[6].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

            </div>
        </transition>

    </div>
</template>

<script>
import axios from "axios";
import {OverlayStateWebsocketInGame} from "@/mixins/websocket/OverlayStateWebsocketInGame";
import {MatchWebsocket} from "@/mixins/websocket/MatchWebsocket";
import {MatchMapAllWebsocket} from "@/mixins/websocket/MatchMapAllWebsocket";

require('vue2-animate/dist/vue2-animate.min.css')

export default {
    name: "MapsOverlay",
    mixins: [MatchWebsocket, MatchMapAllWebsocket, OverlayStateWebsocketInGame],
    data() {
        return {
            matchID: null,

            animated: false,
            animateMap1: false,
            animateMap2: false,
            animateMap3: false,
            animateMap4: false,
            animateMap5: false,
            animateMap6: false,
            animateMap7: false,
        }
    },
    computed: {
        user() {
            return this.$route.path.split('/')[2]
        },
        leagueLogoURL() {
            return `${this.$store.state.backendURL}/media/leagues/${this.match.league}_500.webp`
        }
    },
    watch: {
        overlayState: function (newState) {
            if (newState.maps_state) this.animated = true
            else this.resetAnimations();
        },
        matchMaps: function (newState, oldState) {
            if (!oldState) return
            if (oldState.length > newState.length) {
                this.resetAnimations()
                setTimeout(() => {
                    this.animated = true;
                }, 1000)
            }
        },
        match: function (newState, oldState) {
            if (!this.overlayState || !this.overlayState.maps_state) return
            if (oldState != null) {
                if (oldState.id === newState.id)
                    return
            }
            this.resetAnimations()
            setTimeout(() => {
                this.animated = true;
            }, 1000)
        },
        matchID: function(newState){
            if (newState) {
                this.connectMatchWebsocket()
                this.connectMatchMapAllWebsocket()
            }
        }
    },
    methods: {
        mapImgURL(id) {
            return require(`@/assets/img/maps/${id}.webp`)
        },
        teamLogoURL(id) {
            return `${this.$store.state.backendURL}/media/teams/${id}_500.webp`
        },
        mapContainerClass(type) {
            if (type == null) return
            if (type === 1 || type === 4) return "map-container ban"
            else if (type === 2 || type === 3) return "map-container pick"
            return "map-container"
        },
        resetAnimations() {
            this.animated = false;
            setTimeout(() => {
                this.animateMap1 = false;
                this.animateMap2 = false;
                this.animateMap3 = false;
                this.animateMap4 = false;
                this.animateMap5 = false;
                this.animateMap6 = false;
                this.animateMap7 = false;
            }, 500)
        },
        getMatchID(){
            // Get user id
            axios.get(`${this.$store.state.backendURL}/api/user/?username=${this.$route.path.split('/')[2]}`
            ).then((response) => {
                let userID = response.data[0].id

                // Get user match
                axios.get(`${this.$store.state.backendURL}/api/overlay/match_data/?user=${userID}`
                ).then((response) => {
                    this.matchID = response.data[0].current_match
                })
            })
        }
    },
    created() {
        this.getMatchID()
    },
    components: {}
}
</script>

<style scoped lang="scss">
@import "~@/assets/scss/overlays/maps.scss";

.main {
    background: #222;
}

* {
    animation-duration: 0.5s !important;
    overflow: hidden !important;
    line-height: 1 !important;
}
</style>