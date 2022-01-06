<template>
  <div>
    <b-row v-if="this.$fetchState.pending">
      <b-col cols="6">
        <CustomCard color="primary" outline>
          <template #card-body>
            <b-skeleton-table />
            <b-skeleton-table />
          </template>
        </CustomCard>
      </b-col>
      <b-col cols="6">
        <CustomCard color="success" outline>
          <template #card-body>
            <b-skeleton-table />
            <b-skeleton-table />
          </template>
        </CustomCard>
      </b-col>
    </b-row>

    <b-row v-if="!$fetchState.pending">
      <!-- Round Controls -->
      <b-col lg="6" order="1">
        <CustomCard
          color="primary"
          outline
          divider
          :title="$t('matches.rounds.round_control')"
        >
          <template #card-body>
            <b-row>
              <!-- BombSpot -->
              <b-col lg="6">
                <label class="text-bold"
                  >{{ $t("matches.rounds.bomb_spot") }}:</label
                >

                <div v-for="bs in bombSpots" :key="bs.id">
                  <b-btn
                    v-if="selectedBombSpot === bs"
                    :disabled="mapLocked"
                    variant="primary"
                    class="btn-block mb-2"
                  >
                    <b-badge variant="light" pill class="mr-1">{{
                      bs.floor
                    }}</b-badge>
                    <span class="sl-only">{{ bs.name }}</span>
                  </b-btn>

                  <b-btn
                    v-else
                    :disabled="mapLocked"
                    @click="selectBombSpot(bs)"
                    variant="outline-primary"
                    class="btn-block mb-2"
                  >
                    <b-badge variant="primary" pill class="mr-1">{{
                      bs.floor
                    }}</b-badge>
                    <span class="sl-only">{{ bs.name }}</span>
                  </b-btn>
                </div>
              </b-col>

              <!-- Win Type -->
              <b-col lg="6">
                <label class="text-bold"
                  >{{ $t("matches.rounds.win_type") }}:</label
                >

                <div v-for="t in winTypes" :key="t.id">
                  <b-btn
                    v-if="selectedWinType === t"
                    :disabled="mapLocked"
                    variant="primary"
                    class="btn-block mb-2"
                  >
                    {{ t.name }}
                  </b-btn>

                  <b-btn
                    v-else
                    :disabled="mapLocked"
                    @click="selectWinType(t)"
                    variant="outline-primary"
                    class="btn-block mb-2"
                  >
                    {{ t.name }}
                  </b-btn>
                </div>
              </b-col>
            </b-row>

            <hr class="divider" />

            <b-row>
              <!-- Win Team -->
              <b-col lg="6">
                <label class="text-bold"
                  >{{ $t("matches.rounds.win_team") }}:</label
                >

                <b-row>
                  <b-col xl="6">
                    <template v-if="winTeam === match.team_blue">
                      <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                        {{ match.team_blue_name }}
                      </b-btn>
                    </template>
                    <template v-else>
                      <b-btn
                        variant="outline-primary"
                        class="btn-block mb-2 mb-xl-0"
                        :disabled="mapLocked"
                        @click="selectWinTeam(match.team_blue)"
                      >
                        {{ match.team_blue_name }}
                      </b-btn>
                    </template>
                  </b-col>

                  <b-col xl="6">
                    <template v-if="winTeam === match.team_orange">
                      <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                        {{ match.team_orange_name }}
                      </b-btn>
                    </template>
                    <template v-else>
                      <b-btn
                        variant="outline-primary"
                        class="btn-block mb-2 mb-xl-0"
                        :disabled="mapLocked"
                        @click="selectWinTeam(match.team_orange)"
                      >
                        {{ match.team_orange_name }}
                      </b-btn>
                    </template>
                  </b-col>
                </b-row>
              </b-col>

              <!-- Opening Frag Team -->
              <b-col lg="6">
                <label class="text-bold">{{
                  $t("matches.rounds.of_team")
                }}</label>

                <b-row>
                  <b-col xl="6">
                    <template v-if="ofTeam === match.team_blue">
                      <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                        {{ match.team_blue_name }}
                      </b-btn>
                    </template>
                    <template v-else>
                      <b-btn
                        variant="outline-primary"
                        class="btn-block mb-2 mb-xl-0"
                        :disabled="mapLocked"
                        @click="selectOFTeam(match.team_blue)"
                      >
                        {{ match.team_blue_name }}
                      </b-btn>
                    </template>
                  </b-col>

                  <b-col xl="6">
                    <template v-if="ofTeam === match.team_orange">
                      <b-btn variant="primary" class="btn-block mb-2 mb-xl-0">
                        {{ match.team_orange_name }}
                      </b-btn>
                    </template>
                    <template v-else>
                      <b-btn
                        variant="outline-primary"
                        class="btn-block mb-2 mb-xl-0"
                        :disabled="mapLocked"
                        @click="selectOFTeam(match.team_orange)"
                      >
                        {{ match.team_orange_name }}
                      </b-btn>
                    </template>
                  </b-col>
                </b-row>
              </b-col>
            </b-row>

            <hr class="divider" />

            <!-- Notes -->
            <b-row>
              <b-col cols="12">
                <label class="text-bold"
                  >{{ $t("matches.rounds.notes") }}:</label
                >
              </b-col>

              <b-col cols="12">
                <b-textarea
                  :placeholder="$t('matches.rounds.notes_text')"
                  v-model="notes"
                  rows="3"
                />
              </b-col>
            </b-row>

            <hr class="divider" />

            <b-row>
              <b-col lg="6">
                <b-btn
                  variant="primary"
                  class="btn-block"
                  :disabled="mapLocked"
                  @click="addRound"
                >
                  {{ $t("matches.rounds.add_round") }}
                  <b-spinner
                    v-if="loadingSmall === 'addRound'"
                    variant="light"
                    small
                  />
                </b-btn>
              </b-col>

              <b-col lg="6">
                <b-btn
                  variant="danger"
                  class="btn-block"
                  @click="removeLastRound"
                  :disabled="rounds.length === 0 || mapLocked"
                >
                  {{ $t("matches.rounds.remove_round") }}
                  <b-spinner
                    v-if="loadingSmall === 'removeRound'"
                    variant="light"
                    small
                  />
                </b-btn>
              </b-col>

              <b-col cols="12">
                <b-btn
                  variant="success"
                  class="btn-block mt-2"
                  @click="finishMap"
                  :disabled="!canBeFinished || mapLocked"
                >
                  {{ $t("matches.rounds.finish_map") }}
                </b-btn>
              </b-col>
            </b-row>
          </template>
        </CustomCard>
      </b-col>

      <!-- Live Statistics -->
      <b-col lg="6" order="2" order-lg="1">
        <CustomCard
          color="success"
          outline
          divider
          :title="$t('matches.rounds.live_stats')"
        >
          <template #card-body>
            <b-row v-if="rounds.length > 0" class="text-center">
              <b-col cols="12" md="6" lg="12" xl="6" class="mb-2">
                <label>{{ $t("matches.rounds.atk_def_wins") }}</label>
                <apexchart
                  type="donut"
                  :options="sideWinDataOptions"
                  :series="sideWinData"
                />
              </b-col>

              <b-col cols="12" class="d-md-none d-xl-none">
                <hr class="divider" />
              </b-col>

              <b-col cols="12" md="6" lg="12" xl="6" class="mb-2">
                <label>{{ $t("matches.rounds.opening_frags") }}</label>
                <apexchart
                  type="donut"
                  :options="ofDataOptions"
                  :series="ofData"
                />
              </b-col>

              <b-col cols="12">
                <hr class="divider" />
              </b-col>

              <b-col cols="12" md="6" lg="12" xl="6" class="mb-2">
                <label>{{ $t("matches.rounds.type_wins") }}</label>
                <apexchart
                  type="donut"
                  :options="typeWinDataOptions"
                  :series="typeWinData"
                />
              </b-col>

              <b-col cols="12" class="d-md-none d-xl-none">
                <hr class="divider" />
              </b-col>

              <b-col cols="12" md="6" lg="12" xl="6" class="mb-2">
                <label>{{ $t("matches.rounds.bomb_spot_picks") }}</label>
                <apexchart
                  type="donut"
                  :options="bombSpotPickDataOptions"
                  :series="bombSpotPickData"
                />
              </b-col>
            </b-row>

            <b-row v-else>
              <b-col>
                <span class="font-italic">{{
                  $t("matches.rounds.live_stats_placeholder")
                }}</span>
              </b-col>
            </b-row>
          </template>
        </CustomCard>
      </b-col>

      <!-- Rounds Table -->
      <b-col cols="12" order="1" order-lg="2">
        <CustomCard
          color="warning"
          outline
          divider
          :title="$t('matches.rounds.round_details')"
        >
          <template #card-body>
            <b-table
              table-variant="dark"
              small
              striped
              sort-icon-left
              responsive
              :items="rounds"
              :fields="roundTableFields"
              sort-by="round_no"
            >
              <template #cell(bomb_spot)="data">
                <b-badge variant="light" pill class="mr-1">
                  {{ getBombSpotName(data.item.bomb_spot).floor }}
                </b-badge>
                <span class="sl-only">{{
                  getBombSpotName(data.item.bomb_spot).name
                }}</span>
              </template>

              <template #cell(of_team_name)="data">
                <span v-if="data.item.of_team">{{
                  data.item.of_team_name
                }}</span>
                <span v-else>-</span>
              </template>

              <template #cell(score)="data">
                <span
                  >{{ data.item.score_blue }} -
                  {{ data.item.score_orange }}</span
                >
              </template>

              <template #cell(notes)="data">
                <div v-if="data.item.notes">
                  <div
                    v-for="(line, index) in data.item.notes.split('\\n')"
                    :key="index"
                  >
                    <span>{{ line }}</span
                    ><br />
                  </div>
                </div>
                <span v-else>-</span>
              </template>
            </b-table>
          </template>
        </CustomCard>
      </b-col>
    </b-row>
  </div>
