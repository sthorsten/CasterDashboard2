<script setup lang="ts">
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore();

</script>

<template>
  <ul class="navbar-nav ms-auto">

    <li class="nav-item dropdown">
      <a class="nav-link" data-bs-toggle="dropdown" href="#" aria-expanded="false">
        <FaIcon icon="fa-solid fa-user" class="navbar-menu-icon" />
        {{ authStore.user?.username ?? 'Not logged in' }}
      </a>

      <div class="dropdown-menu dropdown-menu-lg dropdown-menu-end">
        <nuxt-link to="/logout" class="dropdown-item">
          <FaIcon icon="fa-solid fa-right-from-bracket" class="navbar-menu-icon" />
          Logout
        </nuxt-link>
      </div>
    </li>
  </ul>
</template>