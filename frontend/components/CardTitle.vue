<template>
    <div>
        <h5 class="card-title card-title-upper">{{ title }}</h5>
        <template v-if="divider">
            <br>
            <div class="card-divider"></div>
        </template>
        <template v-else>
            <br><br>
        </template>
    </div>
</template>

<script>
export default {
    name: "card-title",
    props: {
        title: String,
        divider: Boolean
    }
}
</script>
