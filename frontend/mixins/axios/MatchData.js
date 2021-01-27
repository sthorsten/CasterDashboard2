export const MatchData = {
    data() {
        return {
            matches: [],
        }
    },

    methods: {
        async getMatchData() {
            await this.$axios.$get(`/api/match/?user=${this.$auth.user.id}`)
                .then((data) => {
                    this.matches = data;
                })
        }
    }
}
