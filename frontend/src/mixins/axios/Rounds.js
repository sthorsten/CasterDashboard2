import axios from "axios";

export const Rounds = {
    methods: {
        getRounds(matchID, mapID) {
            return axios.get(`${this.$store.state.backendURL}/api/matches/round/?match=${matchID}&map=${mapID}`, this.$store.getters.authHeader
            ).then((response) => {
                console.debug("Rounds => ", response.data)
                return response.data
            }).catch((error) => {
                console.error(error.response)
            })
        },
    }
}
