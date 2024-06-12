<script>
import DropDown from '../components/DropDown.vue';
import Slider from '../components/Slider.vue';
import TracklistCurator from '../components/TracklistCurator.vue'
import { ref } from 'vue';
import axios from 'axios';

export default {
    name: 'Curator',
    components: {
        DropDown,
        Slider,
        TracklistCurator
    },
    data() {
        return {
            dropdownOptions: [],
            selectedDropdownOption: '',
            selectedSliderValue: 0,
            sliders: [],
            recommendationTracksResponse: [],
            playlistData: {
                name: 'CuratedPlaylist',
                tracks: []
            }
        };
    },
    async created() {
        try {
            const [sliderLabelsResponse, dropdownOptionsResponse] = await Promise.all([
                axios.get('http://localhost:8000/spotify/get_recommendation_attributes/number_range'),
                axios.get('http://localhost:8000/spotify/get_genres')
            ]);

            const sliderLabels = sliderLabelsResponse.data;
            this.sliders = sliderLabels.map(label => ({
                label,
                value: 0
            }));
            this.dropdownOptions = dropdownOptionsResponse.data.map(genre => genre.name);
        } catch (error) {
            console.error('Error fetching form data:', error);
        }
    },
    methods: {
        updateSliderValue(index, value) {
            this.sliders[index].value = value;
        },
        handleActualItemsUpdate(newActualItems) {
            this.playlistData.tracks = newActualItems;
        },
        async submitGetRecommendationFormData() {
            try {
                const requestData = {
                    seed: {
                        id: "genres",
                        values: [this.selectedDropdownOption]
                    },
                    attributes: this.sliders.map(slider => ({
                        name: slider.label,
                        target: slider.value,
                        tolerance: 0.2
                    }))
                };

                const response = await axios.post('http://localhost:8000/spotify/curate', requestData);

                // Populate the recommendationTracksResponse array based on the API response
                this.recommendationTracksResponse = response.data;
            } catch (error) {
                console.error('Error submitting form data:', error);
            }
        },
        async submitCreatePlaylistFormData() {
            try {
                const response = await axios.post('http://localhost:8000/spotify/create_playlist', this.playlistData);
                console.log('Form submitted successfully!', response.data)
            } catch (error) {
                console.error('Error submitting form data:', error.response.data);
            }
        }
    },
}
</script>
<template>
    <div class="parent-grid">
        <div class="L-child-grid">
            <div class="container-seeder">
                <div class="title" id="seeder-container-title">Seeder</div>
                <div class="container-vertical-items">
                    <button>Playlist Seed</button>
                </div>
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
            <div class="container-recommend">
                <button @click="submitGetRecommendationFormData">Get Recommendations</button>
            </div>

        </div>
        <div class="R-child-grid">
            <div class="title" id="curator-title">Recommendations</div>
            <TracklistCurator class="curator-component" 
            :items="this.recommendationTracksResponse"
            @update:actualItems="handleActualItemsUpdate"/>
            <div class="container-recommend">
                <button @click="submitCreatePlaylistFormData">Create Playlist</button>
            </div>
        </div>
    </div>
</template>


<style scoped>
button {
    width: -moz-available;
}

#curator-title {
     grid-area: 1 / 1 / 2 / 2;
}

.curator-component {
    background: black;
    width: 677px;
    height: 600px;
    grid-area: 2 / 1 / 3 / 2;
}

.parent-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(275px, 1fr));
    grid-template-rows: repeat(2, 1fr);
    grid-column-gap: 20px;
    grid-row-gap: 1px;
    background-color: #181818;
}

.L-child-grid {
    grid-area: 1 / 1 / 3 / 3;
    display: grid;
    grid-template-columns: auto-fit, 1fr;
    grid-template-rows: auto-fit;
    grid-column-gap: 5px;
    grid-row-gap: 5px;
    padding: 0% 5% !important;
}

.R-child-grid {
    grid-area: 1 / 3 / 3 / 4;
    border: 2px;
    align-content: center;
    padding: 0% 1% !important;
    width:max-content;
    align-self: start;
    position: inherit;

    display:grid;
    grid-template-rows: auto-fit;
    grid-template-columns: auto-fit, 1fr;
    grid-column-gap: 5px;
    grid-row-gap: 5px;

}

.container-seeder {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-column-gap: 4px;
    grid-row-gap: 4px;
    background-color: #181818;
    grid-area: 1 / 1 / 3 / 4;
    height: fit-content;
}

.container-attributes {
    align-items: center;
    grid-area: 3 / 1 / 5 / 4;
    height: fit-content;
}

.container-settings {
    grid-area: 2 / 2 / 3 / 3;
    align-content: center;
    height: fit-content;
    padding: 4px;
    border-radius: 4px;
    height: fit-content;
}

.container-vertical-items {
    display: flex;
    flex-direction: column;
    padding: 1%;
    gap: 1%;
    grid-area: 2 / 1 / 3 / 2;
    background-color: #181818;
}

.container-recommend {
    grid-area: 5 / 1 / 6 / 4;
    align-content: center;
}

.title {
    grid-area: 1 / 1 / 2 / 3;
    text-align: right;
    color: rgba(235, 235, 235, 0.64);
    opacity: 50%;
}
</style>