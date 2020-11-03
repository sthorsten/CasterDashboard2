<template>
    <BaseLayout :title="$t('navigation.op_bans')" title_icon="fas fa-users-slash" :bc_path="bcPath">

        <template v-if="loadingStatus === 'loaded'">
            <b-row>
                <b-col lg="6">

                    <CustomCard color="primary" outline divider :title="$t('generic.settings')">
                        <template #card-body>

                            <b-row>

                                <!-- ATK Team -->
                                <b-col lg="6">

                                    <label class="text-bold">{{ $t('matches.op_bans.atk_team') }}</label>

                                    <b-row>

                                        <b-col xl="6">
                                            <template v-if="atkTeam === matchData.team_blue">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0" :disabled="opBans.length > 0">
                                                    {{ matchData.team_blue_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                       :disabled="opBans.length > 0"
                                                       @click="setATKTeam(matchData.team_blue)">
                                                    {{ matchData.team_blue_name }}
                                                    <b-spinner v-if="loadingSmall === 'atk-' + matchData.team_blue" variant="light" small/>
                                                </b-btn>
                                            </template>
                                        </b-col>

                                        <b-col xl="6">
                                            <template v-if="atkTeam === matchData.team_orange">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0" :disabled="opBans.length > 0">
                                                    {{ matchData.team_orange_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                       :disabled="opBans.length > 0"
                                                       @click="setATKTeam(matchData.team_orange)">
                                                    {{ matchData.team_orange_name }}
                                                    <b-spinner v-if="loadingSmall === 'atk-' + matchData.team_orange" variant="light" small/>
                                                </b-btn>
                                            </template>
                                        </b-col>

                                    </b-row>

                                </b-col>

                                <!-- OT ATK Team -->
                                <b-col lg="6" class="mt-2 mt-xl-0">

                                    <label class="text-bold">{{ $t('matches.op_bans.ot_atk_team') }}</label>

                                    <b-row>

                                        <b-col xl="6">

                                            <template v-if="otAtkTeam === matchData.team_blue">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                                                    {{ matchData.team_blue_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                       @click="setOTATKTeam(matchData.team_blue)">
                                                    {{ matchData.team_blue_name }}
                                                    <b-spinner v-if="loadingSmall === 'ot-atk-' + matchData.team_blue" variant="light" small/>
                                                </b-btn>
                                            </template>

                                        </b-col>

                                        <b-col xl="6">

                                            <template v-if="otAtkTeam === matchData.team_orange">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                                                    {{ matchData.team_orange_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                       @click="setOTATKTeam(matchData.team_orange)">
                                                    {{ matchData.team_orange_name }}
                                                    <b-spinner v-if="loadingSmall === 'ot-atk-' + matchData.team_orange" variant="light" small/>
                                                </b-btn>
                                            </template>

                                        </b-col>
                                    </b-row>

                                </b-col>

                            </b-row>

                            <hr class="divider">

                            <!-- Swap teams -->
                            <b-row>

                                <b-col cols="12">
                                    <label>{{ $t('matches.op_bans.swap_teams') }}?</label>
                                </b-col>

                                <b-col cols="4" md="3" xl="2">
                                    <span>{{ $t('core.team_blue') }}</span><br>
                                    <span class="font-italic">{{ matchData.team_blue_name }}</span>
                                </b-col>

                                <b-col cols="4" md="6" xl="8">
                                    <b-btn variant="primary" class="btn-block h-100"
                                           :disabled="opBans.length > 0"
                                           @click="swapTeams">
                                        <i class="fa fas fa-long-arrow-alt-left"></i>
                                        {{ $t('matches.op_bans.swap_teams') }}
                                        <i class="fa fas fa-long-arrow-alt-right"></i>
                                    </b-btn>
                                </b-col>

                                <b-col cols="4" md="3" xl="2" class="text-right">
                                    <span>{{ $t('core.team_orange') }}</span><br>
                                    <span class="font-italic">{{ matchData.team_orange_name }}</span>
                                </b-col>

                            </b-row>

                            <hr class="divider">

                            <!-- Current operator bans -->
                            <b-row align-v="center">

                                <b-col cols="12">
                                    <label>{{ $t('matches.op_bans.current_op_bans') }}</label>
                                </b-col>

                                <!-- Ban 1 - ATK -->
                                <b-col cols="3" class="text-center">
                                    <template v-if="opBans[0]">
                                        <img style="height: 50px; width: 50px;" :src="operatorImgUrls[opBans[0].operator - 1]"><br>
                                        <span>{{ opBans[0].operator_name }}</span><br>
                                        <span class="font-italic">{{ opBans[0].team_name }}</span>
                                    </template>

                                    <template v-else>
                                        <span>-</span><br>
                                        <span class="font-italic">{{ $t('matches.op_bans.not_selected') }}</span>
                                    </template>
                                </b-col>

                                <!-- Ban 2 - ATK -->
                                <b-col cols="3" class="text-center">
                                    <template v-if="opBans[1]">
                                        <img style="height: 50px; width: 50px;" :src="operatorImgUrls[opBans[1].operator - 1]"><br>
                                        <span>{{ opBans[1].operator_name }}</span><br>
                                        <span class="font-italic">{{ opBans[1].team_name }}</span>
                                    </template>

                                    <template v-else>
                                        <span>-</span><br>
                                        <span class="font-italic">{{ $t('matches.op_bans.not_selected') }}</span>
                                    </template>
                                </b-col>

                                <!-- Ban 3 - DEF -->
                                <b-col cols="3" class="text-center">
                                    <template v-if="opBans[2]">
                                        <img style="height: 50px; width: 50px;" :src="operatorImgUrls[opBans[2].operator - 1]"><br>
                                        <span>{{ opBans[2].operator_name }}</span><br>
                                        <span class="font-italic">{{ opBans[2].team_name }}</span>
                                    </template>

                                    <template v-else>
                                        <span>-</span><br>
                                        <span class="font-italic">{{ $t('matches.op_bans.not_selected') }}</span>
                                    </template>
                                </b-col>

                                <!-- Ban 4 - DEF  -->
                                <b-col cols="3" class="text-center">
                                    <template v-if="opBans[3]">
                                        <img style="height: 50px; width: 50px;" :src="operatorImgUrls[opBans[3].operator - 1]"><br>
                                        <span>{{ opBans[3].operator_name }}</span><br>
                                        <span class="font-italic">{{ opBans[3].team_name }}</span>
                                    </template>

                                    <template v-else>
                                        <span>-</span><br>
                                        <span class="font-italic">{{ $t('matches.op_bans.not_selected') }}</span>
                                    </template>
                                </b-col>

                            </b-row>

                            <hr class="divider">

                            <!-- Buttons -->
                            <b-row>

                                <b-col lg="6">
                                    <b-btn variant="danger" class="btn-block" :disabled="opBans.length === 0"
                                           @click="removeLastOperatorBan">
                                        {{ $t('matches.op_bans.remove_last_op_ban') }}
                                        <b-spinner v-if="loadingSmall === 'remove-last-opban'" variant="light" small/>
                                    </b-btn>
                                </b-col>


                                <b-col lg="6" class="mt-2 mt-lg-0">
                                    <b-btn variant="danger" class="btn-block" :disabled="opBans.length === 0"
                                           @click="removeAllOperatorsBans">
                                        {{ $t('matches.op_bans.remove_all_op_bans') }}
                                        <b-spinner v-if="loadingSmall === 'remove-all-opBans'" variant="light" small/>
                                    </b-btn>
                                </b-col>

                            </b-row>

                            <b-row class="mt-2">

                                <b-col>
                                    <router-link :to="{name: 'Rounds', params:{match_id: matchData.id, map_id: matchMap.map}}">
                                        <b-btn variant="primary" class="btn-block" :disabled="!allOperatorsBanned">
                                            {{ $t('matches.op_bans.continue') }}
                                        </b-btn>
                                    </router-link>
                                </b-col>

                            </b-row>

                        </template>
                    </CustomCard>

                </b-col>

                <b-col lg="6">

                    <CustomCard color="danger" outline divider :title="$t('matches.op_bans.ban_operators')">
                        <template #card-body>

                            <b-row>

                                <!-- ATK Ops -->
                                <b-col md="6" class="text-center">

                                    <label>{{ $t('matches.op_bans.atk_ops') }}</label><br>

                                    <b-row class="mt-2">

                                        <b-col cols="6" v-for="op in atkOps" :key="op.id">
                                            <template v-if="isOperatorBanned(op.id)">
                                                <b-btn variant="danger" class="btn-block mb-2 text-left" disabled>
                                                    <img :src="operatorImgUrls[op.id - 1]" style="height: 25px; width: 25px;">
                                                    {{ op.name }} ({{ isOperatorBanned(op.id).order }})
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="secondary" class="btn-block mb-2 text-left"
                                                       :disabled="atkOpsBanned || !atkTeam"
                                                       @click="banOperator(op.id)">
                                                    <img :src="operatorImgUrls[op.id - 1]" style="height: 25px; width: 25px;">
                                                    {{ op.name }}
                                                    <b-spinner v-if="loadingSmall === 'ban-' + op.id" variant="light" small/>
                                                </b-btn>
                                            </template>
                                        </b-col>

                                    </b-row>

                                </b-col>

                                <!-- DEF Ops -->
                                <b-col md="6" class="text-center">

                                    <label>{{ $t('matches.op_bans.def_ops') }}</label><br>

                                    <b-row class="mt-2">
                                        <b-col cols="6" v-for="op in defOps" :key="op.id">
                                            <template v-if="isOperatorBanned(op.id)">
                                                <b-btn variant="danger" class="btn-block mb-2 text-left" disabled>
                                                    <img :src="operatorImgUrls[op.id - 1]" style="height: 25px; width: 25px;">
                                                    {{ op.name }} ({{ isOperatorBanned(op.id).order }})
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="secondary" class="btn-block mb-2 text-left"
                                                       :disabled="allOperatorsBanned || !atkTeam"
                                                       @click="banOperator(op.id)">
                                                    <img :src="operatorImgUrls[op.id - 1]" style="height: 25px; width: 25px;">
                                                    {{ op.name }}
                                                    <b-spinner v-if="loadingSmall === 'ban-' + op.id" variant="light" small/>
                                                </b-btn>
                                            </template>
                                        </b-col>

                                    </b-row>

                                </b-col>

                            </b-row>

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
import StatusOverlay from "@/components/elements/StatusOverlay";
import CustomCard from "@/components/elements/CustomCard";

function compareOperators(a, b) {
    if (a.name.toLowerCase() > b.name.toLowerCase()) return 1;
    if (a.name.toLowerCase() < b.name.toLowerCase()) return -1;
    return 0;
}

export default {
    name: "OperatorBans",
    data() {
        return {
            atkTeam: null,
            otAtkTeam: null,

            operators: [],
            atkOps: [],
            defOps: [],
            opBans: [],
            matchData: null,
            matchMap: null,

            operatorsLoaded: false,
            opBansLoaded: false,
            matchDataLoaded: false,
            matchMapLoaded: false,

            resetAllCounter: 0,

            loadingStatus: 'loading',
            loadingSmall: "",
        }
    },
    computed: {
        defTeam() {
            if (this.atkTeam === this.matchData.team_blue) return this.matchData.team_orange
            return this.matchData.team_blue
        },

        nextBanTeam() {
            if (this.opBans.length === 0 || this.opBans.length === 3)
                return this.atkTeam

            return this.defTeam

        },

        atkOpsBanned() {
            return this.opBans.length >= 2
        },

        allOperatorsBanned() {
            return this.opBans.length >= 4
        },

        operatorImgUrls() {
            let urls = []
            this.operators.forEach(o => {
                urls.push(require('@/assets/img/operators/' + o.id + ".svg"))
            })
            return urls
        },

        loadFinished() {
            return this.operatorsLoaded && this.opBansLoaded && this.matchDataLoaded && this.matchMapLoaded
        },

        bcPath() {
            if (this.matchDataLoaded && this.matchMapLoaded) {
                return ["Dashboard", "Matches", this.$route.params.match_id,
                    this.matchMap.map_name + " (Map " + this.matchMap.play_order + "/" + this.matchData.best_of + ")",
                    "Operator Bans"]
            }

            return ["Dashboard", "Matches", this.$route.params.match_id, this.$route.params.map_id, "Operator Bans"]
        }
    },
    watch: {
        loadFinished: function (newState) {
            if (newState) this.loadingStatus = 'loaded'
        },

        resetAllCounter: function (newState) {
            if (newState === 0) {
                console.log("Remove all complete")
                this.$toast.success(this.$t('matches.op_bans.toasts.all_opbans_removed'), this.$t('generic.success'))
                this.getOperatorBans()
            }
        }
    },
    methods: {
        swapTeams() {
            let data = {
                team_blue: this.matchData.team_orange,
                team_orange: this.matchData.team_blue
            }

            axios.patch(`${this.$store.state.backendURL}/api/match/${this.matchData.id}/`, data, this.$store.getters.authHeader
            ).then(() => {
                this.getMatchData()
                this.$toast.success(this.$t('matches.op_bans.toasts.teams_swapped'), this.$t('generic.success'), {timeout: 2000})
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error(this.$t('matches.op_bans.toasts.teams_swapped_failed'), this.$t('generic.error'))
            })

        },

        banOperator(id) {
            this.loadingSmall = "ban-" + id

            let data = {
                order: this.opBans.length + 1,
                match: this.matchData.id,
                map: this.matchMap.map,
                operator: id,
                team: this.nextBanTeam
            }

            console.log(data);

            axios.post(`${this.$store.state.backendURL}/api/matches/opbans/`, data, this.$store.getters.authHeader
            ).then(() => {
                this.getOperatorBans()
                this.$toast.success(this.$t('matches.op_bans.toasts.opban_added'), this.$t('generic.success'), {timeout: 2000})
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error(this.$t('matches.op_bans.toasts.opban_added_failed'), this.$t('generic.error'))
            })

        },

        removeLastOperatorBan() {
            this.loadingSmall = "remove-last-opban"
            let toBeRemoved = this.opBans[this.opBans.length - 1].id

            axios.delete(`${this.$store.state.backendURL}/api/matches/opbans/${toBeRemoved}/`, this.$store.getters.authHeader
            ).then(() => {
                this.getOperatorBans()
                this.$toast.success(this.$t('matches.op_bans.toasts.opban_removed'), this.$t('generic.success'), {timeout: 2000})
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error(this.$t('matches.op_bans.toasts.opban_removed_failed'), this.$t('generic.error'))
            })
        },

        removeAllOperatorsBans() {
            this.loadingSmall = "remove-all-opBans"
            this.resetAllCounter = this.opBans.length

            this.opBans.forEach(o => {
                axios.delete(`${this.$store.state.backendURL}/api/matches/opbans/${o.id}/`, this.$store.getters.authHeader
                ).then(() => {
                    this.resetAllCounter--
                }).catch((error) => {
                    console.log(error.response)
                    this.$toast.error(this.$t('matches.op_bans.toasts.all_opbans_removed_failed'), this.$t('generic.error'))
                })
            })
        },

        isOperatorBanned(id) {
            let opbans_filtered = this.opBans.filter(o => o.operator === id)
            if (opbans_filtered.length > 0) {
                return opbans_filtered[0]
            }
            return null;
        },

        setATKTeam(id) {
            if (this.atkTeam === id) return;
            this.loadingSmall = 'atk-' + id

            let data = {
                atk_team: id
            }

            axios.patch(`${this.$store.state.backendURL}/api/matches/maps/${this.matchMap.id}/`, data, this.$store.getters.authHeader
            ).then(() => {
                this.getMatchMap()
            }).catch((error) => {
                console.log(error.response)
            })
        },

        setOTATKTeam(id) {
            if (this.otAtkTeam === id) return;
            this.loadingSmall = 'ot-atk-' + id

            let data = {
                ot_atk_team: id
            }

            axios.patch(`${this.$store.state.backendURL}/api/matches/maps/${this.matchMap.id}/`, data, this.$store.getters.authHeader
            ).then(() => {
                this.getMatchMap()
            }).catch((error) => {
                console.log(error.response)
            })
        },

        getOperators() {
            axios.get(`${this.$store.state.backendURL}/api/core/operator/`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.operators = response.data
                this.atkOps = response.data.filter(o => o.side === "ATK").sort(compareOperators)
                this.defOps = response.data.filter(o => o.side === "DEF").sort(compareOperators)
                this.operatorsLoaded = true
            })
        },

        getOperatorBans() {
            axios.get(`${this.$store.state.backendURL}/api/matches/opbans/?match=${this.$route.params.match_id}&map=${this.$route.params.map_id}`,
                    this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.opBans = response.data
                this.opBansLoaded = true
                this.loadingSmall = ""
            })
        },

        getMatchData() {
            axios.get(`${this.$store.state.backendURL}/api/match/${this.$route.params.match_id}/`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.matchData = response.data
                this.matchDataLoaded = true
            })
        },

        getMatchMap() {
            axios.get(`${this.$store.state.backendURL}/api/matches/maps/?match=${this.$route.params.match_id}&map=${this.$route.params.map_id}`,
                    this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.matchMap = response.data[0]
                this.atkTeam = response.data[0].atk_team
                this.otAtkTeam = response.data[0].ot_atk_team
                this.matchMapLoaded = true
                this.loadingSmall = ""
            })
        }
    },

    created() {
        this.getOperators()
        this.getOperatorBans()
        this.getMatchData()
        this.getMatchMap()
    },

    components: {
        BaseLayout, CustomCard, StatusOverlay
    }
}
</script>

<style scoped>

</style>