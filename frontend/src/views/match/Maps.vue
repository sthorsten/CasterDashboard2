<template>
    <BaseLayout title="Map Pick & Bans" title_icon="fas fa-map" :bc_path="bc_path">

        <template v-if="loading_status === 'loaded'">

            <b-row v-if="maps_locked">

                <b-col>
                    <b-alert variant="info" show>
                        <span class="font-italic">
                            <i class="fa fas fa-info-circle"></i>
                            One or more maps are already being played or finished. You <b>can not</b> make any changes to the maps anymore.
                        </span>
                    </b-alert>
                </b-col>

            </b-row>

            <b-row>

                <!-- Settings -->
                <b-col md="5">
                    <CustomCard color="danger" outline divider title="Settings & Controls">
                        <template #card-body>

                            <b-form-group label="Select a map pool:">
                                <multiselect id="map-pool" v-model="map_pool_selected" :options="map_pools" track_by="id" label="name"/>
                            </b-form-group>

                            <hr class="divider">

                            <b-btn variant="secondary" class="btn-block" :disabled="maps_locked" @click="removeLastMap">
                                <b-spinner v-if="loading_small === 'remove-last-map'" variant="light" small/>
                                <span v-else>
                                    Remove last map
                                </span>
                            </b-btn>

                            <b-btn variant="danger" class="btn-block" :disabled="maps_locked" @click="removeAllMaps">
                                <b-spinner v-if="loading_small === 'remove-all-maps'" variant="light" small/>
                                <span v-else>
                                    Remove all maps
                                </span>
                            </b-btn>

                            <template v-if="next_map">
                                <router-link :to="{name: 'Operator Bans', params:{match_id: match.id, map_id: next_map.map}}">
                                    <b-btn variant="primary" class="btn-block mt-2">
                                        Continue to operator bans
                                    </b-btn>
                                </router-link>
                            </template>
                            <template v-else>
                                <b-btn variant="primary" class="btn-block mt-2" :disabled="!next_map">
                                    Continue to operator bans
                                </b-btn>
                            </template>


                        </template>
                    </CustomCard>

                    <CustomCard color="success" outline divider title="Log">
                        <template #card-body>

                            <span v-if="match_maps.length === 0" class="font-italic">
                                The map picks & bans will be shown here once you select a map!
                            </span>

                            <ul>
                                <li v-for="map in match_maps" :key="map.id">

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
                    <CustomCard color="primary" outline divider title="Map Picks & Bans">
                        <template #card-body>

                            <!-- Headers -->
                            <b-row class="text-center mb-3">

                                <b-col cols="2">
                                    <i class="text-bold">Image</i>
                                </b-col>

                                <b-col cols="3">
                                    <i class="text-bold">{{ match.team_blue_name }}</i>
                                </b-col>

                                <b-col cols="4">
                                    <i class="text-bold">Map</i>
                                </b-col>

                                <b-col cols="3">
                                    <i class="text-bold">{{ match.team_orange_name }}</i>
                                </b-col>

                            </b-row>

                            <hr class="divider">

                            <!-- Content -->
                            <div v-for="map in maps" :key="map.id">
                                <div v-if="map_pool_selected.maps.includes(map.id)">
                                    <b-row align-v="center" class="text-center">

                                        <!-- Image -->
                                        <b-col cols="2" class="align-items-center">
                                            <img class="w-100" :src="map_img_urls[map.id - 1]" alt="-">
                                        </b-col>

                                        <!-- Buttons left -->
                                        <b-col cols="3">
                                            <b-btn variant="danger" class="btn-block mb-0"
                                                   :disabled="maps_locked" @click="selectMap(map.id, 'ban', match.team_blue)">
                                                <b-spinner v-if="loading_small === map.id + '-ban-' + match.team_blue"
                                                           variant="light" small/>
                                                <span v-else>
                                                    Ban Map
                                                </span>
                                            </b-btn>
                                            <b-btn variant="success" class="btn-block mt-1"
                                                   :disabled="maps_locked" @click="selectMap(map.id, 'pick', match.team_blue)">
                                                <b-spinner v-if="loading_small === map.id + '-pick-' + match.team_blue"
                                                           variant="light" small/>
                                                <span v-else>
                                                    Pick Map
                                                </span>
                                            </b-btn>
                                        </b-col>

                                        <!-- Data -->
                                        <b-col cols="4">
                                            <span class="text-bold">{{ map.name }}</span><br>
                                            <template v-if="match_map_filtered[map.id - 1]">

                                                <template v-if="match_map_filtered[map.id - 1].type === 1">
                                                    <b-badge pill variant="danger">
                                                        Banned
                                                    </b-badge>
                                                    <br>
                                                    <span class="font-italic">
                                                        {{ match_map_filtered[map.id - 1].choose_team_name }}
                                                    </span>
                                                </template>
                                                <template v-if="match_map_filtered[map.id - 1].type === 2">
                                                    <b-badge pill variant="success">
                                                        Picked
                                                    </b-badge>
                                                    <br>
                                                    <span class="font-italic">
                                                        {{ match_map_filtered[map.id - 1].choose_team_name }}
                                                    </span>
                                                </template>
                                                <template v-if="match_map_filtered[map.id - 1].type === 3">
                                                    <b-badge pill variant="success">
                                                        Decider Map
                                                    </b-badge>
                                                </template>
                                                <template v-if="match_map_filtered[map.id - 1].type === 4">
                                                    <b-badge pill variant="danger">
                                                        Default ban
                                                    </b-badge>
                                                </template>

                                            </template>
                                            <template v-else>
                                                <b-badge pill variant="secondary">Not selected yet</b-badge>
                                            </template>
                                        </b-col>

                                        <!-- Buttons right -->
                                        <b-col cols="3">
                                            <b-btn variant="danger" class="btn-block mb-0"
                                                   :disabled="maps_locked" @click="selectMap(map.id, 'ban', match.team_orange)">
                                                <b-spinner v-if="loading_small === map.id + '-ban-' + match.team_orange"
                                                           variant="light" small/>
                                                <span v-else>
                                                    Ban Map
                                                </span>
                                            </b-btn>
                                            <b-btn variant="success" class="btn-block mt-1"
                                                   :disabled="maps_locked" @click="selectMap(map.id, 'pick', match.team_orange)">
                                                <b-spinner v-if="loading_small === map.id + '-pick-' + match.team_orange"
                                                           variant="light" small/>
                                                <span v-else>
                                                    Pick Map
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
        <template v-if="loading_status === 'loading'">
            <CustomCard color="secondary" outline divider title="Loading">
                <template #card-body>
                    <StatusOverlay type="loading" text="Loading..."></StatusOverlay>
                </template>
            </CustomCard>
        </template>

        <!-- Error overlay -->
        <template v-if="loading_status === 'error'">
            <CustomCard color="danger" outline divider title="Error">
                <template #card-body>
                    <StatusOverlay type="icon" icon="fas fa-exclamation-triangle fa-2x"
                                   text="Loading failed!"></StatusOverlay>
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
            map_pool_selected: null,

            map_pools: [],
            maps: [],
            match_maps: [],
            match: null,

            loading_small: "",

            reset_all_counter: 0,
            map_pool_loaded: false,
            maps_loaded: false,
            match_maps_loaded: false,
            match_loaded: false,
            loading_status: 'loading',
            bc_path: ["Dashboard", "Matches", this.$route.params.id, "Map Picks & Bans"]
        }
    },
    computed: {
        map_img_urls() {
            let urls = []
            this.maps.forEach(e => {
                urls.push(require('@/assets/img/maps/' + e.id + ".webp"))
            })
            return urls
        },
        match_map_filtered() {
            let filtered_data = []
            this.match_maps.forEach(m => {
                filtered_data[m.map - 1] = m
            })
            return filtered_data
        },
        next_map() {
            let play_maps = this.match_maps.filter(m => m.play_order > 0 && m.status < 3)
            console.log("play_maps ", play_maps)
            return play_maps[0]
        },
        maps_locked() {
            let locked_maps = this.match_maps.filter(m => m.status > 1)
            return locked_maps.length > 0
        },
        load_complete() {
            return this.map_pool_loaded && this.maps_loaded && this.match_maps_loaded && this.match_loaded
        }
    },
    watch: {
        load_complete: function (newState) {
            if (newState) this.loading_status = 'loaded'
            else this.loading_status = 'loading'
        },
        reset_all_counter: function (newState) {
            if (newState === 0) {
                console.log("Remove all complete")
                this.$toast.success("All maps have been removed", "Success")
                this.getMatchMaps()
            }
        }
    },
    methods: {
        selectMap(map, type, team) {
            if (this.match_maps.length >= 7) {
                this.$toast.warning("You can not select more then 7 maps!")
                return
            }

            let duplicates = this.match_maps.filter(m => m.map === map)
            console.log(duplicates)
            if (duplicates.length > 0) {
                this.$toast.warning("You already selected that map!")
                return
            }

            this.loading_small = map + "-" + type + "-" + team
            console.log(this.loading_small)

            let data = {}
            let typeID = 0
            if (this.match_maps.length < 6) {
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

            axios.post(this.$store.state.backendURL + "/api/matches/maps/", data, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then(() => {
                this.getMatchMaps()
                this.$toast.success("Map Added", "Success", {timeout: 2000})
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error("Failed to add map ;(", "Error")
            })
        },

        removeLastMap() {
            if (this.match_maps.length === 0) {
                this.$toast.warning("There is nothing to remove!")
                return
            }

            this.loading_small = "remove-last-map"
            let last_map_id = this.match_maps.filter(m => m.order === this.match_maps.length)[0].id
            axios.delete(this.$store.state.backendURL + "/api/matches/maps/" + last_map_id, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then(() => {
                this.getMatchMaps()
                this.$toast.success("Map removed", "Success", {timeout: 2000})

            }).catch((error) => {
                console.log(error.response)
                this.$toast.error("Failed to remove map ;(", "Error")
            })
        },

        removeAllMaps() {
            if (this.match_maps.length === 0) {
                this.$toast.warning("There is nothing to remove!")
                return
            }

            this.loading_small = "remove-all-maps"
            this.reset_all_counter = this.match_maps.length
            console.log("Removing " + this.reset_all_counter + " maps...")

            this.match_maps.forEach(m => {
                axios.delete(this.$store.state.backendURL + "/api/matches/maps/" + m.id, {
                    headers: {
                        "Authorization": "Token " + this.$store.state.userToken
                    }
                }).then(() => {
                    this.reset_all_counter--
                }).catch((error) => {
                    console.log(error.response)
                    this.$toast.error("Failed to remove map ;(", "Error")
                })
            })
        },

        getMapPools() {
            axios.get(this.$store.state.backendURL + "/api/core/map_pool/", {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.map_pools = response.data
                this.map_pool_selected = this.map_pools.filter(e => e.name === "Competitive")[0]
                this.map_pool_loaded = true
            })
        },
        getMaps() {
            axios.get(this.$store.state.backendURL + "/api/core/map/", {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.maps = response.data
                this.maps_loaded = true
            })
        },
        getMatchMaps() {
            axios.get(this.$store.state.backendURL + "/api/matches/maps/?match=" + this.$route.params.id, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.match_maps = response.data
                this.match_maps_loaded = true
            }).catch((error) => {
                console.log(error)
                this.loading_status = 'error'
            }).then(() => {
                this.loading_small = ""
            })
        },
        getMatch() {
            axios.get(this.$store.state.backendURL + "/api/match/" + this.$route.params.id, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.match = response.data
                this.match_loaded = true
            })
        }
    },
    created() {
        this.getMapPools()
        this.getMaps()
        this.getMatchMaps()
        this.getMatch()
    },
    components: {
        BaseLayout, CustomCard, StatusOverlay
    }
}
</script>

<style scoped>

</style>