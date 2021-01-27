<template>
    <div>

    </div>
</template>

<script>
import CustomCard from "~/components/CustomCard";
import {SingleMatch} from "~/mixins/axios/SingleMatch";
import {SingleMatchMap} from "~/mixins/axios/SingleMatchMap";

export default {
    name: "OperatorBans",
    layout: "match",

    data() {
        return {}
    },

    head() {
        return {
            title: this.$t("navigation.op_bans") + " - Caster Dashboard"
        }
    },

    computed: {
        matchID() {
            return this.$route.params.matchID
        },
        mapID() {
            return this.$route.params.mapID
        }
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$t("navigation.op_bans"))
        this.$store.commit("setPageTitleIcon", "users-slash")
        this.$store.commit("setBreadcrumbPath",
            ["Dashboard", "Matches", this.$route.params.matchID, "Map " + this.$route.params.mapID, "OpBans"]
        )
    },

    async fetch() {
        await this.getSingleMatch()

        await this.getSingleMatchMap()
        // Set Map to Breadcrumbs
        this.$store.commit("setBreadcrumbPath",
            ["Dashboard", "Matches", this.$route.params.matchID, `${this.matchMap.map_name} (Map ${this.matchMap.play_order}/${this.match.best_of})`, "OpBans"]
        )
    },

    mixins: [
        SingleMatch,
        SingleMatchMap
    ],

    components: {
        "CustomCard": CustomCard
    }

}
</script>

<style scoped>

</style>
