<script lang="ts">
import Spotipy from "../apiClient";

export default {
  props: {
    summary: Object,
    profile: Object,
  },
  methods: {
    createPlaylists: async function () {
      this.$refs.btnToggle.innerText = "Creating playlists";
      this.$refs.btnToggle.disabled = true;
      await Spotipy.makePlaylists();
      this.$refs.btnToggle.disabled = false;
      this.$refs.btnToggle.innerText = "Playlists created";
      this.$refs.btnToggle.disabled = true;
    },
  },
};
</script>

<template>
  <div class="flex items-center justify-center flex-col">
    <img :src="profile.picture" class="rounded-full w-32" />
    <h1 class="text-gray-800 font-semibold text-l mt-5">
      Hey 👋 {{ profile.name }}
    </h1>
    <h1 class="text-gray-500 text-sm py-4 text-center">
      We've organised your <b>{{ summary.tracks }} favorite songs</b> into
      <b>{{ summary.playlists }} playlists</b> spanning
      <b>{{ summary.hours }} hours</b>.
    </h1>
    <!-- Extracting component classes: -->
    <button @click="createPlaylists" class="btn btn-blue" ref="btnToggle">
      Organise Spotify
    </button>
  </div>
</template>

<style scoped>
.btn {
  @apply font-bold py-2 px-4 rounded;
}
.btn-blue {
  @apply bg-blue-500 text-white;
}
.btn-blue:hover {
  @apply bg-blue-700;
}
</style>