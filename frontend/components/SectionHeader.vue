<script setup lang="ts">

interface Props {
  title: string;
  icon: string;
  breadcrumbs: string[]
}

const { title, icon, breadcrumbs } = defineProps<Props>()

</script>

<template>

  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <div class="fs-3">
            <FaIcon :icon="icon" class="section-header-icon" />
            {{ title }}
          </div>
        </div>
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-end">
            <li v-for="breadcrumb in breadcrumbs" class="breadcrumb-item active">
              {{ breadcrumb }}
            </li>
          </ol>
        </div>
      </div>
    </div>
  </div>

</template>