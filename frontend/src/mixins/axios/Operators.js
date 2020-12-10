import axios from "axios";

export const Operators = {
    data() {
        return {
            atkOps: null,
            defOps: null,
            operators: null,
            operatorsLoaded: false,
        }
    },
    computed: {
        operatorImgUrls() {
            let urls = []
            this.operators.forEach(o => {
                urls.push(require('@/assets/img/operators/' + o.id + ".svg"))
            })
            return urls
        },
    },
    methods: {
        getOperators() {
            axios.get(`${this.$store.state.backendURL}/api/core/operator/`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.operators = response.data
                this.atkOps = response.data.filter(o => o.side === "ATK").sort(compareOperators)
                this.defOps = response.data.filter(o => o.side === "DEF").sort(compareOperators)
                this.operatorsLoaded = true
            })
        }
    }
}

function compareOperators(a, b) {
    if (a.name.toLowerCase() > b.name.toLowerCase()) return 1;
    if (a.name.toLowerCase() < b.name.toLowerCase()) return -1;
    return 0;
}
