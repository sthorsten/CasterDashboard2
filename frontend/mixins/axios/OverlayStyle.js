export const OverlayStyle = {
    data() {
        return {
            overlayStyle: null,
        }
    },

    methods: {
        async getOverlayStyle() {
            await this.$axios.$get(`/api/overlay/style/?user=${this.$auth.user.id}`
            ).then((data) => {
                this.overlayStyle = data[0]
            })
        }
    }
}
