<template>
  <div class="login-box">
    <adminlte-header />
    <div class="login-logo">
      <a href="/"><b>Caster Dashboard</b></a>
    </div>

    <div class="card">
      <div class="card-body login-card-body">
        <Nuxt />
      </div>
    </div>
  </div>
</template>

<script>

export default {
  head() {
    return {
      bodyAttrs: {
        class: 'hold-transition dark-mode login-page'
      }
    }
  }
}
</script>
