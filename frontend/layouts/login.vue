<script setup lang="ts">

useHead({
  bodyAttrs: {
    class: 'login-page'
  }
})

</script>

<template>

  <Head>
    <Script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous">
    </Script>
    <Script src="/js/adminlte.min.js"></Script>
    <Link rel="stylesheet" href="/css/adminlte.min.css">
    </Link>
  </Head>

  <div class="login-box">
    <slot />
  </div>


</template>