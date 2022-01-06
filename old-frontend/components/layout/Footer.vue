<template>
  <footer class="main-footer bg-dark">
    <div class="float-right d-none d-sm-block">
      <a href="#">{{ $t("terms") }}</a>
      - <a href="#">{{ $t("privacy") }}</a> - powered by
      <a href="#">Open Source</a> - Version <b>{{ $store.state.version }}</b>
    </div>
    Copyright &copy; 2020 Thorsten "ThorsHero" Schmitt -
    <a href="https://www.thorshero.de" target="_blank">www.thorshero.de</a>
  </footer>
</template>

<script>
  export default {
    name: "Footer",

    mounted() {
      // Get version if not present
      if (this.$store.state.version === "?") {
        this.$axios.$get("/api/version/").then((data) => {
          this.$store.commit("setVersion", data.version)
        })
      }
    },
  }
</script>

<i18n>
{
    "en": {
        "terms": "Terms & Conditions",
        "privacy": "Privacy"
    },
    "de": {
        "terms": "Nutzungsbedingungen",
        "privacy": "Datenschutz"
    }
}
</i18n>
