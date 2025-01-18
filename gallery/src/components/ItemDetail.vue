<script setup lang="ts">
  import { defineProps, computed } from 'vue';
  
  // Define route props for the ID
  const props = defineProps({
    id: {
      type: String,
      required: true,
    },
  });
  
  // List of items (same as in the grid)
  const items = [
    { id: '1', image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 1' },
    { id: '2', image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 2' },
    { id: '3', image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 3' },
    { id: '4', image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 4' },
    { id: '5', image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 5' },
    { id: '6', image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 6' },
    { id: '7', image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 7' },
    { id: '8', image: 'https://m.media-amazon.com/images/I/71cWvcFf4ZL._AC_UF894,1000_QL80_.jpg', title: 'Item 8' },
  ];
  
  // Find the item based on the ID passed in the route
  const item = computed(() => {
    return items.find((item) => item.id === props.id);
  });
  </script>
  
  <template>
    <div v-if="item">
      <h1>{{ item.title }}</h1>
      <img :src="item.image" :alt="item.title" />
      <p>Details about the item...</p>
    </div>
    <div v-else>
      <p>Item not found.</p>
    </div>
  </template>

  