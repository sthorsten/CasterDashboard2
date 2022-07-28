<script setup lang="ts">
interface Props {
  title: string;
  icon: string;
  breadcrumbs: string[]
}
const { title, icon, breadcrumbs } = defineProps<Props>()
</script>

<template>

  <div class="content-wrapper">
    <SectionHeader :title="title" :icon="icon" :breadcrumbs="breadcrumbs" />
    <div class="content">
      <div class="container-fluid">
        <slot />
      </div>
    </div>

  </div>

</template>