<script setup lang="ts">
import { mainSidebarItems } from '@/extra/mainSidebarItems';
import { useCoreDataStore } from '@/store/coreData';
import { useAuthStore } from '@/store/auth';
import { useMainDataStore } from '@/store/mainData';

const router = useRouter()

// Check login
const authStore = useAuthStore();
if (!authStore.loggedIn) {
  router.push('/login');
}

// Load data from store
const coreData = useCoreDataStore()
coreData.connect()

const mainData = useMainDataStore()
mainData.connect()

</script>

<template>

  <Head>

    <Script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous">
    </Script>
    <Script src="/js/adminlte.min.js"></Script>
    <Link rel="stylesheet" href="/css/adminlte.min.css">
    </Link>

  <Body class="layout-fixed sidebar-open"></Body>
  </Head>

  <div class="wrapper">

    <LayoutNavbar />
    <LayoutSidebar :items="mainSidebarItems" />
    <slot />
    <LayoutFooter />

  </div>

</template>