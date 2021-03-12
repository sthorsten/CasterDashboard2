<template>
    <div class="hold-transition login-page">

        <div class="login-box">
            <div class="login-logo">
                <a href="/">R6 <b>Caster Dashboard</b></a>
            </div>
            <!-- /.login-logo -->
            <div class="card">
                <div class="card-body login-card-body">
                    <p v-if="confirmed" class="login-box-msg">{{ $t('login.register_confirm') }}</p>
                    <p v-if="!confirmed" class="login-box-msg">{{ $t('login.register_confirm_error') }}</p>

                    <p class="mb-1 text-center">
                        <router-link to="/login">{{ $t('login.sign_in') }}</router-link>
                    </p>
                </div>
                <!-- /.login-card-body -->
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "RegisterConfirm",
    layout: "empty",
    auth: false,

    data() {
        return {
            confirmed: false
        }
    },

    mounted() {
        if (this.user != null || this.token != null){
            this.$axios.$post("/api/register/confirm/", {
                username: this.user,
                token: this.token,
            })
            .then(() => {
                this.confirmed = true
            })
            .catch((error) => {
                console.log(error)
            })
        }
    },

    computed: {
        user() {
            if (!this.$route.query.user) return null
            return this.$route.query.user
        },
        token() {
            if (!this.$route.query.token) return null
            return this.$route.query.token
        }
    },

    methods: {}
}
</script>

<style scoped>

</style>
