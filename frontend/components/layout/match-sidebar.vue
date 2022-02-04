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

          <li class="nav-header text-uppercase">
            Map Specific
          </li>
          <NavItem
            v-for="item in mapNavItems"
            :key="item.link"
            :text="item.text"
            :link="item.link"
            :icon="item.icon"
            :nuxt-link="true"
          />
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
      ],
      mapNavItems: [

        {
          text: 'Map Overview?',
          link: '/dashboard/matches/234',
          icon: 'map'
        },
        {
          text: 'Operator Bans',
          link: '/dashboard/matches/456',
          icon: 'users-slash'
        },
        {
          text: 'Rounds',
          link: '/dashboard/matches/789',
          icon: 'play-circle'
        }
      ]
    }
  }
}
</script>
