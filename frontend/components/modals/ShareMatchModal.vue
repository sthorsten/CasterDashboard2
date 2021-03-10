<template>
    <b-modal v-if="!$fetchState.pending" :visible="show" size="lg"
             :title="this.$t('matches.overview.modal.share_title')" hide-footer
             header-bg-variant="primary" body-bg-variant="dark" footer-bg-variant="dark"
             @hide="hide">

        <b-form @submit.prevent="onSubmit" novalidate>

            <b-form-group class="mb-3" :label="this.$t('matches.overview.modal.share_user')" label-for="share-user"
                          label-cols-sm="4" label-cols-lg="3">
                <b-input-group>

                    <v-select class="w-100" v-model="shareUser" multiple
                              :options="users" label="username"
                              :placeholder="$t('matches.overview.modal.share_user')"/>

                    <b-form-invalid-feedback id="share-user-feedback">
                        {{ this.$t('matches.overview.modal.share_user_feedback') }}
                    </b-form-invalid-feedback>
                </b-input-group>
            </b-form-group>


            <b-row class="mb-3"></b-row>
            <b-button type="submit" variant="primary" class="btn-block">
                <font-awesome-icon icon="share-alt"/>
                {{ this.$t('matches.overview.modal.share') }}
            </b-button>

        </b-form>

        <hr class="divider">

        <b-row>
            <b-col>
                <p>
                    <i class="fa fas fa-info-circle"></i> <b class="text-uppercase">{{
                        this.$t('generic.quick_info')
                    }}</b><br>
                </p>
                <ul class="font-italic">
                    <li>{{ this.$t('matches.overview.modal.info_line1') }}</li>
                    <li>{{ this.$t('matches.overview.modal.info_line2') }}</li>
                </ul>
            </b-col>
        </b-row>

    </b-modal>
</template>

<script>
export default {
    name: "ShareMatchModal",
    data() {
        return {
            users: [],
            shareUser: []
        }
    },
    props: {
        show: Boolean,
        match: Object,
    },
    methods: {
        hide() {
            this.$emit('hide')
        },
        onSubmit() {
            this.$emit('hide')
            this.$emit('loading')

            // Filter selected users
            let filteredUsers = this.shareUser.map(u => u.id)

            // Set new users to match
            this.match.user = this.match.user.concat(filteredUsers)

            // Update match
            this.$axios.$patch(`/api/match/${this.match.id}/`, this.match)
                .then(() => {
                    this.$toast.success(this.$t('matches.overview.modal.toasts.success'))
                    this.$emit('reload')
                })
                .catch((error) => {
                    console.log(error)
                    this.$toast.success(this.$t('matches.overview.modal.toasts.error'))
                    this.$emit('reload')
                })
        }
    },
    async fetch() {
        this.$axios.$get("/api/user/")
            .then((data) => {
                // Filter out current and default admin user
                let allUsers = data.filter(u => u.id !== this.$auth.user.id && u.id !== 1)
                // Filter out current match users
                this.users = allUsers.filter(u => !this.match.user.includes(u.id))
            })
    }
}
</script>
