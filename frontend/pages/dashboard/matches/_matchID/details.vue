<template>
    <div>

        <CustomCard color="primary" outline divider :title="$t('generic.loading')"
                    v-if="this.$fetchState.pending">
            <template #card-body>
                <b-skeleton-table/>
                <b-skeleton-table/>
            </template>
        </CustomCard>


        <!-- Map Picks & Bans -->
        <b-row v-if="!$fetchState.pending">
            <b-col cols="12">
                <CustomCard color="primary" outline divider :title="$t('navigation.maps')">
                    <template #card-body>
                        <b-row class="text-center">
                            <b-col v-if="matchMaps == null || matchMaps.length === 0">
                                <i>No maps have been banned / picked yet.</i>
                            </b-col>
                            <b-col v-for="(map, index) in matchMaps" :key="index">

                                <!-- Map image -->
                                <template
                                    v-if="map.type === 2 || map.type === 3">
                                    <div class="img-container pick mb-1">
                                        <img class="w-100" :src="mapImgURLs[map.map - 1]" alt="-">
                                    </div>
                                </template>
                                <template
                                    v-else-if="map.type === 1 || map.type === 4">
                                    <div class="img-container ban mb-1">
                                        <img class="w-100" :src="mapImgURLs[map.map - 1]" alt="-">
                                    </div>
                                </template>

                                <!-- Text & Badge -->
                                <span class="text-bold">{{ map.map_name }}</span><br>

                                <template v-if="map.type === 1">
                                    <b-badge pill variant="danger">
                                        Banned
                                    </b-badge>
                                    <br>
                                    <span class="font-italic">
                                        {{ map.choose_team_name }}
                                    </span>
                                </template>
                                <template v-if="map.type === 2">
                                    <b-badge pill variant="success">
                                        Picked
                                    </b-badge>
                                    <br>
                                    <span class="font-italic">
                                        {{ map.choose_team_name }}
                                    </span>
                                </template>
                                <template v-if="map.type === 3">
                                    <b-badge pill variant="success">
                                        {{ $t('matches.maps.decider_map') }}
                                    </b-badge>
                                </template>
                                <template v-if="map.type === 4">
                                    <b-badge pill variant="danger">
                                        {{ $t('matches.maps.default_ban') }}
                                    </b-badge>
                                </template>
                            </b-col>
                            <b-col v-for="i in (7 - matchMaps.length)" :key="i">
                                <div class="mb-1"></div>
                            </b-col>
                        </b-row>
                    </template>
                </CustomCard>
            </b-col>
        </b-row>

        <!-- Map Details for each map -->
        <template v-if="!$fetchState.pending">

            <!-- Finished maps -->
            <b-row v-for="(data, index) in finishedMapData" :key="index">

                <b-col>
                    <CustomCard color="primary" outline divider
                                :title="`Map #${data.map.play_order} - ${data.map.map_name} - ${data.map.status_name}`">
                        <template #card-body>

                            <!-- First row - Operator Bans -->
                            <b-row>
                                <b-col cols="12" lg="6">
                                    <b-row>

                                        <b-col cols="12">
                                            <label>{{ $t('navigation.op_bans') }}:</label>
                                        </b-col>

                                        <!-- Banned Operators -->
                                        <b-col v-for="(n, index) in 4" :key="index" cols="3" class="text-center">
                                            <template v-if="data.opBans.length > index">
                                                <img
                                                    :src="require(`@/assets/img/operators/${data.opBans[index].operator}.svg`)"
                                                    style="height: 50px; width: 50px;"><br>
                                                <span>{{ data.opBans[index].operator_name }}</span><br>
                                                <span class="font-italic">{{ data.opBans[index].team_name }}</span>
                                            </template>

                                            <template v-else>
                                                <span>-</span><br>
                                                <span class="font-italic">{{
                                                        $t('matches.op_bans.not_selected')
                                                    }}</span>
                                            </template>
                                        </b-col>

                                    </b-row>
                                </b-col>

                            </b-row>

                            <hr class="divider">

                            <!-- Second row - Rounds table -->
                            <b-row>

                                <b-col cols="12">
                                    <label>{{ $t('matches.rounds.round_details') }}:</label>
                                </b-col>

                                <b-col>
                                    <b-table table-variant="dark" small striped sort-icon-left responsive
                                             :items="data.rounds"
                                             :fields="roundTableFields"
                                             sort-by="round_no">

                                        <template #cell(bomb_spot)="table_data">
                                            <b-badge variant="light" pill class="mr-1">
                                                {{ getBombSpotName(table_data.item.bomb_spot).floor }}
                                            </b-badge>
                                            <span class="sl-only">{{
                                                    getBombSpotName(table_data.item.bomb_spot).name
                                                }}</span>
                                        </template>

                                        <template #cell(of_team_name)="table_data">
                                            <span v-if="table_data.item.of_team">{{
                                                    table_data.item.of_team_name
                                                }}</span>
                                            <span v-else>-</span>
                                        </template>

                                        <template #cell(score)="table_data">
                                            <span>{{ table_data.item.score_blue }} - {{
                                                    table_data.item.score_orange
                                                }}</span>
                                        </template>

                                        <template #cell(notes)="table_data">
                                            <div v-if="table_data.item.notes">
                                                <div v-for="(line, index) in table_data.item.notes.split('\\n')"
                                                     :key="index">
                                                    <span>{{ line }}</span><br>
                                                </div>
                                            </div>
                                            <span v-else>-</span>
                                        </template>

                                    </b-table>
                                </b-col>
                            </b-row>

                            <hr class="divider">

                            <!-- Third row - Round statistics -->
                            <b-row>

                                <b-col cols="12">
                                    <label>{{ $t('matches.rounds.live_stats') }}:</label>
                                </b-col>

                                <b-col>
                                    <b-row class="text-center">

                                        <b-col cols="12" md="6" lg="3" xl="3" class="mb-2">
                                            <label>{{ $t('matches.rounds.atk_def_wins') }}</label>
                                            <apexchart type="donut" :options="sideWinDataOptions"
                                                       :series="getSideWinData(data.rounds)"/>
                                        </b-col>

                                        <b-col cols="12" class="d-md-none d-lg-none d-xl-none">
                                            <hr class="divider">
                                        </b-col>

                                        <b-col cols="12" md="6" lg="3" xl="3" class="mb-2">
                                            <label>{{ $t('matches.rounds.opening_frags') }}</label>
                                            <apexchart type="donut" :options="ofDataOptions"
                                                       :series="getOfData(data.rounds)"/>
                                        </b-col>

                                        <b-col cols="12" class="d-lg-none d-xl-none">
                                            <hr class="divider">
                                        </b-col>

                                        <b-col cols="12" md="6" lg="3" xl="3" class="mb-2">
                                            <label>{{ $t('matches.rounds.type_wins') }}</label>
                                            <apexchart type="donut" :options="typeWinDataOptions"
                                                       :series="getTypeWinData(data.rounds)"/>
                                        </b-col>

                                        <b-col cols="12" class="d-md-none d-lg-none d-xl-none">
                                            <hr class="divider">
                                        </b-col>

                                        <b-col cols="12" md="6" lg="3" xl="3" class="mb-2">
                                            <label>{{ $t('matches.rounds.bomb_spot_picks') }}</label>
                                            <apexchart type="donut" :options="getBombSpotPickDataOptions(data.map.map)"
                                                       :series="getBombSpotPickData(data.rounds, data.map.map)"/>
                                        </b-col>

                                    </b-row>
                                </b-col>
                            </b-row>

                        </template>
                    </CustomCard>
                </b-col>

            </b-row>

            <!-- Current map -->
            <b-row v-if="this.currentMap != null">

                <b-col>
                    <CustomCard color="primary" outline divider
                                :title="`Map #${this.currentMap.play_order} - ${this.currentMap.map_name} - ${this.currentMap.status_name}`">
                        <template #card-body>

                            <!-- First row - Operator Bans -->
                            <b-row v-if="bannedOperators != null">
                                <b-col cols="12" lg="6">
                                    <b-row>

                                        <b-col cols="12">
                                            <label>{{ $t('navigation.op_bans') }}:</label>
                                        </b-col>

                                        <!-- Banned Operators -->
                                        <b-col v-for="(n, index) in 4" :key="index" cols="3" class="text-center">
                                            <template v-if="bannedOperators.length > index">
                                                <img v-if="bannedOperators[index].operator_name === '_none'"
                                                     :src="require(`@/assets/img/operators/${bannedOperators[index].operator}.svg`)"
                                                     style="height: 50px; width: 50px;">
                                                <svg v-else
                                                     v-html="operatorIcons[bannedOperators[index].operator_name].toSVG()"
                                                     style="height:50px; width: 50px;"/>
                                                <br>
                                                <span>{{ bannedOperators[index].operator_display_name }}</span><br>
                                                <span class="font-italic">{{ bannedOperators[index].team_name }}</span>
                                            </template>

                                            <template v-else>
                                                <span>-</span><br>
                                                <span class="font-italic">{{
                                                        $t('matches.op_bans.not_selected')
                                                    }}</span>
                                            </template>
                                        </b-col>

                                    </b-row>
                                </b-col>

                            </b-row>

                            <hr class="divider">

                            <!-- Second row - Rounds table -->
                            <b-row>
                                <b-col cols="12">
                                    <label>{{ $t('matches.rounds.round_details') }}:</label>
                                </b-col>

                                <b-col>
                                    <b-table table-variant="dark" small striped sort-icon-left responsive
                                             :items="rounds"
                                             :fields="roundTableFields"
                                             sort-by="round_no">

                                        <template #cell(bomb_spot)="table_data">
                                            <b-badge variant="light" pill class="mr-1">
                                                {{ getBombSpotName(table_data.item.bomb_spot).floor }}
                                            </b-badge>
                                            <span class="sl-only">{{
                                                    getBombSpotName(table_data.item.bomb_spot).name
                                                }}</span>
                                        </template>

                                        <template #cell(of_team_name)="table_data">
                                            <span v-if="table_data.item.of_team">{{
                                                    table_data.item.of_team_name
                                                }}</span>
                                            <span v-else>-</span>
                                        </template>

                                        <template #cell(score)="table_data">
                                            <span>{{ table_data.item.score_blue }} - {{
                                                    table_data.item.score_orange
                                                }}</span>
                                        </template>

                                        <template #cell(notes)="table_data">
                                            <div v-if="table_data.item.notes">
                                                <div v-for="(line, index) in table_data.item.notes.split('\\n')"
                                                     :key="index">
                                                    <span>{{ line }}</span><br>
                                                </div>
                                            </div>
                                            <span v-else>-</span>
                                        </template>

                                    </b-table>
                                </b-col>
                            </b-row>

                            <hr class="divider">

                            <!-- Third row - Round statistics -->
                            <b-row>

                                <b-col cols="12">
                                    <label>{{ $t('matches.rounds.live_stats') }}:</label>
                                </b-col>

                                <b-col>
                                    <b-row class="text-center">

                                        <b-col cols="12" md="6" lg="3" xl="3" class="mb-2">
                                            <label>{{ $t('matches.rounds.atk_def_wins') }}</label>
                                            <apexchart type="donut" :options="sideWinDataOptions"
                                                       :series="getSideWinData(rounds)"/>
                                        </b-col>

                                        <b-col cols="12" class="d-md-none d-lg-none d-xl-none">
                                            <hr class="divider">
                                        </b-col>

                                        <b-col cols="12" md="6" lg="3" xl="3" class="mb-2">
                                            <label>{{ $t('matches.rounds.opening_frags') }}</label>
                                            <apexchart type="donut" :options="ofDataOptions"
                                                       :series="getOfData(rounds)"/>
                                        </b-col>

                                        <b-col cols="12" class="d-lg-none d-xl-none">
                                            <hr class="divider">
                                        </b-col>

                                        <b-col cols="12" md="6" lg="3" xl="3" class="mb-2">
                                            <label>{{ $t('matches.rounds.type_wins') }}</label>
                                            <apexchart type="donut" :options="typeWinDataOptions"
                                                       :series="getTypeWinData(rounds)"/>
                                        </b-col>

                                        <b-col cols="12" class="d-md-none d-lg-none d-xl-none">
                                            <hr class="divider">
                                        </b-col>

                                        <b-col cols="12" md="6" lg="3" xl="3" class="mb-2">
                                            <label>{{ $t('matches.rounds.bomb_spot_picks') }}</label>
                                            <apexchart type="donut"
                                                       :options="getBombSpotPickDataOptions(currentMap.map)"
                                                       :series="getBombSpotPickData(rounds, currentMap.map)"/>
                                        </b-col>

                                    </b-row>
                                </b-col>
                            </b-row>

                        </template>
                    </CustomCard>
                </b-col>

            </b-row>
        </template>

    </div>
