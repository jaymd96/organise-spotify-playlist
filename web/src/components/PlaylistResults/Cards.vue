<script lang="ts">
import Card from "./Card.vue";
import Loading from "../Loading.vue";

export default {
  components: {
    Card,
    Loading,
  },
  props: {
    playlists: Object,
    title: String,
  },
};
</script>

<template>
  <div class="container mx-auto">
    <h1 class="mb-3">{{ title }}</h1>
    <div
      class="
        grid grid-cols-1
        sm:grid-cols-2
        md: md:grid-cols-2
        lg:grid-cols-4
        gap-6
      "
    >
      <Card
        v-for="playlist in playlists"
        :title="playlist.name"
        :tracks="playlist.tracks"
        :time="playlist.hours"
        :key="playlist.name"
      />
    </div>
  </div>
</template>