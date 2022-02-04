<template>
  <div>
    <template v-if="status === 'CREATED'">
      <b-badge variant="secondary" pill>
        Created
      </b-badge>
    </template>

    <template v-if="status === 'MAP_BAN'">
      <b-badge variant="warning" pill>
        Map Ban
      </b-badge>
    </template>

    <template v-if="status === 'PLAYING'">
      <b-badge variant="success" pill>
        Playing
      </b-badge>
    </template>

    <template v-if="status === 'CLOSED'">
      <b-badge variant="primary" pill>
        Closed
      </b-badge>
    </template>
  </div>
</template>

<script>
export default {
  props: {
    status: {
      type: String,
      default: ''
    }
  }
}
</script>
