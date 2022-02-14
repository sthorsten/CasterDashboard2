<template>
  <aside class="main-sidebar sidebar-dark-primary elevation-4">
    <a class="brand-link" href="/">
      <img class="brand-image" src="/static/img/ThorsHero_200.webp" style="padding-top: 6px;">
      <span class="brand-text">
        Caster Dashboard
      </span>
    </a>
    <div class="sidebar">
      <nav class="mt-2">
        <ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu" data-accordion="false">
          <li class="nav-header text-uppercase">
            Home
          </li>
          <NavItem
            :key="homeNavItem.link"
            :text="homeNavItem.text"
            :link="homeNavItem.link"
            :icon="homeNavItem.icon"
            :nuxt-link="true"
          />

          <li class="nav-header text-uppercase">
            Matches
          </li>
          <NavItem
            v-for="item in matchesNavItems"
            :key="item.link"
            :text="item.text"
            :link="item.link"
            :icon="item.icon"
            :nuxt-link="true"
          />

          <li class="nav-header text-uppercase">
            Current Match
          </li>
          <NavItem
            v-for="item in currentMatchNavItems"
            :key="item.link"
            :text="item.text"
            :link="item.link"
            :icon="item.icon"
            :nuxt-link="true"
          />

          <template v-if="$route.params.matchID && $route.params.mapName">
            <li class="nav-header text-uppercase">
              {{ $route.params.mapName }}
            </li>
            <NavItem
              v-for="item in mapNavItems"
              :key="item.link"
              :text="item.text"
              :link="item.link"
              :icon="item.icon"
              :nuxt-link="true"
            />
          </template>
        </ul>
      </nav>
    </div>
  </aside>
</template>

<script>
export default {
  data () {
    return {
      homeNavItem: {
        text: 'Home',
        link: '/dashboard/home',
        icon: 'home'
      },
      matchesNavItems: [
        {
          text: 'Match List',
          link: '/dashboard/matches/list',
          icon: 'history'
        },
        {
          text: 'Create a new match',
          link: '/dashboard/matches/new',
          icon: 'plus'
        }
      ],
      currentMatchNavItems: [
        {
          text: 'Match Overview',
          link: `/dashboard/matches/${this.$route.params.matchID}/overview`,
          icon: 'list-ul'
        },
        {
          text: 'Match Details',
          link: `/dashboard/matches/${this.$route.params.matchID}/details`,
          icon: 'info-circle'
        },
        {
          text: 'Map Pick & Ban',
          link: `/dashboard/matches/${this.$route.params.matchID}/mapban`,
          icon: 'map'
        }
      ]
    }
  },

  computed: {
    mapNavItems () {
      return [
        {
          text: 'Map Overview',
          link: `/dashboard/matches/${this.$route.params.matchID}/map/${this.$route.params.mapName}/overview`,
          icon: 'map'
        },
        {
          text: 'Operator Bans',
          link: `/dashboard/matches/${this.$route.params.matchID}/map/${this.$route.params.mapName}/opbans`,
          icon: 'users-slash'
        },
        {
          text: 'Rounds',
          link: `/dashboard/matches/${this.$route.params.matchID}/map/${this.$route.params.mapName}/rounds`,
          icon: 'play-circle'
        }
      ]
    }
  }
}
</script>
