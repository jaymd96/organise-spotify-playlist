<script lang="ts">
import Cards from "./Cards.vue";
import Summary from "./Summary.vue";
import Spotipy from "../apiClient";
import Loading from "../Loading.vue";

export default {
  components: {
    Cards,
    Loading,
    Summary,
  },
  data() {
    return { playlists: null, summary: null };
  },

  methods: {
    async fetchPlaylists() {
      this.playlists = null;
      this.summary = null;
      this.profile = null;
      const res = await Spotipy.playlists();
      this.playlists = res.playlists;
      this.summary = res.summary;
      this.profile = res.profile;
    },
  },
  mounted() {
    this.fetchPlaylists();
  },
};
</script>


<template>
  <main>
    <Loading class="h-screen align-middle" v-if="!playlists" />
    <div v-else>
      <Summary class="mb-10" :profile="profile" :summary="summary" />
      <Cards :playlists="playlists" title="Preview playlists" />
    </div>
  </main>
</template>