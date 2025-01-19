<script setup lang="ts">
defineProps<{
}>()
</script>

<template>
  <div class="greetings">
    <h1 class="green">Mosaic Gallery</h1>
    <h3>
      A more meaningful way to share your photos.
    </h3>
  </div>
</template>

<style scoped>
.greetings {
  /* display text side to side */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  width: 100%;
}
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
