<template>
  <div>
    <ContentHeader icon="home" title="Home" :breadcrumb-items="['Dashboard', 'Home']" />
    <ContentContainer>
      Content...
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  layout: 'main-page',
  data () {
    return {
      test: 'hi'
    }
  }
}
</script>
