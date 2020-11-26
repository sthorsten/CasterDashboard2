<template>

    <div class="min-vh-100 min-vw-100 bg-dark pt-2">

        <vue-headful :title="$t('navigation.control_center') + ' - Caster Dashboard'"/>

        <template v-if="overlayStateWebsocketStatus === 'connected'">

            <b-row class="m-0">

                <!-- Overlay Controls -->
                <b-col cols="12">

                    <CustomCard color="primary" outline divider :title="$t('overlays.control_center.overlay_controls')">
                        <template #card-body>

                            <b-table-simple v-if="overlayState != null" table-variant="dark" striped small responsive>

                                <b-tbody>

                                    <b-tr class="bg-primary">
                                        <b-th colspan="2">{{ $t('overlays.control_center.game_overlays') }}</b-th>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Start Overlay</b-th>
                                        <b-td class="text-right">
                                            <a href="#" @click="overlayState.start_state = !overlayState.start_state; updateOverlayState()">
                                                <b-badge :variant="statusColor(overlayState.start_state)" class="text-uppercase w-100">
                                                    {{ statusText(overlayState.start_state) }}
                                                </b-badge>
                                            </a>
                                        </b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Maps Overlay</b-th>
                                        <b-td class="text-right">
                                            <a href="#" @click="overlayState.maps_state = !overlayState.maps_state; updateOverlayState()">
                                                <b-badge :variant="statusColor(overlayState.maps_state)" class="text-uppercase w-100">
                                                    {{ statusText(overlayState.maps_state) }}
                                                </b-badge>
                                            </a>
                                        </b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">InGame Overlay</b-th>
                                        <b-td class="text-right">
                                            <a href="#" @click="overlayState.ingame_state = !overlayState.ingame_state; updateOverlayState()">
                                                <b-badge :variant="statusColor(overlayState.ingame_state)" class="text-uppercase w-100">
                                                    {{ statusText(overlayState.ingame_state) }}
                                                </b-badge>
                                            </a>
                                        </b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Operator Bans Overlay</b-th>
                                        <b-td class="text-right">
                                            <a href="#" @click="overlayState.opbans_state = !overlayState.opbans_state; updateOverlayState()">
                                                <b-badge :variant="statusColor(overlayState.opbans_state)" class="text-uppercase w-100">
                                                    {{ statusText(overlayState.opbans_state) }}
                                                </b-badge>
                                            </a>
                                        </b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Rounds Overlay</b-th>
                                        <b-td class="text-right">
                                            <a href="#" @click="overlayState.rounds_state = !overlayState.rounds_state; updateOverlayState()">
                                                <b-badge :variant="statusColor(overlayState.rounds_state)" class="text-uppercase w-100">
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
                                            <a href="#" @click="overlayState.poll_state = !overlayState.poll_state; updateOverlayState()">
                                                <b-badge :variant="statusColor(overlayState.poll_state)" class="text-uppercase w-100">
                                                    {{ statusText(overlayState.poll_state) }}
                                                </b-badge>
                                            </a>
                                        </b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Social Overlay</b-th>
                                        <b-td class="text-right">
                                            <a href="#" @click="overlayState.social_state = !overlayState.social_state; updateOverlayState()">
                                                <b-badge :variant="statusColor(overlayState.social_state)" class="text-uppercase w-100">
                                                    {{ statusText(overlayState.social_state) }}
                                                </b-badge>
                                            </a>
                                        </b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Timer Overlay</b-th>
                                        <b-td class="text-right">
                                            <a href="#" @click="overlayState.timer_state = !overlayState.timer_state; updateOverlayState()">
                                                <b-badge :variant="statusColor(overlayState.timer_state)" class="text-uppercase w-100">
                                                    {{ statusText(overlayState.timer_state) }}
                                                </b-badge>
                                            </a>
                                        </b-td>
                                    </b-tr>

                                    <b-tr>
                                        <b-th class="text-bold">Ticker Overlay</b-th>
                                        <b-td class="text-right">
                                            <a href="#" @click="overlayState.ticker_state = !overlayState.ticker_state; updateOverlayState()">
                                                <b-badge :variant="statusColor(overlayState.ticker_state)" class="text-uppercase w-100">
                                                    {{ statusText(overlayState.ticker_state) }}
                                                </b-badge>
                                            </a>
                                        </b-td>
                                    </b-tr>

                                </b-tbody>
                            </b-table-simple>

                        </template>
                    </CustomCard>
                </b-col>
            </b-row>
        </template>

        <!-- Loading overlay -->
        <template v-if="overlayStateWebsocketStatus === 'none' || overlayStateWebsocketStatus === 'reconnecting'">
            <CustomCard color="secondary" outline divider :title="$t('generic.loading')">
                <template #card-body>
                    <StatusOverlay type="loading" :text="$t('generic.loading')"></StatusOverlay>
                </template>
            </CustomCard>
        </template>

    </div>

</template>

<script>
import CustomCard from "@/components/elements/CustomCard";
import StatusOverlay from "@/components/elements/StatusOverlay";
import axios from 'axios';
import {OverlayStateWebsocket} from "@/mixins/websocket/OverlayStateWebsocket";

export default {
    name: "OverlayControlCenterPopout",
    mixins: [OverlayStateWebsocket],
    data() {
        return {
            bcPath: ["Dashboard", "Overlays", "Control Center"]
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
            axios.put(`${this.$store.state.backendURL}/api/overlay/state/${this.$store.state.user.id}/`, this.overlayState, this.$store.getters.authHeader)
        },
    },
    components: {
        CustomCard, StatusOverlay
    },
}
</script>

<style scoped>

</style>