<template>
    <BaseLayout :title="$t('navigation.home')" title_icon="fas fa-home" :bc_path="bc_path">

        <vue-headful :title="$t('navigation.home') + ' - Caster Dashboard'"/>

        <!-- Greeting -->
        <b-row>
            <b-col>
                <b-alert variant="success" show="" class="text-center bg-gradient-success">
                    <span><b>{{ $t('home.welcome') }} </b>{{ this.$store.state.user.username }} &#128075;</span><br>
                    <span>{{ this.getRandomGreeting }}</span>
                </b-alert>
            </b-col>
        </b-row>

        <b-row>

            <!-- Current match -->
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

    </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/layout/BaseLayout.vue'

export default {
    name: "Home",
    data() {
        return {
            random_greetings: [
                this.$t('home.greeting.line1'),
                this.$t('home.greeting.line2'),
                this.$t('home.greeting.line3'),
                this.$t('home.greeting.line4'),
                this.$t('home.greeting.line5'),
            ],
            bc_path: ['Dashboard', 'Home']
        }
    },
    computed: {
        getRandomGreeting() {
            let rand = Math.floor(Math.random() * 5)
            console.log(rand)
            return this.random_greetings[rand]
        }
    },
    components: {
        BaseLayout
    },
}

</script>



