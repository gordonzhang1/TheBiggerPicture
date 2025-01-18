<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import HelloWorld from "./components/HelloWorld.vue";
import TheWelcome from "./components/TheWelcome.vue";
</script>

<template>
  <nav class="nav">
    <RouterLink to="/">DASHBOARD</RouterLink>
    <RouterLink to="/mosaic">MOSAIC</RouterLink>
  </nav>
  <RouterView />
</template>

<style scoped>
.nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #2c3e50;
  padding: 1rem;
  display: flex;
  gap: 1rem;
  z-index: 1000;
}

.nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.nav a:hover {
  background-color: #34495e;
}

.hello-world {
  position: absolute; /* Position relative to the viewport or parent */
  top: 5rem; /* Adjust based on the navbar height */
  left: 1rem;
  padding: 2rem;
}

.router-view {
  margin-top: 2rem;
}
</style>
