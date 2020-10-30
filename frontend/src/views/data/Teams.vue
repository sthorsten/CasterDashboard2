<template>
    <BaseLayout :title="$tc('core.team', 2)" title_icon="fas fa-users" :bc_path="bc_path" class="text-white">

        <!-- Show content once team data is loaded -->
        <template v-if="team_data_loading_status === 'loaded'">

            <div v-show="team_logos_load_finished">
                <CustomCard color="primary" outline footer :title="$t('data.teams.title')">

                    <template #card-body>
                        <div class="table-responsive" style="height: 400px;">
                            <table class="table table-sm table-head-fixed text-nowrap">
                                <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>{{ $tc('core.team') }}</th>
                                    <th>{{ $t('core.logo') }}</th>
                                    <th>{{ $t('data.teams.edit_team') }}</th>
                                </tr>
                                </thead>

                                <tbody id="team_list_tbody">
                                <tr v-for="team in team_data" :key="team.id">
                                    <td>{{ team.id }}</td>
                                    <td>{{ team.name }}</td>
                                    <td>
                                        <img :src="team.team_logo_small" @load="incrementImageLoadCounter" alt="-" style="height: 30px; width: 30px;">
                                    </td>
                                    <td>
                                        <b-button variant="primary" size="sm" :data-teamid="team.id" :data-teamname="team.name"
                                                  @click="$toast.info($t('generic.wip'))">
                                            {{ $t('data.teams.change_logo') }}
                                        </b-button>
                                    </td>
                                </tr>
                                </tbody>

                            </table>
                        </div>
                    </template>

                    <template #card-footer>
                        <div class="row justify-content-center">
                            <b-button variant="success" @click="showNewTeamModal = true">
                                {{ $t('data.teams.add_new_team_btn') }}
                            </b-button>
                        </div>
                    </template>

                </CustomCard>
            </div>
        </template>

        <!-- Loading overlay -->
        <template v-if="team_data_loading_status === 'loading' || !team_logos_load_finished">
            <CustomCard color="secondary" outline divider :title="$t('generic.loading')">
                <template #card-body>
                    <StatusOverlay type="loading" :text="$t('data.teams.loading_teams')"></StatusOverlay>
                </template>
            </CustomCard>
        </template>

        <!-- Error overlay -->
        <template v-if="team_data_loading_status === 'error'">
            <CustomCard color="danger" outline divider :title="$t('generic.error')">
                <template #card-body>
                    <StatusOverlay type="icon" icon="fas fa-exclamation-triangle fa-2x"
                                   :text="$t('data.teams.loading_teams_failed')"></StatusOverlay>
                </template>
            </CustomCard>
        </template>

        <!-- Include modals-->
        <NewTeamModal :show="showNewTeamModal" @hide="showNewTeamModal = false"
                      @loading="team_data_loading_status = 'loading'" @reload="this.loadData"/>

        <!-- Change Logo Modal -->
        <!-- ToDo: Add change logo feature -->

    </BaseLayout>
</template>

<script>
import axios from 'axios';

import BaseLayout from "@/components/layout/BaseLayout";
import CustomCard from "@/components/elements/CustomCard";
import StatusOverlay from "@/components/elements/StatusOverlay";
import NewTeamModal from "@/components/subcomponents/NewTeamModal";

function compareTeams(a, b) {
    if (a.name.toLowerCase() > b.name.toLowerCase()) return 1;
    if (a.name.toLowerCase() < b.name.toLowerCase()) return -1;
    return 0;
}

export default {
    name: "Teams",
    data() {
        return {
            team_logos_loaded: 0,
            team_data: {},
            team_data_loading_status: "loading",
            showNewTeamModal: false,
            bc_path: ['Dashboard', 'Data', 'Teams'],
        }
    },
    computed: {
        team_logos_to_load() {
            return this.team_data.length
        },
        team_logos_load_finished() {
            return this.team_logos_loaded === this.team_logos_to_load
        },
    },
    methods: {
        incrementImageLoadCounter() {
            this.team_logos_loaded++
        },
        loadData() {
            this.team_logos_loaded = 0
            axios.get(this.$store.state.backendURL + "/api/data/team/", {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                this.team_data = response.data.sort(compareTeams);
                this.team_data_loading_status = 'loaded';
                console.log("team data:");
                console.log(this.team_data);
            }).catch((error) => {
                console.log(error);
                this.team_data_loading_status = 'error';
            });
        },

    },
    created() {
        this.loadData();
    },
    components: {
        BaseLayout, CustomCard, StatusOverlay, NewTeamModal
    },
}
</script>

<style scoped>

</style>