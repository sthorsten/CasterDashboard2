<script setup lang="ts">
const props = defineProps<{
  title: string;
  icon: string;
}>()
</script>

<template>

  <div class="content-wrapper">
    <SectionHeader :title="props.title" :icon="props.icon" />
    <section class="content">
      <div class="container-fluid">
        <slot />
      </div>
    </section>

  </div>

</template>