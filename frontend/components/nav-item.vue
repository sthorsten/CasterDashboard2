<template>
  <li class="nav-item">
    <NuxtLink v-if="nuxtLink" class="nav-link" :to="link" exact :active="active">
      <fa-icon v-if="icon" :icon="icon" class="nav-icon" />
      <template v-if="inline">{{ text }}</template>
      <p v-else>{{ text }}</p>
    </NuxtLink>
    <a v-else :class="active ? 'nav-link active' : 'nav-link'" :href="link" :target="target">
      <fa-icon v-if="icon" :icon="icon" class="nav-icon" />
      <template v-if="inline">{{ text }}</template>
      <p v-else>{{ text }}</p>
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
    },
    nuxtLink: {
      type: Boolean,
      default: false
    },
    inline: {
      type: Boolean,
      default: false
    }
  }
}
</script>
