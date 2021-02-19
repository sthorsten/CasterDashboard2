<template>
    <div>

        <b-row v-if="$fetchState.pending">
            <b-col cols="12" md="6">
                <CustomCard color="primary" outline divider :title="$t('overlays.control_center.overlay_controls')">
                    <template #card-body>
                        <b-skeleton-table :columns="1" :rows="8"></b-skeleton-table>
                    </template>
                </CustomCard>
            </b-col>
            <b-col cols="12" md="6">
                <CustomCard color="primary" outline divider :title="$t('overlays.control_center.overlay_actions')">
                    <template #card-body>
                        <b-skeleton-table :columns="1" :rows="8"></b-skeleton-table>
                    </template>
                </CustomCard>
            </b-col>
        </b-row>

        <b-row v-if="!$fetchState.pending">

            <!-- Overlay Toggles -->
            <b-col cols="12" md="6">

                <CustomCard color="primary" outline divider :title="$t('overlays.control_center.overlay_controls')">
                    <template #card-body>

                        <b-table-simple table-variant="dark" striped small responsive>

                            <b-tbody>

                                <b-tr class="bg-primary">
                                    <b-th colspan="2">{{ $t('overlays.control_center.game_overlays') }}</b-th>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">Start Overlay</b-th>
                                    <b-td class="text-right">
                                        <a href="#"
                                           @click="overlayState.start_state = !overlayState.start_state; updateOverlayState()">
                                            <b-badge :variant="statusColor(overlayState.start_state)"
                                                     class="text-uppercase w-100">
                                                {{ statusText(overlayState.start_state) }}
                                            </b-badge>
                                        </a>
                                    </b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">Maps Overlay</b-th>
                                    <b-td class="text-right">
                                        <a href="#"
                                           @click="overlayState.maps_state = !overlayState.maps_state; updateOverlayState()">
                                            <b-badge :variant="statusColor(overlayState.maps_state)"
                                                     class="text-uppercase w-100">
                                                {{ statusText(overlayState.maps_state) }}
                                            </b-badge>
                                        </a>
                                    </b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">InGame Overlay</b-th>
                                    <b-td class="text-right">
                                        <a href="#"
                                           @click="overlayState.ingame_state = !overlayState.ingame_state; updateOverlayState()">
                                            <b-badge :variant="statusColor(overlayState.ingame_state)"
                                                     class="text-uppercase w-100">
                                                {{ statusText(overlayState.ingame_state) }}
                                            </b-badge>
                                        </a>
                                    </b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">Operator Bans Overlay</b-th>
                                    <b-td class="text-right">
                                        <a href="#"
                                           @click="overlayState.opbans_state = !overlayState.opbans_state; updateOverlayState()">
                                            <b-badge :variant="statusColor(overlayState.opbans_state)"
                                                     class="text-uppercase w-100">
                                                {{ statusText(overlayState.opbans_state) }}
                                            </b-badge>
                                        </a>
                                    </b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">Rounds Overlay</b-th>
                                    <b-td class="text-right">
                                        <a href="#"
                                           @click="overlayState.rounds_state = !overlayState.rounds_state; updateOverlayState()">
                                            <b-badge :variant="statusColor(overlayState.rounds_state)"
                                                     class="text-uppercase w-100">
                                                {{ statusText(overlayState.rounds_state) }}
                                            </b-badge>
                                        </a>
                                    </b-td>
                                </b-tr>

                                <b-tr class="bg-primary">
                                    <b-th colspan="2">{{ $t('overlays.control_center.other_overlays') }}</b-th>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">Poll Overlay</b-th>
                                    <b-td class="text-right">
                                        <a href="#"
                                           @click="overlayState.poll_state = !overlayState.poll_state; updateOverlayState()">
                                            <b-badge :variant="statusColor(overlayState.poll_state)"
                                                     class="text-uppercase w-100">
                                                {{ statusText(overlayState.poll_state) }}
                                            </b-badge>
                                        </a>
                                    </b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">Social Overlay</b-th>
                                    <b-td class="text-right">
                                        <a href="#"
                                           @click="overlayState.social_state = !overlayState.social_state; updateOverlayState()">
                                            <b-badge :variant="statusColor(overlayState.social_state)"
                                                     class="text-uppercase w-100">
                                                {{ statusText(overlayState.social_state) }}
                                            </b-badge>
                                        </a>
                                    </b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">Timer Overlay</b-th>
                                    <b-td class="text-right">
                                        <a href="#"
                                           @click="overlayState.timer_state = !overlayState.timer_state; updateOverlayState()">
                                            <b-badge :variant="statusColor(overlayState.timer_state)"
                                                     class="text-uppercase w-100">
                                                {{ statusText(overlayState.timer_state) }}
                                            </b-badge>
                                        </a>
                                    </b-td>
                                </b-tr>

                                <b-tr>
                                    <b-th class="text-bold">Ticker Overlay</b-th>
                                    <b-td class="text-right">
                                        <a href="#"
                                           @click="overlayState.ticker_state = !overlayState.ticker_state; updateOverlayState()">
                                            <b-badge :variant="statusColor(overlayState.ticker_state)"
                                                     class="text-uppercase w-100">
                                                {{ statusText(overlayState.ticker_state) }}
                                            </b-badge>
                                        </a>
                                    </b-td>
                                </b-tr>

                            </b-tbody>
                        </b-table-simple>

                        <hr class="divider">

                        <b-row>
                            <b-col align="center">
                                <router-link to="/popout/overlay-toggles" target="_blank">
                                    <b-btn variant="secondary" class="pl-4 pr-4">
                                        {{ $t('generic.popout') }}
                                        <i class="fa fas fa-external-link-alt"></i>
                                    </b-btn>
                                </router-link>
                            </b-col>
                        </b-row>

                    </template>
                </CustomCard>

            </b-col>

            <!-- Overlay Actions -->
            <b-col cols="12" md="6">

                <CustomCard color="primary" outline divider :title="$t('overlays.control_center.overlay_actions')">
                    <template #card-body>

                        <span class="font-italic">
                            This feature hasn't been implemented yet
                        </span>
                        <!-- Neutral Face Emoji -->
                        &#128528;<br>

                    </template>
                </CustomCard>

            </b-col>


        </b-row>

    </div>
</template>

<script>
import CustomCard from "~/components/CustomCard";
import {OverlayStateWebsocket} from "~/mixins/websocket/OverlayStateWeboscket";
import axios from "axios";

export default {
    name: "ControlCenter",

    data() {
        return {}
    },

    head() {
        return {
            title: this.$t("navigation.control_center") + " - Caster Dashboard"
        }
    },

    computed: {
        userID(){
            return this.$auth.user.id
        }
    },

    methods: {
        statusColor(status) {
            if (status) return "success"
            return "danger"
        },
        statusText(status) {
            if (status) return this.$t('generic.on')
            return this.$t('generic.off')
        },
        updateOverlayState() {
            this.$axios.$put(`/api/overlay/state/${this.$auth.user.id}/`, this.overlayState)
        },
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$t("navigation.control_center"))
        this.$store.commit("setPageTitleIcon", "desktop")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Overlays", "Control Center"])
    },

    async fetch() {
        this.connectOverlayStateWebsocket()
    },

    mixins: [
        OverlayStateWebsocket
    ],

    components: {
        "CustomCard": CustomCard
    }

}
</script>

<style scoped>

</style>
