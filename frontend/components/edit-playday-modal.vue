<template>
  <b-modal
    id="edit-playday-modal"
    size="lg"
    header-bg-variant="primary"
    hide-footer
  >
    <template #modal-header>
      <h5 class="modal-title">
        <fa-icon icon="calendar-day" class="mr-1" />
        <span>Edit playday</span>
      </h5>
    </template>

    <!-- Playday ID -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="list-ol" class="mr-1" />
        <span>Playday ID</span>
      </template>

      <div class="d-flex align-items-center text-center h-100">
        <span v-if="playday">
          {{ playday.id }}
        </span>
      </div>
    </b-form-group>

    <!-- Playday League -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="trophy" class="mr-1" />
        <span>League</span>
      </template>

      <div class="d-flex align-items-center text-center h-100">
        <span v-if="playday">
          <img :src="leagueLogo" width="25" height="25" />
          {{ playday.leagueName }}
        </span>
      </div>
    </b-form-group>

    <!-- Playday Season -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="calendar-alt" class="mr-1" />
        <span>Season</span>
      </template>

      <div class="d-flex align-items-center text-center h-100">
        <span v-if="playday">
          {{ playday.seasonName }}
        </span>
      </div>
    </b-form-group>

    <!-- Playday Date -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="calendar-check" class="mr-1" />
        <span>Playday Date</span>
      </template>

      <b-form-input
        v-model="playdayDate"
        type="date"
        placeholder="Enter a playday date"
      />
    </b-form-group>

    <!-- Playday Number -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="list-ol" class="mr-1" />
        <span>Playday Number</span>
      </template>

      <b-form-input
        v-model="playdayNumber"
        type="number"
        placeholder="Enter a playday number"
      />
    </b-form-group>

    <!-- Playday Name -->
    <b-form-group label-cols="4">
      <template #label>
        <fa-icon icon="header" class="mr-1" />
        <span>Playday Name</span>
      </template>

      <b-form-input
        v-model="playdayName"
        type="text"
        placeholder="Enter a playday name"
      />
    </b-form-group>

    <hr class="border-secondary" />

    <b-btn
      block
      variant="primary"
      :disabled="!playdayDate || !playdayNumber || !playdayName"
      @click="updatePlayday"
    >
      <fa-icon icon="check-circle" class="mr-1" />
      <span>Update playday</span>
    </b-btn>
  </b-modal>
</template>

<script>
export default {
  name: 'EditPlaydayModal',

  data() {
    return {
      playdayDate: null,
      playdayNumber: 0,
      playdayName: '',
    }
  },

  props: {
    playdayId: Number
  },

  watch: {
    playday(newVal) {
      if (newVal) {
        this.playdayDate = newVal.date
        this.playdayNumber = newVal.playdayNo
        this.playdayName = newVal.name
      }
    },
  },

  computed: {
    playday() {
      return this.$store.getters['mainSocket/getPlayday'](this.playdayId)
    },
    leagueLogo() {
      if (this.playday) {
        return this.$store.getters['mainSocket/getLeagueLogo'](this.playday.league)
      }
    }
  },

  methods: {
    async updatePlayday() {
      const data = {
        date: this.playdayDate,
        playdayNo: this.playdayNumber,
        name: this.playdayName
      }

      try {
        await this.$axios.$patch(`/api/v2/main/playday/${this.playday.id}/`, data)
        this.$toast.success("Playday updated successfully")
      } catch (e) {
        this.$toast.error("Failed to update playday!")
      }

      this.$bvModal.hide('edit-playday-modal')
    }
  }

}
</script>