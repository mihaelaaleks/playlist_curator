<script>
export default {
  name: 'DropDown',
  props: {
    options: {
      type: Array,
      required: true
    },
    label: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      selectedOption: ''
    }
  },
  methods: {
    emitSelectedOption() {
      this.$emit('update:modelValue', this.selectedOption);
    }
  }
}
</script>

<template>
    <select v-model="selectedOption" :aria-label="label" required @change="emitSelectedOption">
      <option v-for="(option, index) in options" :key="index" :value="option">
        {{ option }}
      </option>
    </select>
</template>