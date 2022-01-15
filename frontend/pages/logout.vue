<template>
  <div>
    Logging out...
  </div>
</template>

<script>
export default {
  auth: false,

  mounted () {
    this.$auth.logout()
    this.$toast.info('Logout successful. See you next time!')
    this.$router.push('/login')
  }
}
</script>
