<template>
    <BaseLayout :title="title" title_icon="fas fa-icon" :bc_path="bc_path"></BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";

export default {
    name: "Name",
    data() {
        return {
            bc_path: ["Dashboard", "Category", "Name"]
        }
    },
    components: {
        BaseLayout
    }
}
</script>

<style scoped>

</style>