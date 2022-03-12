import Vue from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Icons
import {
  faHome,
  faBars,
  faUserCircle,
  faChevronCircleRight,
  faHistory,
  faPlus,
  faDesktop,
  faPalette,
  faTrophy,
  faAward,
  faCalendarAlt,
  faCalendarDay,
  faUsers,
  faMoneyBillAlt,
  faUser,
  faLock,
  faPencilAlt,
  faInfoCircle,
  faListUl,
  faMap,
  faUsersSlash,
  faPlayCircle,
  faClipboardList,
  faBug,
  faHeading,
  faListOl,
  faSave,
  faBan,
  faHandPointUp,
  faArrowRight,
  faArrowRightToBracket,
  faTrashCan,
faCheckCircle
} from '@fortawesome/free-solid-svg-icons'

import { faGithub } from '@fortawesome/free-brands-svg-icons'

library.add(faHome)
library.add(faBars)
library.add(faUserCircle)
library.add(faChevronCircleRight)
library.add(faHistory)
library.add(faPlus)
library.add(faDesktop)
library.add(faPalette)
library.add(faTrophy)
library.add(faAward)
library.add(faCalendarAlt)
library.add(faCalendarDay)
library.add(faUsers)
library.add(faMoneyBillAlt)
library.add(faUser)
library.add(faLock)
library.add(faPencilAlt)
library.add(faInfoCircle)
library.add(faListUl)
library.add(faMap)
library.add(faUsersSlash)
library.add(faPlayCircle)
library.add(faClipboardList)
library.add(faBug)
library.add(faHeading)
library.add(faListOl)
library.add(faSave)
library.add(faBan)
library.add(faHandPointUp)
library.add(faArrowRight)
library.add(faArrowRightToBracket)
library.add(faTrashCan)
library.add(faCheckCircle)

library.add(faGithub)

/* add font awesome icon component */
Vue.component('FaIcon', FontAwesomeIcon)

Vue.config.productionTip = false
