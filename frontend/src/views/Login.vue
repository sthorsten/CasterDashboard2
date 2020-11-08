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

                        <validation-observer ref="observer" v-slot="{ handleSubmit }">
                            <b-form @submit.stop.prevent="handleSubmit(onSubmit)" novalidate>
                                <validation-provider name="username" :rules="{ required: true }" v-slot="validationContext">
                                    <b-form-group class="mb-3">
                                        <b-input-group>
                                            <b-form-input id="username" v-model="username" :placeholder="$t('generic.username')"
                                                          aria-describedby="username-feedback" :state="getValidationState(validationContext)">
                                            </b-form-input>
                                            <b-input-group-append>
                                                <b-input-group-text>
                                                    <span class="fas fa-user"></span>
                                                </b-input-group-text>
                                            </b-input-group-append>
                                            <b-form-invalid-feedback id="username-feedback">
                                                {{ $t('login.enter_username') }}
                                            </b-form-invalid-feedback>
                                        </b-input-group>
                                    </b-form-group>
                                </validation-provider>

                                <validation-provider name="password" :rules="{ required: true }" v-slot="validationContext">
                                    <b-form-group class="mb-3">
                                        <b-input-group>
                                            <b-form-input v-model="password" type="password" :placeholder="$t('generic.password')"
                                                          aria-describedby="password-feedback" :state="getValidationState(validationContext)">
                                            </b-form-input>
                                            <b-input-group-append>
                                                <b-input-group-text>
                                                    <span class="fas fa-lock"></span>
                                                </b-input-group-text>
                                            </b-input-group-append>
                                            <b-form-invalid-feedback id="password-feedback">
                                                {{ $t('login.enter_password') }}
                                            </b-form-invalid-feedback>
                                        </b-input-group>
                                    </b-form-group>
                                </validation-provider>

                                <div class="row">
                                    <!-- /.col -->
                                    <div class="col-12">
                                        <b-button type="submit" variant="primary" class="btn-block">{{ $t('login.sign_in') }}</b-button>
                                    </div>
                                    <!-- /.col -->
                                </div>
                            </b-form>
                        </validation-observer>

                        <div class="social-auth-links text-center mb-3">
                            <p class="text-uppercase">- {{ $t('generic.or') }} -</p>
                        </div>
                        <!-- /.social-auth-links -->

                        <p class="mb-1 text-center">
                            <a href="#">{{ $t('login.forgot_password') }}</a>
                        </p>
                        <p class="mb-0 text-center">
                            <a href="/register/" class="text-center">{{ $t('login.register') }}</a>
                        </p>
                    </div>
                    <!-- /.login-card-body -->
                </div>
            </div>
        </b-overlay>
    </div>
</template>

<script>

import axios from "axios";

export default {
    name: "Login",
    data() {
        return {
            username: "",
            password: "",
            loginLoading: false
        }
    },
    methods: {
        getValidationState({dirty, validated, valid = null}) {
            return dirty || validated ? valid : null;
        },
        getUserToken() {
            this.loginLoading = true
            axios.post(this.$store.state.backendURL + '/api/api-token-auth/', {
                username: this.username,
                password: this.password
            }).then((response) => {
                this.$store.commit('setUserToken', response.data.token)
                this.logInUser(response.data.token)
            }).catch((error) => {
                if (error.response.status === 400) {
                    this.$toast.error(this.$t('login.invalid_credentials'), this.$t('login.login_failed'))
                }
            }).then(() => {
                this.loginLoading = false
            })
        },
        logInUser(token) {
            this.loginLoading = true;
            axios.get(this.$store.state.backendURL + '/api/user/current/', {
                headers: {
                    "Authorization": "Token " + token
                }
            }).then((response) => {
                this.$store.commit('setUser', response.data)
                this.$store.commit('setLoggedIn', true)

                if (this.$route.query.next)
                    this.$router.push(this.$route.query.next)
                else
                    this.$router.push({name: "Home"})
                this.$toast.success(this.$t('login.welcome', {user: response.data.username}), this.$t('login.login_success'))
            })
        },
        onSubmit() {
            this.getUserToken()
        }
    },
}
</script>

<style scoped>

</style>