// Vue Imports
import Vue from 'vue'

import BootstrapVue from 'bootstrap-vue'
import VueSweetalert2 from "vue-sweetalert2";
import VueIziToast from "vue-izitoast";
import Multiselect from 'vue-multiselect'
import VueApexCharts from "vue-apexcharts";
import VueCookies from 'vue-cookies'
import vueHeadful from 'vue-headful';
import Clipboard from 'v-clipboard';
import axios from 'axios'
import VueAxios from 'vue-axios'
import Vuex from 'vuex'
import VuexPersistence from "vuex-persist";
import {
    ValidationObserver,
    ValidationProvider,
    extend,
    localize
} from "vee-validate";
import en from "vee-validate/dist/locale/en.json";
import * as rules from "vee-validate/dist/rules";

// Other JS imports
import '@fortawesome/fontawesome-free/js/all.js'

// Local imports
import App from './App.vue'
import router from './router'
import i18n from './i18n'

// Install VeeValidate rules and localization
Object.keys(rules).forEach(rule => {
    extend(rule, rules[rule]);
});
localize("en", en);
// Install VeeValidate components globally
Vue.component("ValidationObserver", ValidationObserver);
Vue.component("ValidationProvider", ValidationProvider);

// JS Options
const iziToastOptions = {
    closeOnClick: true,
    drag: false,
    position: "topCenter",
    transitionIn: 'revealIn',
    transitionOut: 'fadeOut'
}

// Vue module registration
Vue.use(BootstrapVue)
Vue.use(VueSweetalert2)
Vue.use(VueIziToast, iziToastOptions);
Vue.use(VueApexCharts)
Vue.use(VueCookies)
Vue.use(Clipboard)
Vue.use(VueAxios, axios)
Vue.use(Vuex)
Vue.config.productionTip = false

Vue.component('vue-headful', vueHeadful)
Vue.component('multiselect', Multiselect)
Vue.component('apexchart', VueApexCharts)

// Combined style
import "@/assets/scss/index.scss"

// Vuex
const vuexStorage = new VuexPersistence({
    key: 'vuex',
    storage: window.localStorage
})

const store = new Vuex.Store({
    state: {
        version: "Version 0.0.0",
        frontendURL: "http://localhost:8080",
        backendURL: "http://localhost:8000",
        userToken: "",
        user: null,
        loggedIn: false
    },
    getters: {
        websocketURL: state => {
            if (state.backendURL.startsWith("http://")){
                return "ws://" + state.backendURL.substr(7)
            }
            return "wss://" + state.backendURL
        },
        authHeader: state => {
            return {
                headers: {"Authorization": "Token " + state.userToken}
            }
        }
    },
    mutations: {
        setUserToken(state, userToken) {
            state.userToken = userToken
        },
        setUser(state, user) {
            state.user = user
        },
        setLoggedIn(state, logInStatus) {
            state.loggedIn = logInStatus
        },
        setVersion(state, version){
            state.version = version
        }
    },
    plugins: [vuexStorage.plugin]
})

new Vue({
    router,
    i18n,
    store,
    render: h => h(App)
}).$mount('#app')


