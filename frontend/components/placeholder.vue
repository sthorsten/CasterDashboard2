<template>
  <div>
    <ContentHeader
      icon="circle-question"
      title="Empty page"
      :breadcrumb-items="['Dashboard']"
    />
    <ContentContainer>
      <b-container fluid>
        <CustomCard title="To be implemented">
          This page is not available yet :/
        </CustomCard>
      </b-container>
    </ContentContainer>
  </div>
</template>

<script>
export default {
  name: "Placeholder",

  head() {
    return {
      title: "Empty page"
    }
  },
}
</script>