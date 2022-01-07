<template>
  <div>
    Login...

    <form>
      Username: <input @input="username = value">
      <br>
      Password: <input :value="password" type="password">
    </form>

    <button @click="login">
      Login
    </button>

    <a href="/">Link</a>
  </div>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login () {
      const data = {
        username: 'admin',
        password: 'caster_dashboard_2'
      }
      await this.$auth.loginWith('local', { data })
    }
  }

}
</script>
