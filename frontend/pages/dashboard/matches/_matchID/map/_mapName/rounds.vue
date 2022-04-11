<template>
  <div>
    <ContentHeader
      icon="play-circle"
      title="Rounds"
      :breadcrumb-items="[
        'Dashboard',
        'Matches',
        $route.params.matchID,
        $route.params.mapName,
        'Rounds',
      ]"
    />
    <ContentContainer v-if="match != null && matchMap != null">
      <b-container fluid>
        <!-- Add round & Round Actions -->
        <b-row>
          <!-- Add round -->
          <b-col cols="6">
            <CustomCard title="Add Round">
              <!-- Bomb spot-->
              <label>
                <b-badge variant="secondary" pill class="mr-2">1</b-badge>Select
                Bomb Spot:
              </label>
              <b-row style="margin-top: -0.5rem">
                <b-col cols="6" v-for="bs in bombSpots" :key="bs.id">
                  <BombspotSelectBtn
                    :bombspot="bs"
                    @clicked="selectedBombspot = bs.id"
                    :selected="selectedBombspot == bs.id"
                  />
                </b-col>
              </b-row>

              <hr class="border-secondary" />

              <!-- OF Team -->
              <label>
                <b-badge variant="secondary" pill class="mr-2">2</b-badge>Select
                Opening Frag Team:
              </label>
              <b-row>
                <b-col cols="6">
                  <b-btn
                    :variant="
                      selectedOFTeam === match.teamBlue
                        ? 'primary'
                        : 'outline-primary'
                    "
                    block
                    @click="selectedOFTeam = match.teamBlue"
                  >
                    <img
                      :src="
                        $store.getters['mainSocket/getTeamLogo'](
                          match.teamBlue,
                          true
                        )
                      "
                      height="20"
                      width="20"
                      alt="teamBlue logo"
                      class="mr-1"
                    />
                    {{ match.teamBlueName }}
                  </b-btn>
                </b-col>
                <b-col cols="6">
                  <b-btn
                    :variant="
                      selectedOFTeam === match.teamOrange
                        ? 'primary'
                        : 'outline-primary'
                    "
                    block
                    @click="selectedOFTeam = match.teamOrange"
                  >
                    <img
                      :src="
                        $store.getters['mainSocket/getTeamLogo'](
                          match.teamOrange,
                          true
                        )
                      "
                      height="20"
                      width="20"
                      alt="teamBlue logo"
                      class="mr-1"
                    />
                    {{ match.teamOrangeName }}
                  </b-btn>
                </b-col>
              </b-row>

              <hr class="border-secondary" />

              <!-- Win Team -->
              <label>
                <b-badge variant="secondary" pill class="mr-2">3</b-badge>Select
                Win Team:
              </label>
              <b-row>
                <b-col cols="6">
                  <b-btn
                    :variant="
                      selectedWinTeam === match.teamBlue
                        ? 'primary'
                        : 'outline-primary'
                    "
                    block
                    @click="selectedWinTeam = match.teamBlue"
                  >
                    <img
                      :src="
                        $store.getters['mainSocket/getTeamLogo'](
                          match.teamBlue,
                          true
                        )
                      "
                      height="20"
                      width="20"
                      alt="teamBlue logo"
                      class="mr-1"
                    />
                    {{ match.teamBlueName }}
                  </b-btn>
                </b-col>
                <b-col cols="6">
                  <b-btn
                    :variant="
                      selectedWinTeam === match.teamOrange
                        ? 'primary'
                        : 'outline-primary'
                    "
                    block
                    @click="selectedWinTeam = match.teamOrange"
                  >
                    <img
                      :src="
                        $store.getters['mainSocket/getTeamLogo'](
                          match.teamOrange,
                          true
                        )
                      "
                      height="20"
                      width="20"
                      alt="teamBlue logo"
                      class="mr-1"
                    />
                    {{ match.teamOrangeName }}
                  </b-btn>
                </b-col>
              </b-row>

              <hr class="border-secondary" />

              <!-- Win Type-->
              <label>
                <b-badge variant="secondary" pill class="mr-2">4</b-badge>Select
                Win Type:
              </label>
              <b-row>
                <b-col cols="6">
                  <b-btn
                    :variant="
                      selectedWinType === 'KILLS'
                        ? 'primary'
                        : 'outline-primary'
                    "
                    @click="selectedWinType = 'KILLS'"
                    block
                    >Kills</b-btn
                  >
                  <b-btn
                    :variant="
                      selectedWinType === 'DEFUSER_PLANTED'
                        ? 'primary'
                        : 'outline-primary'
                    "
                    @click="selectedWinType = 'DEFUSER_PLANTED'"
                    block
                    >Defuser Planted</b-btn
                  >
                </b-col>
                <b-col cols="6">
                  <b-btn
                    :variant="
                      selectedWinType === 'TIME' ? 'primary' : 'outline-primary'
                    "
                    @click="selectedWinType = 'TIME'"
                    block
                    >Time</b-btn
                  >
                  <b-btn
                    :variant="
                      selectedWinType === 'DEFUSER_DISABLED'
                        ? 'primary'
                        : 'outline-primary'
                    "
                    @click="selectedWinType = 'DEFUSER_DISABLED'"
                    block
                    >Defuser Disabled</b-btn
                  >
                </b-col>
              </b-row>

              <hr class="border-secondary" />

              <!-- Notes -->
              <label>
                <b-badge variant="secondary" pill class="mr-2">5</b-badge>Notes:
              </label>
              <b-form-textarea
                rows="3"
                max-rows="3"
                :placeholder="'What happened during the round?\nThis field is optional'"
                v-model="notes"
              ></b-form-textarea>
            </CustomCard>
          </b-col>

          <!-- Round Actions -->
          <b-col cols="6">
            <CustomCard title="Round Actions" color="info">
              <b-btn
                variant="primary"
                block
                :disabled="!roundDetailsOK"
                @click="addRound"
              >
                <fa-icon icon="plus" class="mr-1" />
                <span>Add round</span>
              </b-btn>

              <hr class="border-secondary" />

              <b-btn variant="danger" block disabled>
                <fa-icon icon="trash-can" class="mr-1" />
                <span>Remove last round</span>
              </b-btn>
              <b-btn variant="danger" block disabled>
                <fa-icon icon="trash-can" class="mr-1" />
                <span>Remove all rounds</span>
              </b-btn>

              <hr class="border-secondary" />

              <b-btn variant="success" block @click="finishMap">
                <fa-icon icon="circle-check" class="mr-1" />
                <span>Finish map</span>
              </b-btn>
            </CustomCard>

            <CustomCard title="Map & Round Info" color="secondary">
              <b-table-simple striped small>
                <b-tbody>
                  <b-tr>
                    <b-th>Best Of</b-th>
                    <b-td class="text-right">BO{{ match.bestOf }}</b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Current match score</b-th>
                    <b-td class="text-right"
                      >{{ match.scoreBlue }} - {{ match.scoreOrange }}</b-td
                    >
                  </b-tr>

                  <b-tr>
                    <b-th>Current map</b-th>
                    <b-td class="text-right">{{ matchMap.mapName }}</b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Current map score</b-th>
                    <b-td class="text-right"
                      >{{ matchMap.scoreBlue }} -
                      {{ matchMap.scoreOrange }}</b-td
                    >
                  </b-tr>

                  <b-tr>
                    <b-th>Next round</b-th>
                    <b-td class="text-right">{{ rounds.length + 1 }}</b-td>
                  </b-tr>
                </b-tbody>
              </b-table-simple>
            </CustomCard>
          </b-col>
        </b-row>

        <!-- Round Details -->
        <b-row>
          <b-col cols="12">
            <CustomCard title="Round Details" color="success">
              <RoundTable :match-map-id="matchMap.id" />
            </CustomCard>
          </b-col>
        </b-row>

        <!-- Round stats -->
        <b-row>
          <b-col cols="12">
            <CustomCard title="Round Statistics" color="secondary">
              <b-row>
                <b-col cols="12" md="6" xl="4">
                  <RoundBombspotChart :map-id="this.matchMap.map" />
                </b-col>
                <b-col cols="12" md="6" xl="4">
                  <RoundWintypeChart />
                </b-col>
                <b-col cols="12" md="6" xl="4">
                  <RoundSideChart
                    :team-blue="match.teamBlueName"
                    :team-orange="match.teamOrangeName"
                    :atk-team="matchMap.atkTeamName"
                    :ot-atk-team="matchMap.otAtkTeamName"
                  />
                </b-col>
              </b-row>
            </CustomCard>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>

