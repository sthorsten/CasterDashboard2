<template>
  <b-modal
    id="edit-season-modal"
    size="lg"
    header-bg-variant="primary"
    hide-footer
  >
    <template #modal-header>
      <h5 class="modal-title">
        <fa-icon icon="calendar-alt" class="mr-1" />
        <span>Edit season</span>
      </h5>
    </template>

    <!-- Season ID -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="list-ol" class="mr-1" />
        <span>Season ID</span>
      </template>

      <div class="d-flex align-items-center text-center h-100">
        <span v-if="season">
          {{ season.id }}
        </span>
      </div>
    </b-form-group>

    <!-- Season League -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="trophy" class="mr-1" />
        <span>League</span>
      </template>

      <div class="d-flex align-items-center text-center h-100">
        <span v-if="season">
          <img :src="leagueLogo" width="25" height="25" />
          {{ season.leagueName }}
        </span>
      </div>
    </b-form-group>

    <!-- Season start date -->
    <b-form-group label-cols-lg="4">
      <template #label>
        <fa-icon icon="calendar-check" class="mr-1" />
        <span>Season Start Date</span>
      </template>

      <b-form-input v-model="seasonStartDate" type="date" />
    </b-form-group>

    <!-- Season end date -->
    <b-form-group label-cols-lg="4">
      <template #label>
        <fa-icon icon="calendar-check" class="mr-1" />
        <span>Season End Date</span>
      </template>

      <b-form-input v-model="seasonEndDate" type="date" />
    </b-form-group>

    <!-- Season playday count -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="list-ol" class="mr-1" />
        <span>Number of Playdays</span>
      </template>

      <b-form-input
        v-model="playdayCount"
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
        v-model="seasonNumber"
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

      <b-form-input v-model="seasonName" placeholder="Enter a season name" />
    </b-form-group>

    <hr class="border-secondary" />

    <b-btn
      block
      variant="primary"
      :disabled="
        !seasonStartDate ||
        !seasonEndDate ||
        !playdayCount ||
        !seasonNumber ||
        !seasonName
      "
      @click="updateSeason"
    >
      <fa-icon icon="check-circle" class="mr-1" />
      <span>Update season</span>
    </b-btn>
  </b-modal>
</template>

<script>
export default {

  data() {
    return {
      seasonStartDate: null,
      seasonEndDate: null,
      playdayCount: null,
      seasonNumber: null,
      seasonName: null,
    }
  },

  props: {
    seasonId: Number
  },

  watch: {
    season(newVal) {
      if (newVal) {
        this.seasonStartDate = newVal.startDate
        this.seasonEndDate = newVal.endDate
        this.playdayCount = newVal.playdayCount
        this.seasonNumber = newVal.seasonNo
        this.seasonName = newVal.name
      }
    },
  },

  computed: {
    season() {
      return this.$store.getters['mainSocket/getSeason'](this.seasonId)
    },
    leagueLogo() {
      if (this.season) {
        return this.$store.getters['mainSocket/getLeagueLogo'](this.season.league)
      }
    }
  },

  methods: {
    async updateSeason() {
      const data = {
        league: this.season.league,
        startDate: this.seasonStartDate,
        endDate: this.seasonEndDate,
        playdayCount: this.playdayCount,
        seasonNo: this.seasonNumber,
        name: this.seasonName
      }

      try {
        await this.$axios.$patch(`/api/v2/main/season/${this.season.id}/`, data)
        this.$toast.success("Season updated successfully")
      } catch (e) {
        this.$toast.error("Failed to update season!")
      }

      this.$bvModal.hide('edit-season-modal')
    }
  }

}
</script>