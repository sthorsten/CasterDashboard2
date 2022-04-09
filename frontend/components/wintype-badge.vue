<template>
  <div>
    <template v-if="status === 'NONE'">
      <b-badge variant="secondary" pill> None </b-badge>
    </template>

    <template v-if="status === 'BLUE_WIN'">
      <b-badge variant="primary" pill> Blue Win </b-badge>
    </template>

    <template v-if="status === 'BLUE_OT_WIN'">
      <b-badge variant="primary" pill> Blue Overtime Win </b-badge>
    </template>

    <template v-if="status === 'ORANGE_WIN'">
      <b-badge class="bg-orange" pill> Orange Win </b-badge>
    </template>

    <template v-if="status === 'ORANGE_OT_WIN'">
      <b-badge variant="primary" pill> Orange Overtime Win </b-badge>
    </template>

    <template v-if="status === 'DRAW'">
      <b-badge variant="warning" pill> Draw </b-badge>
    </template>
  </div>
</template>

<script>
export default {
  name: 'WintypeBadge',

  props: {
    status: {
      type: String,
      default: ''
    }
  }
}
</script>
