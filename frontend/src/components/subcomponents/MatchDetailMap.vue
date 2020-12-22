<template>

    <CustomCard :title="'Map #' + matchMap.play_order + ' - ' + matchMap.map_name" color="success" outline divider>
        <template #card-body>
            <b-row v-if="loaded">

                <!-- Map Details -->
                <b-col lg="6" cols="12">
                    <b-row>
                        <b-col>
                            <label>{{ $t('matches.details.map_details') }}:</label>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <ul>
                                <li><b>{{ $t('generic.state') }}:</b> {{ matchMap.status_name }}</li>
                                <li><b>{{ $t('matches.op_bans.atk_team') }}:</b> {{ matchMap.atk_team_name }}</li>
                                <li><b>{{ $t('matches.details.ot_atk_team') }}:</b> {{ matchMap.ot_atk_team_name }}</li>
                            </ul>
                        </b-col>
                    </b-row>
                </b-col>

                <!-- Operator Bans -->
                <b-col lg="6" cols="12">
                    <b-row>
                        <b-col cols="12">
                            <label>{{ $t('navigation.op_bans') }}:</label>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col lg="3" md="6" cols="12" v-for="(opban, i) in opBans" :key="opban.id" class="text-center">
                            <img style="height: 50px; width: 50px;" :src="operatorImgUrls[opBans[i].operator - 1]"><br>
                            <span>{{ opBans[i].operator_name }}</span><br>
                            <span class="font-italic">{{ opBans[i].team_name }}</span>
                        </b-col>
                    </b-row>
                </b-col>

                <b-col>
                    <hr class="divider">
                </b-col>

                <!-- Round Table -->
                <b-col cols="12">
                    <b-row>
                        <b-col cols="12">
                            <label>{{ $t('matches.rounds.round_details') }}:</label>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col cols="12">
                            <b-table table-variant="dark" small striped sort-icon-left responsive :items="rounds"
                                     :fields="roundTableFields"
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
                        </b-col>
                    </b-row>
                </b-col>

                <b-col>
                    <hr class="divider">
                </b-col>

                <!-- Statistics -->
                <b-col cols="12">
                    <b-row>
                        <b-col cols="12">
                            <label>{{ $t('matches.rounds.live_stats') }}:</label>
                        </b-col>
                    </b-row>

                    <b-row v-if="rounds.length > 0" class="text-center">
                        <b-col cols="12" md="6" xl="3" class="mb-2">
                            <label>{{ $t('matches.rounds.atk_def_wins') }}</label>
                            <apexchart type="donut" :options="sideWinDataOptions" :series="sideWinData"/>
                        </b-col>

                        <b-col cols="12" md="6" xl="3" class="mb-2">
                            <label>{{ $t('matches.rounds.opening_frags') }}</label>
                            <apexchart type="donut" :options="ofDataOptions" :series="ofData"/>
                        </b-col>

                        <b-col cols="12" md="6" xl="3" class="mb-2">
                            <label>{{ $t('matches.rounds.type_wins') }}</label>
                            <apexchart type="donut" :options="typeWinDataOptions" :series="typeWinData"/>
                        </b-col>

                        <b-col cols="12" md="6" xl="3" class="mb-2">
                            <label>{{ $t('matches.rounds.bomb_spot_picks') }}</label>
                            <apexchart type="donut" :options="bombSpotPickDataOptions" :series="bombSpotPickData"/>
                        </b-col>
                    </b-row>
                    <b-row v-else>
                        <b-col>
                            <i>{{ $t('matches.rounds.live_stats_placeholder') }}</i>
                        </b-col>
                    </b-row>
                </b-col>
            </b-row>

            <b-row v-else>
                <b-col>
                    <i>{{$t('generic.no_data')}}</i>
                </b-col>
            </b-row>
        </template>
    </CustomCard>

</template>

<script>
import CustomCard from "@/components/elements/CustomCard";
import {Operators} from "@/mixins/axios/Operators";
import {BombSpots} from "@/mixins/axios/BombSpots";

export default {
    name: "MatchDetailMap",
    mixins: [Operators, BombSpots],
    props: {
        match: Object,
        matchMap: Object,
        opBans: Array,
        rounds: Array
    },
    data() {
        return {
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

        }
    },
    computed: {
        mapID() {
            return this.matchMap.map
        },

        loaded(){
            return this.match && this.matchMap && this.opBans && this.rounds && this.bombSpots && this.operators
        },

        sideWinData() {
            let atkWins = this.rounds.filter(r => r.win_team === r.atk_team).length
            let defWins = this.rounds.length - atkWins
            return [atkWins, defWins]
        },

        ofData() {
            let ofBlue = this.rounds.filter(r => r.of_team === this.match.team_blue).length
            let ofOrange = this.rounds.filter(r => r.of_team === this.match.team_orange).length
            return [ofBlue, ofOrange]
        },

        typeWinData() {
            let typeData = [0, 0, 0, 0]
            this.rounds.forEach((r) => {
                typeData[r.win_type - 1]++
            })
            return typeData;
        },

        bombSpotPickData() {
            let bs1 = this.rounds.filter(r => r.bomb_spot === this.bombSpots[0].id).length
            let bs2 = this.rounds.filter(r => r.bomb_spot === this.bombSpots[1].id).length
            let bs3 = this.rounds.filter(r => r.bomb_spot === this.bombSpots[2].id).length
            let bs4 = this.rounds.filter(r => r.bomb_spot === this.bombSpots[3].id).length
            return [bs1, bs2, bs3, bs4]
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
    },
    created() {
        this.getBombSpots()
        this.getOperators()
    },
    components: {
        CustomCard
    }
}
</script>

<style scoped>

</style>