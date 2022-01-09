<template>
  <div>
    <ContentHeader icon="home" title="Home" :breadcrumb-items="['Dashboard', 'Home']" />
    <ContentContainer>
      Content...
      <br>
      Map 4: {{ $store.getters['coreSocket/getMap'](4) }}
      <br>
      BombSpots: {{ $store.getters['coreSocket/getBombSpotsByMap'](4) }}
      <br>
      DEF Operators: {{ $store.getters['coreSocket/getOperatorsBySide']('DEF') }}
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
  },
  mounted () {
  }
}
</script>
