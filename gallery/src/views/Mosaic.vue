<script setup lang="ts">
import { ref } from "vue";

// Sample array of image URLs (Replace with actual array in your component)
const images = ref([
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
]);
function removeImage(index: number) {
  images.value.splice(index, 1);
}
</script>

<template>
  <div class="outer-con">
    <div class="uploadbigcon">
      <div class="uploadcon">
        <div class="image-grid">
          <div v-for="(img, index) in images" :key="index" class="image-item">
            <img :src="img" :alt="'Image ' + (index + 1)" />
            <button class="delete-btn" @click="removeImage(index)">X</button>
          </div>
        </div>
      </div>
      <div class="uploadbutton">Upload Image</div>
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
  </div>
</template>

<style>
.outer-con {
  display: flex;
  gap: 10px;
}
.uploadcon {
  margin-top: 50px;
  height: 650px;
  overflow-y: auto;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.image-item {
  position: relative; /* Allow absolute positioning of delete button */
}

.image-container {
  position: relative;
}

.image-item img {
  width: 100%;
  height: auto;
  transition: opacity 0.3s ease; /* Smooth transition for hover effect */
}

.delete-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: red;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  text-align: center;
  font-size: 14px;
  cursor: pointer;
  display: none; /* Hide by default */
}

.image-item:hover .delete-btn {
  display: block; /* Show when hovering over the image */
}

.bottom-buttons {
  display: flex;
  gap: 5px;
  flex-direction: column;
}

.collab,
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

.uploadbutton {
  border: 1px solid white;
  padding: 17px;
  text-align: center;
}
</style>
