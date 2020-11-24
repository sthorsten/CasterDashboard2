<template>
    <div>
        <vue-headful :title="$t('overlays.maps') + ' - Caster Dashboard'"/>

        <transition name="fade" @after-enter="animateMap1 = true">
            <div class="main" style="bottom: 0; overflow: hidden;" v-show="animated" v-if="matchData != null && mapData != null">

                <div v-if="mapData && mapData.length >= 1" :class="mapContainerClass(mapData[0].type)">
                    <transition name="zoom" @after-enter="animateMap2 = true">
                        <div v-show="mapData[0] && animateMap1" class="img-container">
                            <img class="map" :src="mapImgURL(mapData[0].map)" alt="">
                            <img class="team" :src="teamLogoURL(mapData[0].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="mapData[0] && animateMap1" class="map-description">{{ mapData[0].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="mapData && mapData.length >= 2" :class="mapContainerClass(mapData[1].type)">
                    <transition name="zoom" @after-enter="animateMap3 = true">
                        <div v-show="mapData[1] && animateMap2" class="img-container">
                            <img class="map" :src="mapImgURL(mapData[1].map)" alt="">
                            <img class="team" :src="teamLogoURL(mapData[1].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="mapData[1] && animateMap2" class="map-description">{{ mapData[1].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="mapData && mapData.length >= 3" :class="mapContainerClass(mapData[2].type)">
                    <transition name="zoom" @after-enter="animateMap4 = true">
                        <div v-show="mapData[2] && animateMap3" class="img-container">
                            <img class="map" :src="mapImgURL(mapData[2].map)" alt="">
                            <img class="team" :src="teamLogoURL(mapData[2].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="mapData[2] && animateMap3" class="map-description">{{ mapData[2].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="mapData && mapData.length >= 4" :class="mapContainerClass(mapData[3].type)">
                    <transition name="zoom" @after-enter="animateMap5 = true">
                        <div v-show="mapData[3] && animateMap4" class="img-container">
                            <img class="map" :src="mapImgURL(mapData[3].map)" alt="">
                            <img class="team" :src="teamLogoURL(mapData[3].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="mapData[3] && animateMap4" class="map-description">{{ mapData[3].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="mapData && mapData.length >= 5" :class="mapContainerClass(mapData[4].type)">
                    <transition name="zoom" @after-enter="animateMap6 = true">
                        <div v-show="mapData[4] && animateMap5" class="img-container">
                            <img class="map" :src="mapImgURL(mapData[4].map)" alt="">
                            <img class="team" :src="teamLogoURL(mapData[4].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="mapData[4] && animateMap5" class="map-description">{{ mapData[4].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="mapData && mapData.length >= 6" :class="mapContainerClass(mapData[5].type)">
                    <transition name="zoom" @after-enter="animateMap7 = true">
                        <div v-show="mapData[5] && animateMap6" class="img-container">
                            <img class="map" :src="mapImgURL(mapData[5].map)" alt="">
                            <img class="team" :src="teamLogoURL(mapData[5].choose_team)" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="mapData[5] && animateMap6" class="map-description">{{ mapData[5].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

                <div v-if="mapData && mapData.length >= 7" :class="mapContainerClass(mapData[6].type)">
                    <transition name="zoom">
                        <div v-show="mapData[6] && animateMap7" class="img-container">
                            <img class="map" :src="mapImgURL(mapData[6].map)" alt="">
                            <img class="team" :src="leagueLogoURL" alt="">
                        </div>
                    </transition>
                    <transition name="slideUp">
                        <span v-show="mapData[6] && animateMap7" class="map-description">{{ mapData[6].map_name }}</span>
                    </transition>
                </div>
                <div v-else class="map-container"></div>

            </div>
        </transition>

    </div>
</template>

<script>
import {MatchDataWebsocketInGame} from "@/mixins/MatchDataWebsocketInGame";
import {OverlayStateWebsocketInGame} from "@/mixins/OverlayStateWebsocketInGame";
import {MapDataWebsocketInGame} from "@/mixins/MapDataWebsocketInGame";

require('vue2-animate/dist/vue2-animate.min.css')

export default {
    name: "MapsOverlay",
    mixins: [MatchDataWebsocketInGame, MapDataWebsocketInGame, OverlayStateWebsocketInGame],
    data() {
        return {
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
            return `${this.$store.state.backendURL}/media/leagues/${this.matchData.league}_500.webp`
        }
    },
    watch: {
        overlayState: function (newState) {
            if (newState.maps_state) this.animated = true
            else this.resetAnimations();
        },
        mapData: function (newState, oldState) {
            if (!oldState) return
            if (oldState.length > newState.length) {
                this.resetAnimations()
                setTimeout(() => {
                    this.animated = true;
                }, 1000)
            }
        },
        matchData: function (newState, oldState) {
            if (!this.overlayState || !this.overlayState.maps_state) return
            if (oldState != null) {
                if (oldState.id === newState.id)
                    return
            }
            this.resetAnimations()
            setTimeout(() => {
                this.animated = true;
            }, 1000)
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