<template>
  <div>
    <CustomCard color="primary" outline divider title="Coming Soon">
      <template #card-body>
        <span class="font-italic"> This page hasn't been implemented yet </span>

        <!-- Neutral Face Emoji -->
        &#128528;<br />
      </template>
    </CustomCard>
  </div>
</template>

<script>
  import CustomCard from "~/components/CustomCard"

  export default {
    name: "",

    data() {
      return {}
    },

    head() {
      return {
        title: this.$t("navigation.") + " - Caster Dashboard",
      }
    },

    computed: {},

    mounted() {
      this.$store.commit("setPageTitle", this.$t("navigation."))
      this.$store.commit("setPageTitleIcon", "")
      this.$store.commit("setBreadcrumbPath", ["Dashboard", ""])
    },

    async fetch() {},

    mixins: [],

    components: {
      CustomCard: CustomCard,
    },
  }
</script>

<style scoped></style>
