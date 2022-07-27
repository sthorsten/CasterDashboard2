<script setup lang="ts">
import Navbar from '~~/components/layout/Navbar.vue';
import Sidebar from '../components/layout/Sidebar.vue';
import Footer from '~~/components/layout/Footer.vue';
import { mainSidebarItems } from '~~/extra/mainSidebarItems';
import { useCoreDataStore } from '~~/store/coreData';
import { useAuthStore } from '~~/store/auth';
import { useMainStore } from '~~/store/main';

const mainStore = useMainStore()
const router = useRouter()

// Check login
const authStore = useAuthStore();
if (!authStore.loggedIn) {
  router.push('/login');
}

// Load core data from store
const coreData = useCoreDataStore()
coreData.connect()

</script>

<template>

  <Head>

  <Body class="sidebar-mini layout-fixed layout-navbar-fixed dark-mode"
    :class="mainStore.sidebarCollapse ? 'sidebar-collapse' : ''">

  </Body>
  </Head>

  <div class="wrapper">

    <Navbar />
    <Sidebar :items="mainSidebarItems" />
    <slot />
    <Footer />

  </div>

</template>