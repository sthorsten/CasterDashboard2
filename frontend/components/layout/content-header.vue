<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">
            <fa-icon :icon="icon" />
            {{ title }}
          </h1>
        </div>

        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="mr-2">
              <fa-icon icon="chevron-circle-right" style="color: #adb5bd" />
            </li>
            <li v-for="item in breadcrumbItems" :key="item" class="breadcrumb-item active">
              {{ item }}
            </li>
          </ol>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    icon: {
      type: [String, Array],
      default: null
    },
    title: {
      type: String,
      default: ''
    },
    breadcrumbItems: {
      type: Array,
      default: null
    }
  }
}
</script>
