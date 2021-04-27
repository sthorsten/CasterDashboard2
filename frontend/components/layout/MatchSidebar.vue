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

      <!-- Current Match -->
      <b-nav-item class="text-uppercase nav-header" disabled>{{
        $t("navigation.current_match")
      }}</b-nav-item>

      <!-- Overview -->
      <b-nav-item
        :to="`/dashboard/matches/${$route.params.matchID}/overview`"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-gamepad"></i>
        {{ $t("navigation.overview") }}
      </b-nav-item>

      <!-- Details -->
      <b-nav-item
        :to="`/dashboard/matches/${$route.params.matchID}/details`"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-list-ul"></i>
        {{ $t("navigation.details") }}
      </b-nav-item>

      <!-- Map Picks & Bans -->
      <b-nav-item
        :to="`/dashboard/matches/${$route.params.matchID}/maps`"
        exact
        class="nav-link"
        active-class="active"
      >
        <i class="nav-icon fas fa-map"></i>
        {{ $t("navigation.maps") }}
      </b-nav-item>

      <!-- Current Map -->
      <b-nav-item class="text-uppercase nav-header" disabled>{{
        $t("navigation.current_map")
      }}</b-nav-item>

      <!-- Operator Bans -->
      <b-nav-item
        :to="`/dashboard/matches/${$route.params.matchID}/map/${$route.params.mapID}/opbans`"
        exact
        class="nav-link"
        active-class="active"
        :disabled="$route.params.mapID == null"
      >
        <i class="nav-icon fas fa-users-slash"></i>
        {{ $t("navigation.op_bans") }}
      </b-nav-item>

      <!-- Rounds -->
      <b-nav-item
        :to="`/dashboard/matches/${$route.params.matchID}/map/${$route.params.mapID}/rounds`"
        exact
        class="nav-link"
        active-class="active"
        :disabled="$route.params.mapID == null"
      >
        <i class="nav-icon fas fa-list-ol"></i>
        {{ $t("navigation.rounds") }}
      </b-nav-item>
    </b-nav>
  </div>
</template>

<script>
  export default {
    name: "MatchSidebar",
  }
</script>
