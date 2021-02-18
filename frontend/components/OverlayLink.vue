<template>
    <b-input-group>
        <b-input-group-prepend>
            <b-input-group-text class="bg-secondary" style="width: 200px">
                {{ title }}
            </b-input-group-text>
        </b-input-group-prepend>

        <b-form-input readonly disabled
                      :value="`${baseLink}/overlays/${$auth.user.username}/${url}`"
                      class="bg-dark"/>

        <b-input-group-append>
            <b-input-group-text class="bg-primary">
                <a href="#" @click="overlayCopied()"
                   v-clipboard="`${baseLink}/overlays/${$auth.user.username}/${url}`"
                   v-b-popover.hover.top="$t('generic.copy_to_clipboard')">
                    <i class="fa fas fa-clipboard"></i>
                </a>
            </b-input-group-text>

            <b-input-group-text class="bg-warning">
                <a :href="`${baseLink}/overlays/${$auth.user.username}/${url}?layer-name=${title}&layer-width=1920&layer-height=1080`"
                   @click="$event.preventDefault()"
                   style="cursor: move"
                   v-b-popover.hover.top="$t('overlays.customize.drag_to_obs')">
                    <i class="fa fas fa-arrows-alt"></i>
                </a>
            </b-input-group-text>

            <b-input-group-text class="bg-success">
                <a :href="`${baseLink}/overlays/${$auth.user.username}/${url}`" target="_blank"
                   v-b-popover.hover.top="$t('generic.open_in_new_tab')">
                    <i class="fa fas fa-external-link-alt"></i>
                </a>
            </b-input-group-text>
        </b-input-group-append>
    </b-input-group>
</template>

<script>
export default {
    name: "OverlayLink",
    props: {
        title: String,
        url: String,
    },
    computed: {
        baseLink() {
            if (this.$config.browserBaseURL) return this.$config.baseURL
            return location.origin
        }
    },
    methods: {
        overlayCopied() {
            this.$toast.success(this.$t('overlays.customize.overlay_copied'), this.$t('generic.success'),{timeout: 2000})
        }
    }
}
</script>
