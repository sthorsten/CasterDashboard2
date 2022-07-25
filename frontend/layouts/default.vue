<script setup lang="ts">
import Navbar from '~~/components/layout/Navbar.vue';
import Sidebar from '../components/layout/Sidebar.vue';
import Footer from '~~/components/layout/Footer.vue';
import { mainSidebarItems } from '~~/extra/mainSidebarItems';
import { useCoreDataStore } from '~~/store/coreData';

useHead({
  bodyAttrs: {
    class: 'sidebar-mini layout-fixed layout-navbar-fixed dark-mode'
  }
})

// Load core data from store
const coreData = useCoreDataStore()
coreData.connect()

</script>

<template>
  <div class="wrapper">
    <Navbar />
    <Sidebar :items="mainSidebarItems" />
    <slot />
    <Footer />

  </div>

</template>