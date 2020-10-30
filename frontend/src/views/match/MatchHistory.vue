<template>
    <BaseLayout :title="$t('navigation.history')" title_icon="fas fa-history" :bc_path="bc_path">

        <template v-if="loading_status === 'loaded'">

            <CustomCard color="primary" outline divider :title="$t('navigation.history')">
                <template #card-body>

                    <b-row class="text-center">
                        <b-col cols="12">
                            <b-table id="match_table" table-variant="dark" small striped sort-icon-left responsive :items="matches" :fields="fields"
                                     :per-page="per_page" :current-page="current_page" sort-by="id" sort-desc>

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
                            <b-pagination v-model="current_page" :total-rows="total_rows" :per-page="per_page" aria-controls="match_table"
                                          align="center"/>
                        </b-col>
                    </b-row>

                </template>
            </CustomCard>

        </template>

        <!-- Loading overlay -->
        <template v-if="loading_status === 'loading'">
            <CustomCard color="secondary" outline divider :title="$t('core.loading')">
                <template #card-body>
                    <StatusOverlay type="loading" :text="$t('matches.history.loading_matches')"></StatusOverlay>
                </template>
            </CustomCard>
        </template>

        <!-- Error overlay -->
        <template v-if="loading_status === 'error'">
            <CustomCard color="danger" outline divider :title="$t('core.error')">
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
    name: "ControlCenter",
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

            per_page: 10,
            current_page: 1,
            loading_status: "loading",
            bc_path: ["Dashboard", "Matches", "History"]
        }
    },
    computed: {
        total_rows() {
            return this.matches.length
        }
    },
    methods: {
        getMatches() {
            axios.get(this.$store.state.backendURL + "/api/match/?user=" + this.$store.state.user.id, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response)
                this.matches = response.data
                this.loading_status = 'loaded'
            }).catch((error) => {
                console.log(error.response)
                this.loading_status = 'error'
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