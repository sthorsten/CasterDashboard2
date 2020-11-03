<template>
    <BaseLayout :title="$t('navigation.overview')" title_icon="fas fa-gamepad" :bc_path="bcPath">

        <b-row>

            <!-- Match Details -->
            <b-col md="6">

                <template v-if="loadingStatus === 'loaded'">
                    <CustomCard color="primary" outline divider :title="$t('matches.overview.match_info')">
                        <template #card-body>

                            <b-table-simple table-variant="dark" striped small responsive>

                                <b-tbody>
                                    <b-tr class="bg-primary">
                                        <b-th colspan="2">{{ $t('matches.overview.base_info') }}</b-th>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">ID</b-th>
                                        <b-td class="text-right">{{ matchData.id }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $tc('generic.user', matchData.user.length) }}</b-th>
                                        <b-td class="text-right">{{ matchData.user_name.join(", ") }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $t('core.title') }}</b-th>
                                        <b-td class="text-right">{{ matchData.title }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $t('core.playday') }}</b-th>
                                        <b-td class="text-right">{{ matchData.subtitle }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $t('core.best_of') }}</b-th>
                                        <b-td class="text-right">{{ matchData.best_of }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $t('generic.state') }}</b-th>
                                        <b-td class="text-right">{{ matchData.state_name }}</b-td>
                                    </b-tr>

                                    <b-tr class="bg-primary">
                                        <b-th colspan="2">{{ $t('matches.overview.match_details') }}</b-th>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $tc('core.league') }}</b-th>
                                        <b-td class="text-right">{{ matchData.league_name }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $tc('core.season') }}</b-th>
                                        <b-td class="text-right">{{ matchData.season_name }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $t('core.team_blue') }}</b-th>
                                        <b-td class="text-right">{{ matchData.team_blue_name }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $t('core.team_orange') }}</b-th>
                                        <b-td class="text-right">{{ matchData.team_orange_name }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $tc('core.sponsor', matchData.sponsors.length) }}</b-th>
                                        <b-td v-if="matchData.sponsors.length > 0" class="text-right">
                                            {{ matchData.sponsors_name.join(", ") }}
                                        </b-td>
                                        <b-td v-else class="text-right">-</b-td>
                                    </b-tr>

                                    <b-tr class="bg-primary">
                                        <b-th colspan="2">{{ $t('matches.overview.match_results') }}</b-th>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $t('matches.overview.current_score') }}</b-th>
                                        <b-td class="text-right">{{ matchData.score_blue }} - {{ matchData.score_orange }}</b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">{{ $t('matches.overview.win_team') }}</b-th>
                                        <b-td v-if="matchData.win_team_name" class="text-right">{{ matchData.win_team_name }}</b-td>
                                        <b-td v-else class="text-right">-</b-td>
                                    </b-tr>

                                </b-tbody>

                            </b-table-simple>

                        </template>
                    </CustomCard>
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

            </b-col>

            <!-- Match actions -->
            <b-col md="6">

                <CustomCard color="success" outline divider :title="$t('matches.overview.actions.title')">
                    <template #card-body>

                        <b-row>

                            <b-col cols="12" class="mb-2">
                                <b-btn variant="success" class="btn-block" @click="setMatchToOverlay">
                                    {{ $t('matches.overview.actions.set_overlay') }}
                                </b-btn>
                            </b-col>

                            <b-col cols="12">
                                <router-link :to="{name: 'Map Picks & Bans', params: {id: $route.params.id}}">
                                    <b-btn variant="success" class="btn-block">
                                        {{ $t('matches.overview.actions.continue') }}
                                    </b-btn>
                                </router-link>
                            </b-col>

                        </b-row>

                        <hr class="divider">

                        <b-row>

                            <b-col cols="12" class="mb-2">
                                <b-btn variant="secondary" class="btn-block">
                                    {{ $t('matches.overview.actions.show_details') }}
                                </b-btn>
                            </b-col>

                            <b-col cols="12">
                                <b-btn variant="secondary" class="btn-block">
                                    {{ $t('matches.overview.actions.share') }}
                                </b-btn>
                            </b-col>

                        </b-row>

                        <hr class="divider">

                        <b-row>

                            <b-col cols="12" class="mb-2">
                                <b-btn variant="danger" class="btn-block">
                                    {{ $t('matches.overview.actions.edit') }}
                                </b-btn>
                            </b-col>

                            <b-col cols="12">
                                <b-btn variant="danger" class="btn-block">
                                    {{ $t('matches.overview.actions.delete') }}
                                </b-btn>
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
            matchData: {},
            loadingStatus: 'loading',
            bcPath: ["Dashboard", "Matches", this.$route.params.id, "Overview"]
        }
    },
    methods: {
        setMatchToOverlay() {
            let data = {
                "user": this.$store.state.user.id,
                "current_match": this.$route.params.id
            }

            axios.put(`${this.$store.state.backendURL}/api/overlay/match_data/${this.$store.state.user.id}/`, data, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.$toast.success(this.$t('matches.overview.toasts.overlay_success'))
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error(this.$t('matches.overview.toasts.overlay_failed'))
            })
        },
        getMatchData() {
            axios.get(`${this.$store.state.backendURL}/api/match/${this.$route.params.id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.matchData = response.data
                this.loadingStatus = 'loaded'
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