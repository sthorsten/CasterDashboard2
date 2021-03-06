<template>
  <div>
    <b-row v-if="$fetchState.pending">
      <b-col cols="12" lg="6">
        <CustomCard
          color="primary"
          outline
          divider
          :title="$t('generic.loading')"
        >
          <template #card-body>
            <b-skeleton-table columns="1" rows="8"></b-skeleton-table>
          </template>
        </CustomCard>
      </b-col>
      <b-col cols="12" lg="6">
        <CustomCard
          color="success"
          outline
          divider
          :title="$t('overlays.customize.preview')"
        >
          <template #card-body>
            <b-skeleton-table columns="1" rows="4"></b-skeleton-table>
          </template>
        </CustomCard>
      </b-col>
    </b-row>

    <b-row v-if="!$fetchState.pending">
      <b-col cols="12" lg="6">
        <b-row>
          <!-- Overlay Selection -->
          <b-col cols="12">
            <CustomCard
              color="primary"
              outline
              divider
              :title="$t('overlays.customize.select_overlay')"
            >
              <template #card-body>
                <b-row>
                  <b-col cols="12">
                    <b-btn
                      v-if="selectedOverlay === 'start'"
                      variant="primary"
                      class="btn-block"
                    >
                      {{ $t("overlays.start") }}
                    </b-btn>
                    <b-btn
                      v-else
                      @click="selectedOverlay = 'start'"
                      variant="outline-primary"
                      class="btn-block"
                    >
                      {{ $t("overlays.start") }}
                    </b-btn>
                  </b-col>
                  <b-col cols="12" class="mt-2">
                    <b-btn
                      v-if="selectedOverlay === 'ingame'"
                      variant="primary"
                      class="btn-block"
                    >
                      {{ $t("overlays.ingame") }}
                    </b-btn>
                    <b-btn
                      v-else
                      @click="selectedOverlay = 'ingame'"
                      variant="outline-primary"
                      class="btn-block"
                    >
                      {{ $t("overlays.ingame") }}
                    </b-btn>
                  </b-col>
                </b-row>
              </template>
            </CustomCard>
          </b-col>

          <!-- Customize Overlay -->
          <b-col cols="12">
            <CustomCard
              color="primary"
              outline
              divider
              :title="$t('overlays.customize.customize_overlay')"
            >
              <template #card-body>
                <b-row>
                  <b-col cols="12">
                    <label>{{ $t("overlays.customize.default_styles") }}</label>
                  </b-col>
                  <b-col cols="4">
                    <b-btn
                      v-if="selectedOverlayStyle === 'default'"
                      :disabled="!selectedOverlay"
                      variant="primary"
                      class="btn-block"
                    >
                      {{ $t("overlays.customize.default") }}
                    </b-btn>
                    <b-btn
                      v-else
                      @click="setOverlayStyle('default')"
                      :disabled="!selectedOverlay"
                      variant="outline-primary"
                      class="btn-block"
                    >
                      {{ $t("overlays.customize.default") }}
                    </b-btn>
                  </b-col>
                  <b-col cols="4">
                    <b-btn
                      v-if="selectedOverlayStyle === 'light'"
                      :disabled="!selectedOverlay"
                      variant="primary"
                      class="btn-block"
                    >
                      {{ $t("overlays.customize.light") }}
                    </b-btn>
                    <b-btn
                      v-else
                      @click="setOverlayStyle('light')"
                      :disabled="!selectedOverlay"
                      variant="outline-primary"
                      class="btn-block"
                    >
                      {{ $t("overlays.customize.light") }}
                    </b-btn>
                  </b-col>
                  <b-col cols="4">
                    <b-btn
                      v-if="selectedOverlayStyle === 'dark'"
                      :disabled="!selectedOverlay"
                      variant="primary"
                      class="btn-block"
                    >
                      {{ $t("overlays.customize.dark") }}
                    </b-btn>
                    <b-btn
                      v-else
                      @click="setOverlayStyle('dark')"
                      :disabled="!selectedOverlay"
                      variant="outline-primary"
                      class="btn-block"
                    >
                      {{ $t("overlays.customize.dark") }}
                    </b-btn>
                  </b-col>
                </b-row>

                <hr class="divider" />

                <b-row>
                  <b-col cols="12">
                    <label>
                      {{ $t("overlays.customize.custom_styles") }}
                    </label>
                  </b-col>
                  <b-col v-if="customLeagueStyles.length === 0">
                    <i>{{ $t("overlays.customize.no_custom_style") }}</i>
                  </b-col>
                  <b-col
                    v-for="(league, index) in customLeagueStyles"
                    :key="league.id"
                    cols="4"
                  >
                    <b-btn
                      v-if="selectedOverlayStyle === league.name.toLowerCase()"
                      @click="setOverlayStyle(league.name.toLowerCase())"
                      :disabled="!selectedOverlay"
                      variant="primary"
                      class="btn-block"
                    >
                      {{ league.name }}
                    </b-btn>
                    <b-btn
                      v-else
                      @click="setOverlayStyle(league.name.toLowerCase())"
                      :disabled="!selectedOverlay"
                      variant="outline-primary"
                      class="btn-block"
                    >
                      {{ league.name }}
                    </b-btn>
                  </b-col>
                </b-row>
              </template>
            </CustomCard>
          </b-col>
        </b-row>
      </b-col>

      <b-col cols="12" lg="6">
        <CustomCard
          color="success"
          outline
          divider
          :title="$t('overlays.customize.preview')"
        >
          <template #card-body>
            <b-img
              v-if="selectedOverlay && selectedOverlayStyle"
              fluid
              class="w-100"
              :src="getStyleScreenshot(selectedOverlay, selectedOverlayStyle)"
              alt="Screenshot not available :/"
            >
            </b-img>
            <span v-else class="font-italic">
              {{ $t("overlays.customize.select_first") }}
            </span>
          </template>
        </CustomCard>
      </b-col>
    </b-row>

    <!-- Links -->
    <b-row>
      <b-col cols="12">
        <CustomCard
          color="secondary"
          outline
          divider
          :title="$t('overlays.customize.overlay_links')"
        >
          <template #card-body>
            <b-row>
              <b-col lg="6">
                <OverlayLink
                  :title="$t('overlays.start')"
                  url="start"
                ></OverlayLink>
              </b-col>

              <b-col lg="6">
                <OverlayLink
                  :title="$t('overlays.ingame')"
                  url="ingame"
                ></OverlayLink>
              </b-col>

              <b-col lg="6" class="mt-2">
                <OverlayLink
                  :title="$t('overlays.start_next')"
                  url="start/next"
                ></OverlayLink>
              </b-col>

              <b-col lg="6" class="mt-2">
                <OverlayLink
                  :title="$t('overlays.opbans')"
                  url="opbans"
                ></OverlayLink>
              </b-col>

              <b-col lg="6" class="mt-2">
                <OverlayLink
                  :title="$t('overlays.maps')"
                  url="maps"
                ></OverlayLink>
              </b-col>

              <b-col lg="6" class="mt-2">
                <OverlayLink
                  :title="$t('overlays.rounds')"
                  url="rounds"
                ></OverlayLink>
              </b-col>
            </b-row>
          </template>
        </CustomCard>
      </b-col>
    </b-row>
  </div>
