export const MapPools = {
    data() {
        return {
            mapPools: [],
        }
    },

    methods: {
        async getMapPools() {
            await this.$axios.$get("/api/core/map_pool/")
                .then((data) => {
                    this.mapPools = data.sort(compareMapPools);
                })
        }
    }
}

function compareMapPools(a, b){
    if (a.name.toLowerCase() > b.name.toLowerCase()) return 1
    if (a.name.toLowerCase() < b.name.toLowerCase()) return -1
    return 0
}
