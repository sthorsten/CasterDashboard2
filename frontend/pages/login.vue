<template>
  <div>
    <p class="login-box-msg">
      Welcome to the Caster Dashboard!
      <br />
      Sign in below to get started.
    </p>

    <b-input-group>
      <b-form-input v-model="username" placeholder="Username" />
      <b-input-group-append>
        <b-input-group-text>
          <fa-icon icon="user" />
        </b-input-group-text>
      </b-input-group-append>
    </b-input-group>

    <b-input-group class="mt-2">
      <b-form-input v-model="password" placeholder="Password" type="password" />
      <b-input-group-append>
        <b-input-group-text>
          <fa-icon icon="lock" />
        </b-input-group-text>
      </b-input-group-append>
    </b-input-group>

    <b-btn block variant="primary" class="mt-2" @click="login"> Login </b-btn>
  </div>
</template>

<script>
export default {
  name: "Login",
  layout: "login-page",
  auth: false,

  head() {
    return {
      title: "Login"
    }
  },

  data() {
    return {
      username: "",
      password: "",
    }
  },

  methods: {
    async login() {
      const data = {
        username: this.username,
        password: this.password,
      }

      try {
        await this.$auth.loginWith("local", { data })
        if (this.$auth.user.first_name) {
          this.$toast.success(
            `Login successful. Welcome ${this.$auth.user.first_name}!`
          )
        } else {
          this.$toast.success(
            `Login successful. Welcome ${this.$auth.user.username}!`
          )
        }
        if (this.$store.state.auth.redirect) {
          this.$router.push(this.$store.state.auth.redirect)
        } else {
          this.$router.push("/dashboard/home")
        }
      } catch {
        this.$toast.error(
          "Login failed. Check your credentials and try again!"
        )
      }
    },
  },
};
</script>
