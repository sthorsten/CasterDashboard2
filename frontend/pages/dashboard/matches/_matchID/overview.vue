<template>
    <div>

        <CustomCard color="primary" outline divider :title="$t('matches.overview.match_info')"
                    v-if="this.$fetchState.pending">
            <template #card-body>
                <b-skeleton-table/>
                <b-skeleton-table/>
            </template>
        </CustomCard>

        <b-row v-if="!this.$fetchState.pending">

            <!-- Match Details -->
            <b-col md="6">

                <CustomCard color="primary" outline divider :title="$t('matches.overview.match_info')">
                    <template #card-body>

                        <b-table-simple table-variant="dark" striped small responsive>

                            <b-tbody>
                                <b-tr class="bg-primary">
                                    <b-th colspan="2">{{ $t('matches.overview.base_info') }}</b-th>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">ID</b-th>
                                    <b-td class="text-right">{{ match.id }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $tc('generic.user', match.user.length) }}</b-th>
                                    <b-td class="text-right">{{ match.user_name.join(", ") }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('core.title') }}</b-th>
                                    <b-td class="text-right">{{ match.title }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('core.playday') }}</b-th>
                                    <b-td class="text-right">{{ match.subtitle }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('core.best_of') }}</b-th>
                                    <b-td class="text-right">{{ match.best_of }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('generic.state') }}</b-th>
                                    <b-td class="text-right">{{ match.state_name }}</b-td>
                                </b-tr>

                                <b-tr class="bg-primary">
                                    <b-th colspan="2">{{ $t('matches.overview.match_details') }}</b-th>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $tc('core.league') }}</b-th>
                                    <b-td class="text-right">{{ match.league_name }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $tc('core.season') }}</b-th>
                                    <b-td class="text-right">{{ match.season_name }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('core.team_blue') }}</b-th>
                                    <b-td class="text-right">{{ match.team_blue_name }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('core.team_orange') }}</b-th>
                                    <b-td class="text-right">{{ match.team_orange_name }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $tc('core.sponsor', match.sponsors.length) }}</b-th>
                                    <b-td v-if="match.sponsors.length > 0" class="text-right">
                                        {{ match.sponsors_name.join(", ") }}
                                    </b-td>
                                    <b-td v-else class="text-right">-</b-td>
                                </b-tr>

                                <b-tr class="bg-primary">
                                    <b-th colspan="2">{{ $t('matches.overview.match_results') }}</b-th>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('matches.overview.current_score') }}</b-th>
                                    <b-td class="text-right">{{ match.score_blue }} - {{ match.score_orange }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('matches.overview.win_team') }}</b-th>
                                    <b-td v-if="match.win_team_name" class="text-right">{{ match.win_team_name }}</b-td>
                                    <b-td v-else class="text-right">-</b-td>
                                </b-tr>

                            </b-tbody>

                        </b-table-simple>

                    </template>
                </CustomCard>

            </b-col>

            <!-- Match actions -->
            <b-col md="6">

                <CustomCard color="success" outline divider :title="$t('matches.overview.actions.title')">
                    <template #card-body>

                        <b-row>

                            <b-col cols="12" class="mb-2">
                                <b-btn variant="success" class="btn-block" @click="setMatchToOverlay(false)">
                                    <font-awesome-icon icon="share-square"/>
                                    {{ $t('matches.overview.actions.set_overlay') }}
                                </b-btn>
                            </b-col>

                            <b-col cols="12" class="mb-2">
                                <b-btn variant="success" class="btn-block" @click="setMatchToOverlay(true)">
                                    <font-awesome-icon icon="share-square"/>
                                    {{ $t('matches.overview.actions.set_overlay_next') }}
                                </b-btn>
                            </b-col>

                            <b-col cols="12">
                                <nuxt-link :to="`/dashboard/matches/${matchID}/maps`">
                                    <b-btn variant="success" class="btn-block">
                                        <font-awesome-icon icon="arrow-right"/>
                                        {{ $t('matches.overview.actions.continue') }}
                                    </b-btn>
                                </nuxt-link>
                            </b-col>

                        </b-row>

                        <hr class="divider">

                        <b-row>

                            <b-col cols="12" class="mb-2">
                                <nuxt-link :to="`/dashboard/matches/${matchID}/details`">
                                    <b-btn variant="secondary" class="btn-block">
                                        <font-awesome-icon icon="list-ul"/>
                                        {{ $t('matches.overview.actions.show_details') }}
                                    </b-btn>
                                </nuxt-link>
                            </b-col>

                            <b-col cols="12">
                                <b-btn variant="secondary" class="btn-block" @click="shareMatchModal = true">
                                    <font-awesome-icon icon="share-alt"/>
                                    {{ $t('matches.overview.actions.share') }}
                                </b-btn>
                            </b-col>

                        </b-row>

                        <hr class="divider">

                        <b-row>

                            <b-col cols="12" class="mb-2">
                                <b-btn variant="danger" class="btn-block" disabled>
                                    <font-awesome-icon icon="pen"/>
                                    {{ $t('matches.overview.actions.edit') }} <i>(coming soon)</i>
                                </b-btn>
                            </b-col>

                            <b-col cols="12">
                                <b-btn variant="danger" class="btn-block" disabled>
                                    <font-awesome-icon icon="trash"/>
                                    {{ $t('matches.overview.actions.delete') }} <i>(coming soon)</i>
                                </b-btn>
                            </b-col>

                        </b-row>

                    </template>
                </CustomCard>

            </b-col>

            <ShareMatchModal :show="shareMatchModal" @hide="shareMatchModal = false" :match="match"
                             @reload="$fetch(); shareMatchLoading = false"/>
        </b-row>

    </div>
</template>

<script>
import CustomCard from "~/components/CustomCard";
import ShareMatchModal from "~/components/modals/ShareMatchModal";
import {SingleMatch} from "~/mixins/axios/SingleMatch";

export default {
    name: "MatchOverview",
    layout: "match",

    data() {
        return {
            shareMatchModal: false,
        }
    },

    head() {
        return {
            title: this.$t("navigation.overview") + " - Caster Dashboard"
        }
    },

    computed: {
        matchID() {
            return this.$route.params.matchID
        }
    },

    methods: {
        setMatchToOverlay(next) {
            let data = {}
            if (next) {
                data = {
                    "user": this.$auth.user.id,
                    "next_match": this.matchID
                }
            } else {
                data = {
                    "user": this.$auth.user.id,
                    "current_match": this.matchID
                }
            }

            this.$axios.$put(`/api/overlay/match_data/${this.$auth.user.id}/`, data,)
                .then((data) => {
                    this.$toast.success(this.$t('matches.overview.toasts.overlay_success'))
                })
                .catch((error) => {
                    console.log(error)
                    this.$toast.error(this.$t('matches.overview.toasts.overlay_failed'))
                })
        },
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$t("navigation.overview"))
        this.$store.commit("setPageTitleIcon", "gamepad")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Matches", this.$route.params.matchID, "Overview"])
    },

    async fetch() {
        await this.getSingleMatch()
    },

    mixins: [
        SingleMatch
    ],

    components: {
        "CustomCard": CustomCard,
        ShareMatchModal
    }

}
</script>

<style scoped>

</style>
