export const SingleMatchMap = {
  data() {
    return {
      matchMap: null,
    }
  },

  methods: {
    async getSingleMatchMap() {
      await this.$axios
        .$get(`/api/matches/maps/?match=${this.matchID}&map=${this.mapID}`)
        .then((data) => {
          this.matchMap = data[0]
        })
    },
  },
}
