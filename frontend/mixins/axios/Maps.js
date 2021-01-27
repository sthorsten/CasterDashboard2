export const Maps = {
    data() {
        return {
            maps: [],
        }
    },

    methods: {
        async getMaps() {
            await this.$axios.$get("/api/core/map/")
                .then((data) => {
                    this.maps = data.sort(compareMaps);
                })
        }
    }
}

function compareMaps(a, b){
    if (a.name.toLowerCase() > b.name.toLowerCase()) return 1
    if (a.name.toLowerCase() < b.name.toLowerCase()) return -1
    return 0
}
