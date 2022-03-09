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
    },
    operatorBans: {
      type: Array,
      default: []
    }
  },

  computed: {
    isBanned() {
      return this.operatorBans.filter(o => o.operatorIdentifier === this.operator.identifier).length > 0
    },
    sideDisabled() {
      if (this.operator.side === 'ATK') {
        return this.operatorBans.length >= 2
      } else if (this.operator.side === 'DEF') {
        return this.operatorBans.length < 2
      }
    }
  },

  methods: {
    banOperator(id) {
      this.$emit('ban', id)
    }
  }
}

</script>