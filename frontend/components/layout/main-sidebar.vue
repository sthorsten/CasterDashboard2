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
            v-for="item in navItems"
            :key="item.link"
            :text="item.text"
            :link="item.link"
            :icon="item.icon"
            :active="true"
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
      navItems: [
        {
          text: 'Home',
          link: '/',
          icon: 'home'
        }
      ]
    }
  }
}
</script>
