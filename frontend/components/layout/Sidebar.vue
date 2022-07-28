<script setup lang="ts">
import { SidebarItem } from '@/types/SidebarItem';

const props = defineProps<{
  items: SidebarItem[]
}>()

</script>

<template>

  <aside class="main-sidebar sidebar-bg-dark sidebar-color-primary shadow">

    <div class="brand-container">
      <a href="/" class="brand-link d-flex justify-content-center">
        <span class="brand-text">R6 Caster Dashboard</span>
      </a>
      <a class="pushmenu mx-1" data-lte-toggle="sidebar-mini" href="#" role="button">
        <FaIcon icon="fa-solid fa-angles-left" />
      </a>
    </div>

    <div class="sidebar">

      <nav class="mt-2">
        <ul class="nav nav-pills nav-sidebar flex-column">

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