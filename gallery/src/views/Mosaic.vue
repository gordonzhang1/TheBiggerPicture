<script setup lang="ts">
import { onMounted, ref, defineProps, computed } from "vue";
import axios from "axios";
import { io } from "socket.io-client";
import { backendData } from "@/stores/backend-data";

// Sample array of image URLs (Replace with actual array in your component)
const images = ref<string[]>([
  // Add more image URLs as needed
]);

const showModal = ref(false); // Control the modal visibility
const emailInput = ref(""); // Store email input
const showDalleModal = ref(false); // Control the modal visibility
const dalleInput = ref(""); // Store email input
  
// Define route props for the ID
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const bigImage = ref("");
const hoveredImage = ref<string>("")

async function fetchData() {
  const formData = new FormData();

  formData.append('category', props.id);

  const res = await fetch('http://127.0.0.1:5001/api/get-images', {
    method: 'POST',
    body: formData,
  });

  const json = await res.json();

  images.value = json.album_images;
  bigImage.value = json.big_image;
}

onMounted(() => {
  fetchData();
});

async function removeImage(url: string) {
  // images.value.splice(index, 1);

  const formData = new FormData();
  formData.append('url', url);
  formData.append('category', props.id);

  const res = await fetch('http://127.0.0.1:5001/api/delete-image', {
    method: 'POST',
    body: formData
  });
}

// Hover functions to update preview
const handleImageHover = (imageUrl: string) => {
  hoveredImage.value = imageUrl; // Set the hovered image to display as preview
};

const handleImageLeave = () => {
  hoveredImage.value = ""; // Reset to default image when mouse leaves
};

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
        // images.value.push(reader.result ? reader.result as string : "");
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

