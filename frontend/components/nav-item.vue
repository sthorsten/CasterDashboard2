<template>
  <li class="nav-item">
    <a :class="active ? 'nav-link active' : 'nav-link'" :href="link" :target="target">
      <fa-icon v-if="icon" :icon="icon" class="nav-icon" />
      {{ text }}
    </a>
  </li>
</template>

<script>
export default {
  props: {
    link: {
      type: String,
      default: '#'
    },
    icon: {
      type: [Array, String],
      default: null
    },
    text: {
      type: String,
      default: ''
    },
    active: {
      type: Boolean,
      default: false
    },
    target: {
      type: String,
      default: ''
    }
  }
}
</script>
