<template>
    <div class="hold-transition login-page">

        <b-overlay :show="loginLoading" variant="dark" :opacity=0.9 class="text-white">
            <div class="login-box">
                <div class="login-logo">
                    <a href="/">R6 <b>Caster Dashboard</b></a>
                </div>
                <!-- /.login-logo -->
                <div class="card">
                    <div class="card-body login-card-body">
                        <p class="login-box-msg">{{ $t('login.sign_in') }}</p>


                        <b-form @submit.prevent="onSubmit" novalidate>
                            <b-form-group class="mb-3">
                                <b-input-group>
                                    <b-form-input v-model="username" :placeholder="$t('generic.username')"
                                                  :state="this.$v.username.$error ? false : null">
                                    </b-form-input>
                                    <b-input-group-append>
                                        <b-input-group-text>
                                            <span class="fas fa-user"></span>
                                        </b-input-group-text>
                                    </b-input-group-append>
                                    <b-form-invalid-feedback :state="!this.$v.username.$error">
                                        {{ $t('login.enter_username') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <b-form-group class="mb-3">
                                <b-input-group>
                                    <b-form-input v-model="password" type="password" :placeholder="$t('generic.password')"
                                                  :state="this.$v.password.$error ? false : null">
                                    </b-form-input>
                                    <b-input-group-append>
                                        <b-input-group-text>
                                            <span class="fas fa-lock"></span>
                                        </b-input-group-text>
                                    </b-input-group-append>
                                    <b-form-invalid-feedback :state="!this.$v.password.$error">
                                        {{ $t('login.enter_password') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <div class="row">
                                <!-- /.col -->
                                <div class="col-12">
                                    <b-button type="submit" variant="primary" class="btn-block">{{ $t('login.sign_in') }}</b-button>
                                </div>
                                <!-- /.col -->
                            </div>
                        </b-form>

                        <div class="social-auth-links text-center mb-3">
                            <p class="text-uppercase">- {{ $t('generic.or') }} -</p>
                        </div>
                        <!-- /.social-auth-links -->

                        <p class="mb-1 text-center">
                            <a href="#">{{ $t('login.forgot_password') }}</a>
                        </p>
                        <p class="mb-0 text-center">
                            <a href="/register" class="text-center">{{ $t('login.register') }}</a>
                        </p>
                    </div>
                    <!-- /.login-card-body -->
                </div>
            </div>
        </b-overlay>
    </div>
</template>

<script>
import required from "vuelidate/lib/validators/required";

export default {
    name: "login",
    layout: "empty",

    data() {
        return {
            loginLoading: false,
            username: null,
            password: null,
        }
    },

    validations: {
        username: {required},
        password: {required}
    },

    mounted() {
        console.log(this.$config.baseURL)
        // Redirect if already logged in
        if (this.$auth.loggedIn){
            this.loginRedirect()
        }
    },

    methods: {
        loginRedirect(){
            if (this.$route.query.next) {
                this.$router.push(this.$route.query.next)
            } else {
                this.$router.push("/dashboard/home")
            }
        },

        onSubmit() {
            this.$v.$touch()

            if (this.$v.$invalid) {
                return
            }

            this.loginLoading = true

            this.$auth.loginWith('local', {
                data: {
                    username: this.username,
                    password: this.password
                }
            }).then((response) => {
                console.log(response.data)
                this.$auth.setUser(response.data.user)

                this.$toast.success(this.$t('login.welcome', {user: this.username}), this.$t('login.login_success'))
                this.loginRedirect()

            }).catch((error) => {
                console.log(error)
                this.$toast.error(this.$t('login.invalid_credentials'), this.$t('login.login_failed'))
            })
        }
    },
}
</script>

<style scoped>

</style>
