export const OverlayStyle = {
    data() {
        return {
            overlayStyle: null,
        }
    },

    methods: {
        async getOverlayStyle() {
            let userID = null

            // Use username for overlays
            if (this.username) {
                await this.$axios.$get(`/api/user/?username=${this.username}`)
                    .then((data) => {
                        this.currentUser = data[0]
                        userID = data[0].id
                    })
            } else {
                // Dashboard variant for logged in User
                if (this.$auth.user) userID = this.$auth.user.id
                else return;
            }


            await this.$axios.$get(`/api/overlay/style/?user=${userID}`
            ).then((data) => {
                this.overlayStyle = data[0]
            })
        }
    }
}
