export const CurrentUserMatch = {
  data() {
    return {
      currentUser: null,
      currentUserMatch: null,
    }
  },

  methods: {
    async getCurrentUserMatch() {
      let userID = null

      // Use username for overlays
      if (this.username) {
        await this.$axios
          .$get(`/api/user/?username=${this.username}`)
          .then((data) => {
            this.currentUser = data[0]
            userID = data[0].id
          })
      } else {
        // Dashboard variant for logged in User
        if (this.$auth.user) userID = this.$auth.user.id
        else return
      }

      let userOverlayMatchData = await this.$axios.$get(
        `/api/overlay/match_data/?user=${userID}`
      )
      await this.$axios
        .$get(`/api/match/${userOverlayMatchData[0].current_match}/`)
        .then((data) => {
          this.currentUserMatch = data
        })
    },
  },
}
