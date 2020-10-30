<template>
    <BaseLayout :title="$t('navigation.create')" title_icon="fas fa-plus" :bc_path="bc_path" class="text-white">

        <b-row>

            <!-- Create match form -->
            <b-col md="8">

                <!-- Show content once team data is loaded -->
                <template v-if="loading_status === 'loaded'">
                    <CustomCard color="primary" outline divider :title="$t('matches.create.create_match')">
                        <template #card-body>

                            <validation-observer ref="observer" v-slot="{ handleSubmit }">
                                <b-form @submit.stop.prevent="handleSubmit(onSubmit)" novalidate>

                                    <!-- First row - User / Share match -->
                                    <b-row>

                                        <b-col>
                                            <b-form-group class="mb-3" :label="$t('matches.create.share_match')" label-for="users"
                                                          aria-describedby="users-feedback">
                                                <b-input-group>
                                                    <multiselect id="users" v-model="users" :options="user_options" track_by="id" :multiple="true"
                                                                 label="username" :placeholder="$t('matches.create.share_match_text')"
                                                                 aria-describedby="users-feedback"/>
                                                </b-input-group>
                                            </b-form-group>
                                        </b-col>

                                    </b-row>

                                    <!-- First row -->
                                    <b-row>

                                        <!-- League -->
                                        <b-col lg="6">
                                            <validation-provider name="league" :rules="{ required: true }" v-slot="validationContext">
                                                <b-form-group class="mb-3" :label="$tc('core.league')" label-for="league"
                                                              aria-describedby="league-feedback">
                                                    <b-input-group>
                                                        <multiselect id="league" v-model="league" :options="league_options" track_by="id"
                                                                     label="league_name" :placeholder="$t('matches.create.league_select')"
                                                                     aria-describedby="league-feedback"/>
                                                        <b-form-invalid-feedback id="league-feedback" :state="getValidationState(validationContext)">
                                                            {{ $t('matches.create.league_select_text') }}
                                                        </b-form-invalid-feedback>
                                                    </b-input-group>
                                                </b-form-group>
                                            </validation-provider>
                                        </b-col>

                                        <!-- Season -->
                                        <b-col lg="6">
                                            <validation-provider name="season" :rules="{ required: true }" v-slot="validationContext">
                                                <b-form-group class="mb-3" :label="$tc('core.season')" label-for="season">
                                                    <b-input-group>
                                                        <multiselect id="season" v-model="season" :options="season_options"
                                                                     group-values="seasons" group-label="category"
                                                                     track_by="id" label="name" :placeholder="$t('matches.create.season_select')">
                                                            <template slot="singleLabel" slot-scope="props">
                                                    <span v-if="props.option.official_season">
                                                        {{ props.option.name }}
                                                    </span>
                                                                <span v-else>
                                                        {{ props.option.name }} ({{ props.option.league_name }})
                                                    </span>
                                                            </template>
                                                            <template slot="option" slot-scope="props">
                                                    <span v-if="props.option.$isLabel">
                                                        {{ props.option.$groupLabel }}
                                                    </span>
                                                                <span v-else-if="props.option.official_season">
                                                        {{ props.option.name }}
                                                    </span>
                                                                <span v-else>
                                                        {{ props.option.name }} ({{ props.option.league_name }})
                                                    </span>
                                                            </template>
                                                        </multiselect>
                                                        <b-form-invalid-feedback id="season-feedback" :state="getValidationState(validationContext)">
                                                            {{ $t('matches.create.season_select_text') }}
                                                        </b-form-invalid-feedback>
                                                    </b-input-group>
                                                </b-form-group>
                                            </validation-provider>
                                        </b-col>
                                    </b-row>

                                    <!-- Second row - Best Of -->
                                    <validation-provider name="best_of" :rules="{ required: true }" v-slot="validationContext">
                                        <b-form-group class="mb-3" :label="$t('core.best_of')" label-for="bestof">
                                            <b-radio-group id="best_of" v-model="best_of" :options="best_of_options"
                                                           :state="getValidationState(validationContext)">
                                                <b-form-invalid-feedback id="best_of-feedback" :state="getValidationState(validationContext)">
                                                    {{ $t('matches.create.best_of_text') }}
                                                </b-form-invalid-feedback>
                                            </b-radio-group>
                                        </b-form-group>
                                    </validation-provider>

                                    <hr class="divider">

                                    <!-- Third row -->
                                    <b-row>

                                        <!-- Match Title -->
                                        <b-col lg="6">
                                            <validation-provider name="match_title" :rules="{ required: true }" v-slot="validationContext">
                                                <b-form-group class="mb-3" :label="$t('matches.create.match_title')" label-for="match_title">
                                                    <b-input-group>
                                                        <b-form-input id="match_title" v-model="match_title"
                                                                      :placeholder="$t('matches.create.match_title_placeholder')"
                                                                      :state="getValidationState(validationContext)">
                                                        </b-form-input>
                                                        <b-form-invalid-feedback id="match_title-feedback">
                                                            {{ $t('matches.create.match_title_text') }}
                                                        </b-form-invalid-feedback>
                                                    </b-input-group>
                                                </b-form-group>
                                            </validation-provider>
                                        </b-col>

                                        <!-- Match Subtitle / Playday -->
                                        <b-col lg="6">
                                            <b-form-group class="mb-3" :label="$t('matches.create.playday')" label-for="match-playday-name">
                                                <b-input-group>
                                                    <b-form-input id="match-title-name" v-model="match_playday"
                                                                  :placeholder="$t('matches.create.playday_placeholder')"/>
                                                </b-input-group>
                                            </b-form-group>
                                        </b-col>

                                    </b-row>

                                    <!-- Fourth row -->
                                    <b-row>

                                        <!-- Team Blue -->
                                        <b-col lg="6">
                                            <validation-provider name="team_blue" :rules="{ required: true }" v-slot="validationContext">
                                                <b-form-group class="mb-3" :label="$t('core.team_blue')" label-for="team-blue-name">
                                                    <b-input-group>
                                                        <multiselect id="team_blue" v-model="team_blue" :options="team_options" track_by="id"
                                                                     label="name" :placeholder="$t('matches.create.team_select')"/>
                                                        <b-form-invalid-feedback id="team_blue-feedback"
                                                                                 :state="getValidationState(validationContext)">
                                                            {{ $t('matches.create.team_select') }}
                                                        </b-form-invalid-feedback>
                                                    </b-input-group>
                                                </b-form-group>
                                            </validation-provider>
                                        </b-col>

                                        <!-- Team Orange -->
                                        <b-col lg="6">
                                            <validation-provider name="team_orange" :rules="{ required: true }" v-slot="validationContext">
                                                <b-form-group class="mb-3" :label="$t('core.team_orange')" label-for="team-orange-name">
                                                    <b-input-group>
                                                        <multiselect id="team_orange" v-model="team_orange" :options="team_options" track_by="id"
                                                                     label="name" :placeholder="$t('matches.create.team_select')"/>
                                                        <b-form-invalid-feedback id="team_orange-feedback"
                                                                                 :state="getValidationState(validationContext)">
                                                            {{ $t('matches.create.team_select') }}
                                                        </b-form-invalid-feedback>
                                                    </b-input-group>
                                                </b-form-group>
                                            </validation-provider>
                                        </b-col>

                                    </b-row>

                                    <!-- Fifth row - Sponsors -->
                                    <b-form-group class="mb-3" :label="$t('matches.create.sponsors')" label-for="sponsors">
                                        <b-input-group>
                                            <multiselect id="sponsors" v-model="sponsors" :options="sponsor_options" track_by="id"
                                                         :multiple="true"
                                                         label="name" :placeholder="$t('matches.create.sponsors_select')"/>
                                        </b-input-group>
                                    </b-form-group>

                                    <hr class="divider mt-4 mb-3">

                                    <!-- Submit button -->
                                    <b-row class="text-center">
                                        <b-col>
                                            <b-btn type="submit" variant="success">
                                                {{ $t('matches.create.create_match_btn') }}
                                            </b-btn>
                                        </b-col>
                                    </b-row>

                                </b-form>
                            </validation-observer>

                        </template>
                    </CustomCard>

                </template>

                <!-- Loading overlay -->
                <template v-if="loading_status === 'loading'">
                    <CustomCard color="secondary" outline divider title="Loading">
                        <template #card-body>
                            <StatusOverlay type="loading" :text="$t('generic.loading')"></StatusOverlay>
                        </template>
                    </CustomCard>
                </template>

                <!-- Error overlay -->
                <template v-if="loading_status === 'error'">
                    <CustomCard color="danger" outline divider :title="$t('generic.error')">
                        <template #card-body>
                            <StatusOverlay type="icon" icon="fas fa-exclamation-triangle fa-2x"
                                           :text="$t('generic.loading_failed')"></StatusOverlay>
                        </template>
                    </CustomCard>
                </template>

            </b-col>

            <!-- Quick actions -->
            <b-col md="4">

                <b-row>

                    <b-col cols="12" order="2" order-md="1">
                        <CustomCard color="secondary" outline divider icon="fa fas fa-info-circle" :title="$t('generic.quick_info')">
                            <template #card-body>
                                <ul class="font-italic">
                                    <li>{{ $t('matches.create.info.line1') }}</li>
                                    <li>{{ $t('matches.create.info.line2') }}</li>
                                    <li>{{ $t('matches.create.info.line3') }}</li>
                                </ul>
                            </template>
                        </CustomCard>
                    </b-col>

                    <b-col cols="12" order="1" order-md="2">
                        <CustomCard color="success" outline divider :title="$t('generic.quick actions')">
                            <template #card-body>
                                <b-row>
                                    <b-btn variant="success" class="btn-block" @click="showNewTeamModal = true">
                                        {{ $t('data.teams.add_new_team_btn') }}
                                    </b-btn>
                                    <router-link :to="{name: 'Match Overview', params: {id: last_match}}" class="btn-block">
                                        <b-btn variant="success" class="btn-block">
                                            {{ $t('matches.create.last_match_btn') }}
                                        </b-btn>
                                    </router-link>
                                    <b-btn variant="secondary" class="btn-block" @click="resetForm">
                                        {{ $t('matches.create.reset_btn') }}
                                    </b-btn>
                                </b-row>
                            </template>
                        </CustomCard>
                    </b-col>

                </b-row>
            </b-col>

        </b-row>

        <NewTeamModal :show="showNewTeamModal" @hide="showNewTeamModal = false" @loading="loading_status = 'loading'" @reload="this.getTeams"/>

    </BaseLayout>
