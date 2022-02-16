<template>
  <div>
    <ContentHeader
      icon="users-slash"
      title="Operator Bans"
      :breadcrumb-items="['Dashboard', 'Matches', $route.params.matchID, $route.params.mapName, 'Operator Bans']"
    />
    <ContentContainer v-if="match != null && matchMap != null">
      <b-container fluid>
        <b-row>
          <!-- Left column -->
          <b-col cols="6">
            <CustomCard title="Operator Bans">
              tmp
            </CustomCard>
          </b-col>

          <!-- Right column -->
          <b-col cols="6">
            <!-- Actions -->
            <b-row>
              <b-col>
                <CustomCard color="info" title="Operator Ban Actions">
                  tmp
                </CustomCard>
              </b-col>
            </b-row>

            <!-- Current Operator Bans -->
            <b-row>
              <b-col>
                <CustomCard color="secondary" title="Current Operator Bans">
                  tmp
                </CustomCard>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'OperatorBans',
  layout: 'match-page',

  computed: {
    match () {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters['matchSocket/getMatch'](matchID)
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
    operatorBans () {
      if (!this.matchMap) { return }
      try {
        return this.$store.getters['matchSocket/getOperatorBansByMatchMap'](this.matchMap.id)
      } catch {
        return null
      }
    },

    matchMap () {
      return this.matchMaps.filter(m => m.mapName === this.$route.params.mapName)[0]
    }

  }
}
</script>
