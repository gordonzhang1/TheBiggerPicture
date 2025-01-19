<script setup lang="ts">
import { backendData } from '@/stores/backend-data';
import { ref, computed } from 'vue';

// List of items (Add a unique ID for each item)
const items = ref([
  { id: 1, image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 1' },
  { id: 2, image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 2' },
  { id: 3, image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 3' },
  { id: 4, image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 4' },
  { id: 5, image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 5' },
  { id: 6, image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 6' },
  { id: 7, image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 7' },
  { id: 8, image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 8' },
]);

// Search query for filtering
const searchQuery = ref('');

// Computed property to filter items based on search query
const filteredItems = computed(() => {
  return items.value.filter(item => 
    item.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});
</script>

<template>
  <div>
    <!-- Search bar -->
    <input 
      v-model="searchQuery" 
      type="text" 
      placeholder="Search by title" 
      class="search-bar" 
    />

    <!-- Grid of items -->
    <div class="grid-items">
      <RouterLink
        v-for="(item, index) in backendData.mosaics.filter((m: any) => m.includes(searchQuery)) as any"
        :key="index"
        :to="{ name: 'mosaic', params: { id: item.id } }" 
        class="grid-item-link"
      >
        <div class="grid-item">
          <img :src="item.url" :alt="item.image_name" class="grid-item-image" />
          <h3 class="grid-item-title">{{ item.image_name }}</h3>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
/* Ensure the entire body and html take the full height */
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

/* Search bar styling */
.search-bar {
  width: 100%;
  scale: 0.99;
  padding: 0.8rem;
  font-size: 1rem;
  border-radius: 20px;
  border: 2px solid #383838;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
  margin-bottom: 2rem;  
  opacity: 80%;
  background-color: rgba(99, 99, 99, 0.356);
  caret-color: white;
  color: white;
}

.search-bar:focus {
  outline: none;
}

/* Grid container styling */
.grid-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* Responsive columns */
  gap: 2rem;
  padding: 1rem;
  width: 100%; /* Ensure it takes full width */
  height: 400px; /* Full screen height */
  box-sizing: border-box; /* Include padding in the width/height calculation */
}

/* Individual grid item styling */
.grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #6e6e6e2c;
  border-radius: 30px;
  padding: 1rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease; /* Smooth scale transition */
}

.grid-item-image {
  max-width: 100%;
  border-radius: 15px;
}

.grid-item-title {
  padding-top: 1rem;
  font-weight: bold;
}

.grid-item:hover {
  cursor: pointer;
  transform: scale(1.03); /* Slight scale-up on hover */
}

/* Make the link around the grid item */
.grid-item-link {
  text-decoration: none;
  color: inherit;
}
</style>
