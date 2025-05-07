<script>
export default {
  name: 'TracklistCurator',
  props: {
    items: {
      type: Array,
      default: () => []
    }
  },
  data() {
      return {
        recommendedItems: [],
        actualItems: [],
      }
  },
  watch: {
    items: {
      handler(newItems) {
        this.recommendedItems = newItems;
        console.log("old items:", this.recommendedItems);
        console.log("new items:", newItems);
      },
      deep: true,
    },
    actualItems: {
      handler(newActualItems) {
        this.$emit('update:actualItems', newActualItems)
      },
      deep: true,
    }
  },
  methods: {
    handleAddClick(item) {
      //remove item from recommendedItems array & add to actualItems
      this.recommendedItems = this.recommendedItems.filter((i) => i.id !== item.id);
      // this.actualItems.push(item);
      this.actualItems = [...this.actualItems, item];
    },
    handleRemoveClick(item) {
      //remove item from actualItems array & add back to recommendedItems
      this.actualItems = this.actualItems.filter((i) => i.id !== item.id);
      // this.recommendedItems.push(item);
      this.recommendedItems = [...this.recommendedItems, item];
    }
  }
}
</script>

<template>
  <div class="tracklist-container">
    <div class="recommmended-list">
        <div v-for="item in recommendedItems" :key="item.id" class="container-item">
            <div class="iframe-container">
              <iframe style="border-radius:12px;" :src="`https://open.spotify.com/embed/track/${item.id}`" height="80" frameBorder="0" allowfullscreen="" 
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            </div>
            <div class="button-container">
              <button @click="handleAddClick(item)"> + </button>
            </div>
        </div>
      </div>
      <div class="actual-list">
        <div v-for="item in actualItems" :key="item.id" class="container-item">
            <div class="iframe-container">
              <iframe style="border-radius:12px;" :src="`https://open.spotify.com/embed/track/${item.id}`" height="80" frameBorder="0" allowfullscreen="" 
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            </div>
            <div class="button-container">
              <button @click="handleRemoveClick(item)"> - </button>
            </div>
        </div>
      </div>
  </div>
</template>

<style scoped>
.tracklist-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: 1fr;
  grid-column-gap: 0px;
  grid-row-gap: 0px; 
}

button {
    height: 152;
    background-color:black;
}

.recommmended-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  max-width: 320px; /* Adjust the maximum width as needed */
  max-height: 600px; /* Adjust the maximum height as needed */
  overflow: auto; /* Enable scrolling when content exceeds the maximum dimensions */

  grid-area: 1 / 1 / 2 / 2;
}

.actual-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  max-width: 320px; /* Adjust the maximum width as needed */
  max-height: 500px; /* Adjust the maximum height as needed */
  overflow: auto; /* Enable scrolling when content exceeds the maximum dimensions */

  grid-area: 1 / 2 / 2 / 3;
}

.container-item {
  width: max-content;
  height: fit-content;
  display: flex;
  border-radius: 4px;
  overflow: hidden;
  background-color:black;
}

.iframe-container {
  flex: 1;
  /* height: 100%; */
  align-items: center;
}

.iframe-container iframe {
  width: 100%;
}

.button-container {
  display: flex;
  align-items: center;
  padding: 0 10px;
}

.button-container button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  /* height: max-content; */
  height: 40px;
  align-self: stretch;
}
</style>