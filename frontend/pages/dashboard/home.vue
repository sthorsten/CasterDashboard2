<script setup lang="ts">
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore();

</script>

<template>

  <NuxtLayout name="main">
    <MainPage title="Home" icon="fa-solid fa-house-chimney" :breadcrumbs="['Dashboard', 'Home']">

      <CustomCard title="Welcome" color="warning">
        Welcome to the R6 Caster Dashboard!
        <br><br>
        <b>⚠ Work in progress.</b>
      </CustomCard>

    </MainPage>
  </NuxtLayout>


</template>