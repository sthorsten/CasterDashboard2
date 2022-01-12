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
            Overlays
          </li>
          <NavItem
            v-for="item in overlaysNavItems"
            :key="item.link"
            :text="item.text"
            :link="item.link"
            :icon="item.icon"
            :nuxt-link="true"
          />

          <li class="nav-header text-uppercase">
            Main Data
          </li>
          <NavItem
            v-for="item in mainDataNavItems"
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
      overlaysNavItems: [
        {
          text: 'Control Center',
          link: '/dashboard/overlays/control-center',
          icon: 'desktop'
        },
        {
          text: 'Customize',
          link: '/dashboard/overlays/customize',
          icon: 'palette'
        }
      ],
      mainDataNavItems: [
        {
          text: 'Leagues',
          link: '/dashboard/main/leagues',
          icon: 'trophy'
        },
        {
          text: 'Seasons',
          link: '/dashboard/main/seasons',
          icon: 'calendar-alt'
        },
        {
          text: 'Playdays',
          link: '/dashboard/main/playdays',
          icon: 'calendar-day'
        },
        {
          text: 'Tournaments',
          link: '/dashboard/main/tournaments',
          icon: 'award'
        },
        {
          text: 'Teams',
          link: '/dashboard/main/teams',
          icon: 'users'
        },
        {
          text: 'Sponsors',
          link: '/dashboard/main/sponsors',
          icon: 'money-bill-alt'
        }
      ]
    }
  }
}
</script>
