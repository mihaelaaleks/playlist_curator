<script>
export default {
    name: 'Slider', 
    props: {
        min: {
            type: Number, 
            required: true
        },
        max: {
            type: Number, 
            required: true
        },
        label: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            sliderValue: this.min
        }
    }
    
}
</script>

<template>
    <label>
        <p>{{ label }}: {{ sliderValue }}</p>
        <input type="range" v-model="sliderValue" :aria-label="label" :max="max" :min="min"
        @input="$emit('update:modelValue', sliderValue)"/>
    </label>
</template>

<style scoped>

</style>