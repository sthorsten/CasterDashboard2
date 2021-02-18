export const Operators = {
    data() {
        return {
            atkOps: [],
            defOps: []
        }
    },

    methods: {
        async getOperators() {
            await this.$axios.$get(`/api/core/operator/?side=ATK`)
                .then((data) => {
                    this.atkOps = data.sort(compareOperators)
                })

            await this.$axios.$get(`/api/core/operator/?side=DEF`)
                .then((data) => {
                    this.defOps = data.sort(compareOperators)
                })
        }
    }
}

function compareOperators(a, b) {
    if (a.name.toLowerCase() > b.name.toLowerCase()) return 1
    if (a.name.toLowerCase() < b.name.toLowerCase()) return -1
    return 0
}
