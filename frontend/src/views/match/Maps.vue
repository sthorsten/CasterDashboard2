<template>
    <BaseLayout :title="$t('navigation.maps')" title_icon="fas fa-map" :bc_path="bcPath">

        <template v-if="loadingStatus === 'loaded'">

            <b-row v-if="mapsLocked">
                <b-col>
                    <b-alert variant="info" show>
                        <span class="font-italic">
                            <i class="fa fas fa-info-circle mr-1"></i>
                            <i18n path="matches.maps.locked_info_text">
                                <b>{{ $t('matches.maps.locked_info_text_bold') }}</b>
                            </i18n>
                        </span>
                    </b-alert>
                </b-col>
            </b-row>

            <b-row>

                <!-- Settings -->
                <b-col md="5">
                    <CustomCard color="danger" outline divider :title="$t('matches.maps.settings')">
                        <template #card-body>

                            <b-form-group :label="$t('matches.maps.select_map_pool')">
                                <multiselect id="map-pool" v-model="mapPoolSelected" :options="mapPools" track_by="id" label="name"/>
                            </b-form-group>

                            <hr class="divider">

                            <b-btn variant="secondary" class="btn-block" :disabled="mapsLocked || matchMaps.length === 0" @click="removeLastMap">
                                <b-spinner v-if="loadingSmall === 'remove-last-map'" variant="light" small/>
                                <span v-else>
                                    {{ $t('matches.maps.remove_last_map') }}
                                </span>
                            </b-btn>

                            <b-btn variant="danger" class="btn-block" :disabled="mapsLocked || matchMaps.length === 0" @click="removeAllMaps">
                                <b-spinner v-if="loadingSmall === 'remove-all-maps'" variant="light" small/>
                                <span v-else>
                                    {{ $t('matches.maps.remove_all_maps') }}
                                </span>
                            </b-btn>

                            <template v-if="nextMap">
                                <router-link :to="{name: 'Operator Bans', params:{match_id: match.id, map_id: nextMap.map}}">
                                    <b-btn variant="primary" class="btn-block mt-2">
                                        {{ $t('matches.maps.continue') }}
                                    </b-btn>
                                </router-link>
                            </template>
                            <template v-else>
                                <b-btn variant="primary" class="btn-block mt-2" :disabled="!nextMap">
                                    {{ $t('matches.maps.continue') }}
                                </b-btn>
                            </template>


                        </template>
                    </CustomCard>

                    <CustomCard color="success" outline divider title="Log">
                        <template #card-body>

                            <span v-if="matchMaps.length === 0" class="font-italic">
                               {{ $t('matches.maps.log_placeholder') }}
                            </span>

                            <ul>
                                <li v-for="map in matchMaps" :key="map.id">

                                    <!-- Default ban -->
                                    <template v-if="map.type === 4">
                                        {{ map.order }} / {{ map.type_name }} / {{ map.map_name }}
                                    </template>

                                    <!-- Decider map -->
                                    <template v-else-if="map.type === 3">
                                        <span class="text-success text-bold">
                                            {{ map.order }} / {{ map.type_name }} / {{ map.map_name }} (Map #{{ map.play_order }})
                                        </span>
                                    </template>

                                    <template v-else>
                                        <!-- Pick -->
                                        <template v-if="map.type !== 1">
                                            <span class="text-success text-bold">
                                                {{ map.order }} / {{ map.type_name }} / {{ map.choose_team_name }} / {{ map.map_name }} (Map
                                                #{{ map.play_order }})
                                            </span>
                                        </template>

                                        <!-- Ban -->
                                        <template v-else>
                                            {{ map.order }} / {{ map.type_name }} / {{ map.choose_team_name }} / {{ map.map_name }}
                                        </template>
                                    </template>

                                </li>
                            </ul>

                        </template>
                    </CustomCard>

                </b-col>

                <!-- Maps -->
                <b-col md="7">
                    <CustomCard color="primary" outline divider :title="$t('navigation.maps')">
                        <template #card-body>

                            <!-- Headers -->
                            <b-row class="text-center mb-3">

                                <b-col cols="2">
                                    <i class="text-bold">{{ $t('generic.image') }}</i>
                                </b-col>

                                <b-col cols="3">
                                    <i class="text-bold">{{ match.team_blue_name }}</i>
                                </b-col>

                                <b-col cols="4">
                                    <i class="text-bold">{{ $tc('core.map') }}</i>
                                </b-col>

                                <b-col cols="3">
                                    <i class="text-bold">{{ match.team_orange_name }}</i>
                                </b-col>

                            </b-row>

                            <hr class="divider">

                            <!-- Content -->
                            <div v-for="map in maps" :key="map.id">
                                <div v-if="mapPoolSelected.maps.includes(map.id)">
                                    <b-row align-v="center" class="text-center">

                                        <!-- Image -->
                                        <b-col cols="2" class="align-items-center">
                                            <img class="w-100" :src="mapImgURLs[map.id - 1]" alt="-">
                                        </b-col>

                                        <!-- Buttons left -->
                                        <b-col cols="3">
                                            <b-btn variant="danger" class="btn-block mb-0"
                                                   :disabled="mapsLocked || matchMaps.length === 7" @click="selectMap(map.id, 'ban', match.team_blue)">
                                                <b-spinner v-if="loadingSmall === map.id + '-ban-' + match.team_blue"
                                                           variant="light" small/>
                                                <span v-else>
                                                    {{ $t('matches.maps.ban_map') }}
                                                </span>
                                            </b-btn>
                                            <b-btn variant="success" class="btn-block mt-1"
                                                   :disabled="mapsLocked || matchMaps.length === 7" @click="selectMap(map.id, 'pick', match.team_blue)">
                                                <b-spinner v-if="loadingSmall === map.id + '-pick-' + match.team_blue"
                                                           variant="light" small/>
                                                <span v-else>
                                                    {{ $t('matches.maps.pick_map') }}
                                                </span>
                                            </b-btn>
                                        </b-col>

                                        <!-- Data -->
                                        <b-col cols="4">
                                            <span class="text-bold">{{ map.name }}</span><br>
                                            <template v-if="matchMapFiltered[map.id - 1]">

                                                <template v-if="matchMapFiltered[map.id - 1].type === 1">
                                                    <b-badge pill variant="danger">
                                                        Banned
                                                    </b-badge>
                                                    <br>
                                                    <span class="font-italic">
                                                        {{ matchMapFiltered[map.id - 1].choose_team_name }}
                                                    </span>
                                                </template>
                                                <template v-if="matchMapFiltered[map.id - 1].type === 2">
                                                    <b-badge pill variant="success">
                                                        Picked
                                                    </b-badge>
                                                    <br>
                                                    <span class="font-italic">
                                                        {{ matchMapFiltered[map.id - 1].choose_team_name }}
                                                    </span>
                                                </template>
                                                <template v-if="matchMapFiltered[map.id - 1].type === 3">
                                                    <b-badge pill variant="success">
                                                        {{ $t('matches.maps.decider_map') }}
                                                    </b-badge>
                                                </template>
                                                <template v-if="matchMapFiltered[map.id - 1].type === 4">
                                                    <b-badge pill variant="danger">
                                                        {{ $t('matches.maps.default_ban') }}
                                                    </b-badge>
                                                </template>

                                            </template>
                                            <template v-else>
                                                <b-badge pill variant="secondary">
                                                    {{ $t('matches.maps.not_selected') }}
                                                </b-badge>
                                            </template>
                                        </b-col>

                                        <!-- Buttons right -->
                                        <b-col cols="3">
                                            <b-btn variant="danger" class="btn-block mb-0"
                                                   :disabled="mapsLocked || matchMaps.length === 7" @click="selectMap(map.id, 'ban', match.team_orange)">
                                                <b-spinner v-if="loadingSmall === map.id + '-ban-' + match.team_orange"
                                                           variant="light" small/>
                                                <span v-else>
                                                    {{ $t('matches.maps.ban_map') }}
                                                </span>
                                            </b-btn>
                                            <b-btn variant="success" class="btn-block mt-1"
                                                   :disabled="mapsLocked || matchMaps.length === 7" @click="selectMap(map.id, 'pick', match.team_orange)">
                                                <b-spinner v-if="loadingSmall === map.id + '-pick-' + match.team_orange"
                                                           variant="light" small/>
                                                <span v-else>
                                                    {{ $t('matches.maps.pick_map') }}
                                                </span>
                                            </b-btn>
                                        </b-col>

                                    </b-row>

                                    <hr class="divider" style="margin: 0.8rem 0;">
                                </div>
                            </div>


                        </template>
                    </CustomCard>
                </b-col>

            </b-row>
        </template>

        <!-- Loading overlay -->
        <template v-if="loadingStatus === 'loading'">
            <CustomCard color="secondary" outline divider :title="$t('generic.loading')">
                <template #card-body>
                    <StatusOverlay type="loading" :text="$t('generic.loading')"></StatusOverlay>
                </template>
            </CustomCard>
        </template>

        <!-- Error overlay -->
        <template v-if="loadingStatus === 'error'">
            <CustomCard color="danger" outline divider :title="$t('generic.error')">
                <template #card-body>
                    <StatusOverlay type="icon" icon="fas fa-exclamation-triangle fa-2x"
                                   :text="$t('generic.loading_failed')"></StatusOverlay>
                </template>
            </CustomCard>
        </template>

    </BaseLayout>
</template>

<script>
import axios from "axios";
import BaseLayout from "@/components/layout/BaseLayout";
import CustomCard from "@/components/elements/CustomCard";
import StatusOverlay from "@/components/elements/StatusOverlay";

export default {
    name: "Maps",
    data() {
        return {
            mapPoolSelected: null,

            mapPools: [],
            maps: [],
            matchMaps: [],
            match: null,

            loadingSmall: "",

            resetAllCounter: 0,
            mapPoolLoaded: false,
            mapsLoaded: false,
            matchMapsLoaded: false,
            matchLoaded: false,
            loadingStatus: 'loading',
            bcPath: ["Dashboard", "Matches", this.$route.params.id, this.$t('navigation.maps')]
        }
    },
    computed: {
        mapImgURLs() {
            let urls = []
            this.maps.forEach(e => {
                urls.push(require('@/assets/img/maps/' + e.id + ".webp"))
            })
            return urls
        },
        matchMapFiltered() {
            let filtered_data = []
            this.matchMaps.forEach(m => {
                filtered_data[m.map - 1] = m
            })
            return filtered_data
        },
        nextMap() {
            let play_maps = this.matchMaps.filter(m => m.play_order > 0 && m.status < 3)
            console.log("play_maps ", play_maps)
            return play_maps[0]
        },
        mapsLocked() {
            let locked_maps = this.matchMaps.filter(m => m.status > 1)
            return locked_maps.length > 0
        },
        loadComplete() {
            return this.mapPoolLoaded && this.mapsLoaded && this.matchMapsLoaded && this.matchLoaded
        }
    },
    watch: {
        loadComplete: function (newState) {
            if (newState) this.loadingStatus = 'loaded'
            else this.loadingStatus = 'loading'
        },
        resetAllCounter: function (newState) {
            if (newState === 0) {
                console.log("Remove all complete")
                this.$toast.success(this.$t('matches.maps.toasts.maps_removed'), this.$t('generic.success'))
                this.getMatchMaps()
            }
        }
    },
    methods: {
        selectMap(map, type, team) {
            let duplicates = this.matchMaps.filter(m => m.map === map)
            console.log(duplicates)
            if (duplicates.length > 0) {
                this.$toast.warning(this.$t('matches.maps.toasts.map_already_selected'))
                return
            }

            this.loadingSmall = map + "-" + type + "-" + team
            console.log(this.loadingSmall)

            let data = {}
            let typeID = 0
            if (this.matchMaps.length < 6) {
                typeID = type === "ban" ? 1 : 2
                data = {
                    match: this.match.id,
                    map: map,
                    type: typeID,
                    choose_team: team
                }
            } else {
                typeID = type === "ban" ? 4 : 3
                data = {
                    match: this.match.id,
                    map: map,
                    type: typeID
                }
            }

            axios.post(`${this.$store.state.backendURL}/api/matches/maps/`, data, this.$store.getters.authHeader
            ).then(() => {
                this.getMatchMaps()
                this.$toast.success(this.$t('matches.maps.toasts.map_added'), this.$t('generic.success'), {timeout: 2000})
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error(this.$t('matches.maps.toasts.map_added_failed'), this.$t('generic.error'))
            })
        },

        removeLastMap() {
            this.loadingSmall = "remove-last-map"
            let last_map_id = this.matchMaps.filter(m => m.order === this.matchMaps.length)[0].id

            axios.delete(`${this.$store.state.backendURL}/api/matches/maps/${last_map_id}/`, this.$store.getters.authHeader
            ).then(() => {
                this.getMatchMaps()
                this.$toast.success(this.$t('matches.maps.toasts.map_removed'), this.$t('generic.success'), {timeout: 2000})

            }).catch((error) => {
                console.log(error.response)
                this.$toast.error(this.$t('matches.maps.toasts.map_removed_failed'), this.$t('generic.error'))
            })
        },

        removeAllMaps() {
            this.loadingSmall = "remove-all-maps"
            this.resetAllCounter = this.matchMaps.length
            console.log("Removing " + this.resetAllCounter + " maps...")

            this.matchMaps.forEach(m => {
                axios.delete(`${this.$store.state.backendURL}/api/matches/maps/${m.id}/`, this.$store.getters.authHeader
                ).then(() => {
                    this.resetAllCounter--
                }).catch((error) => {
                    console.log(error.response)
                    this.$toast.error(this.$t('matches.maps.toasts.map_removed_failed'), this.$t('generic.error'))
                })
            })
        },

        getMapPools() {
            axios.get(`${this.$store.state.backendURL}/api/core/map_pool/`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.mapPools = response.data
                this.mapPoolSelected = this.mapPools.filter(e => e.name === "Competitive")[0]
                this.mapPoolLoaded = true
            })
        },

        getMaps() {
            axios.get(`${this.$store.state.backendURL}/api/core/map/`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.maps = response.data
                this.mapsLoaded = true
            })
        },

        getMatchMaps() {
            axios.get(`${this.$store.state.backendURL}/api/matches/maps/?match=${this.$route.params.id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.matchMaps = response.data
                this.matchMapsLoaded = true
            }).catch((error) => {
                console.log(error)
                this.loadingStatus = 'error'
            }).then(() => {
                this.loadingSmall = ""
            })
        },

        getMatchData() {
            axios.get(`${this.$store.state.backendURL}/api/match/${this.$route.params.id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.match = response.data
                this.matchLoaded = true
            })
        }
    },

    created() {
        this.getMapPools()
        this.getMaps()
        this.getMatchMaps()
        this.getMatchData()
    },

    components: {
        BaseLayout, CustomCard, StatusOverlay
    }
}
</script>

<style scoped>

</style>