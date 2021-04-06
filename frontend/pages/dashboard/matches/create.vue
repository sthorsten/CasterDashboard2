<template>
    <div>

        <!-- Skeleton on loading -->
        <b-row v-if="this.$fetchState.pending">

            <b-col>
                <CustomCard color="primary" outline divider :title="$t('matches.create.create_match')">
                    <template #card-body>

                        <div v-for="n in 5">
                            <b-skeleton class="mb-3"></b-skeleton>
                            <b-skeleton type="input" class="w-100"></b-skeleton>
                            <br>
                        </div>

                    </template>
                </CustomCard>
            </b-col>
        </b-row>

        <b-overlay :show="newTeamLoading" variant="dark">
            <b-row v-if="!this.$fetchState.pending">

                <!-- Create match form -->
                <b-col md="8">

                    <CustomCard color="primary" outline divider :title="$t('matches.create.create_match')">
                        <template #card-body>

                            <b-form novalidate @submit.prevent="onSubmit">

                                <!-- 1st row - User / Share match -->
                                <b-row>

                                    <b-col>
                                        <b-form-group class="mb-3">
                                            <template #label>
                                                <font-awesome-icon icon="share-alt"/>
                                                {{ $t('matches.create.share_match') }}
                                            </template>

                                            <b-input-group>
                                                <v-select class="w-100" v-model="selectedUsers" multiple
                                                          :options="users" label="username"
                                                          :placeholder="$t('matches.create.share_match_text')"/>
                                            </b-input-group>
                                        </b-form-group>
                                    </b-col>

                                </b-row>

                                <!-- 2nd row - League / Season -->
                                <b-row>

                                    <!-- League -->
                                    <b-col lg="6">
                                        <b-form-group class="mb-3">
                                            <template #label>
                                                <font-awesome-icon icon="trophy"/>
                                                {{ $tc('core.league') }}
                                            </template>

                                            <b-input-group>
                                                <v-select class="w-100" v-model="selectedLeague" :options="leagues"
                                                          label="name"
                                                          :placeholder="$t('matches.create.league_select')"/>
                                                <b-form-invalid-feedback :state="!$v.selectedLeague.$error">
                                                    {{ $t('matches.create.league_select_text') }}
                                                </b-form-invalid-feedback>
                                            </b-input-group>
                                        </b-form-group>
                                    </b-col>

                                    <!-- Season -->
                                    <b-col lg="6">
                                        <b-form-group class="mb-3">
                                            <template #label>
                                                <font-awesome-icon icon="calendar-alt"/>
                                                {{ $tc('core.season') }}
                                            </template>

                                            <b-input-group>
                                                <v-select class="w-100" v-model="selectedSeason" :options="seasons"
                                                          label="label"
                                                          :placeholder="$t('matches.create.season_select')"/>
                                                <b-form-invalid-feedback :state="!$v.selectedSeason.$error">
                                                    {{ $t('matches.create.season_select_text') }}
                                                </b-form-invalid-feedback>
                                            </b-input-group>
                                        </b-form-group>
                                    </b-col>

                                </b-row>

                                <!-- 3rd row - Best Of -->
                                <b-row>
                                    <b-col>

                                        <b-form-group class="mb-3">
                                            <template #label>
                                                <font-awesome-icon icon="dot-circle"/>
                                                {{ $t('core.best_of') }}
                                            </template>

                                            <b-radio-group v-model="selectedBestOf" :options="bestOfOptions">
                                                <b-form-invalid-feedback :state="!$v.selectedBestOf.$error">
                                                    {{ $t('matches.create.best_of_text') }}
                                                </b-form-invalid-feedback>
                                            </b-radio-group>
                                        </b-form-group>

                                    </b-col>
                                </b-row>

                                <!-- 4th row - Title / Subtitle -->
                                <b-row>

                                    <!-- Match title -->
                                    <b-col lg="6">
                                        <b-form-group class="mb-3">
                                            <template #label>
                                                <font-awesome-icon icon="heading"/>
                                                {{ $t('matches.create.match_title') }}
                                            </template>

                                            <b-input-group>
                                                <b-form-input v-model="matchTitle" :maxlength="22"
                                                              :placeholder="$t('matches.create.match_title_placeholder')"
                                                              :state="$v.matchTitle.$error ? false : null">
                                                </b-form-input>
                                                <b-form-invalid-feedback :state="!$v.matchTitle.$error">
                                                    {{ $t('matches.create.match_title_text') }}
                                                </b-form-invalid-feedback>
                                            </b-input-group>
                                        </b-form-group>
                                    </b-col>

                                    <!-- Match Playday / Subtitle -->
                                    <b-col lg="6">
                                        <b-form-group class="mb-3">
                                            <template #label>
                                                <font-awesome-icon icon="paragraph"/>
                                                {{ $t('matches.create.playday') }}
                                            </template>

                                            <b-input-group>
                                                <b-form-input v-model="matchPlayday" :maxlength="22"
                                                              :placeholder="$t('matches.create.playday_placeholder')">
                                                </b-form-input>
                                            </b-input-group>
                                        </b-form-group>
                                    </b-col>

                                </b-row>

                                <!-- 5th row - Teams -->
                                <b-row>

                                    <!-- Team Blue -->
                                    <b-col lg="6">
                                        <b-form-group class="mb-3">
                                            <template #label>
                                                <font-awesome-icon icon="users"/>
                                                {{ $tc('core.team_blue') }}
                                            </template>

                                            <b-input-group>
                                                <v-select class="w-100" v-model="teamBlue" :options="teams" label="name"
                                                          :placeholder="$t('matches.create.team_select')"/>
                                                <b-form-invalid-feedback :state="!$v.teamBlue.$error">
                                                    {{ $t('matches.create.team_select') }}
                                                </b-form-invalid-feedback>
                                            </b-input-group>
                                        </b-form-group>
                                    </b-col>

                                    <!-- Team Orange -->
                                    <b-col lg="6">
                                        <b-form-group class="mb-3">
                                            <template #label>
                                                <font-awesome-icon icon="users"/>
                                                {{ $tc('core.team_orange') }}
                                            </template>

                                            <b-input-group>
                                                <v-select class="w-100" v-model="teamOrange" :options="teams"
                                                          label="name"
                                                          :placeholder="$t('matches.create.team_select')"/>
                                                <b-form-invalid-feedback :state="!$v.teamOrange.$error">
                                                    {{ $t('matches.create.team_select') }}
                                                </b-form-invalid-feedback>
                                            </b-input-group>
                                        </b-form-group>
                                    </b-col>

                                </b-row>

                                <!-- 6th row - Sponsors -->
                                <b-row>
                                    <b-col>
                                        <b-form-group class="mb-3">
                                            <template #label>
                                                <font-awesome-icon icon="money-bill-alt"/>
                                                {{ $t('matches.create.sponsors') }}
                                            </template>

                                            <b-input-group sponsors_select>
                                                <v-select class="w-100" v-model="selectedSponsors" multiple
                                                          :options="sponsors" label="name"
                                                          :placeholder="$t('matches.create.sponsors_select')"/>
                                            </b-input-group>
                                        </b-form-group>
                                    </b-col>
                                </b-row>

                                <!-- 7th row - Submit Btn -->
                                <b-row>
                                    <b-col>
                                        <b-btn block variant="primary" type="submit">
                                            <font-awesome-icon icon="plus"/>
                                            {{ $t('matches.create.create_match_btn') }}
                                        </b-btn>
                                    </b-col>
                                </b-row>

                            </b-form>

                        </template>
                    </CustomCard>

                </b-col>

                <!-- Quick actions -->
                <b-col md="4">

                    <b-row>

                        <b-col cols="12">
                            <CustomCard color="success" outline divider :title="$t('generic.quick actions')">
                                <template #card-body>
                                    <b-row>
                                        <b-btn variant="success" class="btn-block" @click="showNewTeamModal = true">
                                            <font-awesome-icon icon="plus"/>
                                            {{ $t('data.teams.add_new_team_btn') }}
                                        </b-btn>

                                        <template v-if="currentUserMatch">
                                            <nuxt-link :to="`/dashboard/matches/${currentUserMatch.id}/overview`"
                                                       class="btn-block">
                                                <b-btn variant="success" block>
                                                    <font-awesome-icon icon="arrow-right"/>
                                                    {{ $t('matches.create.last_match_btn') }}
                                                </b-btn>
                                            </nuxt-link>
                                        </template>
                                        <template v-else>
                                            <b-btn variant="success" block disabled>
                                                <font-awesome-icon icon="arrow-right"/>
                                                {{ $t('matches.create.last_match_btn') }}
                                            </b-btn>
                                        </template>

                                        <b-btn variant="secondary" block @click="resetForm">
                                            <font-awesome-icon icon="trash"/>
                                            {{ $t('matches.create.reset_btn') }}
                                        </b-btn>
                                    </b-row>
                                </template>
                            </CustomCard>
                        </b-col>

                        <b-col cols="12">
                            <CustomCard color="secondary" outline divider icon="fa fas fa-info-circle"
                                        :title="$t('generic.quick_info')">
                                <template #card-body>
                                    <ul class="font-italic">
                                        <li>{{ $t('matches.create.info.line1') }}</li>
                                        <li>{{ $t('matches.create.info.line2') }}</li>
                                        <li>{{ $t('matches.create.info.line3') }}</li>
                                    </ul>
                                </template>
                            </CustomCard>
                        </b-col>

                    </b-row>

                </b-col>

            </b-row>

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
import required from "vuelidate/lib/validators/required";
import CustomCard from "~/components/CustomCard";
import NewTeamModal from "~/components/modals/NewTeamModal";
import {LeagueData} from "~/mixins/axios/LeagueData";
import {SeasonData} from "~/mixins/axios/SeasonData";
import {TeamData} from "~/mixins/axios/TeamData";
import {SponsorData} from "~/mixins/axios/SponsorData";
import {UserData} from "~/mixins/axios/UserData";
import {CurrentUserMatch} from "~/mixins/axios/CurrentUserMatch";

