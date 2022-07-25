<script setup lang="ts">

const props = defineProps<{
  title: string;
  icon: string;
}>()

</script>

<template>

  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1>
            <FaIcon :icon="props.icon" class="section-header-icon" />
            {{ props.title }}
          </h1>
        </div>
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item active">
              Home
            </li>
          </ol>
        </div>
      </div>
    </div>
  </div>

</template>