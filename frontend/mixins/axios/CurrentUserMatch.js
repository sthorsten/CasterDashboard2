export const CurrentUserMatch = {
    data() {
        return {
            currentUserMatch: null,
        }
    },

    methods: {
        async getCurrentUserMatch() {
            let userOverlayMatchData = await this.$axios.$get(`/api/overlay/match_data/?user=${this.$auth.user.id}`)
            await this.$axios.$get(`/api/match/${userOverlayMatchData[0].current_match}/`)
                .then((data) => {
                    this.currentUserMatch = data
                })
        }
    }
}
