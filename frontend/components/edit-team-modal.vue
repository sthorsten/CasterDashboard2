<template>
  <b-modal
    id="edit-team-modal"
    size="lg"
    header-bg-variant="primary"
    hide-footer
  >
    <template #modal-header>
      <h5 class="modal-title">
        <fa-icon icon="pencil" class="mr-1" />
        <span>Edit team</span>
      </h5>
    </template>

    <!-- Team ID -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="list-ol" class="mr-1" />
        <span>Team ID</span>
      </template>

      <div class="d-flex align-items-center text-center h-100">
        <span v-if="team">
          {{ team.id }}
        </span>
      </div>
    </b-form-group>

    <!-- Team Name -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="header" class="mr-1" />
        <span>Team Name</span>
      </template>

      <b-form-input
        v-model="teamName"
        type="text"
        placeholder="Enter a team name"
      />
    </b-form-group>

    <!-- Current Team Logo -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="image" class="mr-1" />
        <span>Current Team Logo</span>
      </template>

      <div class="d-flex align-items-center text-center h-100">
        <img v-if="team" :src="team.logoSmall" width="25" height="25" />
      </div>
    </b-form-group>

    <!-- New Team Logo -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="image" class="mr-1" />
        <span>Upload New Team Logo</span>
      </template>

      <div class="custom-file">
        <input
          type="file"
          class="custom-file-input"
          id="editTeamLogoFile"
          @change="editTeamLogoFile = $event.target.files[0]"
          accept="image/*"
        />
        <label class="custom-file-label" for="editTeamLogoFile">
          Choose file...
        </label>
      </div>
    </b-form-group>

    <hr class="border-secondary" />

    <b-btn block variant="primary" @click="updateTeam">
      <fa-icon icon="check-circle" class="mr-1" />
      <span>Update team</span>
    </b-btn>
  </b-modal>
</template>

<script>
//import bsCustomFileInput from 'bs-custom-file-input'

export default {
  name: 'EditTeamModal',

  data() {
    return {
      teamName: '',
      editTeamLogoFile: null
    }
  },

  props: {
    teamId: Number
  },

  mounted() {
    if (process.client) {
      const bsCustomFileInput = require('bs-custom-file-input')
      bsCustomFileInput.init()
    }
  },

  watch: {
    team(newVal) {
      if (newVal) {
        this.teamName = newVal.name
      }
    }

  },

  computed: {
    team() {
      return this.$store.getters['mainSocket/getTeam'](this.teamId)
    }
  },

  methods: {
    async updateTeam() {
      if (this.editTeamLogoFile) {
        let formData = new FormData()
        formData.append('name', this.teamName)
        formData.append('logo', this.editTeamLogoFile)

        try {
          await this.$axios.$patch(`/api/v2/main/team/${this.team.id}/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          this.$toast.success("Team updated successfully")
        } catch (e) {
          this.$toast.error("Failed to update team!")
        }
      } else {
        if (this.teamName) {
          try {
            await this.$axios.$patch(`/api/v2/main/team/${this.team.id}/`, {
              name: this.teamName
            })
            this.$toast.success("Team updated successfully")
          } catch (e) {
            this.$toast.error("Failed to update team!")
          }
        }
      }

      this.$bvModal.hide('edit-team-modal')
    }
  }
}
</script>