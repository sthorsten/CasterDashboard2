<template>
    <BaseLayout :title="$tc('core.sponsor', 2)" title_icon="fas fa-money-bill-alt" :bc_path="bc_path"></BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";

export default {
    name: "ControlCenter",
    data() {
        return {
            bc_path: ["Dashboard", "Data", "Sponsors"]
        }
    },
    components: {
        BaseLayout
    }
}
</script>

<style scoped>

</style>