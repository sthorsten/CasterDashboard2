<template>
  <div>
    <ContentHeader
      icon="map"
      title="Map Pick & Ban"
      :breadcrumb-items="['Dashboard', 'Matches', $route.params.matchID, 'MapBan']"
    />
    <ContentContainer v-if="match">
      <b-container fluid>
        <b-row>
          <!-- Left column -->
          <b-col cols="6">
            <CustomCard title="Map Picks and Bans">
              <b-container fluid>
                <!-- Map Pool -->
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="map" />Select Map Pool
                  </template>

                  <v-select
                    v-model="selectedMapPool"
                    :options="mapPools"
                    label="name"
                    class="mt-1"
                  />
                </b-form-group>

                <hr class="border-secondary" />

                <!-- Map Pool -->
                <b-form-group label-cols-lg="3">
                  <template #label>
                    <fa-icon icon="list-ol" />Select Map Count
                  </template>

                  <b-form-input v-model="mapCount" type="number" min="0" max="9" />
                </b-form-group>

                <hr class="border-secondary" />

                <!-- Current pick team -->
                <b-form-group>
                  <b-row>
                    <b-col lg="3" class="d-flex align-items-center">
                      <fa-icon icon="users" />Select next Team
                    </b-col>

                    <b-col>
                      <b-btn
                        :variant="currentPickTeam === match.teamBlue ? 'primary' : 'outline-primary'"
                        block
                        @click="currentPickTeam = match.teamBlue"
                      >
                        <img
                          :src="$store.getters['mainSocket/getTeamLogo'](match.teamBlue, true)"
                          height="20"
                          width="20"
                          alt="teamBlue logo"
                        />
                        {{ match.teamBlueName }}
                      </b-btn>
                    </b-col>

                    <b-col>
                      <b-btn
                        :variant="currentPickTeam === match.teamOrange ? 'primary' : 'outline-primary'"
                        block
                        @click="currentPickTeam = match.teamOrange"
                      >
                        <img
                          :src="$store.getters['mainSocket/getTeamLogo'](match.teamOrange, true)"
                          height="20"
                          width="20"
                          alt="teamOrange logo"
                        />
                        {{ match.teamOrangeName }}
                      </b-btn>
                    </b-col>

                    <!--
                    <b-form-radio-group v-model="currentPickTeam">
                      <b-form-radio :value="match.teamBlue">
                        <img
                          :src="$store.getters['mainSocket/getTeamLogo'](match.teamBlue, true)"
                          height="20"
                          width="20"
                          alt="teamBlue logo"
                        >
                        {{ match.teamBlueName }}
                      </b-form-radio>
                      <b-form-radio :value="match.teamOrange">
                        <img
                          :src="$store.getters['mainSocket/getTeamLogo'](match.teamOrange, true)"
                          height="20"
                          width="20"
                          alt="teamOrange logo"
                        >
                        {{ match.teamOrangeName }}
                      </b-form-radio>
                    </b-form-radio-group>
                    -->
                  </b-row>
                </b-form-group>

                <hr class="border-secondary" />

                <!-- Maps -->
                <div v-if="selectedMapPool">
                  <b-container v-for="map in filteredMaps" :key="map.id" fluid>
                    <b-row>
                      <!-- Map image -->
                      <b-col lg="3">
                        <MapbanImage :map-name="map.name" :map-ban="mapBansByMap[map.id]" />
                      </b-col>

                      <!-- Buttons -->
                      <b-col lg="3" class="pt-1">
                        <b-btn
                          variant="danger"
                          block
                          :disabled="currentPickTeam === -1 || !!mapBansByMap[map.id]"
                          @click="selectMap(map, 'BAN')"
                        >
                          <fa-icon icon="ban" />Ban Map
                        </b-btn>
                        <b-btn
                          variant="success"
                          block
                          :disabled="currentPickTeam === -1 || !!mapBansByMap[map.id]"
                          @click="selectMap(map, 'PICK')"
                        >
                          <fa-icon icon="hand-point-up" />Pick Map
                        </b-btn>
                      </b-col>

                      <!-- Text -->
                      <b-col>
                        <MapbanText :map="map" :map-ban="mapBansByMap[map.id]" />
                      </b-col>
                    </b-row>

                    <hr class="border-secondary my-2" />
                  </b-container>
                </div>
              </b-container>
            </CustomCard>
          </b-col>

          <!-- Right column -->
          <b-col cols="6">
            <CustomCard color="info" title="Map Ban Actions">
              <b-btn variant="danger" block @click="removeLastMap">
                <fa-icon icon="trash-can" />Remove last map
              </b-btn>
              <b-btn variant="danger" block @click="removeAllMaps">
                <fa-icon icon="trash-can" />Remove all maps
              </b-btn>

              <hr class="border-secondary" />

              <b-btn
                variant="primary"
                block
                :disabled="!nextMap"
                @click="$router.push(`/dashboard/matches/${match.id}/map/${nextMap.mapName}/overview`)"
              >
                <fa-icon icon="arrow-right" />Continue to next map
                <template v-if="nextMap">({{ nextMap.mapName }})</template>
                <!-- ToDo: Add next map in text -->
              </b-btn>
            </CustomCard>
            <CustomCard color="secondary" title="Current Map Ban">
              <MapbanLog v-for="mapBan in mapBans" :key="mapBan.id" :map-ban="mapBan" />
              <span v-if="!mapBans || mapBans.length === 0">
                <i>None selected yet.</i>
              </span>
            </CustomCard>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'MapBan',
  layout: 'match-page',

  data() {
    return {
      currentPickTeam: -1,
      selectedMapPool: null,
      mapCount: -1
    }
  },

  computed: {
    match() {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters['matchSocket/getMatch'](matchID)
      } catch {
        return null
      }
    },
    mapBans() {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters['matchSocket/getMapBansByMatch'](matchID)
      } catch {
        return null
      }
    },
    matchMaps() {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        const matchMaps = this.$store.getters['matchSocket/getMatchMapsByMatch'](matchID)
        matchMaps.sort((e1, e2) => {
          return e1.order > e2.order ? 1 : -1
        })
        return matchMaps
      } catch {
        return null
      }
    },

    maps() {
      return this.$store.state.coreSocket.maps
    },
    mapPools() {
      return this.$store.state.coreSocket.mapPools
    },

    filteredMaps() {
      if (!this.selectedMapPool) { return this.maps }
      return this.maps.filter(m => this.selectedMapPool.maps.includes(m.id))
    },

    mapBansByMap() {
      if (!this.mapBans || this.mapBans.length === 0) { return [] }
      const mapBans = {}
      this.mapBans.forEach((m) => {
        mapBans[m.map] = m
      })
      return mapBans
    },

    nextMap() {
      if (!this.matchMaps) { return null }
      return this.matchMaps.find(m => m.status !== 'FINISHED')
    }

  },

  mounted() {
    // Set map pool to competitive by default
    if (this.mapPools && this.mapPools.length > 0) {
      this.selectedMapPool = this.mapPools.find(m => m.name === 'Competitive')
      this.mapCount = 9
    }

    // Set next ban team if bans are present
    if (this.match && this.mapBans) {
      const lastBan = this.mapBans.find(m => m.order === this.mapBans.length)
      if (!lastBan) return
      this.currentPickTeam = this.match.teamBlue === lastBan.team ? this.match.teamOrange : this.match.teamBlue
    }
  },

  methods: {
    async selectMap(map, type) {
      let mapCount = -1

      try {
        mapCount = parseInt(this.mapCount)
        if (mapCount < 0 || mapCount > 9) {
          this.$toast.error("Invalid map count. Must be between 0 and 9!")
          return
        }
      } catch (e) {
        console.log(e)      
        return
      }

      const order = this.mapBans.length + 1
      const isDecider = order === mapCount

      const mapBanData = {
        type,
        order,
        isDecider,
        match: this.match.id,
        map: map.id,
        team: isDecider ? null : this.currentPickTeam
      }

      try {
        await this.$axios.$post('/api/v2/match/mapban/', mapBanData)
      } catch (e) {
        this.$toast.error('Error')
      }
      this.currentPickTeam = this.currentPickTeam === this.match.teamBlue ? this.match.teamOrange : this.match.teamBlue
    },

    async removeLastMap() {
      const lastMapBan = this.mapBans[this.mapBans.length - 1]

      try {
        await this.$axios.$delete(`/api/v2/match/mapban/${lastMapBan.id}/`)
      } catch (e) { console.error(e) }

    },

    removeAllMaps() {
      for (let i = 0; i < this.mapBans.length; i++) {
        setTimeout(async () => {
          await this.removeLastMap()
        }, 100 * i)
      }
    }
  }
}
</script>
