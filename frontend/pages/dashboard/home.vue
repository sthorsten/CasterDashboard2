<template>
  <div>
    <ContentHeader
      icon="home"
      title="Home"
      :breadcrumb-items="['Dashboard', 'Home']"
    />
    <ContentContainer>
      <b-container fluid>
        <CustomCard title="Home Page">
          <fa-icon icon="heart" class="mr-1" />
          Welcome to the Rainbow Six Siege Caster Dashboard!
          <br />
          <i>
            The dashboard is currently under construction! Check out the project
            on
            <a
              href="https://github.com/sthorsten/CasterDashboard2"
              target="_blank"
            >
              Github
            </a>
            to learn more.
          </i>
        </CustomCard>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  layout: 'main-page',

  head() {
    return {
      title: "Home"
    }
  },

}
</script>