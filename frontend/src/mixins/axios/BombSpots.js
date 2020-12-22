import axios from "axios";

export const BombSpots = {
    data() {
        return {
            bombSpots: null,
            bombSpotsLoaded: false,
        }
    },
    methods: {
        getBombSpots() {
            axios.get(`${this.$store.state.backendURL}/api/core/bomb_spot/?map=${this.mapID}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.bombSpots = response.data
                this.bombSpotsLoaded = true
            }).catch((error) => {
                console.log(error.response)
            })
        },
        getBombSpotName(id) {
            let bomb_spot = this.bombSpots.filter(b => b.id === id)[0]
            return bomb_spot.floor + " - " + bomb_spot.name
        },
    }
}
