<template>
  <div class="h-100 d-flex justify-content-center align-items-center">
    <span v-if="mapBan" class="text-center">
      <b>{{ map.name }}</b>
      <br>

      <template v-if="mapBan.isDecider">
        <b-badge pill :variant="mapBan.type === 'BAN' ? 'danger' : 'success'">
          {{ mapBan.type === 'BAN' ? 'DEFAULT BAN' : 'DECIDER MAP' }}
        </b-badge>
      </template>

      <template v-else>
        <b-badge pill :variant="mapBan.type === 'BAN' ? 'danger' : 'success'">
          {{ mapBan.type }}
        </b-badge>

        <br>

        <img
          :src="$store.getters['mainSocket/getTeamLogo'](mapBan.team, true)"
          height="20"
          width="20"
          alt="team logo"
        >

        {{ mapBan.teamName }}

      </template>
    </span>

    <span v-else class="text-center">
      <b>{{ map.name }}</b>
      <br>
      <i>Not selected yet.</i>
    </span>
  </div>
</template>

<script>
export default {
  name: 'MapBanText',

  props: {
    map: {
      type: Object,
      default: null
    },
    mapBan: {
      type: Object,
      default: null
    }
  },

  computed: {
    isBan () {
      return (this.mapBan !== null) && this.mapBan.type === 'BAN'
    }
  }

}
</script>
