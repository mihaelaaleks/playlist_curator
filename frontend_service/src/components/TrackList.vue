<template>
    <div>
      <h2>Recommended Tracks</h2>
      <ul>
        <li v-for="track in tracks" :key="track.id">{{ track.name }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TrackList',
    props: {
      tracks: {
        type: Array,
        required: true,
      },
    },
  };
  </script>