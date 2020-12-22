<template>
    <b-modal :visible="show" size="lg" :title="this.$t('data.teams.add_new_team_btn')" hide-footer
             header-bg-variant="success" body-bg-variant="dark" footer-bg-variant="dark"
             @hide="hide">

        <b-row>
            <b-col>
                <p>
                    <i class="fa fas fa-info-circle"></i> <b>{{ this.$t('generic.quick_info') }}</b>:<br>
                </p>
                <ul class="font-italic">
                    <li>{{ this.$t('data.teams.modal.info.line1') }}</li>
                    <li>{{ this.$t('data.teams.modal.info.line2') }}</li>
                    <li>{{ this.$t('data.teams.modal.info.line3') }}</li>
                    <li>{{ this.$t('data.teams.modal.info.line4') }}</li>
                </ul>
            </b-col>
        </b-row>

        <hr class="divider">

        <b-form @submit.prevent="onSubmit" novalidate>

            <b-form-group class="mb-3" :label="this.$t('data.teams.modal.team_name')" label-for="new-team-name" label-cols-sm="4" label-cols-lg="3">
                <b-input-group>
                    <b-form-input id="new-team-name" v-model="new_team_name" type="text" :placeholder="this.$t('data.teams.modal.team_name_text')"
                                  aria-describedby="new-team-name-feedback"
                                  maxlength="22" :state="new_team_name_state" @input="onTeamNameChange">
                    </b-form-input>
                    <b-form-invalid-feedback id="new-team-name-feedback">
                        {{ this.$t('data.teams.modal.team_name_feedback') }}
                    </b-form-invalid-feedback>
                </b-input-group>
            </b-form-group>

            <hr class="divider">

            <div class="mb-3">
                <label class="font-italic">
                    {{ this.$t('data.teams.modal.team_logo') }}
                </label>
            </div>

            <b-form-group class="mb-3" :label="this.$t('data.teams.modal.logo_upload')" label-for="new-team-file" label-cols-sm="4" label-cols-lg="3">
                <b-input-group>
                    <b-form-file id="new-team-file" v-model="new_team_logo_file"
                                 :placeholder="this.$t('data.teams.modal.logo_upload_text')"
                                 :drop-placeholder="this.$t('data.teams.modal.logo_upload_text_drop')"
                                 class="bg-dark text-white">
                    </b-form-file>
                </b-input-group>
            </b-form-group>

            <b-form-group class="mb-3" :label="this.$t('data.teams.modal.logo_url')" label-for="new-team-logo-url" label-cols-sm="4"
                          label-cols-lg="3">
                <b-input-group>
                    <b-form-input id="new-team-logo-url" v-model="new_team_logo_url" type="url"
                                  :placeholder="this.$t('data.teams.modal.logo_url_text')"
                                  aria-describedby="new-team-logo-url-feedback">
                    </b-form-input>
                </b-input-group>
            </b-form-group>

            <b-row class="mb-3"></b-row>
            <b-button type="submit" variant="success" class="btn-block">
                {{ this.$t('data.teams.modal.add_btn') }}
            </b-button>

        </b-form>

    </b-modal>
</template>

<script>
import axios from "axios"

export default {
    name: "NewTeamModal",
    data() {
        return {
            new_team_name: "",
            new_team_name_state: null,
            new_team_logo_file: null,
            new_team_logo_url: "",
            test: true,
        }
    },
    props: {
        show: Boolean,
    },
    methods: {
        hide() {
            this.$emit('hide')
        },
        onTeamNameChange() {
            this.new_team_name_state = Boolean(this.new_team_name)
        },
        onSubmit() {
            // Validate name
            this.new_team_name_state = Boolean(this.new_team_name)
            if (this.new_team_name_state)
                this.addNewTeam()
        },
        addNewTeam() {
            this.$emit('hide')
            this.$emit('loading')

            // Parse FormData
            const fd = new FormData()
            fd.append('name', this.new_team_name)
            if (this.new_team_logo_file)
                fd.append('team_logo', this.new_team_logo_file)
            if (this.new_team_logo_url)
                fd.append('team_logo_url', this.new_team_logo_url)

            axios.post(this.$store.state.backendURL + "/api/data/team/", fd, {
                headers: {
                    "Authorization": "Token " + this.$store.state.userToken
                },
            }).then((response) => {
                console.log(response)
                this.$toast.success(this.$t('data.teams.modal.team_created'))
                this.$emit('reload')
            }).catch((error) => {
                console.log(error.response)
                if (error.response.status === 500)
                    this.$toast.error(this.$t('generic.internal_server_error'), this.$t('generic.oops'))
                else
                    this.$toast.error(error.response.data.error.toString(), this.$t('data.teams.modal.team_create_failed'))
                this.$emit('reload')
            })

            console.log("Submit!")
        }
    }
}
</script>

<style scoped>
</style>