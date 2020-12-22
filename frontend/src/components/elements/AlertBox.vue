<template>

    <b-row v-if="show">
        <b-col>
            <b-alert :variant="variant" :show="true">
                <span class="font-italic">
                    <i :class="icon"></i>
                    <b>{{ title }}</b> {{ text }}
                </span>
                <span v-if="loading">
                    <b-spinner :variant="loadingVariant" small></b-spinner>
                </span>
            </b-alert>
        </b-col>
    </b-row>

</template>

<script>
export default {
    name: "AlertBox",
    props: {
        "icon": String,
        "title": String,
        "text": String,
        "variant": String,
        "show": Boolean,
        "loading": Boolean,
        "loadingVariant": String
    },
}
</script>

<style scoped>

</style>