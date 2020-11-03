<template>
    <BaseLayout title="Rounds" title_icon="fas fa-list-ol" :bc_path="bc_path"></BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";
import axios from "axios";

export default {
    name: "Rounds",
    data() {
        return {
            matchData: null,
            matchMap: null,
            roundData: [],

            matchDataLoaded: false,
            matchMapLoaded: false,
            roundDataLoaded: false,
        }
    },
    computed: {
        bc_path() {
            if (this.matchDataLoaded && this.matchMapLoaded) {
                return ["Dashboard", "Matches", this.$route.params.match_id,
                    this.matchMap.map_name + " (Map " + this.matchMap.play_order + "/" + this.matchData.best_of + ")",
                    "Rounds"]
            } else {
                return ["Dashboard", "Matches", this.$route.params.match_id, this.$route.params.map_id, "Rounds"]
            }
        }
    },
    methods: {
        getMatchData() {
            axios.get(`${this.$store.state.backendURL}/api/match/${this.$route.params.match_id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.matchData = response.data
                this.matchDataLoaded = true
            })
        },
        getMatchMap() {
            axios.get(`${this.$store.state.backendURL}/api/matches/maps/?match=${this.$route.params.match_id}&map=${this.$route.params.map_id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.matchMap = response.data[0]
                this.matchMapLoaded = true
            })
        },
        getRounds(){
            axios.get(`${this.$store.state.backendURL}/api/matches/round/?match=${this.$route.params.match_id}&map=${this.$route.params.map_id}`, this.$store.getters.authHeader
            ).then((response) => {
                console.log(response.data)
                this.roundData = response.data[0]
                this.roundDataLoaded = true
            })
        },
    },
    created() {
        this.getMatchData()
        this.getMatchMap()
        this.getRounds()
    },
    components: {
        BaseLayout
    }
}
</script>

<style scoped>

</style>