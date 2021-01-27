export const Notifications = {
    data() {
        return {
            notifications: null,
        }
    },

    methods: {
        async getNotifications() {
            await this.$axios.$get('/api/notification/?type=&show=true')
                .then((data) => {
                    this.notifications = data.sort(compareNotifications);
                })
        }
    }
}

// Sort notifications - last first
function compareNotifications(a,b){
    if (a.id > b.id) return -1;
    if (a.id < b.id) return 1;
    return 0;
}
