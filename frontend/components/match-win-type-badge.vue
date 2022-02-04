<template>
  <div>
    <template v-if="status === 'NONE'">
      <b-badge variant="secondary" pill>
        None
      </b-badge>

      <template v-if="status === 'BLUE_WIN'">
        <b-badge variant="primary" pill>
          Map Ban
        </b-badge>
      </template>

      <template v-if="status === 'ORANGE_WIN'">
        <b-badge class="bg-orange" pill>
          Map Ban
        </b-badge>
      </template>

      <template v-if="status === 'DRAW'">
        <b-badge variant="warning" pill>
          Draw
        </b-badge>
      </template>
    </template>
  </div>
</template>

<script>
export default {
  name: 'MatchWinTypeBadge',

  props: {
    status: {
      type: String,
      default: ''
    }
  }
}
</script>