async function handleBigFileUpload(event: Event) {
  console.log("Big file upload");
  const input = event.target as HTMLInputElement;
  if (input?.files) {
    const fileList = input.files;
    const formData = new FormData(); // Create FormData to hold files
    formData.append("category_id", props.id);

    // Loop through the selected files
    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];

      // Add file to formData
      formData.append("file", file);
    }

    // Send the files to the backend
    try {
      const response = await axios.post(
        "http://127.0.0.1:5001/api/upload_big_image",
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

function collab() {
  showModal.value = true; // Show the modal when "Collaborate" is clicked
}

function closeModal() {
  showModal.value = false; // Close the modal without sending an invite
}

function sendInvite() {
  var socket = io("http://127.0.0.1:5001");

  console.log("Sending:", images);

  socket.on(`add image `, function(images) {
        // console.log(msg)
        // document.body.innerHTML += msg.images.map((img) => `<img src="${img}" width="200" height="200" />`).join("\n");
    });
}

const shuffle = (array: string[]) => {
  return array.map((a) => ({ sort: Math.random(), value: a }))
    .sort((a, b) => a.sort - b.sort)
    .map((a) => a.value);
};

const goodImages: any = ref([]);

function generate() {
  goodImages.value = [];
  while (goodImages.value.length < 400) {
    goodImages.value = goodImages.value.concat(shuffle([...images.value]))
  }
  goodImages.value = goodImages.value.slice(0, 400);
};

function dalle(){
  console.log("Dall-E button clicked");
  showDalleModal.value = true; // Show the modal when "Collaborate" is clicked
}

function closedalle() {
  showDalleModal.value = false; // Close the modal without sending an invite
}

async function sendDalleRequest() {
  closedalle();
  console.log("Sending Dall-E request");
  console.log(dalleInput);
  const formData = new FormData();
  formData.append("prompt", dalleInput.value);
  formData.append("category_id", props.id);
  try {
      const response = await axios.post(
        "http://127.0.0.1:5001/api/generate-dalle",
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

const imageText = ref(""); // Store the text entered by the user
let socket;
onMounted(() => {
  socket = io('http://127.0.0.1:5001');
  console.log(socket);
  socket.on(`add image ${props.id}`, (msg) => {
    images.value = [...images.value, ...msg.images];
  });
  console.log(`delete image ${props.id}`)
  socket.on(`delete image ${props.id}`, (msg) => {
    console.log('test!');
    images.value = images.value.filter((val) => val != msg.url);
  });

  socket.on(`edit big image ${props.id}`, (msg) => {
    bigImage.value = msg.url;
  })
})

</script>

<template>
  <div class="outer-con">
    <!-- Placeholder for an image -->
    <div class="placeholder-container">
      <!-- Optionally, add a placeholder image -->
       <div class="placeholder-subcontainer">
        <img :src="hoveredImage || 'https://placehold.co/600x400'" alt="Placeholder Image" />
       </div>
    

      <div class="uploadbigcon">
        <div class="uploadcon">
          <div class="image-grid">
            <div v-for="(img, index) in images" :key="index" class="image-item">
            <img :src="img" :alt="'Image ' + (index + 1)" 
            />
            <button class="delete-btn" @click="removeImage(img)">X</button>
            </div>
          </div>
        </div>
        <label for="file-upload" class="custom-file-upload">
        Upload Mosaic Images
    </label>
      <input
        type="file"
        id="file-upload"
        multiple
        @change="handleFileUpload"
        class="file-upload-input"
      />
      </div>
    </div>
      <div class="right-side-con">
        <div class="right-center">
          <div class="big-image-upload">
            <div class="createcon">
              <button class="dalle" @click="dalle()">Ask Dall-E</button>
              <label for="big-file-upload" class="big-custom-file-upload">
                Upload Big Image
                </label>
                <input
                type="file"
                id="big-file-upload"
                multiple
                @change="handleBigFileUpload"
                class="big-file-upload-input"
              />
            </div>
          </div>
        <div class="mosaicpicture mosaic-grid">
          <img id="main-img" :src="bigImage" />
          <div v-for="(img, index) in goodImages" :key="index" >

            <img v-if="index < 400" :src="img" :alt="'Image ' + (index + 1)" style="height: 30px; width: 30px;"
              :class="'mosaic-item fade-in' + Math.min(Math.abs(10-Math.floor(index / 20)), Math.abs(10-(index % 20)))"
              @mouseover="handleImageHover(img)" 
            @mouseleave="handleImageLeave"
            />
          </div>
        </div>
      <div class="bottom-buttons">
        <button class="generate" @click="generate()">Generate Image</button>
        <button class="collab" @click="collab">Collaborate</button>
      </div>
    </div>
  </div>
</div>

  <!-- Modal for Dalle request-->
  <div v-if="showDalleModal" class="modal-overlay">
    <div class="modal">
      <h2>Ask Dall-E</h2>
      <input
        v-model="dalleInput"
        type="text"
        placeholder="Enter text"
        class="email-input"
      />
      <div class="modal-buttons">
        <button @click="sendDalleRequest" class="invite-btn">Send Request</button>
        <button @click="closedalle" class="close-btn">Close</button>
      </div>
    </div>
  </div>

  <!-- Modal for Invite -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal">
      <h2>Invite Collaborators</h2>
      <input
        v-model="emailInput"
        type="email"
        placeholder="Enter email address"
        class="email-input"
      />
      <div class="modal-buttons">
        <button @click="sendInvite" class="invite-btn">Send Invite</button>
        <button @click="closeModal" class="close-btn">Close</button>
      </div>
    </div>
  </div>

</template>

<style>

.placeholder-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 600px;
  border: 1px dashed gray;
  border-radius: 20px;
  margin-bottom: 20px; /* Space between placeholder and uploadbigcon */
  background-color: rgb(240, 240, 240); /* Light gray background */
  gap: 20px;
  padding: 20px;
}

.placeholder-subcontainer {
  padding: 40px;
  width: 600px; /* Set a fixed width for the placeholder */
  height: 600px; /* Set a fixed height for the placeholder */
  overflow: hidden; /* Hide overflow to keep the black bars */
  position: relative; /* Ensure positioning of the image inside the container */
  border-radius: 10px; /* Rounded corners for the placeholder */
}

.placeholder-subcontainer img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Ensures the image covers the entire container, keeping aspect ratio */
}


.right-center {
  width: 100%;
  padding: 10px;
}

input[type="file"] {
  display: none;
}

.custom-file-upload {
  margin-top: 1rem;
  border: 1px solid #ccc;
  display: inline-block;
  padding: 6px 12px;
  cursor: pointer;
  background-color: #555;
  border-radius: 20px;
}

.uploadbigcon {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* Ensure content is aligned at the top */
  width: 100%;
  height: 100%; /* Full height, adjust as needed */
  border: 1px solid rgb(55, 55, 55);
  background-color: rgb(72, 72, 72);
  border-radius: 20px;  
  padding: 5px;
  padding-bottom: 20px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* Two columns */
  gap: 10px;
  padding: 20px; /* Add some padding */
  width: 100%;
  height: auto; /* Adjust height automatically to content */
}

.big-image-upload {
  display: flex;
  flex-direction: row;
  margin-bottom: 2rem;
}

.uploadbutton,
.dalle,
.big-custom-file-upload,
.big-file-upload-input {
  background-color: rgb(219, 219, 219);
  height: 50px; /* Standardize the height */
  border-radius: 10px;
  display: flex;
  color: black;
  justify-content: center;
  align-items: center;
}

.uploadbutton,
.dalle,
.big-custom-file-upload,
.big-file-upload-input {
  width: 50%; /* Adjust button width as needed for balance */
  text-align: center;
  border: 1px solid white;
  transition: all 0.3s ease;
}

.uploadbutton:hover,
.dalle:hover,
.big-custom-file-upload:hover,
.big-file-upload-input {
  background-color: white;
  color: black;
  cursor: pointer;
  transition: all 0.3s ease;
}


.createcon{
  display:flex;
  width: 100%;
  height: 40px;
  align-items: center; 
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-end;
  gap: 20px;
  margin-top: 1rem;
 }

.outer-con {
  display: flex;
  flex-direction: row;
  align-items: flex-start; /* Align children to the top */
  justify-content: center;  
  gap: 5rem;
  margin-top: 5rem;
}

.uploadcon {
  display: flex;
  width: 100%; /* Ensure it takes full width of its container */
  max-height: 30rem; /* Ensure it takes full height of its container */
  overflow-y: auto; /* Allow vertical scrolling if content overflows */
  border-radius: 15px; /* Optional: Add rounded corners */
  background-color: rgb(46, 46, 46); /* Match the existing style */
}

.image-grid {
  min-width: 100%;

  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  background-color: rgb(46, 46, 46);
  padding: 50px;
  border-radius: 20px;
}

.image-item {
  position: relative;
  /* Allow absolute positioning of delete button */
}

.image-container {
  position: relative;
}

.image-item img {
  border-radius: 10px;
  width: 100%;
  height: auto;
  transition: opacity 0.3s ease;
  /* Smooth transition for hover effect */
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
  display: none;
  /* Hide by default */
}

.image-item:hover .delete-btn {
  display: block;
  /* Show when hovering over the image */
}

.bottom-buttons {
  margin-top: 2rem;
  display: flex;
  gap: 30px;
  flex-direction: column;
}

.collab,
.generate {
  border: 1px solid white;
  text-align: center;
  border-radius: 20px;
  height: 4rem;
  transition: all 0.3s ease;
}

.collab:hover,
.generate:hover {
  background-color: white;
  color: black;
  cursor: pointer;
  transition: all 0.3s ease;
}

.right-side-con {
  text-align: center;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Ensure no overflow */
  border: 1px solid rgb(55, 55, 55); /* Optional: Add a border for clarity */
  background-color: rgb(72, 72, 72);
  border-radius: 20px;  
  padding: 5px;
  padding-bottom: 20px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5); /* Transparent background */
  display: flex;
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
  z-index: 1000; /* Ensure it appears above other content */
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px; /* You can adjust the width of the modal */
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Optional: Add a shadow to make it stand out */
}

#main-img {
  width: 600px;
  height: 600px;
  object-fit: cover;
  position: absolute;
  opacity: 100%;
}

.mosaicpicture {
  width: 600px;
  height: 600px;
  opacity: 90%;
}

.mosaic-grid {
  width: 600px;
  height: 600px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(30px, 1fr));
  grid-column-gap: 0;
  grid-row-gap: 0;
  gap: 0;
}

