<template>
  <div class="container">Loading...</div>
</template>

<script>
  export default {
    mounted() {
      this.$router.push({path: "/dashboard/home"})
    },
  }
</script>

<style></style>
