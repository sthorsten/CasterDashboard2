export const SponsorData = {
    data() {
        return {
            sponsors: [],
        }
    },

    methods: {
        async getSponsorData() {
            await this.$axios.$get("/api/data/sponsor/")
                .then((data) => {
                    this.sponsors = data;
                })
        }
    }
}
