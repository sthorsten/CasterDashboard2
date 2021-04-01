<template>
    <div>

        <!-- Global notifications -->
        <template v-if="!$fetchState.pending">
            <b-row v-for="n in notifications" :key="n.index">
                <b-col>
                    <b-alert show :variant="n.variant" :class="`bg-gradient-${n.variant}`">
                        <h5>
                            <font-awesome-icon icon="exclamation-triangle"></font-awesome-icon>
                            {{ n.title }}
                        </h5>
                        <div v-html="n.text">
                        </div>
                    </b-alert>
                </b-col>
            </b-row>
        </template>

        <!-- Greeting -->
        <b-row>
            <b-col>
                <b-alert variant="success" show="" class="text-center bg-gradient-success">
                    <span><b>{{ $t('home.welcome') }} </b>{{ this.$auth.user.userName }} &#128075;</span><br>
                    <span>{{ this.getRandomGreeting }}</span>
                </b-alert>
            </b-col>
        </b-row>

        <b-row>

            <!-- Current matchMaps -->
            <b-col cols="12" sm="6" lg="3">
            </b-col>

            <!-- Overlay status -->
            <b-col cols="12" sm="6" lg="3">

            </b-col>

            <!-- ??? -->
            <b-col cols="12" sm="6" lg="3">

            </b-col>

            <!-- ??? -->
            <b-col cols="12" sm="6" lg="3">

            </b-col>

        </b-row>

    </div>
</template>

<script>
import {Notifications} from "~/mixins/axios/Notifications";

export default {
    name: "HomePage",

    data() {
        return {
            randomGreetings: [
                this.$t('home.greeting.line1'),
                this.$t('home.greeting.line2'),
                this.$t('home.greeting.line3'),
                this.$t('home.greeting.line4'),
                this.$t('home.greeting.line5'),
            ],
        }
    },

    head() {
        return {
            title: this.$t("navigation.home") + " - Caster Dashboard"
        }
    },

    computed: {
        getRandomGreeting() {
            let rand = Math.floor(Math.random() * 5)
            return this.randomGreetings[rand]
        }
    },

    mounted() {
        this.$store.commit("setPageTitle", this.$t("navigation.home"))
        this.$store.commit("setPageTitleIcon", "home")
        this.$store.commit("setBreadcrumbPath", ["Dashboard", "Home"])
    },

    async fetch() {
        await this.getNotifications()
        this.notifications.forEach(n => {
            if (n.type === 1) n.variant = "info"
            else if (n.type === 2) n.variant = "success"
            else if (n.type === 3) n.variant = "warning"
            else if (n.type === 4) n.variant = "danger"

            // Remove expired notifications
            let now = new Date(Date.now())
            let valid_until = new Date(n.valid_until)
            if (n.valid_until != null && now > valid_until) this.notifications.splice(n.index, 1)
        })
    },

    mixins: [
        Notifications
    ]
}
</script>

<style scoped>

</style>
