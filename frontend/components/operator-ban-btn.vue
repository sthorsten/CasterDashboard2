<template>
  <b-btn
    :disabled="isBanned || sideDisabled"
    :variant="isBanned ? 'danger' : 'secondary'"
    @click="banOperator(operator.id)"
    block
    style="margin: 0.15rem"
  >
    <div class="d-flex">
      <R6OperatorIcon :operator="operator.identifier" height="25" width="25" />
      <span class="text-center w-100">{{ operator.name }}</span>
    </div>
  </b-btn>
</template>

<script>

export default {
  props: {
    operator: {
      type: Object,
      default: '_none'
    }
  },

  computed: {
    isBanned() {
      return this.operatorBans.findIndex(o => o.operatorIdentifier === this.operator.identifier) !== -1
    },
    sideDisabled() {
      if (this.operator.side === 'ATK') {
        return this.operatorBans.length >= 2
      } else if (this.operator.side === 'DEF') {
        return this.operatorBans.length < 2 || this.operatorBans.length >= 4
      }
    },

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
      return this.matchMaps.filter(m => m.mapName === this.$route.params.mapName)[0]
    },
    operatorBans() {
      if (!this.matchMap) {
        return
      }
      try {
        return this.$store.getters["matchSocket/getOperatorBansByMatchMap"](this.matchMap.id)
      }
      catch {
        return null
      }
    },
  },

  methods: {
    banOperator(id) {
      this.$emit('ban', id)
    }
  }
}

</script>