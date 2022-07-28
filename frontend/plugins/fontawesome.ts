import { defineNuxtPlugin } from "#app";

import { library, config } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

config.autoAddCss = false

import {
  faHouseChimney,
  faUser,
  faClockRotateLeft,
  faPlus,
  faLock,
  faRightFromBracket,
  faRightToBracket,
  faBars,
} from '@fortawesome/free-solid-svg-icons'

import {
  faGithub
} from '@fortawesome/free-brands-svg-icons'

library.add(
  faHouseChimney,
  faUser,
  faClockRotateLeft,
  faPlus,
  faLock,
  faRightFromBracket,
  faRightToBracket,
  faBars,

  faGithub
)

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('FaIcon', FontAwesomeIcon)
})