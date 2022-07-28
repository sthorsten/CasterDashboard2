import { defineNuxtPlugin } from "#app";

import { library, config } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

config.autoAddCss = false

import {
  faHouseChimney,
  faUser,
  faPlus,
  faLock,
  faRightFromBracket,
  faRightToBracket,
  faBars,
  faListOl,
  faArrowRightLong,
  faCompass,
  faAnglesLeft,
} from '@fortawesome/free-solid-svg-icons'

import {
  faGithub
} from '@fortawesome/free-brands-svg-icons'

library.add(
  faHouseChimney,
  faUser,
  faPlus,
  faLock,
  faRightFromBracket,
  faRightToBracket,
  faBars,
  faListOl,
  faArrowRightLong,
  faCompass,
  faAnglesLeft,

  faGithub
)

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('FaIcon', FontAwesomeIcon)
})