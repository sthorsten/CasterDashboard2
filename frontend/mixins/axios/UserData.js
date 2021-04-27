export const UserData = {
  data() {
    return {
      users: [],
    }
  },

  methods: {
    async getUserData() {
      await this.$axios.$get("/api/user/").then((data) => {
        this.users = data.sort(compareUsers)
      })
    },
  },
}

function compareUsers(a, b) {
  if (a.username.toLowerCase() > b.username.toLowerCase()) return 1
  if (a.username.toLowerCase() < b.username.toLowerCase()) return -1
  return 0
}
