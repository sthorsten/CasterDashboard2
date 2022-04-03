<template>
  <div>
    <ContentHeader
      icon="trophy"
      title="Leagues"
      :breadcrumb-items="['Dashboard', 'Main', 'Leagues']"
    />
    <ContentContainer>
      <b-container fluid>
        <CustomCard title="Leagues">
          <b-table small dark striped :items="leagues" :fields="leagueFields">
            <template #cell(logoSmall)="data">
              <img :src="data.item.logoSmall" width="25" height="25" />
            </template>
          </b-table>
        </CustomCard>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'Leagues',
  layout: 'main-page',

  data() {
    return {
      leagueFields: [
        {
          key: 'id',
          label: 'ID'
        },
        'name',
        'logoSmall'
      ]
    }
  },

  computed: {
    leagues() {
      return this.$store.state.mainSocket.leagues
    }
  }
}
</script>

<style lang="scss">
@import "~/assets/style/vue-select.scss";
</style>
