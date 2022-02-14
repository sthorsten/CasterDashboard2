<template>
  <div>
    <template v-if="status === 'CREATED'">
      <b-badge variant="secondary" pill>
        Created
      </b-badge>
    </template>

    <template v-if="status === 'PREPARING'">
      <b-badge variant="warning" pill>
        Preparing
      </b-badge>
    </template>

    <template v-if="status === 'OPERATOR_BAN'">
      <b-badge variant="info" pill>
        Operator Ban
      </b-badge>
    </template>

    <template v-if="status === 'PLAYING'">
      <b-badge variant="success" pill>
        Playing
      </b-badge>
    </template>

    <template v-if="status === 'OVERTIME'">
      <b-badge variant="danger" pill>
        Overtime
      </b-badge>
    </template>

    <template v-if="status === 'FINISHED'">
      <b-badge variant="primary" pill>
        Finished
      </b-badge>
    </template>
  </div>
</template>

<script>
export default {
  name: 'MapStatusBadge',

  props: {
    status: {
      type: String,
      default: ''
    }
  }
}
</script>