.mosaic-item {
  display: block;
  margin: 0;
  padding: 0;
  opacity: 35%;
  /* mix-blend-mode: overlay; */
  grid-column-gap: 0;
  grid-row-gap: 0;
}

.mosaic-item img {
  width: 100%;
  /* Ensure the image fills the item */
  height: 100%;
  /* Maintain full height */
  object-fit: cover;
  /* Ensures the image covers the entire area without distortion */
  display: block;
  /* Remove any inline spacing */
}




@keyframes fadeIn {
  0% {
    opacity: 0;
    /* Start fully transparent */
  }

  60% {
    opacity: 1;
    /* Fully visible at halfway point */
  }

  100% {
    opacity: 35%;
    /* Fully transparent again */
  }
}

.fade-in0 {
  animation: fadeIn 1s ease-in-out; /* 0s for fade-in0 */
}

.fade-in1 {
  animation: fadeIn 1.25s ease-in-out; /* 1s for fade-in1 */
}

.fade-in2 {
  animation: fadeIn 1.5s ease-in-out; /* 2s for fade-in2 */
}

.fade-in3 {
  animation: fadeIn 1.75s ease-in-out; /* 3s for fade-in3 */
}

.fade-in4 {
  animation: fadeIn 2s ease-in-out; /* 0s for fade-in0 */
}

.fade-in5 {
  animation: fadeIn 2.25s ease-in-out; /* 1s for fade-in1 */
}

.fade-in6 {
  animation: fadeIn 2.5s ease-in-out; /* 2s for fade-in2 */
}

.fade-in7 {
  animation: fadeIn 2.75s ease-in-out; /* 3s for fade-in3 */
}

.fade-in8 {
  animation: fadeIn 3s ease-in-out; /* 0s for fade-in0 */
}

.fade-in9 {
  animation: fadeIn 3.25s ease-in-out; /* 1s for fade-in1 */
}

</style>
