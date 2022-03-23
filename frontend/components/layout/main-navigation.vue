<template>
  <nav class="main-header navbar navbar-expand navbar-dark">
    <!-- Navbar left -->
    <ul class="navbar-nav">
      <!-- Sidebar toggle -->
      <li class="nav-item">
        <a class="nav-link" data-widget="pushmenu" href="#" role="button">
          <fa-icon icon="bars" />
        </a>
      </li>

      <NavItem inline text="Home" link="/" icon="home" />
      <NavItem inline text="GitHub" link="https://github.com/sthorsten/CasterDashboard2" :icon="['fab', 'github']" target="_blank" />
      <NavItem inline text="Changelog" link="https://github.com/sthorsten/CasterDashboard2/blob/develop/CHANGELOG.md" icon="clipboard-list" target="_blank" />
      <NavItem inline text="Issues" link="https://github.com/sthorsten/CasterDashboard2/issues" icon="bug" target="_blank" />
    </ul>

    <!-- Navbar right-->
    <ul class="navbar-nav ml-auto">
      <NavItem v-if="$store.state.auth.loggedIn" inline :text="$store.state.auth.user.username" link="/logout" icon="user-circle" />
      <NavItem v-else inline text="UserName" link="#" icon="user-circle" />
    </ul>
  </nav>
</template>
