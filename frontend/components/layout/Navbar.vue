<template>
    <b-navbar type="dark" variant="dark" class="shadow">

        <b-navbar-brand href="/" class="ml-3">
            <strong>R6</strong> Caster Dashboard
        </b-navbar-brand>

        <b-navbar-nav class="ml-auto mr-2">
            <li class="nav-item">
                <a href="https://github.com/sthorsten/CasterDashboard2/wiki" target="_blank" class="nav-link">
                    <i class="fas fa-question-circle"></i>
                    Wiki
                </a>
            </li>
            <li class="nav-item">
                <a href="https://github.com/sthorsten/CasterDashboard2/blob/master/CHANGELOG.md" target="_blank" class="nav-link">
                    <i class="fas fa-list"></i>
                    Changelog
                </a>
            </li>
            <li class="nav-item">
                <a href="https://github.com/sthorsten/CasterDashboard2" target="_blank" class="nav-link">
                    <i class="fab fa-github"></i>
                    GitHub
                </a>
            </li>
        </b-navbar-nav>

        <b-navbar-nav>

            <!-- User menu -->
            <b-dd variant="dark" right>
                <template #button-content>
                    <i class="fas fa-lg fa-user-circle text-white mr-1"></i>
                    <template v-if="$auth.loggedIn">
                        {{ $auth.user.username }}
                    </template>
                    <template v-else>
                    <span>
                        UserName
                    </span>
                    </template>
                </template>

                <template v-if="$auth.loggedIn">
                    <template v-if="$auth.user.is_staff">
                        <b-dd-header>
                            <i class="fa fas fa-wrench"></i>
                            {{ $t('navigation.admin') }}
                        </b-dd-header>
                        <b-dd-item class="text-center" :href="this.$config.baseURL + '/admin'" target="_blank">
                            Django Admin
                        </b-dd-item>
                        <b-dd-item class="text-center" :href="this.$config.baseURL + '/api'" target="_blank">
                            {{ $t('navigation.api_access') }}
                        </b-dd-item>
                        <b-dd-item class="text-center" to="/dashboard/settings/league-admin">
                            {{ $t('navigation.league_admin') }}
                        </b-dd-item>
                        <b-dd-divider></b-dd-divider>
                    </template>
                    <b-dd-header>
                        <i class="fa fas fa-user-cog"></i>
                        {{ $t('navigation.user_settings') }}
                    </b-dd-header>
                    <b-dd-item class="text-center" to="/dashboard/settings/profile">
                        {{ $t('navigation.profile') }}
                    </b-dd-item>
                    <b-dd-item class="text-center" to="/logout">
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
    methods: {
        logoutUser() {
            this.$auth.logout()
            this.$toast.success("You have been logged out!", "Logout successful")
            this.$router.push("/login")
        }
    }
}
</script>

<style scoped>

</style>
