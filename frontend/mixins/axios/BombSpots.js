export const BombSpots = {
  data() {
    return {
      bombSpots: [],
    }
  },

  methods: {
    async getAllBombSpots() {
      await this.$axios.$get("/api/core/bomb_spot/").then((data) => {
        this.bombSpots = data.sort(compareBombSpots)
      })
    },
    async getBombSpots() {
      await this.$axios
        .$get(`/api/core/bomb_spot/?map=${this.mapID}`)
        .then((data) => {
          this.bombSpots = data.sort(compareBombSpots)
        })
    },
  },
}

// Sort by floor
function compareBombSpots(a, b) {
  if (a.floor.toLowerCase() > b.floor.toLowerCase()) return 1
  if (a.floor.toLowerCase() < b.floor.toLowerCase()) return -1
  return 0
}
