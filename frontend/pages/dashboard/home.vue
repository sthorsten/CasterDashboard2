<script setup lang="ts">
import { useAuthStore } from '@/store/auth';
import MainPage from '~~/components/MainPage.vue';

const authStore = useAuthStore();

onMounted(async () => {


});


</script>

<template>

  <MainPage title="Home" icon="fa-solid fa-house-chimney">



  </MainPage>


</template>