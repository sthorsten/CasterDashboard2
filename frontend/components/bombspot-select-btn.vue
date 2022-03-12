<template>
  <b-btn
    :variant="selected ? 'primary' : 'outline-primary'"
    block
    class="mt-2 d-flex align-items-center"
    @click="clicked"
  >
    <b-badge :variant="selected ? 'light' : 'primary'" pill>{{ bombspot.floor }}</b-badge>
    <span class="w-100 ml-auto">{{ bombspot.name }}</span>
  </b-btn>
</template>

<script>
export default {
  name: 'BombspotSelectBtn',
  props: {
    bombspot: {
      type: Object,
      default: {}
    },
    selected: {
      type: Boolean,
      default: false
    }
  },

  methods: {
    clicked() {
      this.$emit('clicked')
    }
  }
}
</script>