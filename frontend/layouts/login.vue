<script setup lang="ts">

useHead({
  bodyAttrs: {
    class: 'hold-transition login-page dark-mode'
  }
})

</script>

<template>

  <div class="login-box">

    <div class="card card-outline card-primary">
      <slot />
    </div>

  </div>


</template>