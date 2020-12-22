<template>
    <BaseLayout :title="$t('navigation.customize')" title_icon="fas fa-palette" :bc_path="bcPath">

        <vue-headful :title="$t('navigation.customize') + ' - Caster Dashboard'"/>

        <template v-if="loadingStatus === 'loaded'">
            <b-row>

                <b-col lg="6">

                    <b-row>
                        <b-col cols="12">
                            <CustomCard color="primary" outline divider :title="$t('overlays.customize.select_overlay')">
                                <template #card-body>

                                    <b-row>
                                        <b-col cols="12">
                                            <b-btn v-if="selectedOverlay === 'start'"
                                                   variant="primary" class="btn-block">
                                                {{ $t('overlays.start') }}
                                            </b-btn>
                                            <b-btn v-else
                                                   @click="selectedOverlay = 'start'"
                                                   variant="outline-primary" class="btn-block">
                                                {{ $t('overlays.start') }}
                                            </b-btn>
                                        </b-col>
                                        <b-col cols="12" class="mt-2">
                                            <b-btn v-if="selectedOverlay === 'ingame'"
                                                   variant="primary" class="btn-block">
                                                {{ $t('overlays.ingame') }}
                                            </b-btn>
                                            <b-btn v-else
                                                   @click="selectedOverlay = 'ingame'"
                                                   variant="outline-primary" class="btn-block">
                                                {{ $t('overlays.ingame') }}
                                            </b-btn>
                                        </b-col>
                                    </b-row>

                                </template>
                            </CustomCard>
                        </b-col>

                        <b-col cols="12">
                            <CustomCard color="success" outline divider :title="$t('overlays.customize.customize_overlay')">
                                <template #card-body>

                                    <b-row>
                                        <b-col cols="12">
                                            <label>{{ $t('overlays.customize.default_styles') }}</label>
                                        </b-col>
                                        <b-col cols="4">
                                            <b-btn v-if="selectedOverlayStyle === 'default'"
                                                   :disabled="!selectedOverlay"
                                                   variant="success" class="btn-block">
                                                {{ $t('overlays.customize.default') }}
                                            </b-btn>
                                            <b-btn v-else
                                                   @click="setOverlayStyle('default')"
                                                   :disabled="!selectedOverlay"
                                                   variant="outline-success" class="btn-block">
                                                {{ $t('overlays.customize.default') }}
                                            </b-btn>
                                        </b-col>
                                        <b-col cols="4">
                                            <b-btn v-if="selectedOverlayStyle === 'light'"
                                                   :disabled="!selectedOverlay"
                                                   variant="success" class="btn-block">
                                                {{ $t('overlays.customize.light') }}
                                            </b-btn>
                                            <b-btn v-else
                                                   @click="setOverlayStyle('light')"
                                                   :disabled="!selectedOverlay"
                                                   variant="outline-success" class="btn-block">
                                                {{ $t('overlays.customize.light') }}
                                            </b-btn>
                                        </b-col>
                                        <b-col cols="4">
                                            <b-btn v-if="selectedOverlayStyle === 'dark'"
                                                   :disabled="!selectedOverlay"
                                                   variant="success" class="btn-block">
                                                {{ $t('overlays.customize.dark') }}
                                            </b-btn>
                                            <b-btn v-else
                                                   @click="setOverlayStyle('dark')"
                                                   :disabled="!selectedOverlay"
                                                   variant="outline-success" class="btn-block">
                                                {{ $t('overlays.customize.dark') }}
                                            </b-btn>
                                        </b-col>
                                    </b-row>

                                    <hr class="divider">

                                    <b-row>
                                        <b-col cols="12">
                                            <label>{{ $t('overlays.customize.custom_styles') }}</label>
                                        </b-col>
                                        <b-col cols="4">
                                            <b-btn variant="outline-success" class="btn-block" disabled="true">
                                                FearNix
                                            </b-btn>
                                        </b-col>
                                    </b-row>

                                </template>
                            </CustomCard>
                        </b-col>
                    </b-row>

                </b-col>

                <b-col lg="6">

                    <CustomCard color="danger" outline divider :title="$t('overlays.customize.preview')">
                        <template #card-body>

                            <b-img v-if="selectedOverlay && selectedOverlayStyle"
                                   fluid class="w-100" :src="overlayImageURL"></b-img>
                            <span v-else class="font-italic">
                                {{ $t('overlays.customize.select_first') }}
                            </span>

                        </template>
                    </CustomCard>

                </b-col>


            </b-row>


            <b-row>
                <b-col cols="12">

                    <CustomCard color="secondary" outline divider :title="$t('overlays.customize.overlay_links')">
                        <template #card-body>

                            <b-row>

                                <b-col lg="6">
                                    <OverlayLink :title="$t('overlays.start')" url="start"></OverlayLink>
                                </b-col>

                                <b-col lg="6" class="mt-2 mt-lg-0">
                                    <OverlayLink :title="$t('overlays.maps')" url="maps"></OverlayLink>
                                </b-col>

                                <b-col lg="6" class="mt-2">
                                    <OverlayLink :title="$t('overlays.ingame')" url="ingame"></OverlayLink>
                                </b-col>

                                <b-col lg="6" class="mt-2">
                                    <OverlayLink :title="$t('overlays.opbans')" url="opbans"></OverlayLink>
                                </b-col>

                                <b-col lg="6" class="mt-2">
                                    <OverlayLink :title="$t('overlays.rounds')" url="rounds"></OverlayLink>
                                </b-col>

                            </b-row>

                        </template>
                    </CustomCard>

                </b-col>
            </b-row>

        </template>

        <!-- Loading overlay -->
        <template v-if="loadingStatus === 'loading'">
            <CustomCard color="secondary" outline divider :title="$t('generic.loading')">
                <template #card-body>
                    <StatusOverlay type="loading" :text="$t('generic.loading')"></StatusOverlay>
                </template>
            </CustomCard>
        </template>

        <!-- Error overlay -->
        <template v-if="loadingStatus === 'error'">
            <CustomCard color="danger" outline divider :title="$t('generic.error')">
                <template #card-body>
                    <StatusOverlay type="icon" icon="fas fa-exclamation-triangle fa-2x"
                                   :text="$t('generic.loading_failed')"></StatusOverlay>
                </template>
            </CustomCard>
        </template>


    </BaseLayout>
