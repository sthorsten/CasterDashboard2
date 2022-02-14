<template>
  <div>
    <ContentHeader
      icon="map"
      title="Map Overview"
      :breadcrumb-items="['Dashboard', 'Matches', $route.params.matchID, $route.params.mapName, 'Overview']"
    />
    <ContentContainer v-if="match != null && matchMap != null">
      <b-container fluid>
        <b-row>
          <!-- Left column -->
          <b-col cols="6">
            <CustomCard title="Map Details">
              <b-table-simple striped small>
                <b-tbody>
                  <b-tr>
                    <b-th colspan="2" class="bg-primary">
                      Base Information
                    </b-th>
                  </b-tr>

                  <b-tr>
                    <b-th>Map</b-th>
                    <b-td class="text-right">
                      {{ matchMap.mapName }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Map Status</b-th>
                    <b-td class="text-right">
                      <MapStatusBadge :status="matchMap.status" />
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th colspan="2" class="bg-primary">
                      Teams
                    </b-th>
                  </b-tr>

                  <b-tr>
                    <b-th>Team Blue</b-th>
                    <b-td class="text-right">
                      <img :src="teamLogo(match.teamBlue)" width="20" height="20" alt="Team Blue Logo">
                      {{ match.teamBlueName }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Team Orange</b-th>
                    <b-td class="text-right">
                      <img :src="teamLogo(match.teamOrange)" width="20" height="20" alt="Team Orange Logo">
                      {{ match.teamOrangeName }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Team starting ATK</b-th>
                    <b-td class="text-right">
                      <template v-if="matchMap.atkTeam">
                        <img :src="teamLogo(matchMap.atkTeam)" width="20" height="20" alt="Team Orange Logo">
                        {{ matchMap.atkTeamName }}
                      </template>
                      <template v-else>
                        <i>Not selected yet.</i>
                      </template>
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Team starting ATK (Overtime)</b-th>
                    <b-td class="text-right">
                      <template v-if="matchMap.otAtkTeam">
                        <img :src="teamLogo(matchMap.otAtkTeam)" width="20" height="20" alt="Team Orange Logo">
                        {{ matchMap.otAtkTeamName }}
                      </template>
                      <template v-else>
                        <i>Not selected yet.</i>
                      </template>
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th colspan="2" class="bg-primary">
                      Map Result
                    </b-th>
                  </b-tr>

                  <b-tr>
                    <b-th>Score</b-th>
                    <b-td class="text-right">
                      {{ matchMap.scoreBlue }} - {{ matchMap.scoreOrange }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Winner</b-th>
                    <b-td class="text-right">
                      {{ matchMap.winTeam ? matchMap.winTeamName : '-' }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Win type</b-th>
                    <b-td class="text-right">
                      <WintypeBadge :status="matchMap.winType" />
                    </b-td>
                  </b-tr>
                </b-tbody>
              </b-table-simple>
            </CustomCard>
          </b-col>

          <!-- Right column -->
          <b-col cols="6">
            <CustomCard color="info" title="Map Actions">
              <b-form-group>
                <b-row>
                  <b-col lg="6">
                    <fa-icon icon="users" />
                    Select Team starting ATK
                  </b-col>

                  <b-col lg="3">
                    <b-btn
                      :variant="currentAtkTeam === match.teamBlue ? 'primary' : 'outline-primary'"
                      block
                      @click="setAtkTeam(match.teamBlue)"
                    >
                      <img
                        :src="$store.getters['mainSocket/getTeamLogo'](match.teamBlue, true)"
                        height="20"
                        width="20"
                        alt="teamBlue logo"
                      >
                      {{ match.teamBlueName }}
                    </b-btn>
                  </b-col>

                  <b-col lg="3">
                    <b-btn
                      :variant="currentAtkTeam === match.teamOrange ? 'primary' : 'outline-primary'"
                      block
                      @click="setAtkTeam(match.teamOrange)"
                    >
                      <img
                        :src="$store.getters['mainSocket/getTeamLogo'](match.teamOrange, true)"
                        height="20"
                        width="20"
                        alt="teamOrange logo"
                      >
                      {{ match.teamOrangeName }}
                    </b-btn>
                  </b-col>
                </b-row>
              </b-form-group>

              <b-form-group>
                <b-row>
                  <b-col lg="6">
                    <fa-icon icon="users" />
                    Select Team starting ATK (Overtime)
                  </b-col>

                  <b-col lg="3">
                    <b-btn
                      :variant="currentOtAtkTeam === match.teamBlue ? 'primary' : 'outline-primary'"
                      block
                      @click="setOtAtkTeam(match.teamBlue)"
                    >
                      <img
                        :src="$store.getters['mainSocket/getTeamLogo'](match.teamBlue, true)"
                        height="20"
                        width="20"
                        alt="teamBlue logo"
                      >
                      {{ match.teamBlueName }}
                    </b-btn>
                  </b-col>

                  <b-col lg="3">
                    <b-btn
                      :variant="currentOtAtkTeam === match.teamOrange ? 'primary' : 'outline-primary'"
                      block
                      @click="setOtAtkTeam(match.teamOrange)"
                    >
                      <img
                        :src="$store.getters['mainSocket/getTeamLogo'](match.teamOrange, true)"
                        height="20"
                        width="20"
                        alt="teamOrange logo"
                      >
                      {{ match.teamOrangeName }}
                    </b-btn>
                  </b-col>
                </b-row>
              </b-form-group>

              <hr class="border-secondary">

              <b-btn
                variant="primary"
                block
                @click="$router.push(`/dashboard/matches/${match.id}/map/${matchMap.mapName}/opbans`)"
              >
                <fa-icon icon="arrow-right" />
                Continue to operator bans
              </b-btn>
            </CustomCard>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'MapOverview',
  layout: 'match-page',

  data () {
    return {
      // currentAtkTeam: null,
      // currentOtAtkTeam: null
    }
  },

  computed: {
    match () {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters['matchSocket/getMatch'](matchID)
      } catch {
        return null
      }
    },
    mapBans () {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters['matchSocket/getMapBansByMatch'](matchID)
      } catch {
        return null
      }
    },
    matchMaps () {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters['matchSocket/getMatchMapsByMatch'](matchID)
      } catch {
        return null
      }
    },

    currentAtkTeam () {
      return this.matchMap.atkTeam
    },
    currentOtAtkTeam () {
      return this.matchMap.otAtkTeam
    },

    matchMap () {
      return this.matchMaps.filter(m => m.mapName === this.$route.params.mapName)[0]
    }
  },

  methods: {
    teamLogo (id) {
      return this.$store.getters['mainSocket/getTeamLogo'](id, true)
    },

    async setAtkTeam (team) {
      const data = {
        atkTeam: team
      }

      try {
        await this.$axios.$patch(`/api/v2/match/matchmap/${this.matchMap.id}/`, data)
      } catch (e) {
        this.$toast.error('Error')
      }
    },
    async setOtAtkTeam (team) {
      const data = {
        otAtkTeam: team
      }

      try {
        await this.$axios.$patch(`/api/v2/match/matchmap/${this.matchMap.id}/`, data)
      } catch (e) {
        this.$toast.error('Error')
      }
    }
  }
}
</script>
