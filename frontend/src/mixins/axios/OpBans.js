import axios from "axios";

export const OpBans = {
    methods: {
        getOpBans(matchID, mapID) {
            return axios.get(`${this.$store.state.backendURL}/api/matches/opbans/?match=${matchID}&map=${mapID}`, this.$store.getters.authHeader
            ).then((response) => {
                console.debug("OpBans => ", response.data)
                return response.data
            }).catch((error) => {
                console.error(error.response)
            })
        },
    }
}
