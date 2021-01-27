<template>
    <div>

        <CustomCard color="primary" outline divider :title="$t('data.sponsors.title')"
                    v-if="this.$fetchState.pending">
            <template #card-body>
                <b-skeleton-table/>
                <b-skeleton-table/>
            </template>
        </CustomCard>

        <CustomCard color="primary" outline divider :title="$t('data.sponsors.title')"
                    v-if="!this.$fetchState.pending">
            <template #card-body>

                <b-row class="text-center">

                    <b-col cols="12">
                        <b-table id="league_table" table-variant="dark" small striped sort-icon-left responsive :items="sponsors" :fields="fields"
                                 :per-page="perPage" :current-page="currentPage" sort-by="name">

                            <template #cell(logo)="data">
                                <b-img :src="data.item.sponsor_logo" height="30px"/>
                            </template>

                            <template #cell(public_sponsor)="data">
                                <span v-if="data.item.public">
                                    {{ $t('generic.yes') }}
                                </span>
                                <span v-else>
                                    {{ $t('generic.no') }}
                                </span>
                            </template>

                            <template #cell(associated_league)="data">
                                <span v-if="data.item.league_name">
                                    {{ data.item.league_name }}
                                </span>
                                <span v-else>
                                    -
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
import {SponsorData} from "~/mixins/axios/SponsorData";

export default {
    name: "SponsorData",

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
                    label: this.$tc("core.sponsor"),
                    sortable: true
                },
                {
                    key: "public_sponsor",
                    label: this.$t("data.sponsors.public_sponsor"),
                    sortable: false
                },
                {
                    key: "associated_league",
                    label: this.$t("data.seasons.associated_league"),
                    sortable: false
                }
            ],

            perPage: 10,
            currentPage: 1,
        }
    },

    head() {
        return {
            title: this.$tc("core.sponsor", 2) + " - Caster Dashboard"
        }
    },

    computed: {
        totalRows() {
            return this.sponsors.length
        }
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$tc("core.sponsor", 2))
        this.$store.commit("setPageTitleIcon", "money-bill-alt")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Data", "Sponsors"])
    },

    async fetch() {
        await this.getSponsorData()
    },

    mixins: [
        SponsorData
    ],

    components: {
        "CustomCard": CustomCard
    }

}
</script>

<style scoped>

</style>
