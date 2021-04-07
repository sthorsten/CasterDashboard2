<template>
    <div>

        <b-row v-if="$fetchState.pending">
            <b-col>

            </b-col>
        </b-row>

        <b-row v-if="!$fetchState.pending">

            <b-col cols="12" md="6">

                <!-- Add match group -->
                <b-row>
                    <b-col>
                        <CustomCard color="primary" outline divider :title="$t('matches.create_match_group.create')">
                            <template #card-body>

                                <label>{{ $t('generic.name') }}</label>
                                <b-form-input class="mb-2" v-model="newMatchGroupName"
                                              :placeholder="$t('matches.create_match_group.set_name')"/>

                                <label>{{ $t('matches.create_match_group.select_match') }}:</label>

                                <v-select class="w-100 mb-4" v-model="newMatchGroupMatches" :options="matches"
                                          :multiple="true"
                                          :placeholder="$t('matches.create_match_group.select_match')">
                                    <template #selected-option="{ team_blue_name, team_orange_name, id }">
                                        {{ team_blue_name }} vs. {{ team_orange_name }} (ID: {{ id }})
                                    </template>
                                    <template #option="{ team_blue_name, team_orange_name, id }">
                                        {{ team_blue_name }} vs. {{ team_orange_name }} (ID: {{ id }})
                                    </template>
                                </v-select>

                                <b-btn variant="primary" block @click="createNewMatchGroup">
                                    {{ $t('matches.create_match_group.create') }}
                                </b-btn>
                            </template>
                        </CustomCard>
                    </b-col>
                </b-row>

                <!-- Edit match group -->
                <b-row v-if="matchGroup">
                    <b-col>
                        <CustomCard color="primary" outline divider :title="$t('matches.create_match_group.edit')">
                            <template #card-body>

                                <label>{{ $t('generic.name') }}</label>

                                <b-form-input class="mb-2" v-model="editMatchGroupName"
                                              :placeholder="$t('matches.create_match_group.edit_name')"/>

                                <label>{{ $t('matches.create_match_group.select_match') }}:</label>

                                <v-select class="w-100 mb-4" v-model="editMatchGroupMatches" :options="matches"
                                          :multiple="true"
                                          :placeholder="$t('matches.create_match_group.select_match')">
                                    <template #selected-option="{ team_blue_name, team_orange_name, id }">
                                        {{ team_blue_name }} vs. {{ team_orange_name }} (ID: {{ id }})
                                    </template>
                                    <template #option="{ team_blue_name, team_orange_name, id }">
                                        {{ team_blue_name }} vs. {{ team_orange_name }} (ID: {{ id }})
                                    </template>
                                </v-select>

                                <b-btn variant="primary" block @click="editMatchGroup">
                                    {{ $t('matches.create_match_group.edit') }}
                                </b-btn>
                            </template>
                        </CustomCard>
                    </b-col>
                </b-row>

            </b-col>

            <!-- Current match group -->
            <b-col>

                <CustomCard color="secondary" outline divider :title="$t('matches.create_match_group.current')">
                    <template #card-body>

                        <label v-if="!matchGroup">
                            <i>{{ $t('matches.create_match_group.no_match_group') }}</i>
                        </label>

                        <label v-else>
                            {{ $t('matches.create_match_group.select') }}:
                        </label>

                        <v-select class="w-100 mb-2" v-model="matchGroup" :options="userMatchGroups"
                                  label="name"
                                  :placeholder="$t('matches.create_match_group.select')"/>

                        <b-btn class="mb-2" variant="success" block @click="setMatchGroupToOverlay">
                            <font-awesome-icon icon="share-square"/>
                            {{ $t('matches.create_match_group.set_to_overlay') }}
                        </b-btn>

                        <hr class="divider">

                        <b-table-simple table-variant="dark" striped small responsive>

                            <b-tr>
                                <b-th class="text-bold">Name</b-th>
                                <b-td class="text-right">{{ matchGroup.name }}</b-td>
                            </b-tr>

                            <b-tr>
                                <b-th class="text-bold">Date</b-th>
                                <b-td class="text-right">
                                    {{ $d(new Date(matchGroup.date), 'short') }}
                                </b-td>
                            </b-tr>

                            <b-tr>
                                <b-th class="text-bold">Matches</b-th>
                                <b-td class="text-right">
                                    <template v-if="matchGroupData.length === 0">
                                        -
                                    </template>
                                    <template v-for="match in matchGroupData">
                                        {{ match.team_blue_name }} vs. {{ match.team_orange_name }} (ID: {{
                                            match.id
                                        }})<br>
                                    </template>
                                </b-td>
                            </b-tr>

                        </b-table-simple>

                    </template>
                </CustomCard>

            </b-col>

        </b-row>

    </div>
