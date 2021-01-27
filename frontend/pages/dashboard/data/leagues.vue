<template>
    <div>

        <CustomCard color="primary" outline divider :title="$t('data.leagues.title')"
                    v-if="this.$fetchState.pending">
            <template #card-body>
                <b-skeleton-table/>
                <b-skeleton-table/>
            </template>
        </CustomCard>

        <CustomCard color="primary" outline divider :title="$t('data.leagues.title')"
                    v-if="!this.$fetchState.pending">
            <template #card-body>

                <b-row class="text-center">

                    <b-col cols="12">
                        <b-table id="league_table" table-variant="dark" small striped sort-icon-left responsive :items="leagues" :fields="fields"
                                 :per-page="perPage" :current-page="currentPage" sort-by="name">

                            <template #cell(logo)="data">
                                <b-img :src="data.item.league_logo_small" height="30px" width="30px"/>
                            </template>

                            <template #cell(restricted)="data">
                                <span v-if="data.item.is_restricted">
                                    {{ $t('generic.yes') }}
                                </span>
                                <span v-else>
                                    {{ $t('generic.no') }}
                                </span>
                            </template>

                            <template #cell(custom_overlay)="data">
                                <span v-if="data.item.has_custom_overlay">
                                    {{ $t('generic.yes') }}
                                </span>
                                <span v-else>
                                    {{ $t('generic.no') }}
                                </span>
                            </template>

                        </b-table>
                    </b-col>

                    <b-col cols="12">
                        <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="perPage" aria-controls="match_table"
                                      align="center"/>
                    </b-col>

                </b-row>

            </template>
        </CustomCard>

    </div>
</template>

<script>
import CustomCard from "~/components/CustomCard";
import {LeagueData} from "~/mixins/axios/LeagueData";

export default {
    name: "LeagueData",

    data() {
        return {
            fields: [
                {
                    key: "id",
                    label: "ID",
                    sortable: true
                },
                {
                    key: "logo",
                    label: this.$t("core.logo"),
                    sortable: false
                },
                {
                    key: "name",
                    label: this.$tc("core.league"),
                    sortable: true
                },
                {
                    key: "restricted",
                    label: this.$t("data.leagues.restricted"),
                    sortable: false
                },
                {
                    key: "custom_overlay",
                    label: this.$t("data.leagues.custom_overlay"),
                    sortable: false
                }
            ],

            perPage: 10,
            currentPage: 1,
        }
    },

    head() {
        return {
            title: this.$tc("core.league", 2) + " - Caster Dashboard"
        }
    },

    computed: {
        totalRows() {
            return this.leagues.length
        }
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$tc("core.league", 2))
        this.$store.commit("setPageTitleIcon", "trophy")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Data", "Leagues"])
    },

    async fetch() {
        await this.getLeagueData()
    },

    mixins: [
        LeagueData
    ],

    components: {
        "CustomCard": CustomCard
    }

}
</script>

<style scoped>

</style>
