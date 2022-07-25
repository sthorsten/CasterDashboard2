<script setup lang="ts">
import { SidebarItem } from '~~/types/SidebarItem';

const props = defineProps<{
  items: SidebarItem[]
}>()

</script>

<template>

  <aside class="main-sidebar sidebar-dark-primary elevation-4">

    <a href="/" class="brand-link d-flex justify-content-center">
      <span class="brand-text">R6 Caster Dashboard</span>
    </a>

    <div class="sidebar">

      <nav class="mt-2">
        <ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu" data-accordion="false">

          <li v-for="item in props.items" :class="item.isHeader ? 'nav-header' : 'nav-item'">
            <span v-if="item.isHeader" class="text-uppercase">
              {{ item.name }}
            </span>

            <nuxt-link v-else class="nav-link" active-class="active" :to="item.url">
              <FaIcon :icon="item.icon" class="nav-icon navbar-menu-icon" />
              <p>{{ item.name }}</p>
            </nuxt-link>
          </li>

        </ul>
      </nav>

    </div>

  </aside>
</template>