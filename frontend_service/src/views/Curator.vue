<script>
import DropDown from '../components/DropDown.vue';
import Slider from '../components/Slider.vue';
import Toggle from '../components/Toggle.vue';
import { ref } from 'vue';

export default {
    name: 'Curator',
    components: {
        DropDown,
        Slider,
        Toggle
    },
    data() {
        return {
            dropdownOptions: ['Option 1', 'Option 2', 'Option 3', 'fart', 'sjart'],
            selectedDropdownOption: '',
            selectedSliderValue: 0,
            sliders: [
                { label: 'acousticness', value: 0 },
                { label: 'danceability', value: 0 },
                { label: 'energy', value: 0 },
                { label: 'loudness', value: 0 }
            ],
            playlistToggleLabel: "playlist seed"
        };
    },
    methods: {
        updateSliderValue(index, value) {
            this.sliders[index].value = value;
        }
    }
}
</script>
<template>
    <div class="parent-grid">
        <div class="L-child-grid">
            <div class="container-seeder">
                <div class="title">Seeder</div>
                <div class="container-vertical-items">
                    <Toggle :label="playlistToggleLabel" />
                </div           >
                <div class="container-settings">
                    <DropDown :options="dropdownOptions" label="Select an option" v-model="selectedDropdownOption" />
                    <!-- <p>Selected option in Curator: {{ selectedDropdownOption }}</p> -->
                </div>
            </div>
            <div class="container-attributes">
                <div class="title">Attributes</div>
                <div>
                    <div v-for="(slider, index) in sliders" :key="index">
                        <Slider :min="0" :max="100" :label="slider.label" :value="slider.value"
                            @update:modelValue="updateSliderValue(index, $event)" />
                    </div>
                </div>
            </div>
            <div class="container-curate">
                <input class="primary" type="button" value="Submit" />
            </div>

        </div>
        <div class="R-child-grid">
            <div class="title">Recommendations</div>
        </div>
    </div>
</template>


<style scoped>
@import '../assets/base.css';


input[type="checkbox"] {
    transform: rotate(90deg);
}

.parent-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 1fr);
    grid-column-gap: 1px;
    grid-row-gap: 1px;
    background-color: #181818;
}

.L-child-grid {
    grid-area: 1 / 1 / 3 / 3;

    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: repeat(5, 1fr);
    grid-column-gap: 5px;
    grid-row-gap: 5px;
}

.container-seeder {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: repeat(5, 1fr);
    grid-column-gap: 0px;
    grid-row-gap: 5px;

    background-color: #181818;

    grid-area: 1 / 1 / 3 / 4;

}

.container-attributes {
    align-items: center;
    grid-area: 3 / 1 / 5 / 4;
}

.container-curate {
    grid-area: 5 / 1 / 6 / 4;
    align-content: center;
}

.R-child-grid {
    grid-area: 1 / 3 / 3 / 4;
    border: 2;
}


.title {
    grid-area: 1 / 1 / 2 / 3;
    text-align: right;
    color: rgba(235, 235, 235, 0.64);
    opacity: 50%;
}

.container-vertical-items {
    display: flex;
    flex-direction: column;
    padding: 1%;
    gap: 1%;
    grid-area: 2 / 1 / 6 / 3;
    background-color: #181818;
}

.container-settings {
    grid-area: 1 / 3 / 6 / 6;
    align-content: center;
    height:fit-content;
    padding: 4px;
    border-radius: 4px;

}
</style>