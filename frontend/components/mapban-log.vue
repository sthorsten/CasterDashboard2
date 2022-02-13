<template>
  <b-container>
    <b-row>
      <b-col cols="4">
        <b-badge variant="secondary" pill>
          {{ mapBan.order }}
        </b-badge>
        <b-badge :variant="mapBan.type === 'BAN' ? 'danger' : 'success'" pill>
          {{ mapBan.type }}
        </b-badge>
        <span>
          <b>{{ mapBan.mapName }}</b>
        </span>
      </b-col>
      <b-col cols="8">
        <span v-if="mapBan.team">
          <img
            :src="$store.getters['mainSocket/getTeamLogo'](mapBan.team, true)"
            height="20"
            width="20"
            alt="team logo"
          >
          {{ mapBan.teamName }}
        </span>
        <span v-else>
          <i>{{ mapBan.type === 'BAN' ? 'Default Ban' : 'Decider Map' }}
          </i>
        </span>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'MapBanLog',
  props: {
    mapBan: {
      type: Object,
      default: null
    }
  }

}
</script>
