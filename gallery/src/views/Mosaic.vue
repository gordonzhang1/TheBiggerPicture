<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { io } from "socket.io-client";

// Sample array of image URLs (Replace with actual array in your component)
const images = ref([
  "https://placehold.co/600x600",
  "https://placehold.co/600x600",
  // Add more image URLs as needed
]);

const showModal = ref(false); // Control the modal visibility
const emailInput = ref(""); // Store email input


function removeImage(index: number) {
  images.value.splice(index, 1);
}
async function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input?.files) {
    const fileList = input.files;
    const formData = new FormData(); // Create FormData to hold files

    // Loop through the selected files
    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];

      // Add file to formData
      formData.append("files[]", file);

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
        "https://your-backend-url.com/upload",
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
        <div class="generate">Generate Image</div>
        <img class="mosaicpicture" src="https://placehold.co/600x600" />
        <div class="bottom-buttons">
          <button class="collab" @click="collab">Collaborate</button>
          <div class="slide">Start Slideshow</div>
        </div>
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
</style>
