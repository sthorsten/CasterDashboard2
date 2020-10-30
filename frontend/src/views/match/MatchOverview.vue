<template>
    <BaseLayout title="Match Overview" title_icon="fas fa-gamepad" :bc_path="bc_path">

        <b-row>

            <!-- Match Details -->
            <b-col md="6">

                <template v-if="loading_status === 'loaded'">
                    <CustomCard color="primary" outline divider title="Match Info">
                        <template #card-body>

                            <b-table-simple table-variant="dark" striped small responsive>

                                <b-tbody>
                                    <b-tr class="bg-primary">
                                        <b-th colspan="2">Base Information</b-th>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">ID</b-th>
                                        <b-td class="text-right">{{ match_data.id }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Users</b-th>
                                        <b-td class="text-right">{{ match_data.user_name.join(", ") }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Title</b-th>
                                        <b-td class="text-right">{{ match_data.title }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Playday</b-th>
                                        <b-td class="text-right">{{ match_data.subtitle }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Best Of</b-th>
                                        <b-td class="text-right">{{ match_data.best_of }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">State</b-th>
                                        <b-td class="text-right">{{ match_data.state_name }}</b-td>
                                    </b-tr>

                                    <b-tr class="bg-primary">
                                        <b-th colspan="2">Match Details</b-th>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">League</b-th>
                                        <b-td class="text-right">{{ match_data.league_name }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Season</b-th>
                                        <b-td class="text-right">{{ match_data.season_name }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Team Blue</b-th>
                                        <b-td class="text-right">{{ match_data.team_blue_name }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Team Orange</b-th>
                                        <b-td class="text-right">{{ match_data.team_orange_name }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Sponsors</b-th>
                                        <b-td class="text-right">
                                            {{ match_data.sponsors_name.join(", ") }}
                                        </b-td>
                                    </b-tr>

                                    <b-tr class="bg-primary">
                                        <b-th colspan="2">Match Results</b-th>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Current Score</b-th>
                                        <b-td class="text-right">{{ match_data.score_blue }} - {{ match_data.score_orange }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Win Team</b-th>
                                        <b-td v-if="match_data.win_team_name" class="text-right">{{ match_data.win_team_name }}</b-td>
                                        <b-td v-else class="text-right">-</b-td>
                                    </b-tr>

                                </b-tbody>

                            </b-table-simple>

                        </template>
                    </CustomCard>
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

            </b-col>

            <!-- Match actions -->
            <b-col md="6">

                <CustomCard color="success" outline divider title="Match actions">
                    <template #card-body>

                        <b-row>

                            <b-col cols="12" class="mb-2">
                                <b-btn variant="success" class="btn-block" @click="setMatchToOverlay">Set current match to overlays</b-btn>
                            </b-col>

                            <b-col cols="12">
                                <router-link :to="{name: 'Map Picks & Bans', params: {id: $route.params.id}}">
                                    <b-btn variant="success" class="btn-block">
                                        Continue to Map Picks & Bans
                                    </b-btn>
                                </router-link>
                            </b-col>

                        </b-row>

                        <hr class="divider">

                        <b-row>

                            <b-col cols="12" class="mb-2">
                                <b-btn variant="secondary" class="btn-block">Show match details</b-btn>
                            </b-col>

                            <b-col cols="12">
                                <b-btn variant="secondary" class="btn-block">Share match</b-btn>
                            </b-col>

                        </b-row>

                        <hr class="divider">

                        <b-row>

                            <b-col cols="12" class="mb-2">
                                <b-btn variant="danger" class="btn-block">Edit match details</b-btn>
                            </b-col>

                            <b-col cols="12">
                                <b-btn variant="danger" class="btn-block">Delete match</b-btn>
                            </b-col>

                        </b-row>

                    </template>
                </CustomCard>

            </b-col>

        </b-row>

    </BaseLayout>
</template>

<script>
import axios from "axios";
import BaseLayout from "@/components/layout/BaseLayout";
import CustomCard from "@/components/elements/CustomCard";
import StatusOverlay from "@/components/elements/StatusOverlay";

export default {
    name: "MatchOverview",
    data() {
        return {
            match_data: {},

            loading_status: 'loading',
            bc_path: ["Dashboard", "Matches", this.$route.params.id, "Overview"]
        }
    },
    methods: {
        setMatchToOverlay() {
            let data = {
                "user": this.$store.state.user.id,
                "current_match": this.$route.params.id
            }

            axios.put(this.$store.state.backendURL + "/api/overlay/match_data/" + this.$store.state.user.id + "/", data, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.$toast.success("The match has been set to the overlays!")
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error("Failed to set match to the overlays :(")
            })
        },
        getMatchData() {
            axios.get(this.$store.state.backendURL + "/api/match/" + this.$route.params.id, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.match_data = response.data
                this.loading_status = 'loaded'
            })
        },
    },
    created() {
        this.getMatchData()
    },
    components: {
        BaseLayout, CustomCard, StatusOverlay
    }
}
</script>

<style scoped>

</style>