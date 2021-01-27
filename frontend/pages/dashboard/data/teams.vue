<template>
    <div>

        <CustomCard color="primary" outline divider :title="$t('data.teams.title')"
                    v-if="this.$fetchState.pending">
            <template #card-body>
                <b-skeleton-table/>
                <b-skeleton-table/>
            </template>
        </CustomCard>

        <b-overlay :show="newTeamLoading" variant="dark">
            <CustomCard color="primary" outline divider :title="$t('data.teams.title')"
                        v-if="!this.$fetchState.pending">
                <template #card-body>

                    <b-row class="text-center">

                        <b-col cols="12">
                            <b-table id="league_table" table-variant="dark" small striped sort-icon-left responsive :items="teams" :fields="fields"
                                     :per-page="perPage" :current-page="currentPage" sort-by="name">

                                <template #cell(logo)="data">
                                    <b-img :src="data.item.team_logo_small" height="30px" width="30px"/>
                                </template>

                                <template #cell(date_created)="data">
                                    {{ $d(new Date(data.item.created), 'short') }}
                                </template>

                                <template #cell(edit_team)="data">
                                    <b-btn variant="secondary" size="sm" @click="editTeam(data.item)" disabled>
                                        <font-awesome-icon icon="pen"/>
                                        {{ $t("data.teams.edit_team") }}
                                    </b-btn>
                                </template>

                            </b-table>
                        </b-col>

                        <b-col cols="12">
                            <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="perPage" aria-controls="match_table"
                                          align="center"/>
                        </b-col>

                        <Divider class="mb-4"/>

                        <b-btn variant="primary" block @click="showNewTeamModal = true">
                            <font-awesome-icon icon="plus"/>
                            {{ $t("data.teams.add_new_team_btn") }}
                        </b-btn>

                    </b-row>

                </template>
            </CustomCard>


            <template #overlay>
                <div class="text-center">
                    <b-spinner variant="light"/>
                    <br>
                    <p class="text-light mt-2">
                        {{ $t("data.teams.adding_new_team") }}
                    </p>
                </div>
            </template>

        </b-overlay>

        <NewTeamModal :show="showNewTeamModal" @hide="showNewTeamModal = false"
                      @loading="newTeamLoading = true" @reload="$fetch(); newTeamLoading = false"/>


    </div>
</template>

<script>
import CustomCard from "~/components/CustomCard";
import Divider from "~/components/Divider";
import NewTeamModal from "~/components/modals/NewTeamModal";
import {TeamData} from "~/mixins/axios/TeamData";

export default {
    name: "TeamData",

    data() {
        return {
            showNewTeamModal: false,
            newTeamLoading: false,

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
                    label: this.$tc("core.team"),
                    sortable: true
                },
                {
                    key: "date_created",
                    label: this.$t("data.teams.date_created"),
                    sortable: false
                },
                {
                    key: "edit_team",
                    label: this.$t("data.teams.edit_team"),
                    sortable: false
                }
            ],
            perPage: 10,
            currentPage: 1
        }
    },

    head() {
        return {
            title: this.$tc("core.team", 2) + " - Caster Dashboard"
        }
    },

    computed: {
        totalRows() {
            return this.teams.length
        }
    },

    methods: {
        editTeam(team) {
            this.$toast.info("This feature is not available yet!")
        }
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$tc("core.team", 2))
        this.$store.commit("setPageTitleIcon", "users")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Data", "Teams"])
    },

    async fetch() {
        await this.getTeamData()
    },

    mixins: [
        TeamData
    ],

    components: {
        "Divider": Divider,
        "CustomCard": CustomCard,
        "NewTeamModal": NewTeamModal
    }

}
</script>

<style scoped>

</style>
