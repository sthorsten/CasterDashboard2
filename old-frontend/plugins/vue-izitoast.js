import Vue from "vue"
import VueIziToast from "vue-izitoast"

Vue.use(VueIziToast, {
  closeOnClick: true,
  drag: false,
  position: "topCenter",
  transitionIn: "revealIn",
  transitionOut: "fadeOut",
})
