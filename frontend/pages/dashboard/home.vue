<script setup lang="ts">
import { useCoreDataStore } from '~~/store/coreData';
import MainPage from '~~/components/MainPage.vue';

const coreData = useCoreDataStore()


</script>

<template>

  <MainPage title="Home" icon="fa-solid fa-house-chimney">

    Map Data:
    <br><br>

  </MainPage>


</template>