<template>
    <BaseLayout :title="title" title_icon="fas fa-icon" :bc_path="bcPath"></BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";

export default {
    name: "Name",
    data() {
        return {
            bcPath: ["Dashboard", "Category", "Name"]
        }
    },
    components: {
        BaseLayout
    }
}
</script>

<style scoped>

</style>