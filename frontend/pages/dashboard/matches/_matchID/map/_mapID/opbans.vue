<template>
    <div>

        <b-row v-if="this.$fetchState.pending">
            <b-col cols="6">
                <CustomCard color="primary" outline>
                    <template #card-body>
                        <b-skeleton-table/>
                        <b-skeleton-table/>
                    </template>
                </CustomCard>
            </b-col>
            <b-col cols="6">
                <CustomCard color="danger" outline>
                    <template #card-body>
                        <b-skeleton-table/>
                        <b-skeleton-table/>
                    </template>
                </CustomCard>
            </b-col>
        </b-row>

        <b-row v-else>

            <b-col lg="6">

                <CustomCard color="primary" outline divider :title="$t('generic.settings')">
                    <template #card-body>

                        <b-row>

                            <!-- ATK Team -->
                            <b-col lg="6">

                                <label class="text-bold">{{ $t('matches.op_bans.atk_team') }}</label>

                                <b-row>

                                    <b-col xl="6">
                                        <template v-if="matchMap.atk_team && matchMap.atk_team === match.team_blue">
                                            <b-btn variant="primary" class="btn-block mb-2 mb-xl-0"
                                                   :disabled="bannedOperators.length > 0 || mapLocked">
                                                {{ match.team_blue_name }}
                                            </b-btn>
                                        </template>
                                        <template v-else>
                                            <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                   :disabled="bannedOperators.length > 0 || mapLocked"
                                                   @click="setATKTeam(match.team_blue)">
                                                {{ match.team_blue_name }}
                                                <b-spinner v-if="loadingSmall.atkTeam === match.team_blue"
                                                           variant="light" small/>
                                            </b-btn>
                                        </template>
                                    </b-col>

                                    <b-col xl="6">
                                        <template v-if="matchMap.atk_team === match.team_orange">
                                            <b-btn variant="primary" class="btn-block mb-2 mb-xl-0"
                                                   :disabled="bannedOperators.length > 0 || mapLocked">
                                                {{ match.team_orange_name }}
                                            </b-btn>
                                        </template>
                                        <template v-else>
                                            <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                   :disabled="bannedOperators.length > 0 || mapLocked"
                                                   @click="setATKTeam(match.team_orange)">
                                                {{ match.team_orange_name }}
                                                <b-spinner v-if="loadingSmall.atkTeam === match.team_orange"
                                                           variant="light" small/>
                                            </b-btn>
                                        </template>
                                    </b-col>

                                </b-row>

                            </b-col>

                            <!-- OT ATK Team -->
                            <b-col lg="6" class="mt-2 mt-xl-0">

                                <label class="text-bold">{{ $t('matches.op_bans.ot_atk_team') }}</label>

                                <b-row>

                                    <b-col xl="6">

                                        <template v-if="matchMap.ot_atk_team === match.team_blue">
                                            <b-btn variant="primary" class="btn-block mb-2 mb-xl-0"
                                                   :disabled="mapLocked">
                                                {{ match.team_blue_name }}
                                            </b-btn>
                                        </template>
                                        <template v-else>
                                            <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                   :disabled="mapLocked"
                                                   @click="setOTATKTeam(match.team_blue)">
                                                {{ match.team_blue_name }}
                                                <b-spinner v-if="loadingSmall.otAtkTeam === match.team_blue"
                                                           variant="light" small/>
                                            </b-btn>
                                        </template>

                                    </b-col>

                                    <b-col xl="6">

                                        <template v-if="matchMap.ot_atk_team === match.team_orange">
                                            <b-btn variant="primary" class="btn-block mb-2 mb-xl-0"
                                                   :disabled="mapLocked">
                                                {{ match.team_orange_name }}
                                            </b-btn>
                                        </template>
                                        <template v-else>
                                            <b-btn variant="outline-primary" class="btn-block mb-2 mb-xl-0"
                                                   :disabled="mapLocked"
                                                   @click="setOTATKTeam(match.team_orange)">
                                                {{ match.team_orange_name }}
                                                <b-spinner v-if="loadingSmall.otAtkTeam === match.team_orange"
                                                           variant="light" small/>
                                            </b-btn>
                                        </template>

                                    </b-col>
                                </b-row>

                            </b-col>

                        </b-row>

                        <hr class="divider">

                        <!-- Swap teams -->
                        <b-row>

                            <b-col cols="12">
                                <label>{{ $t('matches.op_bans.swap_teams') }}?</label>
                            </b-col>

                            <b-col cols="4" md="3" xl="2">
                                <span>{{ $t('core.team_blue') }}</span><br>
                                <span class="font-italic">{{ match.team_blue_name }}</span>
                            </b-col>

                            <b-col cols="4" md="6" xl="8">
                                <b-btn variant="primary" class="btn-block h-100"
                                       :disabled="bannedOperators.length > 0 || mapLocked"
                                       @click="swapTeams">
                                    <i class="fa fas fa-long-arrow-alt-left"></i>
                                    {{ $t('matches.op_bans.swap_teams') }}
                                    <i class="fa fas fa-long-arrow-alt-right"></i>
                                </b-btn>
                            </b-col>

                            <b-col cols="4" md="3" xl="2" class="text-right">
                                <span>{{ $t('core.team_orange') }}</span><br>
                                <span class="font-italic">{{ match.team_orange_name }}</span>
                            </b-col>

                        </b-row>

                        <hr class="divider">

                        <!-- Current operator bans -->
                        <b-row align-v="center">

                            <b-col cols="12">
                                <label>{{ $t('matches.op_bans.current_op_bans') }}</label>
                            </b-col>

                            <!-- Banned Operators -->
                            <b-col v-for="(n, index) in 4" :key="index" cols="3" class="text-center">
                                <template v-if="bannedOperators.length > index">
                                    <img :src="require(`@/assets/img/operators/${bannedOperators[index].operator}.svg`)"
                                         style="height: 50px; width: 50px;"><br>
                                    <span>{{ bannedOperators[index].operator_name }}</span><br>
                                    <span class="font-italic">{{ bannedOperators[index].team_name }}</span>
                                </template>

                                <template v-else>
                                    <span>-</span><br>
                                    <span class="font-italic">{{ $t('matches.op_bans.not_selected') }}</span>
                                </template>
                            </b-col>

                        </b-row>

                        <hr class="divider">

                        <!-- Buttons -->
                        <b-row>

                            <b-col lg="6">
                                <b-btn variant="danger" class="btn-block"
                                       :disabled="bannedOperators.length === 0 || mapLocked"
                                       @click="removeLastOperatorBan">
                                    <font-awesome-icon icon="trash"/>
                                    {{ $t('matches.op_bans.remove_last_op_ban') }}
                                    <b-spinner v-if="loadingSmall === 'remove-last-opban'" variant="light" small/>
                                </b-btn>
                            </b-col>


                            <b-col lg="6" class="mt-2 mt-lg-0">
                                <b-btn variant="danger" class="btn-block"
                                       :disabled="bannedOperators.length === 0 || mapLocked"
                                       @click="removeAllOperatorsBans">
                                    <font-awesome-icon icon="trash"/>
                                    {{ $t('matches.op_bans.remove_all_op_bans') }}
                                    <b-spinner v-if="loadingSmall === 'remove-all-opBans'" variant="light" small/>
                                </b-btn>
                            </b-col>

                        </b-row>

                        <b-row class="mt-2">

                            <b-col>
                                <nuxt-link to="rounds">
                                    <b-btn variant="primary" class="btn-block">
                                        <font-awesome-icon icon="arrow-right"/>
                                        {{ $t('matches.op_bans.continue') }}
                                    </b-btn>
                                </nuxt-link>
                            </b-col>

                        </b-row>

                    </template>
                </CustomCard>
            </b-col>

            <b-col lg="6">

                <CustomCard color="primary" outline divider :title="$t('matches.op_bans.ban_operators')">
                    <template #card-body>

                        <b-row>

                            <!-- ATK Ops -->
                            <b-col md="6" class="text-center">

                                <label>{{ $t('matches.op_bans.atk_ops') }}</label><br>

                                <b-row class="mt-2">

                                    <b-col cols="6" v-for="op in atkOps" :key="op.id">
                                        <template v-if="isOperatorBanned(op.id)">
                                            <b-btn variant="danger" class="btn-block mb-2 text-left" disabled>
                                                <img :src="require(`@/assets/img/operators/${op.id}.svg`)"
                                                     style="height: 25px; width: 25px;">
                                                {{ op.name }}
                                            </b-btn>
                                        </template>
                                        <template v-else>
                                            <b-btn variant="secondary" class="btn-block mb-2 text-left"
                                                   :disabled="atkOpsBanned || !matchMap.atk_team || mapLocked"
                                                   @click="banOperator(op.id)">
                                                <img :src="require(`@/assets/img/operators/${op.id}.svg`)"
                                                     style="height: 25px; width: 25px;">
                                                {{ op.name }}
                                                <b-spinner v-if="loadingSmall === 'ban-' + op.id" variant="light"
                                                           small/>
                                            </b-btn>
                                        </template>
                                    </b-col>

                                </b-row>

                            </b-col>

                            <!-- DEF Ops -->
                            <b-col md="6" class="text-center">

                                <label>{{ $t('matches.op_bans.def_ops') }}</label><br>

                                <b-row class="mt-2">
                                    <b-col cols="6" v-for="op in defOps" :key="op.id">
                                        <template v-if="isOperatorBanned(op.id)">
                                            <b-btn variant="danger" class="btn-block mb-2 text-left" disabled>
                                                <img :src="require(`@/assets/img/operators/${op.id}.svg`)"
                                                     style="height: 25px; width: 25px;">
                                                {{ op.name }}
                                            </b-btn>
                                        </template>
                                        <template v-else>
                                            <b-btn variant="secondary" class="btn-block mb-2 text-left"
                                                   :disabled="allOperatorsBanned || !atkOpsBanned || !matchMap.atk_team || mapLocked"
                                                   @click="banOperator(op.id)">
                                                <img :src="require(`@/assets/img/operators/${op.id}.svg`)"
                                                     style="height: 25px; width: 25px;">
                                                {{ op.name }}
                                                <b-spinner v-if="loadingSmall === 'ban-' + op.id" variant="light"
                                                           small/>
                                            </b-btn>
                                        </template>
                                    </b-col>

                                </b-row>

                            </b-col>

                        </b-row>

                    </template>
                </CustomCard>

            </b-col>

        </b-row>

    </div>
