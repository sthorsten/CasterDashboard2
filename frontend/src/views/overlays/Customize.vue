<template>
    <BaseLayout :title="$t('navigation.customize')" title_icon="fas fa-palette" :bc_path="bc_path">

        <vue-headful :title="$t('navigation.customize') + ' - Caster Dashboard'"/>

    </BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";

export default {
    name: "ControlCenter",
    data() {
        return {
            bc_path: ["Dashboard", "Overlays", "Customize"]
        }
    },
    components: {
        BaseLayout
    }
}
</script>

<style scoped>

</style>