<template>
  <b-input-group>
    <b-input v-model="value" :disabled="!edit" :size="size" />

    <b-input-group-append>
      <b-btn v-if="!edit" variant="primary" :size="size" @click="edit = true">
        <fa-icon icon="pencil-alt" />
        Edit
      </b-btn>

      <b-btn v-else variant="success" :size="size" @click="save">
        <fa-icon icon="save" />
        Save
      </b-btn>
    </b-input-group-append>
  </b-input-group>
</template>

<script>
export default {
  name: 'InputEditor',

  props: {
    text: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'md'
    }
  },

  data () {
    return {
      edit: false,
      value: this.text
    }
  },

  methods: {
    save () {
      this.edit = false
      this.$emit('save', this.value)
    }
  }
}
</script>