</template>

<script>
import axios from "axios";

import BaseLayout from "@/components/layout/BaseLayout";
import CustomCard from "@/components/elements/CustomCard";
import NewTeamModal from "@/components/subcomponents/NewTeamModal";
import StatusOverlay from "@/components/elements/StatusOverlay";

function compareTeams(a, b) {
    if (a.name.toLowerCase() > b.name.toLowerCase()) return 1;
    if (a.name.toLowerCase() < b.name.toLowerCase()) return -1;
    return 0;
}

export default {
    name: "MatchCreate",
    data() {
        return {
            users: [],
            user_options: [],

            league: null,
            league_options: [],

            season: null,
            season_options: [
                {
                    category: this.$t('matches.create.season_options.official'),
                    seasons: []
                },
                {
                    category: this.$t('matches.create.season_options.league'),
                    seasons: []
                }
            ],

            best_of: null,
            best_of_options: [
                {text: "Best Of 1", value: 1},
                {text: "Best Of 2", value: 2},
                {text: "Best Of 3", value: 3},
                {text: "Best Of 5", value: 5}
            ],

            match_title: "",
            match_playday: "",

            team_blue: null,
            team_orange: null,
            team_options: [],

            sponsors: [],
            sponsor_options: [],

            last_match: 0,

            loading_status: 'loading',
            showNewTeamModal: false,
            users_loaded: false,
            leagues_loaded: false,
            seasons_loaded: false,
            teams_loaded: false,
            sponsors_loaded: false,
            last_match_loaded: false,

            bc_path: ['Dashboard', 'Matches', 'Create']
        }
    },
    computed: {
        load_complete() {
            return this.users_loaded && this.leagues_loaded && this.seasons_loaded && this.teams_loaded && this.sponsors_loaded && this.last_match_loaded
        }
    },
    watch: {
        load_complete: function (newState) {
            if (newState) this.loading_status = 'loaded'
        }
    },
    methods: {
        getUsers() {
            axios.get(this.$store.state.backendURL + "/api/user/", {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.user_options = response.data.filter(user => user.id !== this.$store.state.user.id)
                this.users_loaded = true
            })
        },
        getLeagues() {
            axios.get(this.$store.state.backendURL + "/api/data/league_group/?user=" + this.$store.state.user.id, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.league_options = response.data
                this.leagues_loaded = true
                this.getSeasons() // Must be synchronous after getting all leagues
            }).catch((error) => {
                console.log(error.response)
                this.loading_status = 'error'
            })
        },
        getSeasons() {
            // Get official season
            axios.get(this.$store.state.backendURL + "/api/data/season/?official_season=true", {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.season_options[0].seasons = response.data
            }).catch((error) => {
                console.log(error.response)
                this.loading_status = 'error'
            })

            // Get user leagues
            let user_league_ids = []
            for (let i = 0; i < this.league_options.length; i++) {
                user_league_ids.push(this.league_options[i].league)
            }
            console.log(user_league_ids)

            // Get restricted leagues the user has access to
            axios.get(this.$store.state.backendURL + "/api/data/season/?league__in=" + user_league_ids.toString(), {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.season_options[1].seasons = response.data
                this.seasons_loaded = true
            }).catch((error) => {
                console.log(error.response)
                this.loading_status = 'error'
            })
        },
        getTeams() {
            this.teams_loaded = false
            axios.get(this.$store.state.backendURL + "/api/data/team/", {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.team_options = response.data.sort(compareTeams)
                this.teams_loaded = true
            }).catch((error) => {
                console.log(error.response)
                this.loading_status = 'error'
            })
        },
        getSponsors() {
            axios.get(this.$store.state.backendURL + "/api/data/sponsor/", {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.sponsor_options = response.data
                this.sponsors_loaded = true
            }).catch((error) => {
                console.log(error.response)
                this.loading_status = 'error'
            })
        },
        getLastMatch() {
            axios.get(this.$store.state.backendURL + "/api/overlay/match_data/?user=" + this.$store.state.user.id, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response.data)
                this.last_match = response.data[0].current_match
                this.last_match_loaded = true
            }).catch((error) => {
                console.log(error.response)
                this.loading_status = 'error'
            })
        },
        resetForm() {
            this.league = null
            this.season = null
            this.best_of = null
            this.match_title = ""
            this.match_playday = ""
            this.team_blue = null
            this.team_orange = null
            this.sponsors = []
        },
        getValidationState({dirty, validated, valid = null}) {
            return dirty || validated ? valid : null;
        },
        onSubmit() {
            let sponsors = []
            this.sponsors.forEach((s) => {
                sponsors.push(s.id)
            })
            let users = []
            this.users.forEach((u) => {
                users.push(u.id)
            })
            users.push(this.$store.state.user.id)

            let formData = {
                "user": users,
                "league": this.league.id,
                "season": this.season.id,
                "best_of": this.best_of,
                "title": this.match_title,
                "subtitle": this.match_playday,
                "team_blue": this.team_blue.id,
                "team_orange": this.team_orange.id,
                "sponsors": sponsors
            }

            console.log(formData)

            axios.post(this.$store.state.backendURL + "/api/match/", formData, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                }
            }).then((response) => {
                console.log(response)
                this.$toast.success(this.$t('matches.create.match_created'))
                this.$router.push({name: "Match Overview", params: {id: response.data.id}})
            }).catch((error) => {
                console.log(error.response)
                this.$toast.error(this.$t('matches.create.match_create_failed'), this.$t('generic.error'))
            })

        }
    },
    created() {
        this.getUsers()
        this.getLeagues()
        this.getTeams()
        this.getSponsors()
        this.getLastMatch()
    },
    components: {NewTeamModal, BaseLayout, CustomCard, StatusOverlay}
}
</script>

<style scoped>

</style>