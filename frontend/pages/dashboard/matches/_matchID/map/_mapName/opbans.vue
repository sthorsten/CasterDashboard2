<template>
  <div>
    <ContentHeader
      icon="users-slash"
      title="Operator Bans"
      :breadcrumb-items="['Dashboard', 'Matches', $route.params.matchID, $route.params.mapName, 'Operator Bans']"
    />
    <ContentContainer v-if="match != null && matchMap != null">
      <b-container fluid>
        <b-row>
          <!-- Left column -->
          <b-col cols="6">
            <CustomCard title="Operator Bans">
              <!-- Labels -->
              <b-row>
                <b-col cols="6">
                  <label class="text-center w-100">ATK Operators</label>
                </b-col>
                <b-col cols="6">
                  <label class="text-center w-100">DEF Operators</label>
                </b-col>
              </b-row>

              <hr class="border-secondary mt-0" />

              <!-- Operator Ban buttons -->
              <b-row>
                <!-- ATK Operators -->
                <b-col cols="6">
                  <b-row>
                    <b-col v-for="operator in atkOperators" :key="operator.id" cols="6">
                      <OperatorBanBtn
                        :operator="operator"
                        :operator-bans="operatorBans"
                        @ban="banOperator"
                        block
                      />
                    </b-col>
                  </b-row>
                </b-col>

                <!-- DEF Operators -->
                <b-col cols="6">
                  <b-row>
                    <b-col v-for="operator in defOperators" :key="operator.id" cols="6">
                      <OperatorBanBtn
                        :operator="operator"
                        :operator-bans="operatorBans"
                        @ban="banOperator"
                        block
                      />
                    </b-col>
                  </b-row>
                </b-col>
              </b-row>
            </CustomCard>
          </b-col>

          <!-- Right column -->
          <b-col cols="6">
            <!-- Actions -->
            <b-row>
              <b-col>
                <CustomCard color="info" title="Operator Ban Actions">
                  <b-btn variant="danger" block disabled>
                    <fa-icon icon="trash-can" class="mr-1" />Remove last operator ban
                  </b-btn>
                  <b-btn variant="danger" block disabled>
                    <fa-icon icon="trash-can" class="mr-1" />Remove all operator bans
                  </b-btn>

                  <hr class="border-secondary" />

                  <b-btn
                    variant="primary"
                    block
                    @click="$router.push(`/dashboard/matches/${match.id}/map/${matchMap.mapName}/rounds`)"
                  >
                    <fa-icon icon="arrow-right" class="mr-1" />Continue to rounds
                  </b-btn>
                </CustomCard>
              </b-col>
            </b-row>

            <!-- Current Operator Bans -->
            <b-row>
              <b-col>
                <CustomCard color="secondary" title="Current Operator Bans">
                  <b-row>
                    <!-- Operator Bans -->
                    <b-col
                      cols="3"
                      v-for="ban in operatorBans"
                      :key="ban.id"
                      class="text-center"
                    >
                      <R6OperatorIcon :operator="ban.operatorIdentifier" height="50" />
                      <br />
                      <b>{{ ban.operatorName }}</b>
                      <br />
                      <i>{{ ban.teamName }}</i>
                    </b-col>

                    <!-- Empty cols -->
                    <b-col
                      cols="3"
                      v-for="i in 4 - operatorBans.length"
                      :key="'empty-ban-' + i"
                      class="text-center pt-4"
                    >
                      <i>No ban</i>
                    </b-col>
                  </b-row>
                </CustomCard>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: "OperatorBans",
  layout: "match-page",
  computed: {
    match() {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters["matchSocket/getMatch"](matchID)
      }
      catch {
        return null
      }
    },
    matchMaps() {
      try {
        const matchID = parseInt(this.$route.params.matchID)
        return this.$store.getters["matchSocket/getMatchMapsByMatch"](matchID)
      }
      catch {
        return null
      }
    },
    operatorBans() {
      if (!this.matchMap) {
        return
      }
      try {
        return this.$store.getters["matchSocket/getOperatorBansByMatchMap"](this.matchMap.id)
      }
      catch {
        return null
      }
    },
    atkOperators() {
      const atkOps = this.$store.getters["coreSocket/getOperatorsBySide"]("ATK")
      return atkOps.sort((e1, e2) => {
        return e1.identifier > e2.identifier ? 1 : -1
      })
    },
    defOperators() {
      const defOps = this.$store.getters["coreSocket/getOperatorsBySide"]("DEF")
      return defOps.sort((e1, e2) => {
        return e1.identifier > e2.identifier ? 1 : -1
      })
    },
    matchMap() {
      return this.matchMaps.filter(m => m.mapName === this.$route.params.mapName)[0]
    },
    nextBanOrder() {
      return this.operatorBans.length + 1
    },
    nextBanTeam() {
      if (this.nextBanOrder === 1 || this.nextBanOrder === 4) {
        return this.matchMap.defTeam
      } else {
        return this.matchMap.atkTeam
      }
    }
  },

  methods: {
    async banOperator(id) {
      const data = {
        matchMap: this.matchMap.id,
        operator: id,
        team: this.nextBanTeam,
        order: this.nextBanOrder
      }
      try {
        await this.$axios.$post('/api/v2/match/operatorban/', data)
      } catch (e) {
        console.error(e)
      }
    }
  }
}
</script>
