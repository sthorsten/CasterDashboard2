<template>
    <b-navbar type="dark" variant="dark" class="shadow">

        <b-navbar-brand href="/" class="ml-3">
            <strong>R6</strong> Caster Dashboard
        </b-navbar-brand>

        <b-navbar-nav class="ml-auto mr-2">
            <li class="nav-item">
                <a href="javascript:void(0);" class="nav-link">
                    <i class="fas fa-question-circle"></i>
                    Wiki
                </a>
            </li>
            <li class="nav-item">
                <a href="javascript:void(0);" class="nav-link">
                    <i class="fas fa-list"></i>
                    Changelog
                </a>
            </li>
        </b-navbar-nav>

        <b-navbar-nav>

            <!-- User menu -->
            <b-dd variant="dark" right>
                <template #button-content>
                    <i class="fas fa-lg fa-user-circle text-white mr-1"></i>
                    <template v-if="user">
                        {{ user.username }}
                    </template>
                    <template v-else>
                    <span>
                        UserName
                    </span>
                    </template>
                </template>


                <template v-if="user">
                    <template v-if="user.is_staff">
                        <b-dd-header>
                            <i class="fa fas fa-wrench"></i>
                            {{ $t('navigation.admin') }}
                        </b-dd-header>
                        <b-dd-item class="text-center" :href="this.$store.state.backendURL + '/admin'" target="_blank">
                            Django Admin
                        </b-dd-item>
                        <b-dd-item class="text-center" :href="this.$store.state.backendURL + '/api'" target="_blank">
                            {{ $t('navigation.api_access') }}
                        </b-dd-item>
                        <b-dd-item class="text-center">
                            {{ $t('navigation.league_admin') }}
                        </b-dd-item>
                        <b-dd-divider></b-dd-divider>
                    </template>
                    <b-dd-header>
                        <i class="fa fas fa-user-cog"></i>
                        {{ $t('navigation.user_settings') }}
                    </b-dd-header>
                    <b-dd-item class="text-center" :to="{name: 'Profile', params:{'username': this.$store.state.user.username}}">
                        {{ $t('navigation.profile') }}
                    </b-dd-item>
                    <b-dd-item class="text-center" @click="logoutUser">
                        {{ $t('navigation.log_out') }}
                    </b-dd-item>
                </template>
            </b-dd>

        </b-navbar-nav>
    </b-navbar>
</template>

<script>

export default {
    name: "Navbar",
    data: function () {
        return {}
    },
    computed: {
        user() {
            return this.$store.state.user
        }
    },
    methods: {
        logoutUser() {
            this.$store.commit('setUser', null)
            this.$store.commit('setUserToken', "")
            this.$store.commit('setLoggedIn', false)
            this.$toast.success("You have been logged out!", "Logout successful")
            this.$router.push({name: "Login"})
        }
    }
}
</script>

<style scoped>

</style>
