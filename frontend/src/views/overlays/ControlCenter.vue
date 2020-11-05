<template>
    <BaseLayout :title="$t('navigation.control_center')" title_icon="fas fa-desktop" :bc_path="bc_path">



    </BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";

export default {
    name: "ControlCenter",
    data() {
        return {
            bc_path: ["Dashboard", "Overlays", "Control Center"]
        }
    },
    components: {
        BaseLayout
    },
    created() {

    }
}
</script>

<style scoped>

</style>