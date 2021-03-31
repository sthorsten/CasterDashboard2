<template>
    <div>

        <b-row v-if="!$fetchState.pending">

            <!-- User Data -->
            <b-col cols="12" lg="6">

                <CustomCard color="primary" outline divider :title="$t('profile.user_data')">
                    <template #card-body>

                        <b-form-group :label="$t('generic.username')" label-cols="4" label-cols-lg="2">
                            <b-form-input type="text" disabled :value="$auth.user.username" class="bg-dark">
                            </b-form-input>
                        </b-form-group>

                        <i>{{ $t('profile.username_change_text') }}</i>

                        <hr class="divider">

                        <b-form @submit.prevent="changeUserData" novalidate>
                            <b-form-group :label="$t('profile.email')" label-cols="4" label-cols-lg="2">
                                <b-input-group>
                                    <b-form-input type="email" v-model="userEmail"
                                                  :state="$v.userEmail.$error ? false : null"
                                                  class="bg-dark-900">
                                    </b-form-input>
                                    <b-form-invalid-feedback :state="!$v.userEmail.$error">
                                        {{ $t('profile.email_invalid') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <b-form-group :label="$t('profile.first_name')" label-cols="4" label-cols-lg="2">
                                <b-input-group>
                                    <b-form-input type="text" v-model="userFirstName"
                                                  :state="$v.userFirstName.$error ? false : null"
                                                  class="bg-dark-900">
                                    </b-form-input>
                                    <b-form-invalid-feedback :state="!$v.userFirstName.$error">
                                        {{ $t('profile.first_name_invalid') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <b-form-group :label="$t('profile.last_name')" label-cols="4" label-cols-lg="2">
                                <b-input-group>
                                    <b-form-input type="text" v-model="userLastName"
                                                  :state="$v.userLastName.$error ? false : null"
                                                  class="bg-dark-900">
                                    </b-form-input>
                                    <b-form-invalid-feedback :state="!$v.userLastName.$error">
                                        {{ $t('profile.last_name_invalid') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <b-btn block variant="primary" type="submit">
                                {{ $t('profile.change_user_data') }}
                            </b-btn>
                        </b-form>

                    </template>
                </CustomCard>

            </b-col>

            <!-- Change Password -->
            <b-col cols="12" lg="6">
                <CustomCard color="danger" outline divider :title="$t('profile.change_password')">
                    <template #card-body>

                        <b-form @submit.prevent="changePassword" novalidate>
                            <b-form-group :label="$t('profile.current_password')" label-cols="6" label-cols-lg="4">
                                <b-input-group>
                                    <b-form-input type="password" v-model="userCurrentPassword"
                                                  :placeholder="$t('profile.current_password_text')"
                                                  :state="$v.userCurrentPassword.$error ? false : null"
                                                  class="bg-dark-900">
                                    </b-form-input>
                                    <b-form-invalid-feedback :state="!$v.userCurrentPassword.$error">
                                        {{ $t('profile.current_password_invalid') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <b-form-group :label="$t('profile.new_password')" label-cols="6" label-cols-lg="4">
                                <b-input-group>
                                    <b-form-input type="password" v-model="userNewPassword"
                                                  :placeholder="$t('profile.new_password_text')"
                                                  :state="$v.userNewPassword.$error ? false : null"
                                                  class="bg-dark-900">
                                    </b-form-input>
                                    <b-form-invalid-feedback :state="!$v.userNewPassword.$error">
                                        {{ $t('profile.new_password_invalid') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <b-form-group :label="$t('profile.new_password_confirm')" label-cols="6" label-cols-lg="4">
                                <b-input-group>
                                    <b-form-input type="password" v-model="userNewPasswordConfirm"
                                                  :placeholder="$t('profile.new_password_confirm_text')"
                                                  :state="$v.userNewPasswordConfirm.$error ? false : null"
                                                  class="bg-dark-900">
                                    </b-form-input>
                                    <b-form-invalid-feedback :state="!$v.userNewPasswordConfirm.$error">
                                        {{ $t('profile.new_password_confirm_invalid') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <b-btn block variant="danger" type="submit">
                                {{ $t('profile.change_password') }}
                            </b-btn>
                        </b-form>

                    </template>
                </CustomCard>
            </b-col>
        </b-row>

    </div>
</template>

<script>
import CustomCard from "~/components/CustomCard";
import {required, email, sameAs} from 'vuelidate/lib/validators'

export default {
    name: "Profile",

    data() {
        return {
            userEmail: "",
            userFirstName: "",
            userLastName: "",

            userCurrentPassword: "",
            userNewPassword: "",
            userNewPasswordConfirm: ""
        }
    },

    head() {
        return {
            title: this.$t("navigation.profile") + " - Caster Dashboard"
        }
    },

    validations: {
        userEmail: {required, email},
        userFirstName: {required},
        userLastName: {required},
        userCurrentPassword: {required},
        userNewPassword: {required},
        userNewPasswordConfirm: {required, sameAsPassword: sameAs('userNewPassword')}
    },

    computed: {},

    methods: {
        changeUserData() {
            this.$v.userEmail.$touch()
            this.$v.userFirstName.$touch()
            this.$v.userLastName.$touch()

            if (this.$v.userEmail.$invalid || this.$v.userFirstName.$invalid || this.$v.userLastName.$invalid) {
                this.$toast.warning(this.$t('generic.form_invalid'), this.$t('generic.warning'))
                return
            }

            this.$axios.$post(`/api/users/change-user-data/`, {
                user: this.$auth.user.id,
                email: this.userEmail,
                first_name: this.userFirstName,
                last_name: this.userLastName
            }).then(() => {
                this.$toast.success(this.$t('profile.change_user_data_success'), this.$t('generic.success'))
            }).catch((error) => {
                console.log(error)
                this.$toast.error(this.$t('profile.change_user_data_error'), this.$t('generic.error'))
            })

        },
        changePassword() {
            this.$v.userCurrentPassword.$touch()
            this.$v.userNewPassword.$touch()
            this.$v.userNewPasswordConfirm.$touch()

            if (this.$v.userCurrentPassword.$invalid || this.$v.userNewPassword.$invalid || this.$v.userNewPasswordConfirm.$invalid) {
                this.$toast.warning(this.$t('generic.form_invalid'), this.$t('generic.warning'))
                return
            }

            this.$axios.$post(`/api/users/change-password/`, {
                username: this.$auth.user.username,
                current_password: this.userCurrentPassword,
                new_password: this.userNewPassword
            }).then(() => {
                this.$toast.success(this.$t('profile.password_change_success'), this.$t('generic.success'))
            }).catch((error) => {
                console.log(error)
                this.$toast.error(this.$t('profile.password_change_error'), this.$t('generic.error'))
            })
        }
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$t("navigation.profile"))
        this.$store.commit("setPageTitleIcon", "user-circle")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Settings", "Profile"])
    },

    async fetch() {
        this.userEmail = this.$auth.user.email
        this.userFirstName = this.$auth.user.first_name
        this.userLastName = this.$auth.user.last_name
    },

    mixins: [],

    components: {
        "CustomCard": CustomCard
    }

}
</script>

<style scoped>

</style>