export default {
    name: "MatchesCreate",

    data() {
        return {
            selectedUsers: [],
            selectedLeague: null,
            selectedSeason: null,
            selectedBestOf: null,
            bestOfOptions: [
                {text: "Best Of 1", value: 1},
                {text: "Best Of 2", value: 2},
                {text: "Best Of 3", value: 3},
                {text: "Best Of 5", value: 5},
            ],
            matchTitle: null,
            matchPlayday: null,
            teamBlue: null,
            teamOrange: null,
            selectedSponsors: [],

            showNewTeamModal: false,
            newTeamLoading: false,
        }
    },

    head() {
        return {
            title: this.$t("navigation.create") + " - Caster Dashboard"
        }
    },

    validations: {
        selectedLeague: {required},
        selectedSeason: {required},
        selectedBestOf: {required},
        matchTitle: {required},
        teamBlue: {required},
        teamOrange: {required},
    },

    methods: {
        resetForm() {
            this.selectedUsers = []
            this.selectedLeague = null
            this.selectedSeason = null
            this.selectedBestOf = null
            this.matchTitle = null
            this.matchPlayday = null
            this.teamBlue = null
            this.teamOrange = null
            this.selectedSponsors = []
        },

        onSubmit() {
            this.$v.$touch()
            if (this.$v.$invalid) {
                this.$toast.error("Please fill out all required data!", "Error")
                return
            }

            let sponsorIDs = []
            this.selectedSponsors.forEach((s) => {
                sponsorIDs.push(s.id)
            })
            let userIDs = []
            this.selectedUsers.forEach((u) => {
                userIDs.push(u.id)
            })
            userIDs.push(this.$auth.user.id)

            let formData = {
                "user": userIDs,
                "league": this.selectedLeague.id,
                "season": this.selectedSeason.id,
                "best_of": this.selectedBestOf,
                "title": this.matchTitle,
                "subtitle": this.matchPlayday,
                "team_blue": this.teamBlue.id,
                "team_orange": this.teamOrange.id,
                "sponsors": sponsorIDs
            }

            this.$axios.$post("/api/match/", formData)
                .then((data) => {
                    this.$toast.success(this.$t('matches.create.match_created'))
                    this.$router.push(`/dashboard/matches/${data.id}/overview`)
                })
                .catch((error) => {
                    console.log(error)
                    this.$toast.error(this.$t('matches.create.match_create_failed'), this.$t('generic.error'))
                })
        }
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$t("navigation.create"))
        this.$store.commit("setPageTitleIcon", "plus")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Matches", "Create"])
    },

    async fetch() {

        await Promise.all([
            this.getUserData(),
            this.getLeagueData(),
            this.getSeasonData(),
            this.getTeamData(),
            this.getSponsorData(),
            this.getCurrentUserMatch()
        ])

        // Filter out current user
        this.users = this.users.filter(user => user.username !== this.$auth.user.userName)

        // Add labels
        this.seasons.forEach(season => {
            if (season.official_season) season.label = `${season.name} (Official Season)`
            else if (season.league) season.label = `${season.name} (${season.league_name})`
            else season.label = season.name
        })
    },

    mixins: [
        UserData,
        LeagueData,
        SeasonData,
        TeamData,
        SponsorData,
        CurrentUserMatch
    ],

    components: {
        "CustomCard": CustomCard,
        "NewTeamModal": NewTeamModal
    }
}
</script>
