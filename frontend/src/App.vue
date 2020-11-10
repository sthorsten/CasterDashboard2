<template>
    <div id="app">
        <router-view/>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "App",
    computed: {
        loggedIn() {
            return this.$store.state.loggedIn
        }
    },
    created() {
        // Skip Login redirect for all overlays
        if (this.$route.name === "Start Overlay") {
            return
        }
        if (!this.loggedIn && this.$route.name !== "Login") {
            this.$toast.warning(this.$t('login.login_required'))
            this.$router.push({name: "Login", query: {"next": this.$route.fullPath}})
        }

        // Get Version
        axios.get(`${this.$store.state.backendURL}/api/version/`, this.$store.getters.authHeader
        ).then((response) => {
            this.$store.commit('setVersion', response.data.version)
        })
    }
}
</script>

<style lang="scss">

</style>
