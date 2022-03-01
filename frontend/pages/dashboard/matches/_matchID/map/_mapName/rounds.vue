<template>
  <div>
    <ContentHeader
      icon="play-circle"
      title="Rounds"
      :breadcrumb-items="['Dashboard', 'Matches', $route.params.matchID, $route.params.mapName, 'Rounds']"
    />
    <ContentContainer v-if="match != null && matchMap != null">
      <b-container fluid />
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'Rounds',
  layout: 'match-page'
}
</script>
