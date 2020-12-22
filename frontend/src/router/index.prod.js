import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '@/views/Home'
import Login from "@/views/Login"
import Teams from "@/views/data/Teams";
import MatchCreate from "@/views/match/MatchCreate";
import ControlCenter from "@/views/overlays/ControlCenter";
import Customize from "@/views/overlays/Customize";
import MatchHistory from "@/views/match/MatchHistory";
import Leagues from "@/views/data/Leagues";
import Seasons from "@/views/data/Seasons";
import Sponsors from "@/views/data/Sponsors";
import MatchOverview from "@/views/match/MatchOverview";
import Maps from "@/views/match/Maps";
import OperatorBans from "@/views/match/OperatorBans";
import Rounds from "@/views/match/Rounds";
import OverlayControlCenter from "@/views/popouts/OverlayControlCenter";
import StartOverlay from "@/views/overlays/StartOverlay";
import InGameOverlay from "@/views/overlays/InGameOverlay";
import MapsOverlay from "@/views/overlays/MapsOverlay";
import MatchDetails from "@/views/match/MatchDetails";
import Profile from "@/views/Profile";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: {name: "Home"},
        beforeEnter: (to, from, next) => {
            const {uri} = to.query;
            if (uri != null && uri != '/') {
                next(false);
                router.push(uri);
            } else {
                next();
            }
        }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/dashboard/home',
        name: 'Home',
        component: Home
    },
    {
        path: '/dashboard/profile/:username',
        name: "Profile",
        component: Profile
    },

    // Matches
    {
        path: '/dashboard/matches/history',
        name: "Match History",
        component: MatchHistory
    },
    {
        path: '/dashboard/matches/create',
        name: "Create Match",
        component: MatchCreate
    },
    {
        path: '/dashboard/matches/:id/overview',
        name: "Match Overview",
        component: MatchOverview
    },
    {
        path: '/dashboard/matches/:id/details',
        name: "Match Details",
        component: MatchDetails
    },
    {
        path: '/dashboard/matches/:id/maps',
        name: "Map Picks & Bans",
        component: Maps
    },
    {
        path: '/dashboard/matches/:match_id/map/:map_id/opbans',
        name: "Operator Bans",
        component: OperatorBans
    },
    {
        path: '/dashboard/matches/:match_id/map/:map_id/rounds',
        name: "Rounds",
        component: Rounds
    },

    // Overlays
    {
        path: '/dashboard/overlays/control-center',
        name: "Control Center",
        component: ControlCenter
    },
    {
        path: '/dashboard/overlays/customize',
        name: "Customize",
        component: Customize
    },
    {
        path: '/overlays/:username/start',
        name: "Start Overlay",
        component: StartOverlay
    },
    {
        path: '/overlays/:username/maps',
        name: "Maps Overlay",
        component: MapsOverlay
    },
    {
        path: '/overlays/:username/ingame',
        name: "InGame Overlay",
        component: InGameOverlay
    },

    // Data
    {
        path: '/dashboard/data/leagues',
        name: "Leagues",
        component: Leagues
    },
    {
        path: '/dashboard/data/seasons',
        name: "Seasons",
        component: Seasons
    },
    {
        path: '/dashboard/data/sponsors',
        name: "Sponsors",
        component: Sponsors
    },
    {
        path: '/dashboard/data/teams',
        name: 'Teams',
        component: Teams
    },

    // Popouts
    {
        path: '/popout/overlay-control-center',
        name: 'Overlay Control Center Popout',
        component: OverlayControlCenter
    }
]

const router = new VueRouter({
    linkActiveClass: 'active',
    linkExactActiveClass: 'active',
    mode: 'history',
    routes: routes
})

export default router