<script setup lang="ts">
import { onMounted, ref, defineProps, computed } from "vue";
import axios from "axios";
import { backendData } from "@/stores/backend-data";
  
// Define route props for the ID
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

// Sample array of image URLs (Replace with actual array in your component)
const images = ref([
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // "https://placehold.co/600x600",
  // Add more image URLs as needed
]);

async function fetchData() {
  const formData = new FormData();

  formData.append('category', props.id);

  const res = await fetch('http://127.0.0.1:5001/api/get-images', {
    method: 'POST',
    body: formData,
  });

  const json = await res.json();

  images.value = json.album_images;
}

onMounted(() => {
  fetchData();
});

function removeImage(index: number) {
  images.value.splice(index, 1);
}
async function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input?.files) {
    const fileList = input.files;
    const formData = new FormData(); // Create FormData to hold files
    formData.append("category", props.id);

    // Loop through the selected files
    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];

      // Add file to formData
      formData.append("images", file);

      // Read and preview the file (for images)
      const reader = new FileReader();
      reader.onload = () => {
        // Push file preview to the images array
        images.value.push(reader.result as string);
      };
      reader.readAsDataURL(file); // Convert the file to a data URL for preview
    }

    // Send the files to the backend
    try {
      const response = await axios.post(
        "http://127.0.0.1:5001/api/upload-images",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data", // Required for file uploads
          },
        }
      );
      console.log("Upload successful:", response.data); // Handle successful response
      // You can update the UI with the server response if needed
    } catch (error) {
      console.error("Error uploading files:", error); // Handle error
    }
  }
}

const shuffle = (array: string[]) => { 
    return array.map((a) => ({ sort: Math.random(), value: a }))
        .sort((a, b) => a.sort - b.sort)
        .map((a) => a.value); 
}; 

const goodImages = ref(["https://www.nutritionadvance.com/wp-content/uploads/2023/07/whole-and-half-oranges-1024x683.jpg"]);

function generate(){
  goodImages.value = [];
  while (goodImages.value.length < 400){
    goodImages.value = goodImages.value.concat(shuffle([...images.value]))
  }
  goodImages.value = goodImages.value.subarray(0, 400);
};
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
      <input
        type="file"
        id="fileInput"
        multiple
        @change="handleFileUpload"
        class="file-upload-input"
      />
    </div>
    <div class="right-side-con">
      <div class="right-center">
        <div class="generate" @click="generate()">Generate Image</div>
        <div class="mosaicpicture mosaic-grid">
          <img id="main-img" src="https://alanbui1.github.io/codequest/assets/images/savio.jpg" />
          <div v-for="(img, index) in goodImages" :key="index" >

            <img v-if="index < 400" :src="img" :alt="'Image ' + (index + 1)" style="height: 30px; width: 30px;" class="mosaic-item"/>
          </div>
        </div>
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
  margin-bottom: 10px;
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

#main-img{
  width: 600px;
  height: 600px;
  object-fit: cover;
  position: absolute;
  opacity: 100%;
}

.mosaicpicture{
  width: 600px;
  height: 600px;
  opacity: 90%;
}

.mosaic-grid{
  width: 600px;
  height: 600px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(30px, 1fr));
  grid-column-gap: 0;
  grid-row-gap: 0;
  gap: 0;
}

.mosaic-item{
  display: block;
  margin: 0;
  padding: 0;
  opacity: 35%;
  /* mix-blend-mode: overlay; */
  grid-column-gap: 0;
  grid-row-gap: 0;
}

.mosaic-item img{
  width: 100%; /* Ensure the image fills the item */
  height: 100%; /* Maintain full height */
  object-fit: cover; /* Ensures the image covers the entire area without distortion */
  display: block; /* Remove any inline spacing */
}

</style>
