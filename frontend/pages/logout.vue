<template>
  <div></div>
</template>

<script>
  export default {
    name: "logout.vue",

    mounted() {
      this.$auth.logout()
      this.$toast.success("You have been logged out!", "Logout successful")
      this.$router.push("/login")
    },
  }
</script>

<style scoped></style>
