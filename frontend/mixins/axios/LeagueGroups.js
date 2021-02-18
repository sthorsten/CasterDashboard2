export const LeagueGroups = {
    data() {
        return {
            leagueGroups: [],
        }
    },

    methods: {
        async getLeagueGroups() {
            await this.$axios.$get(`/api/data/league_group/?user=${this.$auth.user.id}`)
                .then((data) => {
                    this.leagueGroups = data.sort(compareLeagueGroups);
                })
        }
    }
}

function compareLeagueGroups(a, b){
    if (a.league_name.toLowerCase() > b.league_name.toLowerCase()) return 1
    if (a.league_name.toLowerCase() < b.league_name.toLowerCase()) return -1
    return 0
}
