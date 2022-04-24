<script>
export default {
  props: { title: String, tracks: Number, time: Number },
};
</script>

<template>
  <div
    class="
      bg-blue-600 bg-gradient-to-b
      from-blue-400
      to-blue-500
      rounded-xl
      shadow-lg
      w-full
      p-4
    "
  >
    <p class="text-white font-semibold">{{ title }}</p>
    <div class="flex justify-between mt-2">
      <p class="text-gray-200">{{ tracks }} songs</p>
      <p class="text-white">{{ time }} hrs</p>
    </div>
  </div>
</template>
