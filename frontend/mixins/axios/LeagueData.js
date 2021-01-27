export const LeagueData = {
    data() {
        return {
            leagues: [],
        }
    },

    methods: {
        async getLeagueData() {
            await this.$axios.$get("/api/data/league/")
                .then((data) => {
                    this.leagues = data.sort(compareLeagues);
                })
        }
    }
}

function compareLeagues(a, b){
    if (a.name.toLowerCase() > b.name.toLowerCase()) return 1
    if (a.name.toLowerCase() < b.name.toLowerCase()) return -1
    return 0
}
