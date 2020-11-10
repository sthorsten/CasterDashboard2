<template>
    <BaseLayout :title="$tc('core.season', 2)" title_icon="fas fa-calendar-alt" :bc_path="bc_path">

        <vue-headful :title="$tc('core.season', 2) + ' - Caster Dashboard'"/>

    </BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";

export default {
    name: "ControlCenter",
    data() {
        return {
            bc_path: ["Dashboard", "Data", "Seasons"]
        }
    },
    components: {
        BaseLayout
    }
}
</script>

<style scoped>

</style>