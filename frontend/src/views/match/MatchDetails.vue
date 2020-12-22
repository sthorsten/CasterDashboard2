<template>
    <BaseLayout :title="$t('navigation.match_details')" title_icon="fa fas fa-gamepad" :bc_path="bcPath">

        <template v-if="loading === LoadingStatus.LOADED">
            <AlertBox variant="warning" :title="$t('generic.warning')" :text="$t('websocket.connection_lost')"
                      icon="fa mr-1 fas fa-exclamation-triangle" :show="matchWebsocketStatus === WebsocketStatus.RECONNECTING" loading/>

            <AlertBox variant="danger" :title="$t('generic.error')" :text="$t('websocket.error') + ' ' + $t('generic.contact_admin')"
                      icon="fa mr-1 fas fa-times-circle" :show="matchWebsocketStatus === WebsocketStatus.ERROR"/>

            <b-row>
                <b-col>

                    <CustomCard :title="$t('navigation.maps')" color="primary" outline divider>
                        <template #card-body>

                            <b-row v-if="matchMaps && matchMaps.length > 0">

                                <b-col v-for="i in Array(7).keys()" :key="i">
                                    <div class="w-100">

                                        <template v-if="matchMaps && matchMaps[i]">
                                            <div v-if="matchMaps[i].type === 2 || matchMaps[i].type === 3" class="img-container pick">
                                                <img class="w-100" :src="mapImgURLs[matchMaps[i].map - 1]" alt="-">
                                            </div>
                                            <div v-else class="img-container ban">
                                                <img class="w-100" :src="mapImgURLs[matchMaps[i].map - 1]" alt="-">
                                            </div>

                                            <div class="w-100 text-center mt-2">
                                                <i v-if="matchMaps[i].type === 2 || matchMaps[i].type === 3"
                                                   class="text-success">{{ matchMaps[i].type_name }}</i>
                                                <i v-else class="text-danger">{{ matchMaps[i].type_name }}</i>
                                                - <i>{{ matchMaps[i].map_name }}</i><br>
                                                <b>{{ matchMaps[i].choose_team_name }}</b>
                                            </div>
                                        </template>
                                    </div>
                                </b-col>

                            </b-row>

                            <b-row v-else>
                                <b-col>
                                    <i>Nothing here yet!</i>
                                </b-col>
                            </b-row>

                        </template>
                    </CustomCard>
                </b-col>
            </b-row>

            <b-row v-for="(map, index) in mapPicks" :key="index">
                <b-col v-if="map.status === 2">
                    <MatchDetailMap :match="match" :match-map="playMap" :op-bans="opBans" :rounds="rounds"/>
                </b-col>

                <b-col v-else-if="map.status === 3">
                    <template v-if="opBansFinished && roundsFinished">
                        <MatchDetailMap :match="match" :match-map="map" :op-bans="opBansFinished[map.map]" :rounds="roundsFinished[map.map]"/>
                    </template>
                </b-col>

                <b-col v-else>
                    <CustomCard :title="'Map #' + map.play_order + ' - ' + map.map_name" color="success" outline divider>
                        <template #card-body>
                            <i>{{ $t('generic.no_data') }}</i>
                        </template>
                    </CustomCard>
                </b-col>
            </b-row>

        </template>

        <LoadingOverlay :status="loading"/>

    </BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";
import CustomCard from "@/components/elements/CustomCard";
import {MatchWebsocket} from "@/mixins/websocket/MatchWebsocket";
import AlertBox from "@/components/elements/AlertBox";
import {WebsocketStatus} from "@/helpers/const/WebsocketStatus";
import LoadingOverlay from "@/components/elements/LoadingOverlay";
import {LoadingStatus} from "@/helpers/const/LoadingStatus";
import {MatchMapAllWebsocket} from "@/mixins/websocket/MatchMapAllWebsocket";
import {RoundWebsocket} from "@/mixins/websocket/RoundWebsocket";
import {OpBansWebsocket} from "@/mixins/websocket/OpBansWebsocket";
import {Maps} from "@/mixins/axios/Maps";
import MatchDetailMap from "@/components/subcomponents/MatchDetailMap";
import {OpBans} from "@/mixins/axios/OpBans";
import {Rounds} from "@/mixins/axios/Rounds";


export default {
    name: "MatchDetails",
    mixins: [MatchWebsocket, MatchMapAllWebsocket, OpBansWebsocket, RoundWebsocket, Maps, OpBans, Rounds],
    data() {
        return {
            LoadingStatus: LoadingStatus,
            WebsocketStatus: WebsocketStatus,
            matchMapID: null,
            mapPicks: null,
            opBansFinished: {},
            roundsFinished: {},

            loading: LoadingStatus.LOADING,
            bcPath: ["Dashboard", "Matches", this.$route.params.id, "Details"]
        }
    },
    computed: {
        matchID() {
            return this.$route.params.id
        },
        mapID() {
            return this.playMap.map
        },
        playMap() {
            if (!this.matchMaps) return null
            let play_map = this.matchMaps.filter(m => m.status === 2)[0]
            if (play_map) return play_map
            return null
        },
        loadComplete() {
            return this.match && this.matchMaps && this.mapsLoaded && this.opBansFinished && this.roundsFinished
        }
    },
    watch: {
        matchMaps: function(newState){
            if (newState !== null){
                this.getMapPicks()
            }
        },
        mapPicks: function (newState) {
            if (newState) {
                this.getOpBansFinished()
                this.getRoundsFinished()
            }
        },
        playMap: function (newState) {
            if (newState) {
                this.connectOpBansWebsocket()
                this.connectRoundWebsocket()
            }
        },
        loadComplete: function (newState) {
            if (newState) this.loading = LoadingStatus.LOADED
        }
    },
    methods: {
        getMapPicks() {
            let map_picks = this.matchMaps.filter(m => m.type === 2 || m.type === 3)
            if (map_picks) this.mapPicks = map_picks
        },
        getOpBansFinished() {
            let finishedMaps = this.mapPicks.filter(m => m.status === 3)
            finishedMaps.forEach(m => {
                this.getOpBans(this.matchID, m.map).then(data => this.$set(this.opBansFinished, m.map, data))
            })
        },
        getRoundsFinished() {
            let rounds = {};
            let finishedMaps = this.mapPicks.filter(m => m.status === 3)
            finishedMaps.forEach(m => {
                this.getRounds(this.matchID, m.map).then(data => this.$set(this.roundsFinished, m.map, data))
            })
            this.roundsFinished = rounds;
        },
    },
    created() {
        this.getMaps()
        this.connectMatchWebsocket()
        this.connectMatchMapAllWebsocket()
    },
    components: {
        MatchDetailMap,
        LoadingOverlay,
        AlertBox,
        CustomCard,
        BaseLayout,
    }
}
</script>

<style scoped>
.img-container {
    border: 2px solid #111;
    border-radius: 5px;
    box-shadow: 0 0 2px 0 #111;
}

.img-container.ban {
    border: 2px solid red;
    border-radius: 5px;
    box-shadow: 0 0 2px 0 red;
    filter: grayscale(0.5) brightness(0.4);
}

.img-container.pick {
    border: 2px solid green;
    border-radius: 5px;
    box-shadow: 0 0 2px 0 green;
}

img {
    border-radius: 5px;
}
</style>