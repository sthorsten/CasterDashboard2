<template>
    <div id="app">
        <router-view/>
    </div>
</template>

<script>
export default {
    name: "App",
    computed: {
        loggedIn() {
            return this.$store.state.loggedIn
        }
    },
    created() {
        // Skip Login redirect for all overlays
        if (this.$route.name === "Start Overlay"){
            return
        }
        if (!this.loggedIn && this.$route.name !== "Login") {
            this.$router.push({name: "Login"})
        }
    }
}
</script>

<style lang="scss">

</style>
