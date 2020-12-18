<template>
    <BaseLayout :title="$t('generic.profile')" title_icon="fas fa-user-cog" :bc_path="bcPath">

        <b-row>
            <b-col cols="12" lg="6">

                <CustomCard :title="$t('profile.user_data')" outline divider color="primary">
                    <template #card-body>

                        <b-table-simple table-variant="dark" striped small responsive>

                            <b-tbody>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('generic.username') }}</b-th>
                                    <b-td class="text-right">{{ user.username }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('profile.email') }}</b-th>
                                    <b-td class="text-right">{{ user.email }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('profile.first_name') }}</b-th>
                                    <b-td class="text-right">{{ user.first_name }}</b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">{{ $t('profile.last_name') }}</b-th>
                                    <b-td class="text-right">{{ user.last_name }}</b-td>
                                </b-tr>

                            </b-tbody>
                        </b-table-simple>

                    </template>
                </CustomCard>

            </b-col>

            <b-col cols="12" lg="6">

                <CustomCard :title="$t('profile.user_settings')" outline divider color="danger">
                    <template #card-body>

                        <label>{{ $t('profile.change_password') }}:</label>

                        <b-form @submit.prevent="onSubmit" novalidate>

                            <b-form-group class="mb-3" :label="$t('profile.current_password')"
                                          label-for="current-password" label-cols-sm="4" label-cols-lg="3">
                                <b-input-group>
                                    <b-form-input :state="currentPasswordValid" id="current-password"
                                                  v-model="currentPassword" type="password"
                                                  :placeholder="$t('profile.current_password_text')"
                                                  maxlength="22">
                                    </b-form-input>
                                    <b-form-invalid-feedback :state="currentPasswordValid">
                                        {{ $t('profile.current_password_invalid') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <b-form-group :validated="newPasswordValid" class="mb-3" :label="$t('profile.new_password')"
                                          label-for="new-password" label-cols-sm="4" label-cols-lg="3">
                                <b-input-group>
                                    <b-form-input :state="newPasswordValid" id="current-password" v-model="newPassword"
                                                  type="password"
                                                  :placeholder="$t('profile.new_password_text')"
                                                  maxlength="22">
                                    </b-form-input>
                                    <b-form-invalid-feedback :state="newPasswordValid">
                                        {{ $t('profile.new_password_invalid') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <b-form-group :validated="newPasswordConfirmValid" class="mb-3"
                                          :label="$t('profile.new_password_confirm')" label-for="new-password-confirm"
                                          label-cols-sm="4" label-cols-lg="3">
                                <b-input-group>
                                    <b-form-input :state="newPasswordConfirmValid" id="new-password-confirm"
                                                  v-model="newPasswordConfirm" type="password"
                                                  :placeholder="$t('profile.new_password_confirm_text')"
                                                  maxlength="22">
                                    </b-form-input>
                                    <b-form-invalid-feedback :state="newPasswordConfirmValid">
                                        {{ $t('profile.new_password_confirm_invalid') }}
                                    </b-form-invalid-feedback>
                                </b-input-group>
                            </b-form-group>

                            <b-button type="submit" variant="secondary" class="btn-block">
                                {{ $t('profile.change_password') }}
                            </b-button>

                        </b-form>

                    </template>
                </CustomCard>

            </b-col>
        </b-row>

    </BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";
import CustomCard from "@/components/elements/CustomCard";
import axios from "axios";

export default {
    name: "Profile",
    data() {
        return {
            currentPassword: "",
            newPassword: "",
            newPasswordConfirm: "",
            currentPasswordValid: null,
            newPasswordValid: null,
            newPasswordConfirmValid: null,

            bcPath: ["Dashboard", "Profile", this.$store.state.user.username]
        }
    },
    computed: {
        user() {
            return this.$store.state.user
        },
    },
    methods: {
        onSubmit() {
            // Validate input
            if (!this.currentPassword) {
                this.currentPasswordValid = false
                return;
            } else {
                this.currentPasswordValid = true
            }

            if (!this.newPassword) {
                this.newPasswordValid = false
                return;
            } else {
                this.newPasswordValid = true
            }

            if (!this.newPasswordConfirm) {
                this.newPasswordConfirmValid = false
                return;
            } else {
                this.newPasswordConfirmValid = true
            }

            if (this.newPassword !== this.newPasswordConfirm) {
                this.newPasswordValid = false
                this.newPasswordConfirmValid = false
                return
            }

            // Change password
            axios.post(this.$store.state.backendURL + "/api/users/change-password/", {
                "username": this.$store.state.user.username,
                "current_password": this.currentPassword,
                "new_password": this.newPassword
            })
                .then(() => {
                    this.$toast.success(this.$t('profile.password_change_success'))
                    this.currentPassword = ""
                    this.newPassword = ""
                    this.newPasswordConfirm = ""
                })
                .catch((response) => {
                    console.error(response.error)
                    this.$toast.error(this.$t('profile.password_change_error'), this.$t('generic.error'))
                })

        }
    },
    components: {
        CustomCard,
        BaseLayout
    }
}
</script>

<style scoped>

</style>