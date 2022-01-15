<template>
  <div>
    <ContentHeader
      icon="list-ul"
      title="Match Overview"
      :breadcrumb-items="['Dashboard', 'Matches', $route.params.matchID, 'Overview']"
    />
    <ContentContainer v-if="match">
      <b-container fluid>
        Status: <MatchStatusBadge :status="match.status" />
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'MatchOverview',
  layout: 'match-page',

  computed: {
    match () {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters['matchSocket/getMatch'](matchID)
      } catch {
        return null
      }
    }
  }

}
</script>
