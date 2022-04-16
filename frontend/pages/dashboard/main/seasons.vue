<template>
  <div>
    <ContentHeader
      icon="calendar-alt"
      title="Seasons"
      :breadcrumb-items="['Dashboard', 'Main', 'Seasons']"
    />
    <ContentContainer>
      <b-container fluid>
        <b-row>
          <!-- Season Table -->
          <b-col cols="7">
            <CustomCard title="Seasons">
              <b-table
                small
                dark
                striped
                :per-page="10"
                :current-page="seasonPage"
                :items="seasons"
                :fields="seasonFields"
                sort-by="name"
              >
                <template #cell(league)="data">
                  <img
                    :src="
                      $store.getters['mainSocket/getLeagueLogo'](
                        data.item.league
                      )
                    "
                    width="25"
                    height="25"
                  />
                  {{ data.item.leagueName }}
                </template>
                <template #cell(edit)="data">
                  <b-btn
                    size="sm"
                    variant="primary"
                    @click="editSeason(data.item.id)"
                  >
                    <fa-icon icon="pencil" class="mr-1" />
                    <span>Edit</span>
                  </b-btn>
                </template>
              </b-table>

              <div class="mt-2 w-100 d-flex justify-content-center">
                <b-pagination
                  v-model="seasonPage"
                  :per-page="10"
                  :total-rows="seasons.length"
                />
              </div>
            </CustomCard>
          </b-col>

          <!-- New season -->
          <b-col cols="5">
            <CustomCard title="Create a new season" color="success">
              <!-- League -->
              <b-form-group label-cols-lg="4">
                <template #label>
                  <fa-icon icon="trophy" class="mr-1" />
                  <span>League</span>
                </template>

                <v-select
                  v-model="newSeasonLeague"
                  :options="leagues"
                  label="name"
                  placeholder="Select a league"
                >
                  <template #option="{ name, logoSmall }">
                    <img :src="logoSmall" width="20" height="20" class="mr-1" />
                    {{ name }}
                  </template>
                  <template #selected-option="{ name, logoSmall }">
                    <img :src="logoSmall" width="20" height="20" class="mr-2" />
                    {{ name }}
                  </template>
                </v-select>
              </b-form-group>

              <!-- Season start date -->
              <b-form-group label-cols-lg="4">
                <template #label>
                  <fa-icon icon="calendar-check" class="mr-1" />
                  <span>Season Start Date</span>
                </template>

                <b-form-input v-model="newSeasonStartDate" type="date" />
              </b-form-group>

              <!-- Season end date -->
              <b-form-group label-cols-lg="4">
                <template #label>
                  <fa-icon icon="calendar-check" class="mr-1" />
                  <span>Season End Date</span>
                </template>

                <b-form-input v-model="newSeasonEndDate" type="date" />
              </b-form-group>

              <!-- Season playday count -->
              <b-form-group label-cols="4">
                <template #label>
                  <fa-icon icon="list-ol" class="mr-1" />
                  <span>Number of Playdays</span>
                </template>

                <b-form-input
                  v-model="newSeasonPlaydayCount"
                  type="number"
                  placeholder="Enter how many playdays the season has"
                />
              </b-form-group>

              <!-- Season Number -->
              <b-form-group label-cols="4">
                <template #label>
                  <fa-icon icon="list-ol" class="mr-1" />
                  <span>Season number</span>
                </template>

                <b-form-input
                  v-model="newSeasonNumber"
                  type="number"
                  placeholder="Enter a season number"
                />
              </b-form-group>

              <!-- Season Name -->
              <b-form-group label-cols="4">
                <template #label>
                  <fa-icon icon="heading" class="mr-1" />
                  <span>Season name</span>
                </template>

                <b-form-input
                  v-model="newSeasonName"
                  placeholder="Enter a season name"
                />
              </b-form-group>

              <hr class="border-secondary" />

              <!-- Submit -->
              <b-btn
                block
                variant="success"
                @click="createSeason"
                :disabled="
                  !this.newSeasonLeague ||
                  !this.newSeasonStartDate ||
                  !this.newSeasonEndDate ||
                  !this.newSeasonPlaydayCount ||
                  !this.newSeasonNumber ||
                  !this.newSeasonName
                "
              >
                <fa-icon icon="plus" class="mr-1" />
                <span>Create season</span>
              </b-btn>
            </CustomCard>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>

    <EditSeasonModal :season-id="editSeasonID" />
  </div>
</template>

<script>
export default {
  name: 'Seasons',
  layout: 'main-page',

  data() {
    return {
      seasonPage: 1,

      seasonFields: [
        {
          key: 'id',
          label: 'ID'
        },
        'league',
        'name',
        {
          key: 'seasonNo',
          label: 'Season #'
        },
        {
          key: 'playdayCount',
          label: 'Playdays'
        },
        'startDate',
        'endDate',
        'edit'
      ],

      newSeasonLeague: null,
      newSeasonStartDate: null,
      newSeasonEndDate: null,
      newSeasonPlaydayCount: null,
      newSeasonNumber: null,
      newSeasonName: "",

      editSeasonID: null
    }
  },

  computed: {
    leagues() {
      return this.$store.state.mainSocket.leagues
    },
    seasons() {
      return this.$store.state.mainSocket.seasons
    }
  },

  watch: {
    newSeasonNumber(newVal) {
      if (newVal) {
        if (newVal == 0) {
          this.newSeasonName = ""
          return
        }
        this.newSeasonName = "Season " + this.newSeasonNumber
      }
    }
  },

  methods: {
    async createSeason() {
      const data = {
        league: this.newSeasonLeague.id,
        startDate: this.newSeasonStartDate,
        endDate: this.newSeasonEndDate,
        playdayCount: this.newSeasonPlaydayCount,
        seasonNo: this.newSeasonNumber,
        name: this.newSeasonName
      }

      try {
        await this.$axios.$post('/api/v2/main/season/', data)
        this.$toast.success("Season created successfully")
      } catch (e) {
        this.$toast.error("Failed to create season!")
      }
    },

    editSeason(id) {
      this.editSeasonID = id
      this.$bvModal.show('edit-season-modal')
    }
  }

}
</script>