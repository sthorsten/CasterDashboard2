<template>
  <div>
    <ContentHeader
      icon="history"
      title="Match List"
      :breadcrumb-items="['Dashboard', 'Matches', 'List']"
    />
    <ContentContainer>
      <b-container fluid>
        <b-row>
          <b-col>
            <CustomCard title="Recent Matches">
              <b-table
                striped
                small
                :items="matches"
                :fields="matchTableFields"
                :per-page="10"
                :current-page="matchTablePage"
                sort-by="id"
                :sort-desc="true"
              >
                <template #cell(leagueField)="data">
                  <img
                    :src="
                      $store.getters['mainSocket/getLeague'](data.item.league)
                        .logoSmall
                    "
                    width="25"
                    height="25"
                    alt="League Logo"
                  />
                  {{ data.item.leagueName }}
                </template>
                <template #cell(season)="data">
                  {{
                    $store.getters["mainSocket/getSeasonByPlaydayID"](
                      data.item.playday
                    ).name
                  }}
                </template>
                <template #cell(teamBlueField)="data">
                  <img
                    :src="
                      $store.getters['mainSocket/getTeam'](data.item.teamBlue)
                        .logoSmall
                    "
                    width="25"
                    height="25"
                    alt="Team Blue Logo"
                  />
                  {{ data.item.teamBlueName }}
                </template>
                <template #cell(teamOrangeField)="data">
                  <img
                    :src="
                      $store.getters['mainSocket/getTeam'](data.item.teamOrange)
                        .logoSmall
                    "
                    width="25"
                    height="25"
                    alt="Team Orange Logo"
                  />
                  {{ data.item.teamOrangeName }}
                </template>
                <template #cell(status)="data">
                  <MatchStatusBadge :status="data.item.status" />
                </template>
                <template #cell(button)="data">
                  <b-btn
                    size="sm"
                    variant="primary"
                    @click="
                      $router.push(
                        `/dashboard/matches/${data.item.id}/overview`
                      )
                    "
                  >
                    <fa-icon icon="arrow-right" class="mr-1" />
                    <span>Go to match</span>
                  </b-btn>
                </template>
              </b-table>

              <!-- Pagination -->
              <div class="mt-2 w-100 d-flex justify-content-center">
                <b-pagination
                  v-model="matchTablePage"
                  :per-page="10"
                  :total-rows="matches.length"
                />
              </div>
            </CustomCard>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'ListMatches',
  layout: 'main-page',

  data() {
    return {
      matchTableFields: [
        {
          key: 'id',
          label: 'ID',
          sortable: true
        },
        'name',
        {
          key: 'leagueField',
          label: 'League'
        },
        'season',
        {
          key: 'playdayName',
          label: 'Playday'
        },
        {
          key: 'teamBlueField',
          label: 'Team Blue'
        },
        {
          key: 'teamOrangeField',
          label: 'Team Orange'
        },
        'date',
        'status',
        'button'
      ],

      matchTablePage: 1
    }
  },

  computed: {
    matches() {
      return this.$store.state.matchSocket.matches
    }
  }
}
</script>
