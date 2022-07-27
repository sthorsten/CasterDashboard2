<script setup lang="ts">
import { CDropdown, CDropdownToggle, CDropdownMenu, CDropdownItem } from '@coreui/vue';
import { useAuthStore } from '~~/store/auth';

const authStore = useAuthStore();

</script>

<template>
  <ul class="navbar-nav ml-auto">

    <li class="nav-item">
      <CDropdown>
        <CDropdownToggle color="dark">
          <FaIcon icon="fa-solid fa-user" class="navbar-menu-icon" />
          {{ authStore.user.username ?? 'Not logged in' }}
        </CDropdownToggle>
        <CDropdownMenu>
          <CDropdownItem>
            <nuxt-link to="/logout" class="text-white">
              <FaIcon icon="fa-solid fa-right-from-bracket" class="navbar-menu-icon" />
              Logout
            </nuxt-link>
          </CDropdownItem>
        </CDropdownMenu>
      </CDropdown>
    </li>
  </ul>
</template>