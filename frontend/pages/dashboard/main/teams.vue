<template>
  <div>
    <ContentHeader
      icon="users"
      title="Teams"
      :breadcrumb-items="['Dashboard', 'Main', 'Teams']"
    />
    <ContentContainer>
      <b-container fluid>
        <b-row>
          <!-- Team Table -->
          <b-col cols="7">
            <CustomCard title="Teams">
              <b-table
                small
                dark
                striped
                :per-page="10"
                :current-page="teamPage"
                :items="teams"
                :fields="teamFields"
                sort-by="name"
              >
                <template #cell(logoSmall)="data">
                  <img :src="data.item.logoSmall" width="25" height="25" />
                </template>
                <template #cell(edit)="data">
                  <b-btn
                    size="sm"
                    variant="primary"
                    @click="editTeam(data.item.id)"
                  >
                    <fa-icon icon="pencil" class="mr-1" />
                    Edit
                  </b-btn>
                </template>
              </b-table>
              <div class="mt-2 w-100 d-flex justify-content-center">
                <b-pagination
                  v-model="teamPage"
                  :per-page="10"
                  :total-rows="teams.length"
                />
              </div>
            </CustomCard>
          </b-col>

          <!-- New Team -->
          <b-col cols="5">
            <CustomCard title="Create a new team" color="success">
              <!-- Team Name -->
              <b-form-group label-cols="4">
                <template #label>
                  <fa-icon icon="header" />
                  Team Name
                </template>

                <b-form-input
                  v-model="newTeamName"
                  type="text"
                  placeholder="Enter a team name"
                />
              </b-form-group>

              <!-- Team Logo -->
              <b-form-group label-cols="4">
                <template #label>
                  <fa-icon icon="image" />
                  Team Logo
                </template>

                <div class="custom-file">
                  <input
                    type="file"
                    class="custom-file-input"
                    id="newTeamLogoFile"
                    @change="newTeamLogoFile = $event.target.files[0]"
                    accept="image/*"
                  />
                  <label class="custom-file-label" for="newTeamLogoFile">
                    Choose file...
                  </label>
                </div>
              </b-form-group>

              <hr class="border-secondary" />

              <!-- Submit -->
              <b-btn block variant="success" @click="createTeam">
                <fa-icon icon="plus" class="mr-1" />
                Create team
              </b-btn>
            </CustomCard>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>

    <EditTeamModal :team-id="editTeamID" />
  </div>
</template>

<script>
import bsCustomFileInput from 'bs-custom-file-input'

export default {
  name: "Teams",
  layout: 'main-page',

  data() {
    return {
      teamPage: 1,
      teamFields: [
        {
          key: 'id',
          label: 'ID'
        },
        'name',
        {
          key: 'logoSmall',
          label: 'Logo'
        },
        'edit'
      ],

      newTeamName: '',
      newTeamLogoFile: null,

      editTeamID: 0
    }
  },

  mounted() {
    bsCustomFileInput.init()
  },

  computed: {
    teams() {
      return this.$store.state.mainSocket.teams
    }
  },

  methods: {
    editTeam(id) {
      this.editTeamID = id
      this.$bvModal.show('edit-team-modal')
    },
    async createTeam() {
      let formData = new FormData()
      formData.append('name', this.newTeamName)
      formData.append('logo', this.newTeamLogoFile)

      try {
        await this.$axios.$post('/api/v2/main/team/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
      } catch (e) {
        this.$toast.error("Failed to create team!")
      }
    }
  }

}
</script>