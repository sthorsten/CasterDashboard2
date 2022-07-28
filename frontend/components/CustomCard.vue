<script setup lang="ts">

interface Props {
  title: string,
  color?: string,
  icon?: string,
  outline?: boolean,
  divider?: boolean,
  footer?: boolean
}

const {
  title,
  color = "primary",
  icon,
  outline = true,
  divider = true,
  footer = false
} = defineProps<Props>()

const colorClass = computed(() => {
  return 'card-' + color
})

</script>

<template>
  <div class="card mb-3" :class="[colorClass, { 'card-outline-all': outline }]">
    <div class="card-body">
      <h5 class="card-title card-title-upper">
        <fa-icon v-if="icon" :icon="icon" class="mr-1" />
        {{ title }}
      </h5>
      <template v-if="divider">
        <br>
        <div class="card-divider" />
      </template>
      <template v-else>
        <br>
        <br>
      </template>
      <slot />
    </div>
    <template v-if="footer">
      <div class="card-footer bg-gray-700">
        <slot name="card-footer" />
      </div>
    </template>
  </div>
</template>

<style lang="scss">
@import 'bootstrap/scss/functions';
@import 'bootstrap/scss/variables';

@each $name,
$color in $theme-colors {
  .card-#{$name}.card-outline-all {
    border: 3px solid $color;
  }
}

.card-title-upper {
  text-transform: uppercase !important;
  font-weight: bold !important;
  font-size: 0.9rem !important;
  margin-bottom: 0.5em !important;
}

div.card-divider {
  border-bottom: 1px solid #343a40;
  margin-top: 0;
  margin-bottom: 1em;
}
</style>