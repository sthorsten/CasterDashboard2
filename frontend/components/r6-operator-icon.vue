<template>
  <svg
    v-if="operatorSVG"
    :space="operatorSVG.attributes.space"
    :style="operatorSVG.attributes.style"
    :viewBox="operatorSVG.attributes.viewBox"
    :xmlns="operatorSVG.attributes.xmlns"
    :class="operatorSVG.attributes.class"
    v-html="operatorSVG.contents"
  />
</template>

<script>
import r6operators from 'r6operators'

export default {
  name: 'R6OperatorIcon',

  props: {
    operator: {
      type: String,
      default: '_none'
    }
  },

  computed: {
    operatorSVG () {
      if (!this.operator) { return null }
      if (!r6operators[this.operator]) { return null }
      return r6operators[this.operator].svg
    }
  }

}
</script>
