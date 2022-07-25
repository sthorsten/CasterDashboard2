<script setup lang="ts">
import { CDropdown, CDropdownToggle, CDropdownMenu, CDropdownItem } from '@coreui/vue';


</script>

<template>
  <ul class="navbar-nav ml-auto">

    <li class="nav-item">
      <CDropdown>
        <CDropdownToggle color="dark">
          <FaIcon icon="fa-solid fa-user" class="navbar-menu-icon" />
          UserName
        </CDropdownToggle>
        <CDropdownMenu>
          <CDropdownItem href="#">Action</CDropdownItem>
          <CDropdownItem href="#">Another action</CDropdownItem>
          <CDropdownItem href="#">Something else here</CDropdownItem>
        </CDropdownMenu>
      </CDropdown>
    </li>
  </ul>
</template>