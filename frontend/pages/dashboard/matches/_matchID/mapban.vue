<template>
  <div>
    <ContentHeader
      icon="map"
      title="Map Pick & Ban"
      :breadcrumb-items="['Dashboard', 'Matches', $route.params.matchID, 'MapBan']"
    />
    <ContentContainer v-if="match" />
  </div>
</template>

<script>
export default {
  name: 'MapBan',
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
