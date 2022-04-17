<template>
  <div>
    <ContentHeader
      icon="info-circle"
      title="Match Details"
      :breadcrumb-items="[
        'Dashboard',
        'Matches',
        $route.params.matchID,
        'Details',
      ]"
    />
    <ContentContainer>
      <b-container fluid>
        <!-- Maps -->
        <b-row>
          <b-col>
            <CustomCard title="Maps" color="info">
              <i v-if="!mapBans || mapBans.length === 0">
                No maps have been selected yet.
              </i>

              <b-row>
                <!-- Selected maps -->
                <b-col
                  v-for="mapBan in mapBans"
                  :key="mapBan.id"
                  class="text-center"
                >
                  <b-row>
                    <b-col>
                      <MapbanImage
                        :map-name="mapBan.mapName"
                        :map-ban="mapBan"
                      />
                    </b-col>
                  </b-row>

                  <b-row class="mt-2">
                    <b-col>
                      <MapbanText
                        :map="getMapByID(mapBan.map)"
                        :map-ban="mapBan"
                      />
                    </b-col>
                  </b-row>
                </b-col>

                <!-- Placeholder -->
                <b-col v-for="i in 9 - mapBans.length" :key="i"></b-col>
              </b-row>
            </CustomCard>
          </b-col>
        </b-row>

        <!-- Map Details -->
        <b-row>
          <b-col>
            <CustomCard
              v-for="matchMap in matchMaps"
              :key="matchMap.id"
              :title="`Map ${matchMap.order}/${match.bestOf} (${matchMap.mapName})`"
            >
              <b-row>
                <!-- Map Details -->
                <b-col cols="6">
                  <b-table-simple striped small class="h-100">
                    <b-tbody>
                      <b-tr>
                        <b-th>Map Status</b-th>
                        <b-td class="text-right">
                          <MapStatusBadge :status="matchMap.status" />
                        </b-td>
                      </b-tr>

                      <b-tr>
                        <b-th>ATK Team</b-th>
                        <b-td class="text-right">
                          {{ matchMap.atkTeamName || "-" }}
                        </b-td>
                      </b-tr>

                      <b-tr>
                        <b-th>Overtime ATK Team</b-th>
                        <b-td class="text-right">
                          {{ matchMap.otAtkTeamName || "-" }}
                        </b-td>
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
                        <b-td class="text-right">{{
                          getRounds(matchMap).length + 1
                        }}</b-td>
                      </b-tr>
                    </b-tbody>
                  </b-table-simple>
                </b-col>

                <!-- Operator Bans -->
                <b-col cols="6">
                  <b-row class="mb-2">
                    <label class="text-center w-100"> Operator Bans: </label>
                  </b-row>
                  <b-row>
                    <b-col
                      cols="3"
                      v-for="ban in getOperatorBans(matchMap)"
                      :key="ban.id"
                      class="text-center"
                    >
                      <R6OperatorIcon
                        :operator="ban.operatorIdentifier"
                        height="50"
                      />
                      <br />
                      <b>{{ ban.operatorName }}</b>
                      <br />
                      <i>{{ ban.teamName }}</i>
                    </b-col>

                    <!-- Empty cols -->
                    <b-col
                      cols="3"
                      v-for="i in 4 - getOperatorBans(matchMap).length"
                      :key="'empty-ban-' + i"
                      class="text-center pt-4"
                    >
                      <i>No ban</i>
                    </b-col>
                  </b-row>
                </b-col>
              </b-row>

              <hr class="border-secondary" />

              <RoundTable :match-map-id="matchMap.id" />

              <hr class="border-secondary" />

              <b-row>
                <b-col cols="12" md="6" xl="4">
                  <RoundBombspotChart :map-id="matchMap.map" />
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
  name: 'MatchDetails',
  layout: 'match-page',

  head() {
    return {
      title: "Match Details"
    }
  },

  computed: {
    match() {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters['matchSocket/getMatch'](matchID)
      } catch {
        return null
      }
    },
    mapBans() {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters['matchSocket/getMapBansByMatch'](matchID)
      } catch {
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
  },

  methods: {
    getOperatorBans(matchMap) {
      return this.$store.getters["matchSocket/getOperatorBansByMatchMap"](matchMap.id)
    },
    getRounds(matchMap) {
      return this.$store.getters["matchSocket/getRoundsByMatchMap"](matchMap.id)
    },
    getMapByID(map) {
      return this.$store.getters["coreSocket/getMap"](map)
    }
  }
}
</script>