<script>
export default {
    name: 'Toggle', 
    props: {
        label: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            toggleValue: this.min
        }
    }
    
}
</script>

<template>
    <label>
        <div class="title">{{ label }}</div>
        <input name="switch" type="checkbox" role="switch"/>
    </label>
</template>

<style>
.title {
    text-align: right;
    color: rgba(235, 235, 235, 0.64);
    opacity: 50%;
}
</style>