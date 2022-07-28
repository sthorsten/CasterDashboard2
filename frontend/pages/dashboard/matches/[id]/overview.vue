<script setup lang="ts">

const route = useRoute()
const matchId = route.params.id

</script>

<template>

  <NuxtLayout name="match">
    <MainPage title="Match Overview" icon="fa-solid fa-compass"
      :breadcrumbs="['Dashboard', 'Matches', `${matchId}`, 'Overview']">
      Test

    </MainPage>
  </NuxtLayout>

</template>