</template>

<script>
  import CustomCard from "~/components/CustomCard"
  import OverlayLink from "~/components/OverlayLink"
  import {OverlayStyle} from "~/mixins/axios/OverlayStyle"
  import {LeagueGroups} from "~/mixins/axios/LeagueGroups"
  import {LeagueData} from "~/mixins/axios/LeagueData"

  export default {
    name: "OverlayCustomize",

    data() {
      return {
        selectedOverlay: null,
      }
    },

    head() {
      return {
        title: this.$t("navigation.customize") + " - Caster Dashboard",
      }
    },

    computed: {
      selectedOverlayStyle() {
        if (this.overlayStyle)
          return this.overlayStyle[`${this.selectedOverlay}_style`]
        return null
      },
      customLeagueStyles() {
        let leaguesWithCustomStyle = this.leagues.filter(
          (l) => l.has_custom_overlay === true
        )
        let customStyles = []
        for (const group of this.leagueGroups) {
          for (const league of leaguesWithCustomStyle) {
            if (group.league === league.id) customStyles.push(league)
          }
        }
        return customStyles
      },
    },

    methods: {
      setOverlayStyle(style) {
        this.overlayStyle[`${this.selectedOverlay}_style`] = style
        this.$axios
          .$patch(
            `/api/overlay/style/${this.overlayStyle.id}/`,
            this.overlayStyle
          )
          .then(() => {
            this.$toast.success(
              this.$t("overlays.customize.toasts.overlay_updated"),
              this.$t("generic.success")
            )
            this.$fetch()
          })
      },
      getStyleScreenshot(overlay, style) {
        try {
          return require(`~/assets/img/screenshots/${overlay}-${style.toLowerCase()}.png`)
        } catch (e) {
          return ""
        }
      },
    },

    mounted() {
      this.$store.commit("setPageTitle", this.$t("navigation.customize"))
      this.$store.commit("setPageTitleIcon", "palette")
      this.$store.commit("setBreadcrumbPath", [
        "Dashboard",
        "Overlays",
        "Customize",
      ])
    },

    async fetch() {
      await Promise.all([
        this.getOverlayStyle(),
        this.getLeagueGroups(),
        this.getLeagueData(),
      ])
    },

    mixins: [OverlayStyle, LeagueGroups, LeagueData],

    components: {
      CustomCard: CustomCard,
      OverlayLink: OverlayLink,
    },
  }
</script>

<style scoped></style>