</template>

<script>
import axios from 'axios';
import BaseLayout from "@/components/layout/BaseLayout";
import CustomCard from "@/components/elements/CustomCard";
import StatusOverlay from "@/components/elements/StatusOverlay";
import OverlayLink from "@/components/subcomponents/OverlayLink";

export default {
    name: "ControlCenter",
    data() {
        return {
            selectedOverlay: null,
            overlayStyleData: null,

            loadingStatus: 'loading',
            bcPath: ["Dashboard", "Overlays", "Customize"]
        }
    },
    computed: {
        selectedOverlayStyle() {
            return this.overlayStyleData[`${this.selectedOverlay}_style`]
        },
        overlayImageURL() {
            return require(`@/assets/img/screenshots/${this.selectedOverlay}-${this.selectedOverlayStyle}.png`)
        }
    },
    methods: {
        setOverlayStyle(style) {
            this.overlayStyleData[`${this.selectedOverlay}_style`] = style
            axios.patch(`${this.$store.state.backendURL}/api/overlay/style/${this.overlayStyleData.id}/`, this.overlayStyleData, this.$store.getters.authHeader
            ).then(() => {
                this.$toast.success(this.$t('overlays.customize.toasts.overlay_updated'), this.$t('generic.success'))
                this.getOverlayStyles()
            })
        },
        getOverlayStyles() {
            axios.get(`${this.$store.state.backendURL}/api/overlay/style/?user=${this.$store.state.user.id}`, this.$store.getters.authHeader
            ).then((response) => {
                this.overlayStyleData = response.data[0]
                this.loadingStatus = 'loaded'
            })
        }
    },
    created() {
        this.getOverlayStyles()
    },
    components: {
        OverlayLink,
        BaseLayout, CustomCard, StatusOverlay
    }
}
</script>

<style scoped>

</style>