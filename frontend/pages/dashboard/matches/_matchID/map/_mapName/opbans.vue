<template>
  <div>
    <ContentHeader
      icon="users-slash"
      title="Operator Bans"
      :breadcrumb-items="['Dashboard', 'Matches', $route.params.matchID, $route.params.mapName, 'Operator Bans']"
    />
    <ContentContainer v-if="match != null && matchMap != null">
      <b-container fluid />
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'OperatorBans',
  layout: 'match-page'
}
</script>
