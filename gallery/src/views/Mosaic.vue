<script setup lang="ts">
// Sample array of image URLs (Replace with actual array in your component)
const images = [
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  // Add more image URLs as needed
];
</script>

<template>
  <div class="uploadcon">
    <div class="image-grid">
      <div v-for="(img, index) in images" :key="index" class="image-item">
        <img :src="img" :alt="'Image ' + (index + 1)" />
      </div>
    </div>
  </div>

  <div class="right-side-con">
    <div class="right-center">
      <div class="generate">Generate Image</div>
      <img class="mosaicpicture" src="https://placehold.co/600x600" />
      <div class="bottom-buttons">
        <div class="collab">Collaborate</div>
        <div class="slide">Start Slideshow</div>
      </div>
    </div>
  </div>
</template>

<style>
.uploadcon {
  margin-top: 50px;
  height: 710px; /* Set a fixed height for scrollable area */
  overflow-y: auto; /* Makes it scrollable */
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4 columns */
  gap: 10px; /* Spacing between the images */
}

.image-item img {
  width: 100%; /* Make image take full width of its grid cell */
  height: auto; /* Maintain aspect ratio */
}

.bottom-buttons {
  display: flex;
  gap: 5px;
  flex-direction: column;
}

.collab {
  border: 1px solid white;
  text-align: center;
}

.slide {
  border: 1px solid white;
  text-align: center;
}

.generate {
  margin-top: 50px;
  border: 1px solid white;
  padding: 10px;
}

.right-side-con {
  display: flex;
  justify-content: center;
  align-items: center;
}

.right-center {
  text-align: center;
}
</style>
