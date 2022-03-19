<template>
  <b-table striped small :items="rounds" :fields="fields">
    <template #cell(roundNo)="data">
      <b-badge pill>{{ data.item.roundNo }}</b-badge>
    </template>
    <template #cell(bombSpotName)="data">
      <template v-if="getBombSpotById(data.item.bombSpot)">
        <b-badge pill variant="primary" class="mr-1">{{ getBombSpotById(data.item.bombSpot).floor }}</b-badge>
        {{ getBombSpotById(data.item.bombSpot).name }}
      </template>
    </template>
    <template #cell(openingFragTeamName)="data">
      <template v-if="data.item.openingFragTeam">
        <img
          :src="$store.getters['mainSocket/getTeamLogo'](data.item.openingFragTeam, true)"
          height="20"
          width="20"
          alt="opening frag team logo"
        />
        {{ data.item.openingFragTeamName }}
      </template>
      <template v-else>
        <i>None selected</i>
      </template>
    </template>
    <template #cell(winTeamName)="data">
      <img
        :src="$store.getters['mainSocket/getTeamLogo'](data.item.winTeam, true)"
        height="20"
        width="20"
        alt="win team logo"
      />
      {{ data.item.winTeamName }}
    </template>
    <template #cell(winType)="data">
      <b-badge v-if="data.item.winType === 'KILLS'" pill variant="danger">Kills</b-badge>
      <b-badge v-if="data.item.winType === 'DEFUSER_PLANTED'" pill variant="success">Defuser Planted</b-badge>
      <b-badge
        v-if="data.item.winType === 'DEFUSER_DISABLED'"
        pill
        variant="warning"
      >Defuser Disabled</b-badge>
      <b-badge v-if="data.item.winType === 'TIME'" pill variant="secondary">Time</b-badge>
    </template>
    <template #cell(notes)="data">
      <template v-if="data.item.notes">
        <span v-for="line in data.item.notes.split('\n')">
          {{ line }}
          <br />
        </span>
      </template>
      <template v-else>
        <i>None</i>
      </template>
    </template>
  </b-table>
</template>

<script>

export default {
  name: 'RoundTable',

  props: {
    matchMapId: {
      type: Number,
      default: -1
    }
  },

  data() {
    return {
      fields: [
        {
          key: 'roundNo',
          label: '#'
        },
        {
          key: 'bombSpotName',
          label: 'Bomb Spot'
        },
        {
          key: 'openingFragTeamName',
          label: 'Opening Frag Team'
        },
        {
          key: 'winTeamName',
          label: 'Win Team'
        },
        {
          key: 'winType',
          label: 'Win Type'
        },
        'notes'
      ]
    }
  },

  computed: {
    matchMaps() {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters["matchSocket/getMatchMapsByMatch"](matchID)
      }
      catch {
        return null
      }
    },
    matchMap() {
      if (this.matchMapId === -1) return []
      return this.matchMaps.filter(m => m.id === this.matchMapId)[0]
    },
    bombSpots() {
      if (!this.matchMap) return []
      return this.$store.getters["coreSocket/getBombSpotsByMap"](this.matchMap.map)
    },
    rounds() {
      if (!this.matchMap) return []
      return this.$store.getters["matchSocket/getRoundsByMatchMap"](this.matchMap.id)
    },
  },

  methods: {
    getBombSpotById(id) {
      return this.bombSpots.find(b => b.id === id)
    }
  }
}


</script>