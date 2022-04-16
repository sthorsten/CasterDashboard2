<template>
  <div>
    <ContentHeader
      icon="plus"
      title="Create a new match"
      :breadcrumb-items="['Dashboard', 'Matches', 'New']"
    />
    <ContentContainer>
      <b-container fluid>
        <b-row>
          <b-col cols="6">
            <CustomCard title="New Match">
              <!-- League -->
              <b-container fluid>
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="trophy" class="mr-1" />
                    <span>League</span>
                  </template>

                  <v-select
                    v-model="selectedLeague"
                    :options="leagues"
                    label="name"
                    class="mt-1"
                    placeholder="Select a league"
                    @input="selectedSeason = null"
                  >
                    <template #option="{ name, logoSmall }">
                      <img
                        :src="logoSmall"
                        width="20"
                        height="20"
                        class="mr-1"
                      />
                      {{ name }}
                    </template>
                    <template #selected-option="{ name, logoSmall }">
                      <img
                        :src="logoSmall"
                        width="20"
                        height="20"
                        class="mr-2"
                      />
                      {{ name }}
                    </template>
                  </v-select>
                </b-form-group>
              </b-container>

              <!-- Season -->
              <b-container fluid>
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="calendar-alt" class="mr-1" />
                    <span>Season</span>
                  </template>

                  <v-select
                    v-model="selectedSeason"
                    :options="filteredSeasons"
                    label="name"
                    class="mt-1"
                    :placeholder="
                      !selectedLeague
                        ? 'Select a league first'
                        : 'Select a season'
                    "
                    :disabled="!selectedLeague"
                    @option:selected="selectedPlayday = null"
                    @option:deselected="selectedPlayday = null"
                  />
                </b-form-group>
              </b-container>

              <!-- Playday -->
              <b-container fluid>
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="calendar-day" class="mr-1" />
                    <span>Playday</span>
                  </template>

                  <v-select
                    v-model="selectedPlayday"
                    :options="filteredPlaydays"
                    label="name"
                    class="mt-1"
                    :placeholder="
                      !selectedSeason
                        ? 'Select a league / season first'
                        : 'Select a playday'
                    "
                    :disabled="!selectedSeason"
                  />
                </b-form-group>
              </b-container>

              <hr class="border-secondary" />

              <!-- Date -->
              <b-container fluid>
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="calendar-check" class="mr-1" />
                    <span>Match Date</span>
                  </template>

                  <b-form-input v-model="matchDate" type="date" />
                </b-form-group>
              </b-container>

              <!-- Time -->
              <b-container fluid>
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="clock" class="mr-1" />
                    <span>Match Time</span>
                  </template>

                  <b-form-input v-model="matchTime" type="time" />
                </b-form-group>
              </b-container>

              <hr class="border-secondary" />

              <!-- Team Blue -->
              <b-container fluid>
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="users" class="mr-1" />
                    <span>Team Blue</span>
                  </template>

                  <v-select
                    v-model="teamBlue"
                    :options="teams"
                    label="name"
                    class="mt-1"
                    placeholder="Select a team"
                  >
                    <template #option="option">
                      <img
                        :src="option.logoSmall"
                        width="20"
                        height="20"
                        class="mr-1"
                      />
                      {{ option.name }}
                    </template>
                    <template #selected-option="option">
                      <img
                        :src="option.logoSmall"
                        width="20"
                        height="20"
                        class="mr-2"
                      />
                      {{ option.name }}
                    </template>
                  </v-select>
                </b-form-group>
              </b-container>

              <!-- Team Orange -->
              <b-container fluid>
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="users" class="mr-1" />
                    <span>Team Orange</span>
                  </template>

                  <v-select
                    v-model="teamOrange"
                    :options="teams"
                    label="name"
                    class="mt-1"
                    placeholder="Select a team"
                  >
                    <template #option="option">
                      <img
                        :src="option.logoSmall"
                        width="20"
                        height="20"
                        class="mr-1"
                      />
                      {{ option.name }}
                    </template>
                    <template #selected-option="option">
                      <img
                        :src="option.logoSmall"
                        width="20"
                        height="20"
                        class="mr-2"
                      />
                      {{ option.name }}
                    </template>
                  </v-select>
                </b-form-group>
              </b-container>

              <hr class="border-secondary" />

              <!-- Best of -->
              <b-container fluid>
                <b-form-group>
                  <b-row>
                    <b-col lg="3">
                      <fa-icon icon="list-ol" class="mr-1" />
                      <span>Best Of</span>
                    </b-col>
                    <b-col>
                      <b-form-radio-group v-model="bestOf">
                        <b-form-radio :value="1">Best Of 1</b-form-radio>
                        <b-form-radio :value="2">Best Of 2</b-form-radio>
                        <b-form-radio :value="3">Best Of 3</b-form-radio>
                        <b-form-radio :value="5">Best Of 5</b-form-radio>
                      </b-form-radio-group>
                    </b-col>
                  </b-row>
                </b-form-group>
              </b-container>

              <hr class="border-secondary" />

              <!-- Match Title -->
              <b-container fluid>
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="heading" class="mr-1" />
                    <span>Match Title</span>
                  </template>

                  <b-form-input
                    v-model="matchTitle"
                    :disabled="!selectedSeason"
                    placeholder="Select a league / season first"
                  />
                </b-form-group>
              </b-container>

              <!-- Match Subtitle -->
              <b-container fluid>
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="heading" class="mr-1" />
                    <span>Match Subtitle</span>
                  </template>
                  <b-form-input
                    v-model="matchSubtitle"
                    :disabled="!selectedPlayday"
                    placeholder="Select a league / season / playday first"
                  />
                </b-form-group>
              </b-container>

              <!-- Submit -->
              <b-container fluid class="mt-4">
                <b-btn
                  block
                  variant="primary"
                  :disabled="!matchDataValid"
                  @click="createMatch"
                >
                  <fa-icon icon="plus" class="mr-1" />
                  <span>Create match</span>
                </b-btn>
              </b-container>
            </CustomCard>
          </b-col>

          <!-- Right column -->
          <b-col cols="6">
            <CustomCard title="Summary" color="secondary">
              <b-container fluid>...</b-container>
            </CustomCard>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'CreateNewMatch',
  layout: 'main-page',

  head() {
    return {
      title: "New Match"
    }
  },

  data() {
    return {
      selectedLeague: null,
      selectedSeason: null,
      selectedPlayday: null,
      matchDate: null,
      matchTime: "18:00",

      bestOf: 1,
      teamBlue: null,
      teamOrange: null,

      matchTitle: null,
      matchSubtitle: null
    }
  },

  computed: {
    leagues() {
      return this.$store.state.mainSocket.leagues
    },
    seasons() {
      return this.$store.state.mainSocket.seasons
    },
    playdays() {
      return this.$store.state.mainSocket.playdays
    },
    tournaments() {
      return this.$store.state.mainSocket.tournaments
    },
    teams() {
      return this.$store.state.mainSocket.teams
    },

    filteredSeasons() {
      if (!this.seasons) { return null }
      if (!this.selectedLeague) { return this.seasons }
      return this.seasons.filter(s => s.league === this.selectedLeague.id)
    },
    filteredPlaydays() {
      if (!this.playdays) { return null }
      if (!this.selectedSeason) { return this.playdays }
      return this.playdays.filter(p => p.season === this.selectedSeason.id)
    },

    matchDataValid() {
      let valid = true
      if (!this.selectedLeague) { valid = false }
      if (!this.selectedSeason) { valid = false }
      if (!this.selectedPlayday) { valid = false }
      if (!this.bestOf) { valid = false }
      if (!this.teamBlue) { valid = false }
      if (!this.teamOrange) { valid = false }
      if (!this.matchDate) { valid = false }
      if (!this.matchTime) { valid = false }
      return valid
    }
  },

  watch: {
    selectedSeason(newVal) {
      if (newVal === null) { this.selectedPlayday = null }
      if (this.selectedLeague && this.selectedSeason) {
        this.matchTitle = `${this.selectedLeague.name} - ${this.selectedSeason.name}`
      }
    },
    selectedPlayday(newVal) {
      if (newVal) {
        this.matchSubtitle = this.selectedPlayday.name
        this.matchDate = this.selectedPlayday.date
      }
    }
  },

  methods: {
    async createMatch() {

      const data = {
        league: this.selectedLeague.id,
        season: this.selectedSeason.id,
        playday: this.selectedPlayday.id,
        bestOf: this.bestOf,
        teamBlue: this.teamBlue.id,
        teamOrange: this.teamOrange.id,
        creator: this.$auth.user.id,
        date: `${this.matchDate} ${this.matchTime}:00`
      }

      try {
        const matchData = await this.$axios.$post('/api/v2/match/match/', data)
        this.$router.push(`/dashboard/matches/${matchData.id}/overview`)
        this.$toast.success('Match created successfully')
      } catch {
        this.$toast.error('Failed to create match')
      }
    }
  }

}
</script>
