export const SingleMatch = {
  data() {
    return {
      match: null,
    }
  },

  methods: {
    async getSingleMatch() {
      await this.$axios.$get(`/api/match/${this.matchID}/`).then((data) => {
        this.match = data
      })
    },
  },
}
