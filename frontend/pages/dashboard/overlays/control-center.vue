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
                                    <b-th class="text-bold">Start Next Overlay</b-th>
                                    <b-td class="text-right">
                                        <a href="#"
                                           @click="overlayState.start_next_state = !overlayState.start_next_state; updateOverlayState()">
                                            <b-badge :variant="statusColor(overlayState.start_next_state)"
                                                     class="text-uppercase w-100">
                                                {{ statusText(overlayState.start_next_state) }}
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

                        <!-- Ticker Settings -->
                        <b-row>
                            <b-col>
                                <label>{{ $t("overlays.control_center.ticker_data") }}:</label>

                                <b-input-group v-for="(text, index) in tickerText" :key="index" class="mb-2">
                                    <b-form-input v-if="tickerEditIndex !== index" readonly disabled
                                                  :value="text"
                                                  class="bg-dark"/>

                                    <b-form-input v-else class="bg-dark border-success" :formatter="tickerTextFormatter"
                                                  v-model="tickerEditText"/>

                                    <b-input-group-append v-if="tickerEditIndex === index">
                                        <b-btn variant="success" @click="editTickerText">
                                            <font-awesome-icon icon="save" class="mr-1"/>
                                            {{ $t('generic.save') }}
                                        </b-btn>
                                    </b-input-group-append>

                                    <b-input-group-append v-else>
                                        <b-btn variant="secondary"
                                               @click="tickerEditText = text; tickerEditIndex = index">
                                            <font-awesome-icon icon="pencil-alt" class="mr-1"/>
                                            {{ $t('generic.edit') }}
                                        </b-btn>
                                        <b-btn variant="danger" @click="deleteTickerText(index)">
                                            <font-awesome-icon icon="trash" class="mr-1"/>
                                            {{ $t('generic.delete') }}
                                        </b-btn>
                                    </b-input-group-append>
                                </b-input-group>

                                <b-input-group>
                                    <b-form-input class="bg-dark" :formatter="tickerTextFormatter"
                                                  :placeholder="$t('overlays.control_center.add_ticker_line')"
                                                  v-model="tickerAddText"/>

                                    <b-input-group-append>
                                        <b-btn variant="primary" @click="addTickerText">
                                            <font-awesome-icon icon="plus" class="mr-1"/>
                                            {{ $t('generic.add') }}
                                        </b-btn>
                                    </b-input-group-append>
                                </b-input-group>

                            </b-col>
                        </b-row>

                    </template>
                </CustomCard>

            </b-col>


        </b-row>

    </div>
</template>

<script>
import CustomCard from "~/components/CustomCard";
import {OverlayStateWebsocket} from "~/mixins/websocket/OverlayStateWeboscket";
import {OverlayDataWebsocket} from "~/mixins/websocket/OverlayDataWeboscket";

export default {
    name: "ControlCenter",

    data() {
        return {
            tickerEditIndex: -1,
            tickerEditText: "",
            tickerAddText: "",
        }
    },

    head() {
        return {
            title: this.$t("navigation.control_center") + " - Caster Dashboard"
        }
    },

    computed: {
        userID() {
            return this.$auth.user.id
        },
        tickerText() {
            if (this.tickerOverlayData == null || this.tickerOverlayData.text == null) return []
            return this.tickerOverlayData.text.split(",")
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
        tickerTextFormatter(value) {
            return value.split(",").join("")
        },
        addTickerText() {
            if (this.tickerAddText == null) return
            let data = this.tickerText
            data.push(this.tickerAddText)
            this.saveTickerText(data)
        },
        editTickerText() {
            let data = this.tickerText
            data[this.tickerEditIndex] = this.tickerEditText
            this.saveTickerText(data)
        },
        deleteTickerText(index) {
            let data = this.tickerText
            data[index] = null
            this.saveTickerText(data)
        },
        saveTickerText(data) {
            let dataString = data.filter(Boolean).join(",")
            this.tickerOverlayData.text = dataString
            this.$axios.$put(`/api/overlay/ticker_data/${this.$auth.user.id}/`, this.tickerOverlayData)
            this.tickerEditIndex = -1
            this.tickerEditText = ""
            this.tickerAddText = ""
        }
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$t("navigation.control_center"))
        this.$store.commit("setPageTitleIcon", "desktop")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Overlays", "Control Center"])
    },

    async fetch() {
        await Promise.all([
            this.connectOverlayStateWebsocket(),
            this.connectOverlayDataWebsocket()
        ])
    },

    mixins: [
        OverlayStateWebsocket,
        OverlayDataWebsocket,
    ],

    components: {
        "CustomCard": CustomCard
    }

}
</script>

<style scoped>

</style>
