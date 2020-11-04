<template>
    <BaseLayout title="Rounds" title_icon="fas fa-list-ol" :bc_path="bcPath">

        <template v-if="loadingStatus === 'loaded'">

            <b-row v-if="mapLocked">
                <b-col>
                    <b-alert variant="info" show>
                        <span class="font-italic">
                            <i class="fa fas fa-info-circle mr-1"></i>
                            <i18n path="matches.op_bans.locked_info_text">
                                <b>{{ $t('matches.op_bans.locked_info_text_bold') }}</b>
                            </i18n>
                        </span>
                    </b-alert>
                </b-col>
            </b-row>

            <!-- Round Controls & Live Stats-->
            <b-row>

                <!-- Round Controls -->
                <b-col lg="6" order="1">

                    <CustomCard color="primary" outline divider :title="$t('matches.rounds.round_control')">
                        <template #card-body>

                            <b-row>

                                <!-- BombSpot -->
                                <b-col lg="6">

                                    <label class="text-bold">{{ $t('matches.rounds.bomb_spot') }}:</label>

                                    <div v-for="bs in bombSpots" :key="bs.id">
                                        <b-btn v-if="selectedBombSpot === bs" :disabled="mapLocked"
                                               variant="primary" class="btn-block mb-2">
                                            {{ bs.floor }} - {{ bs.name }}
                                        </b-btn>

                                        <b-btn v-else :disabled="mapLocked"
                                               @click="selectBombSpot(bs)"
                                               variant="outline-primary" class="btn-block mb-2">
                                            {{ bs.floor }} - {{ bs.name }}
                                        </b-btn>
                                    </div>

                                </b-col>

                                <!-- Win Type -->
                                <b-col lg="6">

                                    <label class="text-bold">{{ $t('matches.rounds.win_type') }}:</label>

                                    <div v-for="t in winTypes" :key="t.id">
                                        <b-btn v-if="selectedWinType === t" :disabled="mapLocked"
                                               variant="primary" class="btn-block mb-2">
                                            {{ t.name }}
                                        </b-btn>

                                        <b-btn v-else :disabled="mapLocked"
                                               @click="selectWinType(t)"
                                               variant="outline-primary" class="btn-block mb-2">
                                            {{ t.name }}
                                        </b-btn>
                                    </div>

                                </b-col>
                            </b-row>

                            <hr class="divider">

                            <b-row>

                                <!-- Win Team -->
                                <b-col lg="6">

                                    <label class="text-bold">{{ $t('matches.rounds.win_team') }}:</label>

                                    <b-row>
                                        <b-col xl="6">
                                            <template v-if="winTeam === matchData.team_blue">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                                                    {{ matchData.team_blue_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0" :disabled="mapLocked"
                                                       @click="selectWinTeam(matchData.team_blue)">
                                                    {{ matchData.team_blue_name }}
                                                </b-btn>
                                            </template>
                                        </b-col>

                                        <b-col xl="6">
                                            <template v-if="winTeam === matchData.team_orange">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                                                    {{ matchData.team_orange_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0" :disabled="mapLocked"
                                                       @click="selectWinTeam(matchData.team_orange)">
                                                    {{ matchData.team_orange_name }}
                                                </b-btn>
                                            </template>
                                        </b-col>
                                    </b-row>
                                </b-col>


                                <!-- Opening Frag Team -->
                                <b-col lg="6">

                                    <label class="text-bold">{{ $t('matches.rounds.of_team') }}</label>

                                    <b-row>
                                        <b-col xl="6">
                                            <template v-if="ofTeam === matchData.team_blue">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                                                    {{ matchData.team_blue_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0" :disabled="mapLocked"
                                                       @click="selectOFTeam(matchData.team_blue)">
                                                    {{ matchData.team_blue_name }}
                                                </b-btn>
                                            </template>
                                        </b-col>

                                        <b-col xl="6">
                                            <template v-if="ofTeam === matchData.team_orange">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                                                    {{ matchData.team_orange_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0" :disabled="mapLocked"
                                                       @click="selectOFTeam(matchData.team_orange)">
                                                    {{ matchData.team_orange_name }}
                                                </b-btn>
                                            </template>
                                        </b-col>

                                    </b-row>
                                </b-col>
                            </b-row>

                            <hr class="divider">

                            <!-- Notes -->
                            <b-row>
                                <b-col cols="12">
                                    <label class="text-bold">{{ $t('matches.rounds.notes') }}:</label>
                                </b-col>

                                <b-col cols="12">
                                    <b-textarea :placeholder="$t('matches.rounds.notes_text')" v-model="notes" rows="3"/>
                                </b-col>
                            </b-row>

                            <hr class="divider">

                            <b-row>
                                <b-col lg="6">
                                    <b-btn variant="primary" class="btn-block" :disabled="mapLocked"
                                           @click="addRound">
                                        {{ $t('matches.rounds.add_round') }}
                                        <b-spinner v-if="loadingSmall === 'addRound'" variant="light" small/>
                                    </b-btn>
                                </b-col>

                                <b-col lg="6">
                                    <b-btn variant="danger" class="btn-block"
                                           @click="removeLastRound" :disabled="roundData.length === 0 || mapLocked">
                                        {{ $t('matches.rounds.remove_round') }}
                                        <b-spinner v-if="loadingSmall === 'removeRound'" variant="light" small/>
                                    </b-btn>
                                </b-col>

                                <b-col cols="12">
                                    <b-btn variant="success" class="btn-block mt-2"
                                           @click="finishMap" :disabled="!canBeFinished || mapLocked">
                                        {{ $t('matches.rounds.finish_map') }}
                                    </b-btn>
                                </b-col>
                            </b-row>


                        </template>
                    </CustomCard>
                </b-col>

                <!-- Live Statistics -->
                <b-col lg="6" order="2" order-lg="1">
                    <CustomCard color="success" outline divider :title="$t('matches.rounds.live_stats')">
                        <template #card-body>
                            <b-row v-if="roundData.length > 0" class="text-center">

                                <b-col cols="12" md="6" lg="12" xl="6" class="mb-2">
                                    <label>{{ $t('matches.rounds.atk_def_wins') }}</label>
                                    <apexchart type="donut" :options="sideWinDataOptions" :series="sideWinData"/>
                                </b-col>

                                <b-col cols="12" class="d-md-none d-xl-none">
                                    <hr class="divider">
                                </b-col>

                                <b-col cols="12" md="6" lg="12" xl="6" class="mb-2">
                                    <label>{{ $t('matches.rounds.opening_frags') }}</label>
                                    <apexchart type="donut" :options="ofDataOptions" :series="ofData"/>
                                </b-col>

                                <b-col cols="12">
                                    <hr class="divider">
                                </b-col>

                                <b-col cols="12" md="6" lg="12" xl="6" class="mb-2">
                                    <label>{{ $t('matches.rounds.type_wins') }}</label>
                                    <apexchart type="donut" :options="typeWinDataOptions" :series="typeWinData"/>
                                </b-col>

                                <b-col cols="12" class="d-md-none d-xl-none">
                                    <hr class="divider">
                                </b-col>

                                <b-col cols="12" md="6" lg="12" xl="6" class="mb-2">
                                    <label>{{ $t('matches.rounds.bomb_spot_picks') }}</label>
                                    <apexchart type="donut" :options="bombSpotPickDataOptions" :series="bombSpotPickData"/>
                                </b-col>

                            </b-row>

                            <b-row v-else>
                                <b-col>
                                    <span class="font-italic">{{ $t('matches.rounds.live_stats_placeholder') }}</span>
                                </b-col>
                            </b-row>
                        </template>
                    </CustomCard>
                </b-col>

                <!-- Round Details -->
                <b-col cols="12" order="1" order-lg="2">

                    <CustomCard color="warning" outline divider :title="$t('matches.rounds.round_details')">
                        <template #card-body>

                            <b-table table-variant="dark" small striped sort-icon-left responsive :items="roundData" :fields="roundTableFields"
                                     sort-by="round_no">

                                <template #cell(bomb_spot)="data">
                                    <span>{{ getBombSpotName(data.item.bomb_spot) }}</span>
                                </template>

                                <template #cell(of_team_name)="data">
                                    <span v-if="data.item.of_team">{{ data.item.of_team_name }}</span>
                                    <span v-else>-</span>
                                </template>

                                <template #cell(score)="data">
                                    <span>{{ data.item.score_blue }} - {{ data.item.score_orange }}</span>
                                </template>

                                <template #cell(notes)="data">
                                    <span v-if="data.item.notes">{{ data.item.notes }}</span>
                                    <span v-else>-</span>
                                </template>

                            </b-table>

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
import BaseLayout from "@/components/layout/BaseLayout";
import axios from "axios";
import CustomCard from "@/components/elements/CustomCard";
import StatusOverlay from "@/components/elements/StatusOverlay";

export default {
    name: "Rounds",

    data() {
        return {
            selectedBombSpot: null,
            selectedWinType: null,
            winTeam: null,
            ofTeam: null,
            notes: null,

            matchData: null,
            matchMap: null,
            bombSpots: [],
            roundData: [],
            winTypes: [
                {id: 1, name: this.$t('matches.rounds.win_type_names.kills')},
                {id: 2, name: this.$t('matches.rounds.win_type_names.defuser_planted')},
                {id: 3, name: this.$t('matches.rounds.win_type_names.defuser_disabled')},
                {id: 4, name: this.$t('matches.rounds.win_type_names.time')}
            ],

            chartOptions: {
                chart: {
                    type: "donut"
                },
                fill: {
                    type: "gradient"
                },
                legend: {
                    labels: {
                        colors: "white"
                    },
                    position: "bottom"
                }
            },

            roundTableFields: [
                {
                    key: "round_no",
                    label: "#",
                },
                {
                    key: "bomb_spot",
                    label: this.$t('matches.rounds.bomb_spot'),
                },
                {
                    key: "win_type_name",
                    label: this.$t('matches.rounds.win_type'),
                },
                {
                    key: "win_team_name",
                    label: this.$t('matches.rounds.win_team'),
                },
                {
                    key: "of_team_name",
                    label: this.$t('matches.rounds.opening_frag'),
                },
                {
                    key: "score",
                    label: this.$t('core.score'),
                },
                {
                    key: "notes",
                    label: this.$t('matches.rounds.notes'),
                }
            ],

            matchDataLoaded: false,
            matchMapLoaded: false,
            bombSpotsLoaded: false,
            roundDataLoaded: false,

            loadingSmall: "",
            loadingStatus: "loading"
        }
    },

    computed: {
        sideWinData() {
            let atkWins = this.roundData.filter(r => r.win_team === r.atk_team).length
            let defWins = this.roundData.length - atkWins
            return [atkWins, defWins]
        },

        ofData() {
            let ofBlue = this.roundData.filter(r => r.of_team === this.matchData.team_blue).length
            let ofOrange = this.roundData.filter(r => r.of_team === this.matchData.team_orange).length
            return [ofBlue, ofOrange]
        },

        typeWinData() {
            let typeData = [0, 0, 0, 0]
            this.roundData.forEach((r) => {
                typeData[r.win_type - 1]++
            })
            return typeData;
        },

        bombSpotPickData() {
            let bs1 = this.roundData.filter(r => r.bomb_spot === this.bombSpots[0].id).length
            let bs2 = this.roundData.filter(r => r.bomb_spot === this.bombSpots[1].id).length
            let bs3 = this.roundData.filter(r => r.bomb_spot === this.bombSpots[2].id).length
            let bs4 = this.roundData.filter(r => r.bomb_spot === this.bombSpots[3].id).length
            return [bs1, bs2, bs3, bs4]
        },

        sideWinDataOptions() {
            let options = Object.assign({}, this.chartOptions)
            options['labels'] = ["ATK Wins", "DEF Wins"]
            return options
        },

        ofDataOptions() {
            let options = Object.assign({}, this.chartOptions)
            options['labels'] = [this.matchData.team_blue_name, this.matchData.team_orange_name]
            return options
        },

        bombSpotPickDataOptions() {
            let options = Object.assign({}, this.chartOptions)
            options['labels'] = [this.getBombSpotName(this.bombSpots[0].id), this.getBombSpotName(this.bombSpots[1].id),
                this.getBombSpotName(this.bombSpots[2].id), this.getBombSpotName(this.bombSpots[3].id)]
            return options
        },

        typeWinDataOptions() {
            let options = Object.assign({}, this.chartOptions)
            options['labels'] = [this.$t('matches.rounds.win_type_names.kills'), this.$t('matches.rounds.win_type_names.defuser_planted'),
                this.$t('matches.rounds.win_type_names.defuser_disabled'), this.$t('matches.rounds.win_type_names.time')]
            return options
        },

        canBeFinished() {
            let lastRound = this.roundData.filter(r => r.round_no === this.roundData.length)[0]
            return (lastRound.score_blue >= 7 && lastRound.score_orange < 6) // Regular blue win
                    || (lastRound.score_orange >= 7 && lastRound.score_blue < 6) // Regular orange win
                    || (lastRound.score_blue === 6 && lastRound.score_orange === 6) // Draw
                    || (lastRound.score_blue >= 8 || lastRound.score_orange >= 8); // Overtime win
        },

        mapLocked(){
            return this.matchMap.status === 3
        },

        loadComplete() {
            return this.matchDataLoaded && this.matchMapLoaded && this.bombSpotsLoaded && this.roundDataLoaded
        },

        bcPath() {
            if (this.matchDataLoaded && this.matchMapLoaded) {
                return ["Dashboard", "Matches", this.$route.params.match_id,
                    this.matchMap.map_name + " (Map " + this.matchMap.play_order + "/" + this.matchData.best_of + ")",
                    "Rounds"]
            } else {
                return ["Dashboard", "Matches", this.$route.params.match_id, this.$route.params.map_id, "Rounds"]
            }
        }
    },

    watch: {
        loadComplete: function (newState) {
            if (newState) this.loadingStatus = "loaded"
        }
    },

    methods: {
        selectBombSpot(bs) {
            this.selectedBombSpot = bs
        },

        selectWinType(t) {
            this.selectedWinType = t
        },

        selectWinTeam(t) {
            this.winTeam = t;
        },

        selectOFTeam(t) {
            this.ofTeam = t
        },

        addRound() {
            this.loadingSmall = "addRound"

            // Validate input
            if (!this.selectedBombSpot) {
                this.$toast.warning(this.$t('matches.rounds.toasts.bomb_spot_missing'))
                return;
            }
            if (!this.selectedWinType) {
                this.$toast.warning(this.$t('matches.rounds.toasts.win_type_missing'))
                return;
            }
            if (!this.winTeam) {
                this.$toast.warning(this.$t('matches.rounds.toasts.win_team_missing'))
                return;
            }

            // Format optional input
            let notes = null
            if (this.notes) notes = this.notes.replace("\n", "\\n")

            let data = {
                match: this.matchData.id,
                map: this.matchMap.map,
                bomb_spot: this.selectedBombSpot.id,
                win_type: this.selectedWinType.id,
                win_team: this.winTeam,
                of_team: this.ofTeam,
                notes: notes
            }

            console.log(data)

            axios.post(`${this.$store.state.backendURL}/api/matches/round/`, data, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.resetRoundData()
                this.getRounds()
                this.$toast.success(this.$t('matches.rounds.toasts.round_added'), this.$t('generic.success'), {timeout: 2000})
            }).catch(() => {
                this.$toast.error(this.$t('matches.rounds.toasts.round_added_failed'), this.$t('generic.error'))
            })

        },

        removeLastRound() {
            this.loadingSmall = "removeRound"
            let lastRound = this.roundData.filter(r => r.round_no === this.roundData.length)[0]

            axios.delete(`${this.$store.state.backendURL}/api/matches/round/${lastRound.id}/`, this.$store.getters.authHeader
            ).then(() => {
                this.$toast.success(this.$t('matches.rounds.toasts.round_removed'), this.$t('generic.success'))
                this.getRounds()
            }).catch(() => {
                this.$toast.success(this.$t('matches.rounds.toasts.round_removed_failed'), this.$t('generic.error'))
            })
        },

        finishMap() {
            this.$bvModal.msgBoxConfirm(this.$t('matches.rounds.finish_map_confirm_1') + " " + this.$t('matches.rounds.finish_map_confirm_2'), {
                title: this.$t('matches.rounds.finish_map') + "?",
                centered: true,
                okVariant: "danger",
                headerBgVariant: "danger",
                bodyBgVariant: "dark",
                footerBgVariant: "dark"
            }).then(value => {
                if (value) {
                    let lastRound = this.roundData.filter(r => r.round_no === this.roundData.length)[0]
                    let winTeam = null
                    if (lastRound.score_blue !== lastRound.score_orange){
                        winTeam = lastRound.win_team
                    }

                    let data = {
                        win_team: winTeam,
                        score_blue: lastRound.score_blue,
                        score_orange: lastRound.score_orange
                    }

                    axios.patch(`${this.$store.state.backendURL}/api/matches/maps/${this.matchMap.id}/`, data, this.$store.getters.authHeader
                    ).then(() => {

                        axios.get(`${this.$store.state.backendURL}/api/match/${this.$route.params.match_id}`, this.$store.getters.authHeader
                        ).then((response) => {
                            let matchData = response.data
                            let nextURL = "";

                            // Where to redirect next?
                            if (matchData.best_of === 1) {
                                nextURL = "overview"
                            } else if (matchData.best_of === 2 || matchData.best_of === 3) {
                                if (matchData.score_blue >= 2 || matchData.score_orange >= 2)
                                    nextURL = "overview"
                                else
                                    nextURL = "nextMap"
                            } else if (matchData.best_of === 5) {
                                if (matchData.score_blue >= 3 || matchData.score_orange >= 3)
                                    nextURL = "overview"
                                else
                                    nextURL = "nextMap"
                            }

                            if (nextURL === "overview") {
                                // Redirect to match overview
                                this.$toast.info(this.$t('matches.rounds.match_finished'))
                                this.$router.push({name: "Match Overview", params: {id: this.matchData.id}})

                            } else if (nextURL === "nextMap") {
                                // Redirect to next map
                                axios.get(`${this.$store.state.backendURL}/api/matches/maps/?match=${matchData.id}`, this.$store.getters.authHeader
                                ).then((response) => {
                                    this.$toast.info(this.$t('matches.rounds.map_finished'))
                                    let next_map_id = response.data.filter(m => (m.play_order === this.matchMap.play_order + 1))[0].map
                                    this.$router.push({name: "Operator Bans", params: {match_id: this.matchData.id, map_id: next_map_id}})
                                })
                            }
                        })

                    }).catch(() => {
                        this.$toast.error(this.$t('matches.rounds.finish_map_failed'), this.$t('generic.error'))
                    })
                }
            })
        },

        resetRoundData() {
            this.selectedBombSpot = null
            this.selectedWinType = null
            this.winTeam = null
            this.ofTeam = null
            this.notes = ""
        },

        getBombSpotName(id) {
            let bomb_spot = this.bombSpots.filter(b => b.id === id)[0]
            return bomb_spot.floor + " - " + bomb_spot.name
        },

        getMatchData() {
            axios.get(`${this.$store.state.backendURL}/api/match/${this.$route.params.match_id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.matchData = response.data
                this.matchDataLoaded = true
            })
        },

        getMatchMap() {
            axios.get(`${this.$store.state.backendURL}/api/matches/maps/?match=${this.$route.params.match_id}&map=${this.$route.params.map_id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.matchMap = response.data[0]
                this.matchMapLoaded = true
            })
        },

        getBombSpots() {
            axios.get(`${this.$store.state.backendURL}/api/core/bomb_spot/?map=${this.$route.params.map_id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.bombSpots = response.data
                this.bombSpotsLoaded = true
            }).catch((error) => {
                console.log(error.response)
            })
        },

        getRounds() {
            axios.get(`${this.$store.state.backendURL}/api/matches/round/?match=${this.$route.params.match_id}&map=${this.$route.params.map_id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.roundData = response.data
                this.roundDataLoaded = true
                this.loadingSmall = ""
            })
        },
    },
    created() {
        this.getMatchData()
        this.getMatchMap()
        this.getBombSpots()
        this.getRounds()
    },

    components: {
        BaseLayout, CustomCard, StatusOverlay
    }
}
</script>

<style scoped>

</style>