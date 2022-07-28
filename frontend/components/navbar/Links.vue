<template>
  <ul class="navbar-nav">
    <li class="nav-item">
      <a class="nav-link" data-lte-toggle="sidebar-full" href="#" role="button">
        <FaIcon icon="fa-solid fa-bars" class="navbar-menu-icon" />
      </a>
    </li>
    <li class="nav-item d-none d-md-block">
      <nuxt-link to="/" class="nav-link">
        <FaIcon icon="fa-solid fa-house-chimney" class="navbar-menu-icon" />
        Home
      </nuxt-link>
    </li>
    <li class="nav-item d-none d-md-block">
      <nuxt-link to="https://github.com/sthorsten/CasterDashboard2" target="_blank" class="nav-link">
        <FaIcon icon="fa-brands fa-github" class="navbar-menu-icon" />
        GitHub
      </nuxt-link>
    </li>
  </ul>
</template>