</template>

<script>
import CustomCard from "~/components/CustomCard";
import {MatchSingleWebsocket} from "~/mixins/websocket/MatchSingleWebsocket";
import {MatchMapAllWebsocket} from "~/mixins/websocket/MatchMapAllWebsocket";
import {OperatorBansWebsocket} from "~/mixins/websocket/OperatorBansWebsocket";
import {RoundWebsocket} from "~/mixins/websocket/RoundWebsocket";
import {Maps} from "~/mixins/axios/Maps";
import {BombSpots} from "~/mixins/axios/BombSpots";
import r6operators from "r6operators";

export default {
    name: "MatchDetails",
    layout: "match",

    data() {
        return {
            operatorIcons: r6operators,
            finishedMapData: [],
            mapID: null,

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
        }
    },

    head() {
        return {
            title: this.$t("navigation.details") + " - Caster Dashboard"
        }
    },

    computed: {
        matchID() {
            return this.$route.params.matchID
        },
        mapPicks() {
            if (this.matchMaps == null || this.matchMaps.length === 0) return null
            return this.matchMaps.filter(m => m.type === 2 || m.type === 3)
        },
        finishedMaps() {
            if (this.mapPicks == null) return null
            return this.mapPicks.filter(m => m.status === 3)
        },
        currentMap() {
            if (this.mapPicks == null) return null
            let map = this.mapPicks.filter(m => m.status === 2)
            if (map == null || map.length === 0) return null
            return map[0]
        },

        mapImgURLs() {
            let urls = []
            this.maps.forEach(e => {
                urls.push(require('~/assets/img/maps/' + e.id + ".webp"))
            })
            return urls
        },

        sideWinDataOptions() {
            let options = Object.assign({}, this.chartOptions)
            options['labels'] = ["ATK Wins", "DEF Wins"]
            return options
        },
        ofDataOptions() {
            let options = Object.assign({}, this.chartOptions)
            options['labels'] = [this.match.team_blue_name, this.match.team_orange_name]
            return options
        },
        typeWinDataOptions() {
            let options = Object.assign({}, this.chartOptions)
            options['labels'] = [this.$t('matches.rounds.win_type_names.kills'), this.$t('matches.rounds.win_type_names.defuser_planted'),
                this.$t('matches.rounds.win_type_names.defuser_disabled'), this.$t('matches.rounds.win_type_names.time')]
            return options
        },
    },

    watch: {
        match: {
            deep: true,
            handler(newState, oldState) {
                if (oldState == null || newState == null) return
                if (newState.score_blue >= oldState.score_blue || newState.score_orange >= oldState.score_orange) {
                    location.reload()
                }
            }
        },

        currentMap: {
            deep: true,
            async handler(newState, oldState) {
                if (oldState == null || newState == null || newState.status !== 2) return

                // Reset websockets and data
                await this.disconnectOperatorBansWebsocket()
                await this.disconnectRoundWebsocket()
                this.bannedOperators = null
                this.rounds = null

                // Set new websocket data
                this.mapID = this.currentMap.map
                await this.connectOperatorBansWebsocket()
                await this.connectRoundWebsocket()
            }
        },
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$t("navigation.details"))
        this.$store.commit("setPageTitleIcon", "list-ul")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Matches", this.$route.params.matchID, "Details"])
    },

    methods: {
        getBombSpotName(id) {
            let bomb_spot = this.bombSpots.filter(b => b.id === id)[0]
            return {"floor": bomb_spot.floor, "name": bomb_spot.name}
        },
        getBombSpotPickDataOptions(map) {
            let mapBombSpots = this.bombSpots.filter(bs => bs.map === map)
            let options = Object.assign({}, this.chartOptions)
            options['labels'] = [this.getBombSpotName(mapBombSpots[0].id).name, this.getBombSpotName(mapBombSpots[1].id).name,
                this.getBombSpotName(mapBombSpots[2].id).name, this.getBombSpotName(mapBombSpots[3].id).name]
            return options
        },

        getSideWinData(rounds) {
            if (rounds == null) return [0, 0]
            let atkWins = rounds.filter(r => r.win_team === r.atk_team).length
            let defWins = rounds.length - atkWins
            return [atkWins, defWins]
        },
        getOfData(rounds) {
            if (rounds == null) return [0, 0]
            let ofBlue = rounds.filter(r => r.of_team === this.match.team_blue).length
            let ofOrange = rounds.filter(r => r.of_team === this.match.team_orange).length
            return [ofBlue, ofOrange]
        },
        getTypeWinData(rounds) {
            if (rounds == null) return [0, 0, 0, 0]
            let typeData = [0, 0, 0, 0]
            rounds.forEach((r) => {
                typeData[r.win_type - 1]++
            })
            return typeData;
        },
        getBombSpotPickData(rounds, map) {
            if (rounds == null) return [0, 0, 0, 0]
            let mapBombSpots = this.bombSpots.filter(bs => bs.map === map)
            let bs1 = rounds.filter(r => r.bomb_spot === mapBombSpots[0].id).length
            let bs2 = rounds.filter(r => r.bomb_spot === mapBombSpots[1].id).length
            let bs3 = rounds.filter(r => r.bomb_spot === mapBombSpots[2].id).length
            let bs4 = rounds.filter(r => r.bomb_spot === mapBombSpots[3].id).length
            return [bs1, bs2, bs3, bs4]
        },
    },

    async fetch() {
        // Static data
        await this.getAllBombSpots()

        // Match
        await this.connectMatchSingleWebsocket()

        // Maps
        await this.getMaps()
        await this.connectMatchMapAllWebsocket()

        // Get match data for finished maps via websocket and disconnect it afterwards
        for (const map of this.finishedMaps) {
            this.mapID = map.map
            await this.connectOperatorBansWebsocket()
            await this.connectRoundWebsocket()
            let combinedMapData = {
                "map": map,
                "opBans": this.bannedOperators,
                "rounds": this.rounds,
            }
            this.finishedMapData.push(combinedMapData)
            await this.disconnectOperatorBansWebsocket()
            await this.disconnectRoundWebsocket()
            this.bannedOperators = null
            this.rounds = null
        }

        // Get match data for current map
        if (this.currentMap != null) {
            this.mapID = this.currentMap.map
            await this.connectOperatorBansWebsocket()
            await this.connectRoundWebsocket()
        }
    },

    mixins: [
        MatchSingleWebsocket,
        MatchMapAllWebsocket,
        OperatorBansWebsocket,
        RoundWebsocket,
        Maps,
        BombSpots,
    ],

    components: {
        CustomCard
    }

}
</script>

<style scoped type="scss">
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
