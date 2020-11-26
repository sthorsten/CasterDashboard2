<template>
    <div>

        <CustomCard v-if="status === LoadingStatus.LOADING" color="secondary" outline divider :title="$t('generic.loading')">
            <template #card-body>
                <StatusOverlay type="loading" :text="$t('generic.loading')"></StatusOverlay>
            </template>
        </CustomCard>

        <CustomCard v-if="status === LoadingStatus.ERROR" color="danger" outline divider :title="$t('generic.error')">
            <template #card-body>
                <StatusOverlay type="icon" icon="fas fa-exclamation-triangle fa-2x"
                               :text="$t('generic.loading_failed')"></StatusOverlay>
            </template>
        </CustomCard>

    </div>
</template>

<script>
import CustomCard from "@/components/elements/CustomCard";
import {LoadingStatus} from "@/helpers/const/LoadingStatus";
import StatusOverlay from "@/components/elements/StatusOverlay";

export default {
    name: "LoadingOverlay",
    data() {
        return {
            LoadingStatus: LoadingStatus
        }
    },
    props: {
        "status": Number,
    },
    components: {
        CustomCard, StatusOverlay
    }
}
</script>

<style scoped>

</style>