export default {
  name: "Rounds",
  layout: "match-page",

  data() {
    return {
      selectedBombspot: -1,
      selectedOFTeam: -1,
      selectedWinTeam: -1,
      selectedWinType: null,
      notes: '',

      boxTwo: ''
    }
  },

  computed: {
    match() {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters["matchSocket/getMatch"](matchID)
      }
      catch {
        return null
      }
    },
    matchMaps() {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters["matchSocket/getMatchMapsByMatch"](matchID)
      }
      catch {
        return null
      }
    },
    bombSpots() {
      return this.$store.getters["coreSocket/getBombSpotsByMap"](this.matchMap.map)
    },
    matchMap() {
      return this.matchMaps.filter(m => m.mapName === this.$route.params.mapName)[0]
    },
    rounds() {
      return this.$store.getters["matchSocket/getRoundsByMatchMap"](this.matchMap.id)
    },

    roundDetailsOK() {
      return this.selectedBombspot !== -1 &&
        this.selectedWinTeam !== -1 &&
        this.selectedWinType != null
    },
  },

  methods: {
    async addRound() {
      const data = {
        matchMap: this.matchMap.id,
        winTeam: this.selectedWinTeam,
        openingFragTeam: this.selectedOFTeam > -1 ? this.selectedOFTeam : null,
        bombSpot: this.selectedBombspot,
        winType: this.selectedWinType,
        notes: this.notes
      }

      try {
        await this.$axios.$post('/api/v2/match/round/', data)
      } catch (e) {
        console.error(e)
        return
      }

      // Reset values
      this.selectedBombspot = -1
      this.selectedOFTeam = -1
      this.selectedWinTeam = -1
      this.selectedWinType = null
      this.notes = ''
    },

    async finishMap() {
      try {
        await this.$axios.$patch('/api/v2/match/matchmap/' + this.matchMap.id + '/', {
          status: 'FINISHED'
        })
      } catch (e) {
        console.log(e)
        return
      }

      // Redirect to next map or match overview page

      // Match is BO1 or last map
      if (this.match.bestOf === 1 || this.matchMap.order === this.match.bestOf) {
        this.$router.push(`/dashboard/matches/${this.match.id}/overview`)
        return
      }

      const nextMap = this.matchMaps.find(m => m.order === (this.matchMap.order + 1))

      // BO2: Go to map 2 regardless of score
      if (this.match.bestOf === 2) {
        this.$router.push(`/dashboard/matches/${this.match.id}/map/${nextMap.mapName}/overview`)
        return
      }
      // Match finished when score of one team > half of the maps to be played (e.g. 2:0 in BO3 or 3:0 in BO5)
      if (this.match.scoreBlue > Math.floor(this.match.bestOf / 2) || this.match.scoreOrange > Math.floor(this.match.bestOf / 2)) {
        this.$router.push(`/dashboard/matches/${this.match.id}/overview`)
      }
      // Go to next map
      else {
        this.$router.push(`/dashboard/matches/${this.match.id}/map/${nextMap.mapName}/overview`)
      }
    }
  }
}
</script>
