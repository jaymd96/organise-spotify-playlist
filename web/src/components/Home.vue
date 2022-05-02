<script lang="ts">
import Spotify from "./apiClient";

export default {
  computed: {
    // a computed getter
    buttonRedirect: function () {
      // `this` points to the vm instance
      return Spotify.serverUrl();
    },
  },
};
</script>
<template>
  <form :action="buttonRedirect">
    <input type="submit" value="Login to spotify" />
  </form>
</template>
