<template>
    <BaseLayout :title="$t('navigation.match_details')" title_icon="fa fas fa-gamepad" :bc_path="bcPath">

        <template v-if="loading === LoadingStatus.LOADED">
            <AlertBox variant="warning" :title="$t('generic.warning')" :text="$t('websocket.connection_lost')"
                      icon="fa mr-1 fas fa-exclamation-triangle" :show="matchWebsocketStatus === WebsocketStatus.RECONNECTING" loading/>

            <AlertBox variant="danger" :title="$t('generic.error')" :text="$t('websocket.error') + ' ' + $t('generic.contact_admin')"
                      icon="fa mr-1 fas fa-times-circle" :show="matchWebsocketStatus === WebsocketStatus.ERROR"/>

            <b-row>
                <b-col>

                    <CustomCard :title="$t('navigation.maps')" color="primary" outline divider>
                        <template #card-body>

                        </template>
                    </CustomCard>

                </b-col>
            </b-row>

            <b-row>

                <b-col>

                </b-col>

            </b-row>
        </template>

        <LoadingOverlay :status="loading"/>

    </BaseLayout>
</template>

<script>
import BaseLayout from "@/components/layout/BaseLayout";
import CustomCard from "@/components/elements/CustomCard";
import {MatchWebsocket} from "@/mixins/websocket/MatchWebsocket";
import {CurrentMap} from "@/mixins/axios/CurrentMap";
//import {MatchMapWebsocket} from "@/mixins/websocket/MatchMapWebsocket";
import AlertBox from "@/components/elements/AlertBox";
import {WebsocketStatus} from "@/helpers/const/WebsocketStatus";
import LoadingOverlay from "@/components/elements/LoadingOverlay";
import {LoadingStatus} from "@/helpers/const/LoadingStatus";

export default {
    name: "MatchDetails",
    mixins: [MatchWebsocket, CurrentMap],
    data() {
        return {
            LoadingStatus: LoadingStatus,
            WebsocketStatus: WebsocketStatus,
            matchMapID: null,
            loading: LoadingStatus.LOADED,
            bcPath: ["Dashboard", "Matches", this.$route.params.id, "Details"]
        }
    },
    computed: {
        matchID() {
            return this.$route.params.id
        },
    },
    watch: {
        currentMap: function (newState) {
            if (newState) {
                this.matchMapID = this.currentMap.id
                this.connectMatchMapWebsocket()
            }
        }
    },
    methods: {},
    created() {
        this.connectMatchWebsocket()
    },
    components: {
        LoadingOverlay,
        AlertBox,
        CustomCard,
        BaseLayout,
    }
}
</script>

<style scoped>

</style>