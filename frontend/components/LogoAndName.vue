<script setup lang="ts">

interface Props {
  name: string
  logoURL: string
  logoWidth?: number,
  logoHeight?: number
}

const { name, logoURL, logoWidth = 25, logoHeight = 25 } = defineProps<Props>()

</script>

<template>

  <img v-if="logoURL" :src="logoURL" alt="Logo" :width="logoWidth" :heigh="logoHeight" class="mr-1 mt-n0.5">
  <span>
    {{ name }}
  </span>

</template>