</template>

<script>
  import CustomCard from "~/components/CustomCard"
  import {SingleMatch} from "~/mixins/axios/SingleMatch"
  import {SingleMatchMap} from "~/mixins/axios/SingleMatchMap"
  import {BombSpots} from "~/mixins/axios/BombSpots"
  import {RoundWebsocket} from "~/mixins/websocket/RoundWebsocket"

  export default {
    name: "Rounds",
    layout: "match",

    data() {
      return {
        selectedBombSpot: null,
        selectedWinType: null,
        winTeam: null,
        ofTeam: null,
        notes: null,
        loadingSmall: {},
        winTypes: [
          {id: 1, name: this.$t("matches.rounds.win_type_names.kills")},
          {
            id: 2,
            name: this.$t("matches.rounds.win_type_names.defuser_planted"),
          },
          {
            id: 3,
            name: this.$t("matches.rounds.win_type_names.defuser_disabled"),
          },
          {id: 4, name: this.$t("matches.rounds.win_type_names.time")},
        ],
        roundTableFields: [
          {
            key: "round_no",
            label: "#",
          },
          {
            key: "bomb_spot",
            label: this.$t("matches.rounds.bomb_spot"),
          },
          {
            key: "win_type_name",
            label: this.$t("matches.rounds.win_type"),
          },
          {
            key: "win_team_name",
            label: this.$t("matches.rounds.win_team"),
          },
          {
            key: "of_team_name",
            label: this.$t("matches.rounds.opening_frag"),
          },
          {
            key: "score",
            label: this.$t("core.score"),
          },
          {
            key: "notes",
            label: this.$t("matches.rounds.notes"),
          },
        ],
        chartOptions: {
          chart: {
            type: "donut",
          },
          fill: {
            type: "gradient",
          },
          legend: {
            labels: {
              colors: "white",
            },
            position: "bottom",
          },
        },
      }
    },

    head() {
      return {
        title: this.$t("navigation.rounds") + " - Caster Dashboard",
      }
    },

    computed: {
      matchID() {
        return this.$route.params.matchID
      },
      mapID() {
        return this.$route.params.mapID
      },
      sideWinData() {
        let atkWins = this.rounds.filter((r) => r.win_team === r.atk_team)
          .length
        let defWins = this.rounds.length - atkWins
        return [atkWins, defWins]
      },

      ofData() {
        let ofBlue = this.rounds.filter(
          (r) => r.of_team === this.match.team_blue
        ).length
        let ofOrange = this.rounds.filter(
          (r) => r.of_team === this.match.team_orange
        ).length
        return [ofBlue, ofOrange]
      },

      typeWinData() {
        let typeData = [0, 0, 0, 0]
        this.rounds.forEach((r) => {
          typeData[r.win_type - 1]++
        })
        return typeData
      },

      bombSpotPickData() {
        let bs1 = this.rounds.filter(
          (r) => r.bomb_spot === this.bombSpots[0].id
        ).length
        let bs2 = this.rounds.filter(
          (r) => r.bomb_spot === this.bombSpots[1].id
        ).length
        let bs3 = this.rounds.filter(
          (r) => r.bomb_spot === this.bombSpots[2].id
        ).length
        let bs4 = this.rounds.filter(
          (r) => r.bomb_spot === this.bombSpots[3].id
        ).length
        return [bs1, bs2, bs3, bs4]
      },

      sideWinDataOptions() {
        let options = Object.assign({}, this.chartOptions)
        options["labels"] = ["ATK Wins", "DEF Wins"]
        return options
      },

      ofDataOptions() {
        let options = Object.assign({}, this.chartOptions)
        options["labels"] = [
          this.match.team_blue_name,
          this.match.team_orange_name,
        ]
        return options
      },

      bombSpotPickDataOptions() {
        let options = Object.assign({}, this.chartOptions)
        options["labels"] = [
          this.getBombSpotName(this.bombSpots[0].id).name,
          this.getBombSpotName(this.bombSpots[1].id).name,
          this.getBombSpotName(this.bombSpots[2].id).name,
          this.getBombSpotName(this.bombSpots[3].id).name,
        ]
        return options
      },

      typeWinDataOptions() {
        let options = Object.assign({}, this.chartOptions)
        options["labels"] = [
          this.$t("matches.rounds.win_type_names.kills"),
          this.$t("matches.rounds.win_type_names.defuser_planted"),
          this.$t("matches.rounds.win_type_names.defuser_disabled"),
          this.$t("matches.rounds.win_type_names.time"),
        ]
        return options
      },

      canBeFinished() {
        let lastRound = this.rounds.filter(
          (r) => r.round_no === this.rounds.length
        )[0]
        if (lastRound) {
          return (
            (lastRound.score_blue >= 7 && lastRound.score_orange < 6) || // Regular blue win
            (lastRound.score_orange >= 7 && lastRound.score_blue < 6) || // Regular orange win
            (lastRound.score_blue === 6 && lastRound.score_orange === 6) || // Draw
            lastRound.score_blue >= 8 ||
            lastRound.score_orange >= 8
          ) // Overtime win
        }
        return false
      },

      mapLocked() {
        return this.matchMap.status === 3
      },
    },

    methods: {
      selectBombSpot(bombSpot) {
        this.selectedBombSpot = bombSpot
      },
      selectWinType(winType) {
        this.selectedWinType = winType
      },
      selectWinTeam(team) {
        this.winTeam = team
      },
      selectOFTeam(team) {
        this.ofTeam = team
      },
      addRound() {
        this.loadingSmall = {
          addRound: true,
        }

        // Validate input
        if (!this.selectedBombSpot) {
          this.$toast.warning(
            this.$t("matches.rounds.toasts.bomb_spot_missing")
          )
          this.loadingSmall = {}
          return
        }
        if (!this.selectedWinType) {
          this.$toast.warning(this.$t("matches.rounds.toasts.win_type_missing"))
          this.loadingSmall = {}
          return
        }
        if (!this.winTeam) {
          this.$toast.warning(this.$t("matches.rounds.toasts.win_team_missing"))
          this.loadingSmall = {}
          return
        }

        // Format notes
        let notes = null
        if (this.notes) notes = this.notes.replace("\n", "\\n")

        let data = {
          match: this.match.id,
          map: this.matchMap.map,
          bomb_spot: this.selectedBombSpot.id,
          win_type: this.selectedWinType.id,
          win_team: this.winTeam,
          of_team: this.ofTeam,
          notes: notes,
        }

        this.$axios
          .$post("/api/matches/round/", data)
          .then((response) => {
            this.resetRoundData()
            this.$toast.success(
              this.$t("matches.rounds.toasts.round_added"),
              this.$t("generic.success"),
              {timeout: 1000}
            )
            this.loadingSmall = {}
          })
          .catch(() => {
            this.$toast.error(
              this.$t("matches.rounds.toasts.round_added_failed"),
              this.$t("generic.error")
            )
            this.loadingSmall = {}
          })
      },

      removeLastRound() {
        this.loadingSmall = {
          removeRound: true,
        }
        let lastRound = this.rounds.filter(
          (r) => r.round_no === this.rounds.length
        )[0]

        this.$axios
          .$delete(`/api/matches/round/${lastRound.id}/`)
          .then(() => {
            this.$toast.success(
              this.$t("matches.rounds.toasts.round_removed"),
              this.$t("generic.success")
            )
            this.loadingSmall = {}
          })
          .catch(() => {
            this.$toast.success(
              this.$t("matches.rounds.toasts.round_removed_failed"),
              this.$t("generic.error")
            )
            this.loadingSmall = {}
          })
      },

      finishMap() {
        this.$bvModal
          .msgBoxConfirm(
            this.$t("matches.rounds.finish_map_confirm_1") +
              " " +
              this.$t("matches.rounds.finish_map_confirm_2"),
            {
              title: this.$t("matches.rounds.finish_map") + "?",
              centered: true,
              okVariant: "danger",
              headerBgVariant: "danger",
              bodyBgVariant: "dark",
              footerBgVariant: "dark",
            }
          )
          .then((value) => {
            if (value) {
              let lastRound = this.rounds.filter(
                (r) => r.round_no === this.rounds.length
              )[0]
              let winTeam = null
              if (lastRound.score_blue !== lastRound.score_orange) {
                winTeam = lastRound.win_team
              }

              let data = {
                win_team: winTeam,
                score_blue: lastRound.score_blue,
                score_orange: lastRound.score_orange,
              }

              this.$axios
                .$patch(`/api/matches/maps/${this.matchMap.id}/`, data)
                .then(() => {
                  this.$axios
                    .$get(`/api/match/${this.matchID}/`)
                    .then((matchData) => {
                      let nextURL = ""

                      // Where to redirect next?
                      if (matchData.best_of === 1) {
                        nextURL = "overview"
                      } else if (
                        matchData.best_of === 2 ||
                        matchData.best_of === 3
                      ) {
                        if (
                          matchData.score_blue >= 2 ||
                          matchData.score_orange >= 2
                        )
                          nextURL = "overview"
                        else nextURL = "nextMap"
                      } else if (matchData.best_of === 5) {
                        if (
                          matchData.score_blue >= 3 ||
                          matchData.score_orange >= 3
                        )
                          nextURL = "overview"
                        else nextURL = "nextMap"
                      }

                      if (nextURL === "overview") {
                        // Redirect to rounds overview
                        this.$toast.info(
                          this.$t("matches.rounds.match_finished")
                        )
                        this.$router.push(
                          `/dashboard/matches/${this.matchID}/overview`
                        )
                      } else if (nextURL === "nextMap") {
                        // Redirect to next map
                        this.$axios
                          .$get(`/api/matches/maps/?match=${this.matchID}`)
                          .then((data) => {
                            this.$toast.info(
                              this.$t("matches.rounds.map_finished")
                            )
                            let next_map_id = data.filter(
                              (m) =>
                                m.play_order === this.matchMap.play_order + 1
                            )[0].map
                            this.$router.push(
                              `/dashboard/matches/${this.matchID}/map/${next_map_id}/opbans`
                            )
                          })
                      }
                    })
                })
                .catch(() => {
                  this.$toast.error(
                    this.$t("matches.rounds.finish_map_failed"),
                    this.$t("generic.error")
                  )
                })
            }
          })
      },

      resetRoundData() {
        this.selectedBombSpot = null
        this.selectedWinType = null
        this.winTeam = null
        this.ofTeam = null
        this.notes = ""
      },
      getBombSpotName(id) {
        let bomb_spot = this.bombSpots.filter((b) => b.id === id)[0]
        return {floor: bomb_spot.floor, name: bomb_spot.name}
      },
    },

    mounted() {
      this.$store.commit("setPageTitle", this.$t("navigation.rounds"))
      this.$store.commit("setPageTitleIcon", "list-ol")
      this.$store.commit("setBreadcrumbPath", [
        "Dashboard",
        "Matches",
        this.$route.params.matchID,
        "Map",
        this.$route.params.mapID,
        "Rounds",
      ])
    },

    async fetch() {
      await Promise.all([this.getSingleMatch(), this.getSingleMatchMap()])

      // Set Map to Breadcrumbs
      this.$store.commit("setBreadcrumbPath", [
        "Dashboard",
        "Matches",
        this.$route.params.matchID,
        `${this.matchMap.map_name} (Map ${this.matchMap.play_order}/${this.match.best_of})`,
        "Rounds",
      ])

      await Promise.all([this.getBombSpots(), this.connectRoundWebsocket()])
    },

    mixins: [SingleMatch, SingleMatchMap, BombSpots, RoundWebsocket],

    components: {
      CustomCard: CustomCard,
    },
  }
</script>

<style scoped></style>
