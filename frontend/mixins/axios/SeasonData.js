export const SeasonData = {
    data() {
        return {
            seasons: [],
        }
    },

    methods: {
        async getSeasonData() {
            await this.$axios.$get("/api/data/season/")
                .then((data) => {
                    this.seasons = data.sort(compareSeasons)
                })
        }
    }
}

// Sorts season by official season first, then by league and then by name
function compareSeasons(a, b) {
    if (a.official_season === b.official_season) {
        if (a.league_name > b.league_name) return 1
        if (a.league_name < b.league_name) return -1

        if (a.league === b.league){
            if (a.name.toLowerCase() > b.name.toLowerCase()) return 1
            if (a.name.toLowerCase() < b.name.toLowerCase()) return -1
        }
    } else {
        if (a.official_season) return -1
        if (b.official_season) return 1
    }
    return 0
}
