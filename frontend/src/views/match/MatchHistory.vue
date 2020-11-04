<template>
    <BaseLayout :title="$t('navigation.history')" title_icon="fas fa-history" :bc_path="bcPath">

        <template v-if="loadingStatus === 'loaded'">

            <CustomCard color="primary" outline divider :title="$t('navigation.history')">
                <template #card-body>

                    <b-row class="text-center">
                        <b-col cols="12">
                            <b-table id="match_table" table-variant="dark" small striped sort-icon-left responsive :items="matches" :fields="fields"
                                     :per-page="perPage" :current-page="currentPage" sort-by="id" sort-desc>

                                <template #cell(button)="data">
                                    <router-link :to="{name: 'Match Overview', params: {id: data.item.id}}">
                                        <b-btn variant="primary" size="sm">
                                            {{ $t('matches.history.go_to_match') }}
                                        </b-btn>
                                    </router-link>
                                </template>

                            </b-table>
                        </b-col>

                        <b-col cols="12">
                            <b-pagination v-model="currentPage" :total-rows="total_rows" :per-page="perPage" aria-controls="match_table"
                                          align="center"/>
                        </b-col>
                    </b-row>

                </template>
            </CustomCard>

        </template>

        <!-- Loading overlay -->
        <template v-if="loadingStatus === 'loading'">
            <CustomCard color="secondary" outline divider :title="$t('generic.loading')">
                <template #card-body>
                    <StatusOverlay type="loading" :text="$t('matches.history.loading_matches')"></StatusOverlay>
                </template>
            </CustomCard>
        </template>

        <!-- Error overlay -->
        <template v-if="loadingStatus === 'error'">
            <CustomCard color="danger" outline divider :title="$t('generic.error')">
                <template #card-body>
                    <StatusOverlay type="icon" icon="fas fa-exclamation-triangle fa-2x"
                                   :text="$t('matches.history.loading_matches_failed')"></StatusOverlay>
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
    name: "MatchHistory",
    data() {
        return {
            fields: [
                {
                    key: "id",
                    label: "ID",
                    sortable: true
                },
                {
                    key: "league_name",
                    label: this.$tc('core.league'),
                    sortable: true
                },
                {
                    key: "subtitle",
                    label: this.$t('core.playday'),
                },
                {
                    key: "best_of"
                },
                {
                    key: "team_blue_name",
                    label: this.$t('core.team_blue'),
                    sortable: true
                },
                {
                    key: "team_orange_name",
                    label: this.$t('core.team_orange'),
                    sortable: true
                },
                {
                    key: "button",
                    label: this.$t('generic.actions')
                }
            ],
            matches: [],

            perPage: 10,
            currentPage: 1,
            loadingStatus: "loading",
            bcPath: ["Dashboard", "Matches", "History"]
        }
    },
    computed: {
        total_rows() {
            return this.matches.length
        }
    },
    methods: {
        getMatches() {
            axios.get(`${this.$store.state.backendURL}/api/match/?user=${this.$store.state.user.id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response)
                this.matches = response.data
                this.loadingStatus = 'loaded'
            }).catch((error) => {
                console.log(error.response)
                this.loadingStatus = 'error'
            })
        }
    },
    created() {
        this.getMatches()
    },
    components: {
        BaseLayout, CustomCard, StatusOverlay
    }
}
</script>

<style scoped>

</style>