</template>

<script>
import {MatchData} from "~/mixins/axios/MatchData";
import {MatchGroupWebsocket} from "~/mixins/websocket/MatchGroupWebsocket";
import CustomCard from "~/components/CustomCard";

export default {
    name: "CreateMatchGroup",

    data() {
        return {
            userMatchGroups: [],
            matchGroupData: [],
            newMatchGroupName: null,
            newMatchGroupMatches: [],
            editMatchGroupName: null,
            editMatchGroupMatches: []
        }
    },

    head() {
        return {
            title: this.$t("navigation.create_match_group") + " - Caster Dashboard"
        }
    },

    computed: {
        userID() {
            return this.$auth.user.id
        },
    },

    watch: {
        matchGroup: {
            deep: true,
            async handler() {
                if (this.matchGroup) {
                    // Get match details for each match
                    this.matchGroupData = []
                    for (const matchID of this.matchGroup.matches) {
                        if (matchID !== this.matchID) {
                            await this.$axios.$get(`/api/match/${matchID}/`)
                                .then((data) => {
                                    this.matchGroupData.push(data);
                                })
                        }
                    }

                    // Set values for editing
                    this.editMatchGroupName = this.matchGroup.name
                    this.editMatchGroupMatches = this.matchGroupData
                }
            }
        },
    },

    methods: {
        createNewMatchGroup() {
            if (!this.newMatchGroupName) {
                this.$toast.error(this.$t('matches.create_match_group.toasts.no_name'))
                return
            }

            let date = new Date().toISOString().substring(0, 10)
            let matches = this.newMatchGroupMatches.map(m => m.id)

            this.$axios.$post("/api/match_groups/", {
                users: [this.userID],
                name: this.newMatchGroupName,
                date: date,
                matches: matches
            })
                .then((data) => {
                    this.$toast.success(this.$t('matches.create_match_group.toasts.created'), this.$t('generic.success'))
                    this.$fetch()
                })
                .catch((error) => {
                    console.log(error)
                    this.$toast.error(this.$t('matches.create_match_group.toasts.created_failed'), this.$t('generic.error'))
                })
        },
        editMatchGroup() {
            if (!this.editMatchGroupName) {
                this.$toast.error(this.$t('matches.create_match_group.toasts.no_name'))
                return
            }

            let date = new Date().toISOString().substring(0, 10)
            let matches = this.editMatchGroupMatches.map(m => m.id)

            this.$axios.$put(`/api/match_groups/${this.matchGroup.id}/`, {
                users: [this.userID],
                name: this.editMatchGroupName,
                date: date,
                matches: matches
            })
                .then((data) => {
                    this.$toast.success(this.$t('matches.create_match_group.toasts.edited'), this.$t('generic.success'))
                    this.$fetch()
                })
                .catch((error) => {
                    console.log(error)
                    this.$toast.error(this.$t('matches.create_match_group.toasts.edited_failed'), this.$t('generic.error'))
                })
        },
        setMatchGroupToOverlay() {
            this.$axios.$patch(`/api/overlay/match_data/${this.userID}/`, {
                "match_group": this.matchGroup.id
            })
                .then((data) => {
                    this.$toast.success(this.$t('matches.create_match_group.toasts.overlay_set'), this.$t('generic.success'))
                })
                .catch((error) => {
                    console.log(error)
                    this.$toast.error(this.$t('matches.create_match_group.toasts.overlay_set_failed'), this.$t('generic.error'))
                })
        }
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$t("navigation.create_match_group"))
        this.$store.commit("setPageTitleIcon", "plus")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Matches", this.$t('navigation.create_match_group')])
    },

    async fetch() {
        let [r1, r2, r3] =
            await Promise.all([
                this.getMatchData(),
                this.connectMatchGroupWebsocket(),
                await this.$axios.$get(`/api/match_groups/?user=${this.userID}`)
            ])

        this.userMatchGroups = r3

        // Sort matches by ID desc.
        this.matches.sort((a, b) => {
            return a.id > b.id ? -1 : 1
        })
    },

    mixins: [
        MatchData,
        MatchGroupWebsocket
    ],

    components: {
        "CustomCard": CustomCard
    }

}
</script>

<style scoped>

</style>
