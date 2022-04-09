<template>
  <div>
    <ContentHeader
      icon="calendar-day"
      title="Playdays"
      :breadcrumb-items="['Dashboard', 'Main', 'Playdays']"
    />
    <ContentContainer>
      <b-container fluid>
        <b-row>
          <!-- Playday Table -->
          <b-col cols="7">
            <CustomCard title="Playdays">
              <b-table
                small
                dark
                striped
                :per-page="10"
                :current-page="playdayPage"
                :items="playdays"
                :fields="playdayFields"
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
                    @click="editPlayday(data.item.id)"
                  >
                    <fa-icon icon="pencil" class="mr-1" />
                    Edit
                  </b-btn>
                </template>
              </b-table>
              <div class="mt-2 w-100 d-flex justify-content-center">
                <b-pagination
                  v-model="playdayPage"
                  :per-page="10"
                  :total-rows="playdays.length"
                />
              </div>
            </CustomCard>
          </b-col>

          <!-- New playday -->
          <b-col cols="5">
            <CustomCard title="Create a new playday" color="success">
              <!-- League -->
              <b-form-group label-cols-lg="4">
                <template #label>
                  <fa-icon icon="trophy" class="mr-1" />League
                </template>

                <v-select
                  v-model="newPlaydayLeague"
                  :options="leagues"
                  label="name"
                  placeholder="Select a league"
                  @input="newPlaydaySeason = null"
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

              <!-- Season -->
              <b-form-group label-cols-lg="4">
                <template #label>
                  <fa-icon icon="calendar-alt" class="mr-1" />Season
                </template>

                <v-select
                  v-model="newPlaydaySeason"
                  :options="filteredSeasons"
                  label="name"
                  class="mt-1"
                  :placeholder="
                    !newPlaydayLeague
                      ? 'Select a league first'
                      : 'Select a season'
                  "
                  :disabled="!newPlaydayLeague"
                />
              </b-form-group>

              <!-- Playday date -->
              <b-form-group label-cols-lg="4">
                <template #label>
                  <fa-icon icon="calendar-check" class="mr-1" />Playday Date
                </template>

                <b-form-input v-model="newPlaydayDate" type="date" />
              </b-form-group>

              <!-- Playday Number -->
              <b-form-group label-cols="4">
                <template #label>
                  <fa-icon icon="list-ol" class="mr-1" />
                  Playday number
                </template>

                <b-form-input
                  v-model="newPlaydayNumber"
                  type="number"
                  :placeholder="
                    !newPlaydaySeason
                      ? 'Select a season first'
                      : 'Enter a playday number'
                  "
                  :disabled="!newPlaydaySeason"
                />
              </b-form-group>

              <!-- Playday Name -->
              <b-form-group label-cols="4">
                <template #label>
                  <fa-icon icon="heading" class="mr-1" />
                  Playday name
                </template>

                <b-form-input
                  v-model="newPlaydayName"
                  :placeholder="
                    !newPlaydayNumber || newPlaydayNumber == 0
                      ? 'Select a playday number first'
                      : ''
                  "
                  :disabled="!newPlaydayNumber || newPlaydayNumber == 0"
                />
              </b-form-group>

              <hr class="border-secondary" />

              <!-- Submit -->
              <b-btn
                block
                variant="success"
                @click="createPlayday"
                :disabled="
                  !this.newPlaydayDate ||
                  !this.newPlaydayNumber ||
                  !this.newPlaydayName
                "
              >
                <fa-icon icon="plus" class="mr-1" />
                Create playday
              </b-btn>
            </CustomCard>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>

    <EditPlaydayModal :playday-id="editPlaydayID" />
  </div>
</template>

<script>
export default {
  name: 'Playdays',
  layout: 'main-page',

  data() {
    return {
      playdayPage: 1,
      playdayFields: [
        {
          key: 'id',
          label: 'ID'
        },
        'league',
        {
          key: 'seasonName',
          label: 'Season'
        },
        'date',
        {
          key: 'playdayNo',
          label: 'Playday #'
        },
        'name',
        'edit'
      ],

      newPlaydayLeague: null,
      newPlaydaySeason: null,
      newPlaydayDate: null,
      newPlaydayNumber: 0,
      newPlaydayName: '',
      editPlaydayID: 0
    }
  },

  computed: {
    playdays() {
      return this.$store.state.mainSocket.playdays
    },
    leagues() {
      return this.$store.state.mainSocket.leagues
    },
    seasons() {
      return this.$store.state.mainSocket.seasons
    },
    filteredSeasons() {
      if (!this.seasons) { return null }
      if (!this.selectedLeague) { return this.seasons }
      return this.seasons.filter(s => s.league === this.selectedLeague.id)
    },
  },

  watch: {
    newPlaydayLeague(newVal) {
      if (newVal === null) {
        this.newPlaydaySeason = null
        this.newPlaydayNumber = 0
        this.newPlaydayName = ""
      }
    },
    newPlaydaySeason(newVal) {
      if (newVal === null) {
        this.newPlaydayNumber = 0
        this.newPlaydayName = ""
      }
    },
    newPlaydayNumber(newVal) {
      if (newVal) {
        if (newVal == 0) {
          this.newPlaydayName = ""
          return
        }
        this.newPlaydayName = "Playday " + this.newPlaydayNumber
      }
    }
  },

  methods: {
    async createPlayday() {
      const data = {
        season: this.newPlaydaySeason.id,
        date: this.newPlaydayDate,
        playdayNo: this.newPlaydayNumber,
        name: this.newPlaydayName
      }

      try {
        await this.$axios.$post('/api/v2/main/playday/', data)
        this.$toast.success('Playday created successfully')
      } catch (e) {
        this.$toast.error("Failed to create playday!")
      }

    },
    editPlayday(id) {
      {
        this.editPlaydayID = id
        this.$bvModal.show('edit-playday-modal')
      }
    }
  }
}
</script>