<template>
  <!-- Sidebar Navigation -->
  <div class="sidebar pt-3 bg-gray-800 shadow-lg" style="height: 100%">
    <b-nav vertical pills class="navbar-custom">
      <!-- Home -->
      <b-nav-item
        to="/dashboard/home"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-home"></i>
        {{ $t("navigation.home") }}
      </b-nav-item>

      <!-- Matches -->
      <b-nav-item class="text-uppercase nav-header" disabled>{{
        $t("navigation.matches")
      }}</b-nav-item>

      <!-- History -->
      <b-nav-item
        to="/dashboard/matches/history"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-history"></i>
        {{ $t("navigation.history") }}
      </b-nav-item>

      <!-- Create -->
      <b-nav-item
        to="/dashboard/matches/create"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-plus"></i>
        {{ $t("navigation.create") }}
      </b-nav-item>

      <!-- Create MatchGroup -->
      <b-nav-item
        to="/dashboard/matches/create_group"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-layer-group"></i>
        {{ $t("navigation.manage_match_groups") }}
      </b-nav-item>

      <!-- Overlays -->
      <b-nav-item class="text-uppercase nav-header" disabled>{{
        $t("navigation.overlays")
      }}</b-nav-item>

      <!-- Control Center -->
      <b-nav-item
        to="/dashboard/overlays/control-center"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-desktop"></i>
        {{ $t("navigation.control_center") }}
      </b-nav-item>

      <!-- Customize -->
      <b-nav-item
        to="/dashboard/overlays/customize"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-palette"></i>
        {{ $t("navigation.customize") }}
      </b-nav-item>

      <!-- Data -->
      <b-nav-item class="text-uppercase nav-header" disabled>{{
        $t("navigation.data")
      }}</b-nav-item>

      <!-- Leagues -->
      <b-nav-item
        to="/dashboard/data/leagues"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-trophy"></i>
        {{ $tc("core.league", 2) }}
      </b-nav-item>

      <!-- Seasons -->
      <b-nav-item
        to="/dashboard/data/seasons"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-calendar-alt"></i>
        {{ $tc("core.season", 2) }}
      </b-nav-item>

      <!-- Sponsors -->
      <b-nav-item
        to="/dashboard/data/sponsors"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-money-bill-alt"></i>
        {{ $tc("core.sponsor", 2) }}
      </b-nav-item>

      <!-- Teams -->
      <b-nav-item
        to="/dashboard/data/teams"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-users"></i>
        {{ $tc("core.team", 2) }}
      </b-nav-item>

      <!-- Statistics -->
      <b-nav-item class="text-uppercase nav-header" disabled>{{
        $t("navigation.statistics")
      }}</b-nav-item>

      <!-- Maps.vue -->
      <b-nav-item
        to="/dashboard/statistics/maps"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-map"></i>
        {{ $t("navigation.stats_maps") }}
      </b-nav-item>

      <!-- OpBans -->
      <b-nav-item
        to="/dashboard/statistics/opbans"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-user-alt-slash"></i>
        {{ $t("navigation.stats_op_bans") }}
      </b-nav-item>

      <!-- Rounds -->
      <b-nav-item
        to="/dashboard/statistics/rounds"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-list-ol"></i>
        {{ $t("navigation.stats_rounds") }}
      </b-nav-item>
    </b-nav>
  </div>
</template>

<script>
  export default {
    name: "Sidebar",
  }
</script>
