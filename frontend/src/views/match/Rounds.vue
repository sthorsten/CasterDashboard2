<template>
    <BaseLayout title="Rounds" title_icon="fas fa-list-ol" :bc_path="bc_path"></BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";

export default {
    name: "Rounds",
    data() {
        return {
            bc_path: ["Dashboard", "Matches", this.$route.params.match_id, this.$route.params.map_id, "Rounds"]
        }
    },
    components: {
        BaseLayout
    }
}
</script>

<style scoped>

</style>