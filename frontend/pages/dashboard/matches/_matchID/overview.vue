<template>
  <div>
    <ContentHeader
      icon="list-ul"
      title="Match Overview"
      :breadcrumb-items="[
        'Dashboard',
        'Matches',
        $route.params.matchID,
        'Overview',
      ]"
    />
    <ContentContainer v-if="match">
      <b-container fluid>
        <b-row>
          <!-- Left -->
          <b-col cols="6">
            <CustomCard title="Match Info">
              <b-table-simple striped small>
                <b-tbody>
                  <b-tr>
                    <b-th colspan="2" class="bg-primary">
                      Base Information
                    </b-th>
                  </b-tr>

                  <b-tr>
                    <b-th>Match ID</b-th>
                    <b-td class="text-right">
                      <b-badge class="bg-primary" pill>
                        {{ match.id }}
                      </b-badge>
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Match Status</b-th>
                    <b-td class="text-right">
                      <MatchStatusBadge :status="match.status" />
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Date</b-th>
                    <b-td class="text-right">
                      {{ match.date }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th colspan="2" class="bg-primary"> Match Details </b-th>
                  </b-tr>

                  <b-tr>
                    <b-th>League</b-th>
                    <b-td class="text-right">
                      <img
                        :src="leagueLogo"
                        width="20"
                        height="20"
                        alt="League Logo"
                      />
                      {{ match.leagueName }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Season</b-th>
                    <b-td class="text-right">
                      {{
                        $store.getters["mainSocket/getSeasonByPlaydayID"](
                          match.playday
                        ).name
                      }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Playday</b-th>
                    <b-td class="text-right">
                      {{ match.playdayName }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Teams</b-th>
                    <b-td class="text-right">
                      <img
                        :src="teamLogo(match.teamBlue)"
                        width="20"
                        height="20"
                        alt="Team Blue Logo"
                      />
                      {{ match.teamBlueName }} <b>vs.</b>
                      {{ match.teamOrangeName }}
                      <img
                        :src="teamLogo(match.teamOrange)"
                        width="20"
                        height="20"
                        alt="Team Orange Logo"
                      />
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th colspan="2" class="bg-primary"> Match Result </b-th>
                  </b-tr>

                  <b-tr>
                    <b-th>Score</b-th>
                    <b-td class="text-right">
                      {{ match.scoreBlue }} - {{ match.scoreOrange }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Winner</b-th>
                    <b-td class="text-right">
                      {{ match.winTeam ? match.winTeamName : "-" }}
                    </b-td>
                  </b-tr>

                  <b-tr>
                    <b-th>Win type</b-th>
                    <b-td class="text-right">
                      <WintypeBadge :status="match.winType" />
                    </b-td>
                  </b-tr>
                </b-tbody>
              </b-table-simple>
            </CustomCard>
          </b-col>

          <!-- Right -->
          <b-col cols="6">
            <CustomCard title="Match Actions" color="info">
              <b-container fluid>
                <b-btn variant="primary" block @click="setMatchToOverlays">
                  <fa-icon icon="arrow-right-to-bracket" />
                  Set Match to overlays
                </b-btn>
                <b-btn variant="primary" block disabled>
                  <fa-icon icon="arrow-right-to-bracket" />
                  Set Match as <b>next match</b> to overlays
                </b-btn>

                <hr class="border-secondary" />

                <b-btn
                  variant="primary"
                  block
                  @click="$router.push(`/dashboard/matches/${match.id}/mapban`)"
                >
                  <fa-icon icon="arrow-right" />
                  Continue to Map Pick & Ban
                </b-btn>
                <b-btn variant="primary" block disabled>
                  <fa-icon icon="circle-info" />
                  Show match details
                </b-btn>

                <hr class="border-secondary" />

                <b-btn variant="danger" block disabled>
                  <fa-icon icon="pencil-alt" />
                  Edit match
                </b-btn>
                <b-btn variant="danger" block disabled>
                  <fa-icon icon="trash-can" />
                  Delete match
                </b-btn>
              </b-container>
            </CustomCard>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'MatchOverview',
  layout: 'match-page',

  data() {
    return {
      edit: false,
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

    leagueLogo() {
      return this.$store.getters['mainSocket/getLeagueLogo'](this.match.league, true)
    }
  },

  methods: {
    teamLogo(id) {
      return this.$store.getters['mainSocket/getTeamLogo'](id, true)
    },

    async setMatchToOverlays() {
      try {
        await this.$axios.$patch(`/api/v2/overlay/user/${this.$auth.user.id}/`, {
          overlayMatch: this.match.id
        })
        this.$toast.success("Match set to overlays")
      } catch (e) {
        console.error(e)
      }
    }
  }

}
</script>
