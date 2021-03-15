export const MatchGroup = {
    data() {
        return {
            matchGroup: null,
        }
    },

    methods: {
        async getMatchGroup() {
            await this.$axios.$get(`/api/match_groups/?users=${this.userID}`)
                .then((data) => {
                    if (data != null && data.length >= 1) {
                        this.matchGroup = data[0]
                    }
                })
        }
    }
}
