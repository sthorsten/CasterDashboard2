<template>
    <BaseLayout :title="$tc('core.league', 2)" title_icon="fas fa-trophy" :bc_path="bc_path"></BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";

export default {
    name: "ControlCenter",
    data() {
        return {
            bc_path: ["Dashboard", "Data", "Leagues"]
        }
    },
    components: {
        BaseLayout
    }
}
</script>

<style scoped>

</style>