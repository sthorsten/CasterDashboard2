<template>
  <div>
    <ContentHeader
      icon="home"
      title="Home"
      :breadcrumb-items="['Dashboard', 'Home']"
    />
    <ContentContainer>
      <b-container fluid>
        <b-row>
          <b-col cols="8">
            <!-- Welcome -->
            <CustomCard title="Home Page">
              <fa-icon icon="heart" class="mr-1" />
              Welcome to the Rainbow Six Siege Caster Dashboard!
              <br />
              <i>
                The dashboard is currently under construction! Check out the
                project on
                <a
                  href="https://github.com/sthorsten/CasterDashboard2"
                  target="_blank"
                >
                  Github
                </a>
                to learn more.
              </i>
            </CustomCard>
          </b-col>

          <b-col cols="4">
            <CustomCard title="News" color="success">
              <ul>
                <li>
                  <b>2022-05-04</b> - Version 2.6.0-alpha released.
                  <br />
                  <p>
                    See
                    <a
                      href="https://github.com/sthorsten/CasterDashboard2/blob/develop/CHANGELOG.md"
                      target="blank"
                    >
                      Changelog
                    </a>
                    for more details.
                  </p>
                </li>
              </ul>
            </CustomCard>
          </b-col>
        </b-row>
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