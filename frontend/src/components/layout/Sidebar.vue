<template>

    <!-- Sidebar Navigation -->
    <div class="sidebar pt-3 bg-gray-800 shadow-lg" style="height: 100%;">

        <b-nav vertical pills class="navbar-custom">

            <!-- Home -->
            <b-nav-item :to="{name: 'Home'}" class="nav-link">
                <i class="nav-icon fas fa-home"></i>
                {{ $t('navigation.home') }}
            </b-nav-item>

            <!-- Matches -->
            <b-nav-item class="text-uppercase nav-header" disabled>{{ $t('navigation.matches') }}</b-nav-item>

            <!-- History -->
            <b-nav-item :to="{name: 'Match History'}" class="nav-link">
                <i class="nav-icon fas fa-history"></i>
                {{ $t('navigation.history') }}
            </b-nav-item>

            <!-- Create -->
            <b-nav-item :to="{name: 'Create Match'}" class="nav-link">
                <i class="nav-icon fas fa-plus"></i>
                {{ $t('navigation.create') }}
            </b-nav-item>

            <!--
            <-- Match Overview ->
            <li class="nav-item" :to="{name: 'Match Overview'}" class="nav-link disabled">
                    <i class="nav-icon fas fa-gamepad"></i>
                    {{ $t('navigation.overview') }}
            </li>
            <-- Match Details ->
            <li class="nav-item">
                <router-link to="#" class="nav-link disabled">
                    <i class="nav-icon fas fa-eye"></i>
                    <span>{{ $t('navigation.details') }}</span>
                </router-link>
            </li>

            <-- Map Picks & Bans ->
            <li class="nav-item">
                <router-link to="#" class="nav-link disabled">
                    <i class="nav-icon fas fa-map"></i>
                    <span>{{ $t('navigation.maps') }}</span>
                </router-link>
            </li>

            <-- Rounds ->
            <li class="nav-item">
                <router-link to="#" class="nav-link disabled">
                    <i class="nav-icon fas fa-play-circle"></i>
                    <span>{{ $t('navigation.rounds') }}</span>
                </router-link>
            </li>
            -->

            <!-- Overlays -->
            <b-nav-item class="text-uppercase nav-header" disabled>{{ $t('navigation.overlays') }}</b-nav-item>

            <!-- Control Center -->
            <b-nav-item :to="{name: 'Control Center'}" class="nav-link">
                <i class="nav-icon fas fa-desktop"></i>
                {{ $t('navigation.control_center') }}
            </b-nav-item>

            <!-- Customize -->
            <b-nav-item :to="{name: 'Customize'}" class="nav-link">
                <i class="nav-icon fas fa-palette"></i>
                {{ $t('navigation.customize') }}
            </b-nav-item>

            <!-- Data -->
            <b-nav-item class="text-uppercase nav-header" disabled>{{ $t('navigation.data') }}</b-nav-item>

            <!-- Leagues -->
            <b-nav-item :to="{name: 'Leagues'}" class="nav-link">
                <i class="nav-icon fas fa-trophy"></i>
                {{ $tc('core.league', 2) }}
            </b-nav-item>

            <!-- Seasons -->
            <b-nav-item :to="{name: 'Seasons'}" class="nav-link">
                <i class="nav-icon fas fa-calendar-alt"></i>
                {{ $tc('core.season', 2) }}
            </b-nav-item>

            <!-- Sponsors -->
            <b-nav-item :to="{name: 'Sponsors'}" class="nav-link">
                <i class="nav-icon fas fa-money-bill-alt"></i>
                {{ $tc('core.sponsor', 2) }}
            </b-nav-item>

            <!-- Teams -->
            <b-nav-item :to="{name: 'Teams'}" class="nav-link">
                <i class="nav-icon fas fa-users"></i>
                {{ $tc('core.team', 2) }}
            </b-nav-item>

            <!-- Statistics -->
            <b-nav-item class="text-uppercase nav-header" disabled>{{ $t('navigation.statistics') }}</b-nav-item>

            <!-- Maps.vue -->
            <b-nav-item to="#" class="nav-link">
                <i class="nav-icon fas fa-map"></i>
                {{ $t('navigation.stats_maps') }}
            </b-nav-item>

            <!-- OpBans -->
            <b-nav-item to="#" class="nav-link">
                <i class="nav-icon fas fa-user-alt-slash"></i>
                {{ $t('navigation.opbans') }}
            </b-nav-item>

            <!-- Rounds -->
            <b-nav-item to="#" class="nav-link">
                <i class="nav-icon fas fa-list-ol"></i>
                {{ $t('navigation.stats_rounds') }}
            </b-nav-item>
        </b-nav>
        <!--
        </ul>
        </nav>
        -->
    </div>
    <!--</aside>-->

</template>

<script>
export default {
    name: "Sidebar",
}
</script>

<!--
<style scoped>
.sidebar-visible {
    display: none !important;
}

@media (min-width: 992px) {
    .sidebar-visible {
        display: block !important;
    }
}
</style>
-->