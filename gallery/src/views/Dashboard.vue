<script setup lang="ts">

import HelloWorld from '../components/HelloWorld.vue';
import ItemGrid from '../components/ItemGrid.vue';

</script>

<template>
  <HelloWorld class="hello-world" />

<div class="item-grid-container">
  <ItemGrid class="item-grid">
  </ItemGrid>
</div>
</template>

<style>
.item-grid-container {
  padding: 2rem;
}
.hello-world {
  display: flex;
  align-items: center;
  padding: 2rem;
  margin-top: 5rem; /* Adjust based on the navbar height */
}

</style>