</template>

<script>
import CustomCard from "~/components/CustomCard";
import {SingleMatch} from "~/mixins/axios/SingleMatch";
import {SingleMatchMap} from "~/mixins/axios/SingleMatchMap";
import {Operators} from "~/mixins/axios/Operators";
import {WebsocketStatus} from "~/helpers/WebsocketStatus";
import {MatchMapSingleWebsocket} from "~/mixins/websocket/MatchMapSingleWebsocket";
import {OperatorBansWebsocket} from "~/mixins/websocket/OperatorBansWebsocket";
import match from "../../../../../../layouts/match";

export default {
    name: "OperatorBans",
    layout: "match",

    data() {
        return {
            WebsocketStatus: WebsocketStatus,
            mapLocked: false,
            loadingSmall: {},
        }
    },

    head() {
        return {
            title: this.$t("navigation.op_bans") + " - Caster Dashboard"
        }
    },

    computed: {
        matchID() {
            return this.$route.params.matchID
        },
        mapID() {
            return this.$route.params.mapID
        },
        atkOpsBanned() {
            return this.bannedOperators.length >= 2
        },
        allOperatorsBanned() {
            return this.bannedOperators.length >= 4;
        }

    },

    methods: {
        isOperatorBanned(id) {
            for (const o of this.bannedOperators) {
                if (o.operator === id) return true
            }
            return false
        },
        setATKTeam(team) {
            this.loadingSmall = {
                atkTeam: team
            }

            this.$axios.$patch(`/api/matches/maps/${this.matchMap.id}/`, {
                atk_team: team
            }).then(() => {
                this.$toast.success(this.$t("matches.op_bans.toasts.atk_team_set"))
            }).catch(() => {
                this.$toast.error(this.$t("matches.op_bans.toasts.atk_team_set_failed"))
            }).then(() => this.loadingSmall = {})
        },
        setOTATKTeam(team) {
            this.loadingSmall = {
                otAtkTeam: team
            }

            this.$axios.$patch(`/api/matches/maps/${this.matchMap.id}/`, {
                ot_atk_team: team
            }).then(() => {
                this.$toast.success(this.$t("matches.op_bans.toasts.ot_atk_team_set"))
            }).catch(() => {
                this.$toast.error(this.$t("matches.op_bans.toasts.ot_atk_team_set_failed"))
            }).then(() => this.loadingSmall = {})
        },
        swapTeams() {
            let data = {
                team_blue: this.match.team_orange,
                team_orange: this.match.team_blue
            }

            this.$axios.$patch(`/api/match/${this.match.id}/`, data
            ).then(() => {
                this.$toast.success(this.$t("matches.op_bans.toasts.teams_swapped"))
            }).catch(() => {
                this.$toast.error(this.$t("matches.op_bans.toasts.teams_swapped_failed"))
            }).then(() => {
                this.getSingleMatch()
                this.loadingSmall = {}
            })
        },
        banOperator(id) {
            this.loadingSmall = {
                ban: id
            }

            let nextBan = this.bannedOperators.length + 1
            let nextBanTeam = null

            if (this.matchMap.atk_team === this.match.team_blue) {
                if (nextBan === 2 || nextBan === 3) {
                    nextBanTeam = this.match.team_blue
                } else {
                    nextBanTeam = this.match.team_orange
                }
            } else {
                if (nextBan === 1 || nextBan === 4) {
                    nextBanTeam = this.match.team_blue
                } else {
                    nextBanTeam = this.match.team_orange
                }
            }

            let data = {
                match: this.match.id,
                map: this.matchMap.map,
                operator: id,
                order: nextBan,
                team: nextBanTeam
            }

            console.log(data)

            this.$axios.$post("/api/matches/opbans/", data
            ).then(() => {
                this.$toast.success(this.$t("matches.op_bans.toasts.opban_added"))
            }).catch(() => {
                this.$toast.error(this.$t("matches.op_bans.toasts.opban_added_failed"))
            }).then(() => this.loadingSmall = {})
        },
        removeLastOperatorBan() {
            this.loadingSmall = {
                removeLast: true
            }

            let lastBanID = this.bannedOperators[this.bannedOperators.length - 1].id

            this.$axios.$delete(`/api/matches/opbans/${lastBanID}/`
            ).then(() => {
                this.$toast.success(this.$t("matches.op_bans.toasts.opban_removed"))
            }).catch(() => {
                this.$toast.error(this.$t("matches.op_bans.toasts.opban_removed_failed"))
            }).then(() => this.loadingSmall = {})
        },
        async removeAllOperatorsBans() {
            this.loadingSmall = {
                removeAll: true
            }

            let counter = this.bannedOperators.length

            await this.bannedOperators.forEach(o => {
                this.$axios.$delete(`/api/matches/opbans/${o.id}/`
                ).then(() => counter--
                ).catch(() => {
                    this.$toast.error(this.$t("matches.op_bans.toasts.all_opbans_removed_failed"))
                })
            })

            this.loadingSmall = {}
            this.$toast.success(this.$t("matches.op_bans.toasts.all_opbans_removed"))
        }
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$t("navigation.op_bans"))
        this.$store.commit("setPageTitleIcon", "users-slash")
        this.$store.commit("setBreadcrumbPath",
            ["Dashboard", "Matches", this.$route.params.matchID, "Map " + this.$route.params.mapID, "OpBans"]
        )
    },

    async fetch() {
        await this.getSingleMatch()

        await this.getSingleMatchMap()
        // Set Map to Breadcrumbs
        this.$store.commit("setBreadcrumbPath",
            ["Dashboard", "Matches", this.$route.params.matchID, `${this.matchMap.map_name} (Map ${this.matchMap.play_order}/${this.match.best_of})`, "OpBans"]
        )

        await this.getOperators()

        await this.connectMatchMapSingleWebsocket()
        await this.connectOperatorBansWebsocket()
    },

    mixins: [
        SingleMatch,
        SingleMatchMap,
        Operators,
        MatchMapSingleWebsocket,
        OperatorBansWebsocket
    ],

    components: {
        "CustomCard": CustomCard
    }

}
</script>

<style scoped>

</style>
