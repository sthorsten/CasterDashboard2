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

      <NavItem text="Home" link="/" icon="home" />
      <NavItem text="GitHub" link="https://github.com/sthorsten/CasterDashboard2" :icon="['fab', 'github']" target="_blank" />
    </ul>

    <!-- Navbar right-->
    <ul class="navbar-nav ml-auto">
      <NavItem v-if="$auth.loggedIn" :text="$auth.user.username" link="#" icon="user-circle" />
      <NavItem v-else text="UserName" link="#" icon="user-circle" />
    </ul>
  </nav>
</template>
