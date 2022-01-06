<template>
  <div>
    <CustomCard
      color="primary"
      outline
      divider
      :title="$t('navigation.history')"
      v-if="this.$fetchState.pending"
    >
      <template #card-body>
        <b-skeleton-table />
        <b-skeleton-table />
      </template>
    </CustomCard>

    <CustomCard
      color="primary"
      outline
      divider
      :title="$t('navigation.history')"
      v-if="!this.$fetchState.pending"
    >
      <template #card-body>
        <b-row class="text-center">
          <b-col cols="12">
            <b-table
              id="match_table"
              table-variant="dark"
              small
              striped
              sort-icon-left
              responsive
              :items="matches"
              :fields="fields"
              :per-page="perPage"
              :current-page="currentPage"
              sort-by="id"
              sort-desc
            >
              <template #cell(button)="data">
                <nuxt-link :to="`/dashboard/matches/${data.item.id}/overview`">
                  <b-btn variant="primary" size="sm">
                    <font-awesome-icon icon="arrow-right" />
                    {{ $t("matches.history.go_to_match") }}
                  </b-btn>
                </nuxt-link>
              </template>
            </b-table>
          </b-col>

          <b-col cols="12">
            <b-pagination
              v-model="currentPage"
              :total-rows="totalRows"
              :per-page="perPage"
              aria-controls="match_table"
              align="center"
            />
          </b-col>
        </b-row>
      </template>
    </CustomCard>
  </div>
</template>

<script>
  import CustomCard from "~/components/CustomCard"
  import {MatchData} from "~/mixins/axios/MatchData"

  export default {
    name: "MatchesHistory",

    data() {
      return {
        fields: [
          {
            key: "id",
            label: "ID",
            sortable: true,
          },
          {
            key: "league_name",
            label: this.$tc("core.league"),
            sortable: true,
          },
          {
            key: "subtitle",
            label: this.$t("core.playday"),
            sortable: false,
          },
          {
            key: "best_of",
            sortable: false,
          },
          {
            key: "team_blue_name",
            label: this.$t("core.team_blue"),
            sortable: true,
          },
          {
            key: "team_orange_name",
            label: this.$t("core.team_orange"),
            sortable: true,
          },
          {
            key: "button",
            label: this.$t("generic.actions"),
            sortable: false,
          },
        ],

        perPage: 10,
        currentPage: 1,
      }
    },

    head() {
      return {
        title: this.$t("navigation.history") + " - Caster Dashboard",
      }
    },

    computed: {
      totalRows() {
        return this.matches.length
      },
    },

    mounted() {
      this.$store.commit("setPageTitle", this.$t("navigation.history"))
      this.$store.commit("setPageTitleIcon", "history")
      this.$store.commit("setBreadcrumbPath", [
        "Dashboard",
        "Matches",
        "History",
      ])
    },

    async fetch() {
      await this.getMatchData()
    },

    mixins: [MatchData],

    components: {
      CustomCard: CustomCard,
    },
  }
</script>

<style scoped></style>
