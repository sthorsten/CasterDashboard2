export const TeamData = {
  data() {
    return {
      teams: [],
    }
  },

  methods: {
    async getTeamData() {
      await this.$axios.$get("/api/data/team/").then((data) => {
        this.teams = data.sort(compareTeams)
      })
    },
  },
}

function compareTeams(a, b) {
  if (a.name.toLowerCase() > b.name.toLowerCase()) return 1
  if (a.name.toLowerCase() < b.name.toLowerCase()) return -1
  return 0
}
