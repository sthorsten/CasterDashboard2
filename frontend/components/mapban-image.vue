<template>
  <div v-if="mapBan" :class="isBan ? 'border-danger' : 'border-success'" class="rounded border">
    <img
      class="w-100"
      :src="currentMap.image"
      :style="isBan ? 'filter: brightness(0.3)' : ''"
    />
  </div>

  <div v-else class="rounded border border-secondary">
    <img class="w-100" :src="currentMap.image" />
  </div>
</template>

<script>
export default {
  name: 'MapbanImage',

  props: {
    mapName: {
      type: String,
      default: ''
    },
    mapBan: {
      type: Object,
      default: null
    }
  },

  computed: {
    isBan() {
      return (this.mapBan !== null) && this.mapBan.type === 'BAN'
    },
    maps() {
      return this.$store.state.coreSocket.maps
    },
    currentMap() {
      return this.maps.find(m => m.name === this.mapName)
    }
  }
}
</script>

<style scoped>
.border {
  border-width: 2px !important;
}
</style>
