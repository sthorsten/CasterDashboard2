<template>
  <div>
    <template v-if="mapStatus === 'NONE'">
      <b-badge variant="secondary" pill>
        None
      </b-badge>

      <template v-if="mapStatus === 'BLUE_WIN'">
        <b-badge variant="primary" pill>
          Blue Win
        </b-badge>
      </template>

      <template v-if="mapStatus === 'BLUE_OT_WIN'">
        <b-badge variant="primary" pill>
          Blue Overtime Win
        </b-badge>
      </template>

      <template v-if="mapStatus === 'ORANGE_WIN'">
        <b-badge class="bg-orange" pill>
          Orange Win
        </b-badge>
      </template>

      <template v-if="mapStatus === 'BLUE_OT_WIN'">
        <b-badge variant="primary" pill>
          Orange Overtime Win
        </b-badge>

        <template v-if="mapStatus === 'DRAW'">
          <b-badge variant="warning" pill>
            Draw
          </b-badge>
        </template>
      </template>
    </template>
  </div>
</template>

<script>
export default {
  name: 'WinTypeBadge',

  props: {
    mapStatus: {
      type: String,
      default: ''
    }
  }
}
</script>
