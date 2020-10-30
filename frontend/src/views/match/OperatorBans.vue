<template>
    <BaseLayout title="Operator Bans" title_icon="fas fa-users-slash" :bc_path="bc_path">

        <template v-if="loading_status === 'loaded'">
            <b-row>
                <b-col lg="6">

                    <CustomCard color="primary" outline divider title="Settings">
                        <template #card-body>

                            <b-row>

                                <!-- ATK Team -->
                                <b-col lg="6">

                                    <label class="text-bold">ATK team</label>

                                    <b-row>

                                        <b-col xl="6">
                                            <template v-if="atk_team === match_data.team_blue">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0" :disabled="opbans.length > 0">
                                                    {{ match_data.team_blue_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                       :disabled="opbans.length > 0"
                                                       @click="setATKTeam(match_data.team_blue)">
                                                    {{ match_data.team_blue_name }}
                                                    <b-spinner v-if="loading_small === 'atk-' + match_data.team_blue" variant="light" small/>
                                                </b-btn>
                                            </template>
                                        </b-col>

                                        <b-col xl="6">
                                            <template v-if="atk_team === match_data.team_orange">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0" :disabled="opbans.length > 0">
                                                    {{ match_data.team_orange_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                       :disabled="opbans.length > 0"
                                                       @click="setATKTeam(match_data.team_orange)">
                                                    {{ match_data.team_orange_name }}
                                                    <b-spinner v-if="loading_small === 'atk-' + match_data.team_orange" variant="light" small/>
                                                </b-btn>
                                            </template>
                                        </b-col>

                                    </b-row>

                                </b-col>

                                <!-- OT ATK Team -->
                                <b-col lg="6" class="mt-2 mt-xl-0">

                                    <label class="text-bold">Overtime ATK team (optional)</label>

                                    <b-row>

                                        <b-col xl="6">

                                            <template v-if="ot_atk_team === match_data.team_blue">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                                                    {{ match_data.team_blue_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                       @click="setOTATKTeam(match_data.team_blue)">
                                                    {{ match_data.team_blue_name }}
                                                    <b-spinner v-if="loading_small === 'ot-atk-' + match_data.team_blue" variant="light" small/>
                                                </b-btn>
                                            </template>

                                        </b-col>

                                        <b-col xl="6">

                                            <template v-if="ot_atk_team === match_data.team_orange">
                                                <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                                                    {{ match_data.team_orange_name }}
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                       @click="setOTATKTeam(match_data.team_orange)">
                                                    {{ match_data.team_orange_name }}
                                                    <b-spinner v-if="loading_small === 'ot-atk-' + match_data.team_orange" variant="light" small/>
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
                                    <label>Swap teams?</label>
                                </b-col>

                                <b-col cols="4" md="3" xl="2">
                                    <span>Team Blue</span><br>
                                    <span class="font-italic">{{ match_data.team_blue_name }}</span>
                                </b-col>

                                <b-col cols="4" md="6" xl="8">
                                    <b-btn variant="primary" class="btn-block h-100"
                                        :disabled="opbans.length > 0"
                                        @click="swapTeams">
                                        <i class="fa fas fa-long-arrow-alt-left"></i>
                                        Swap teams
                                        <i class="fa fas fa-long-arrow-alt-right"></i>
                                    </b-btn>
                                </b-col>

                                <b-col cols="4" md="3" xl="2" class="text-right">
                                    <span>Team Orange</span><br>
                                    <span class="font-italic">{{ match_data.team_orange_name }}</span>
                                </b-col>

                            </b-row>

                            <hr class="divider">

                            <!-- Current operator bans -->
                            <b-row align-v="center">

                                <b-col cols="12">
                                    <label>Current Operator Bans:</label>
                                </b-col>

                                <!-- Ban 1 - ATK -->
                                <b-col cols="3" class="text-center">
                                    <template v-if="opbans[0]">
                                        <img style="height: 50px; width: 50px;" :src="operator_img_urls[opbans[0].operator - 1]"><br>
                                        <span>{{ opbans[0].operator_name }}</span><br>
                                        <span class="font-italic">{{ opbans[0].team_name }}</span>
                                    </template>

                                    <template v-else>
                                        <span>-</span><br>
                                        <span class="font-italic">Not selected</span>
                                    </template>
                                </b-col>

                                <!-- Ban 2 - ATK -->
                                <b-col cols="3" class="text-center">
                                    <template v-if="opbans[1]">
                                        <img style="height: 50px; width: 50px;" :src="operator_img_urls[opbans[1].operator - 1]"><br>
                                        <span>{{ opbans[1].operator_name }}</span><br>
                                        <span class="font-italic">{{ opbans[1].team_name }}</span>
                                    </template>

                                    <template v-else>
                                        <span>-</span><br>
                                        <span class="font-italic">Not selected</span>
                                    </template>
                                </b-col>

                                <!-- Ban 3 - DEF -->
                                <b-col cols="3" class="text-center">
                                    <template v-if="opbans[2]">
                                        <img style="height: 50px; width: 50px;" :src="operator_img_urls[opbans[2].operator - 1]"><br>
                                        <span>{{ opbans[2].operator_name }}</span><br>
                                        <span class="font-italic">{{ opbans[2].team_name }}</span>
                                    </template>

                                    <template v-else>
                                        <span>-</span><br>
                                        <span class="font-italic">Not selected</span>
                                    </template>
                                </b-col>

                                <!-- Ban 4 - DEF  -->
                                <b-col cols="3" class="text-center">
                                    <template v-if="opbans[3]">
                                        <img style="height: 50px; width: 50px;" :src="operator_img_urls[opbans[3].operator - 1]"><br>
                                        <span>{{ opbans[3].operator_name }}</span><br>
                                        <span class="font-italic">{{ opbans[3].team_name }}</span>
                                    </template>

                                    <template v-else>
                                        <span>-</span><br>
                                        <span class="font-italic">Not selected</span>
                                    </template>
                                </b-col>

                            </b-row>

                            <hr class="divider">

                            <!-- Buttons -->
                            <b-row>

                                <b-col lg="6">
                                    <b-btn variant="danger" class="btn-block" :disabled="opbans.length === 0"
                                           @click="removeLastOperatorBan">
                                        Remove last operator ban
                                        <b-spinner v-if="loading_small === 'remove-last-opban'" variant="light" small/>
                                    </b-btn>
                                </b-col>


                                <b-col lg="6" class="mt-2 mt-lg-0">
                                    <b-btn variant="danger" class="btn-block" :disabled="opbans.length === 0"
                                           @click="removeAllOperatorsBans">
                                        Remove all operator bans
                                        <b-spinner v-if="loading_small === 'remove-all-opbans'" variant="light" small/>
                                    </b-btn>
                                </b-col>

                            </b-row>

                            <b-row class="mt-2">

                                <b-col>
                                    <router-link :to="{name: 'Rounds', params:{match_id: match_data.id, map_id: match_map.map}}">
                                        <b-btn variant="primary" class="btn-block" :disabled="!all_operators_banned">
                                            Continue to rounds
                                        </b-btn>
                                    </router-link>
                                </b-col>

                            </b-row>

                        </template>
                    </CustomCard>

                </b-col>

                <b-col lg="6">

                    <CustomCard color="danger" outline divider title="Ban Operator">
                        <template #card-body>

                            <b-row>

                                <!-- ATK Ops -->
                                <b-col md="6" class="text-center">

                                    <label>ATK Operators</label><br>

                                    <b-row class="mt-2">

                                        <b-col cols="6" v-for="op in atk_ops" :key="op.id">
                                            <template v-if="isOperatorBanned(op.id)">
                                                <b-btn variant="danger" class="btn-block mb-2 text-left" disabled>
                                                    <img :src="operator_img_urls[op.id - 1]" style="height: 25px; width: 25px;">
                                                    {{ op.name }} ({{ isOperatorBanned(op.id).order }})
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="secondary" class="btn-block mb-2 text-left"
                                                       :disabled="atk_ops_banned || !atk_team"
                                                       @click="banOperator(op.id)">
                                                    <img :src="operator_img_urls[op.id - 1]" style="height: 25px; width: 25px;">
                                                    {{ op.name }}
                                                    <b-spinner v-if="loading_small === 'ban-' + op.id" variant="light" small/>
                                                </b-btn>
                                            </template>
                                        </b-col>

                                    </b-row>

                                </b-col>

                                <!-- DEF Ops -->
                                <b-col md="6" class="text-center">

                                    <label>DEF Operators</label><br>

                                    <b-row class="mt-2">
                                        <b-col cols="6" v-for="op in def_ops" :key="op.id">
                                            <template v-if="isOperatorBanned(op.id)">
                                                <b-btn variant="danger" class="btn-block mb-2 text-left" disabled>
                                                    <img :src="operator_img_urls[op.id - 1]" style="height: 25px; width: 25px;">
                                                    {{ op.name }} ({{ isOperatorBanned(op.id).order }})
                                                </b-btn>
                                            </template>
                                            <template v-else>
                                                <b-btn variant="secondary" class="btn-block mb-2 text-left"
                                                       :disabled="all_operators_banned || !atk_team"
                                                       @click="banOperator(op.id)">
                                                    <img :src="operator_img_urls[op.id - 1]" style="height: 25px; width: 25px;">
                                                    {{ op.name }}
                                                    <b-spinner v-if="loading_small === 'ban-' + op.id" variant="light" small/>
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
            atk_team: null,
            ot_atk_team: null,

            operators: [],
            atk_ops: [],
            def_ops: [],
            opbans: [],
            match_data: null,
            match_map: null,

            operators_loaded: false,
            opbans_loaded: false,
            match_data_loaded: false,
            match_map_loaded: false,

            reset_all_counter: 0,

            loading_status: 'loading',
            loading_small: "",
        }
    },
    computed: {
        def_team() {
            if (this.atk_team === this.match_data.team_blue) return this.match_data.team_orange
            return this.match_data.team_blue
        },
        next_ban_team() {
            if (this.opbans.length === 0 || this.opbans.length === 3) {
                return this.atk_team
            } else {
                return this.def_team
            }
        },
        atk_ops_banned() {
            return this.opbans.length >= 2
        },
        all_operators_banned() {
            return this.opbans.length >= 4
        },
        operator_img_urls() {
            let urls = []
            this.operators.forEach(o => {
                urls.push(require('@/assets/img/operators/' + o.id + ".svg"))
            })
            return urls
        },
        load_finished() {
            return this.operators_loaded && this.opbans_loaded && this.match_data_loaded && this.match_map_loaded
        },
        bc_path(){
            if (this.match_data_loaded && this.match_map_loaded){
                return ["Dashboard", "Matches", this.$route.params.match_id,
                    this.match_map.map_name + " (Map " + this.match_map.play_order + "/" + this.match_data.best_of + ")",
                    "Operator Bans"]
            } else {
                return ["Dashboard", "Matches", this.$route.params.match_id, this.$route.params.map_id, "Operator Bans"]
            }
        }
    },
    watch: {
        load_finished: function (newState) {
            if (newState) this.loading_status = 'loaded'
        },
        reset_all_counter: function (newState) {
            if (newState === 0) {
                console.log("Remove all complete")
                this.$toast.success("All operator bans have been removed", "Success")
                this.getOperatorBans()
            }
        }
    },
    methods: {
        swapTeams(){
            let data = {
                team_blue: this.match_data.team_orange,
                team_orange: this.match_data.team_blue
            }

            axios.patch(this.$store.state.backendURL + "/api/match/" + this.match_data.id + "/", data, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then(() => {
                this.getMatchData()
                this.$toast.success("Team swapped!", "Success", {timeout: 2000})
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error("Failed to swap teams ;(", "Error")
            })

        },
        banOperator(id) {
            if (this.atk_team === null) {
                this.$toast.warning("Please select who attacks first!")
                return;
            }

            this.loading_small = "ban-" + id

            let data = {
                order: this.opbans.length + 1,
                match: this.match_data.id,
                map: this.match_map.map,
                operator: id,
                team: this.next_ban_team
            }

            console.log(data);

            axios.post(this.$store.state.backendURL + "/api/matches/opbans/", data, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then(() => {
                this.getOperatorBans()
                this.$toast.success("Operator Ban Added", "Success", {timeout: 2000})
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error("Failed to add operator ban ;(", "Error")
            })

        },
        removeLastOperatorBan() {
            this.loading_small = "remove-last-opban"
            let toBeRemoved = this.opbans[this.opbans.length - 1].id

            axios.delete(this.$store.state.backendURL + "/api/matches/opbans/" + toBeRemoved + "/", {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then(() => {
                this.getOperatorBans()
                this.$toast.success("Operator Ban Removed", "Success", {timeout: 2000})
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error("Failed to remove operator ban ;(", "Error")
            })
        },
        removeAllOperatorsBans() {
            this.loading_small = "remove-all-opbans"
            this.reset_all_counter = this.opbans.length

            this.opbans.forEach(o => {
                axios.delete(this.$store.state.backendURL + "/api/matches/opbans/" + o.id, {
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
        isOperatorBanned(id) {
            let opbans_filtered = this.opbans.filter(o => o.operator === id)
            if (opbans_filtered.length > 0) {
                return opbans_filtered[0]
            }
            return null;
        },
        setATKTeam(id) {
            if (this.atk_team === id) return;
            this.loading_small = 'atk-' + id

            let data = {
                atk_team: id
            }

            axios.patch(this.$store.state.backendURL + "/api/matches/maps/" + this.match_map.id + "/", data, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then(() => {
                this.getMatchMap()
            }).catch((error) => {
                console.log(error.response)
            })
        },
        setOTATKTeam(id) {
            if (this.ot_atk_team === id) return;
            this.loading_small = 'ot-atk-' + id

            let data = {
                ot_atk_team: id
            }

            axios.patch(this.$store.state.backendURL + "/api/matches/maps/" + this.match_map.id + "/", data, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then(() => {
                this.getMatchMap()
            }).catch((error) => {
                console.log(error.response)
            })
        },
        getOperators() {
            axios.get(this.$store.state.backendURL + "/api/core/operator/", {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.operators = response.data
                this.atk_ops = response.data.filter(o => o.side === "ATK").sort(compareOperators)
                this.def_ops = response.data.filter(o => o.side === "DEF").sort(compareOperators)
                this.operators_loaded = true
            })
        },
        getOperatorBans() {
            axios.get(this.$store.state.backendURL + "/api/matches/opbans/?match=" + this.$route.params.match_id + "&map=" + this.$route.params.map_id, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.opbans = response.data
                this.opbans_loaded = true
                this.loading_small = ""
            })
        },
        getMatchData() {
            axios.get(this.$store.state.backendURL + "/api/match/" + this.$route.params.match_id, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.match_data = response.data
                this.match_data_loaded = true
            })
        },
        getMatchMap() {
            axios.get(this.$store.state.backendURL + "/api/matches/maps/?match=" + this.$route.params.match_id + "&map=" + this.$route.params.map_id, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.match_map = response.data[0]
                this.atk_team = response.data[0].atk_team
                this.ot_atk_team = response.data[0].ot_atk_team
                this.match_map_loaded = true
                this.loading_small = ""
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