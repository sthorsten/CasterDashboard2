export const SingleUser = {
  data() {
    return {
      currentUser: null,
    }
  },

  methods: {
    async getSingleUser() {
      let userID = null

      // Use username for overlays
      if (this.username) {
        await this.$axios
          .$get(`/api/user/?username=${this.username}`)
          .then((data) => {
            this.currentUser = data[0]
          })
      } else {
        // Dashboard variant for logged in User
        if (this.$auth.user) this.currentUser = this.$auth.user
        else return
      }
    },
  },
}
