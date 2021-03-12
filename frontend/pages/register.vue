<template>
    <div class="hold-transition login-page">

        <div class="login-box">
            <div class="login-logo">
                <a href="/">R6 <b>Caster Dashboard</b></a>
            </div>
            <!-- /.login-logo -->
            <div class="card">
                <div class="card-body login-card-body">
                    <p class="login-box-msg">{{ $t('login.register') }}</p>

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
                                    {{ $t('login.enter_new_password') }}
                                </b-form-invalid-feedback>
                            </b-input-group>
                        </b-form-group>

                        <b-form-group class="mb-3">
                            <b-input-group>
                                <b-form-input v-model="passwordConfirm" type="password"
                                              :placeholder="$t('generic.password')"
                                              :state="this.$v.passwordConfirm.$error ? false : null">
                                </b-form-input>
                                <b-input-group-append>
                                    <b-input-group-text>
                                        <span class="fas fa-lock"></span>
                                    </b-input-group-text>
                                </b-input-group-append>
                                <b-form-invalid-feedback :state="!this.$v.passwordConfirm.$error">
                                    {{ $t('login.confirm_password') }}
                                </b-form-invalid-feedback>
                            </b-input-group>
                        </b-form-group>

                        <b-form-group class="mb-3">
                            <b-input-group>
                                <b-form-input v-model="firstName" :placeholder="$t('generic.first_name')"
                                              :state="this.$v.firstName.$error ? false : null">
                                </b-form-input>
                                <b-input-group-append>
                                    <b-input-group-text>
                                        <span class="fas fa-user"></span>
                                    </b-input-group-text>
                                </b-input-group-append>
                                <b-form-invalid-feedback :state="!this.$v.firstName.$error">
                                    {{ $t('login.enter_first_name') }}
                                </b-form-invalid-feedback>
                            </b-input-group>
                        </b-form-group>

                        <b-form-group class="mb-3">
                            <b-input-group>
                                <b-form-input v-model="lastName" :placeholder="$t('generic.last_name')"
                                              :state="this.$v.lastName.$error ? false : null">
                                </b-form-input>
                                <b-input-group-append>
                                    <b-input-group-text>
                                        <span class="fas fa-user"></span>
                                    </b-input-group-text>
                                </b-input-group-append>
                                <b-form-invalid-feedback :state="!this.$v.lastName.$error">
                                    {{ $t('login.enter_last_name') }}
                                </b-form-invalid-feedback>
                            </b-input-group>
                        </b-form-group>

                        <b-form-group class="mb-3">
                            <b-input-group>
                                <b-form-input v-model="email" type="email" :placeholder="$t('profile.email')"
                                              :state="this.$v.email.$error ? false : null">
                                </b-form-input>
                                <b-input-group-append>
                                    <b-input-group-text>
                                        <span class="fas fa-envelope"></span>
                                    </b-input-group-text>
                                </b-input-group-append>
                                <b-form-invalid-feedback :state="!this.$v.email.$error">
                                    {{ $t('login.email_invalid') }}
                                </b-form-invalid-feedback>
                            </b-input-group>
                        </b-form-group>

                        <div class="row">
                            <!-- /.col -->
                            <div class="col-12">
                                <b-button type="submit" variant="primary" class="btn-block">{{
                                        $t('login.register_short')
                                    }}
                                </b-button>
                            </div>
                            <!-- /.col -->
                        </div>
                    </b-form>

                    <div class="social-auth-links text-center mb-3">
                        <p class="text-uppercase">- {{ $t('generic.or') }} -</p>
                    </div>
                    <!-- /.social-auth-links -->

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
import required from "vuelidate/lib/validators/required";
import email from "vuelidate/lib/validators/email";
import sameAs from "vuelidate/lib/validators/sameAs";
import minLength from "vuelidate/lib/validators/minLength";

export default {
    name: "login",
    layout: "empty",
    auth: false,

    data() {
        return {
            username: null,
            password: null,
            passwordConfirm: null,
            firstName: null,
            lastName: null,
            email: null
        }
    },

    computed: {
        baseLink() {
            if (this.$config.browserBaseURL) return this.$config.browserBaseURL
            return location.origin
        }
    },

    validations: {
        username: {required},
        password: {required, minLength: minLength(8)},
        passwordConfirm: {required, sameAs: sameAs('password')},
        firstName: {required},
        lastName: {required},
        email: {required, email}
    },

    mounted() {
        if (!this.$config.registrationEnabled){
            this.$toast.warning(this.$t('login.registration_disabled'), this.$t('generic.note'))
            this.$router.push("/login")
        }
    },

    methods: {
        onSubmit() {
            this.$v.$touch()

            if (this.$v.$invalid) {
                return
            }

            // Register user in backend
            this.$axios.$post("/api/register/",
                {
                    username: this.username,
                    password: this.password,
                    email: this.email,
                    first_name: this.firstName,
                    last_name: this.lastName
                })
                .then((data) => {
                    let emailText = `Hello ${this.firstName},
your Caster Dashboard Account has been registered.
- Your username: ${this.username}
Please click the following link (or copy and paste it in a browser) to finish the registration process.
${this.baseLink}/register-confirm?user=${this.username}&token=${data.registration_token}`

                    this.$localAxios.$post('/mail/send', {
                        from: `"Caster Dashboard" <${this.$config.fromEmail}>`,
                        subject: "Caster Dashboard Registration",
                        text: emailText,
                        to: this.email
                    })
                        .then(() => {
                            this.$toast.success("Your account has been created. Please check your emails to finish the registration!")
                        })
                        .catch((error) => {
                            console.log(error.response)
                            this.$toast.error("Your account could not be created. Please try again or contact an administrator!")
                        })

                })
                .catch((error) => {
                    console.log(error.response)
                    if (error.response.data.status === "duplicate user") {
                        this.$toast.error(this.$t('login.user_exists'), this.$t('generic.error'))
                    } else {
                        this.$toast.error("Your account could not be created. Please try again or contact an administrator!")
                    }
                })
        }
    },
}
</script>

<style scoped>

</style>
