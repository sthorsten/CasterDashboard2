<template>
  <div>
    <CustomCard
      color="primary"
      outline
      divider
      :title="$t('data.seasons.title')"
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
      :title="$t('data.seasons.title')"
      v-if="!this.$fetchState.pending"
    >
      <template #card-body>
        <b-row class="text-center">
          <b-col cols="12">
            <b-table
              id="season_table"
              table-variant="dark"
              small
              striped
              sort-icon-left
              responsive
              :items="seasons"
              :fields="fields"
              :per-page="perPage"
              :current-page="currentPage"
              sort-by="official_season"
              sort-desc
            >
              <template #cell(official)="data">
                <span v-if="data.item.official_season">
                  {{ $t("generic.yes") }}
                </span>
                <span v-else>
                  {{ $t("generic.no") }}
                </span>
              </template>

              <template #cell(associated_league)="data">
                <span v-if="data.item.league_name">
                  {{ data.item.league_name }}
                </span>
                <span v-else> - </span>
              </template>

              <template #cell(season_start_date)="data">
                {{ $d(new Date(data.item.start_date), "short") }}
              </template>

              <template #cell(season_end_date)="data">
                <span v-if="data.item.end_date">
                  {{ $d(new Date(data.item.end_date), "short") }}
                </span>
                <span v-else> - </span>
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
  import {SeasonData} from "~/mixins/axios/SeasonData"

  export default {
    name: "SeasonData",

    data() {
      return {
        fields: [
          {
            key: "id",
            label: "ID",
            sortable: true,
          },
          {
            key: "name",
            label: this.$tc("core.season"),
            sortable: true,
          },
          {
            key: "official",
            label: this.$t("data.seasons.official_season"),
            sortable: true,
          },
          {
            key: "associated_league",
            label: this.$t("data.seasons.associated_league"),
            sortable: true,
          },
          {
            key: "season_start_date",
            label: this.$t("data.seasons.start_date"),
            sortable: false,
          },
          {
            key: "season_end_date",
            label: this.$t("data.seasons.end_date"),
            sortable: false,
          },
        ],

        perPage: 10,
        currentPage: 1,
      }
    },

    head() {
      return {
        title: this.$tc("core.season", 2) + " - Caster Dashboard",
      }
    },

    computed: {
      totalRows() {
        return this.seasons.length
      },
    },

    mounted() {
      this.$store.commit("setPageTitle", this.$tc("core.season", 2))
      this.$store.commit("setPageTitleIcon", "calendar-alt")
      this.$store.commit("setBreadcrumbPath", ["Dashboard", "Data", "Seasons"])
    },

    async fetch() {
      await this.getSeasonData()
    },

    mixins: [SeasonData],

    components: {
      CustomCard: CustomCard,
    },
  }
</script>

<style scoped></style>
